import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending','in_progress','done','cancelled')),
            priority TEXT DEFAULT 'medium' CHECK(priority IN ('low','medium','high','urgent')),
            created_at TEXT DEFAULT (datetime('now','localtime')),
            due_date TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()

# ================= Persons =================

def add_person(name):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO persons (name) VALUES (?)", (name,))
        conn.commit()
        return f"✅ تم إضافة {name}"
    except sqlite3.IntegrityError:
        return f"⚠️ {name} موجود مسبقاً"
    finally:
        conn.close()

def delete_person(name):
    conn = get_conn()
    cur = conn.execute("DELETE FROM persons WHERE name=?", (name,))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return f"✅ تم حذف {name}" if affected else f"⚠️ ما لقيت {name}"

def list_persons():
    conn = get_conn()
    rows = conn.execute("SELECT id, name FROM persons ORDER BY name").fetchall()
    conn.close()
    if not rows:
        return "⚠️ لا يوجد أشخاص"
    result = "👥 الأشخاص:\n"
    for r in rows:
        result += f"  {r['id']}. {r['name']}\n"
    return result.strip()

# ================= Tasks =================

def add_task(person_name, title, description="", priority="medium", due_date=""):
    conn = get_conn()
    person = conn.execute("SELECT id FROM persons WHERE name=?", (person_name,)).fetchone()
    if not person:
        conn.close()
        return f"⚠️ ما لقيت شخص اسمه {person_name}"
    conn.execute(
        "INSERT INTO tasks (person_id, title, description, priority, due_date) VALUES (?,?,?,?,?)",
        (person["id"], title, description, priority, due_date or None)
    )
    conn.commit()
    conn.close()
    return f"✅ مهمة '{title}' لـ {person_name}"

def list_tasks(person_name="", status=""):
    conn = get_conn()
    query = """SELECT t.id, p.name, t.title, t.description, t.status, t.priority, t.created_at, t.due_date
               FROM tasks t JOIN persons p ON t.person_id = p.id"""
    filters = []
    params = []
    if person_name:
        filters.append("p.name=?")
        params.append(person_name)
    if status:
        filters.append("t.status=?")
        params.append(status)
    if filters:
        query += " WHERE " + " AND ".join(filters)
    query += " ORDER BY t.priority DESC, t.created_at DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    if not rows:
        return "⚠️ لا يوجد مهام"
    result = "📋 المهام:\n"
    for r in rows:
        status_icon = {"pending":"⏳","in_progress":"🔄","done":"✅","cancelled":"❌"}
        prio_icon = {"low":"🟢","medium":"🟡","high":"🔴","urgent":"⚡"}
        result += f"  [{r['id']}] {status_icon.get(r['status'],'')} {r['title']} - {r['name']} {prio_icon.get(r['priority'],'')}\n"
        if r['description']:
            result += f"       {r['description']}\n"
        if r['due_date']:
            result += f"       📅 {r['due_date']}\n"
    return result.strip()

def update_task(task_id, field, value):
    conn = get_conn()
    cur = conn.execute(f"UPDATE tasks SET {field}=? WHERE id=?", (value, task_id))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return f"✅ تم تحديث المهمة {task_id}" if affected else f"⚠️ ما لقيت مهمة {task_id}"

def delete_task(task_id):
    conn = get_conn()
    cur = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    affected = cur.rowcount
    conn.close()
    return f"✅ تم حذف المهمة {task_id}" if affected else f"⚠️ ما لقيت مهمة {task_id}"

def stats():
    conn = get_conn()
    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    done = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='done'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'").fetchone()[0]
    in_progress = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'").fetchone()[0]
    persons = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    conn.close()
    return f"📊 إحصائيات:\n  👤 {persons} أشخاص\n  📋 {total} مهام\n  ✅ {done} مكتملة\n  🔄 {in_progress} قيد العمل\n  ⏳ {pending} معلقة"

if __name__ == "__main__":
    init_db()
    while True:
        cmd = input("\n> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        action = parts[0]

        if action == "شخص" or action == "person":
            if len(parts) >= 2:
                print(add_person(" ".join(parts[1:])))
            else:
                print("استخدم: شخص [الاسم]")

        elif action == "الأشخاص" or action == "persons":
            print(list_persons())

        elif action == "حذف" or action == "del" and len(parts) >= 2 and parts[1] == "شخص":
            print(delete_person(" ".join(parts[2:])))

        elif action == "مهمة" or action == "task":
            # task person_name "title" "description" priority due_date
            if len(parts) >= 3:
                name = parts[1]
                title = parts[2]
                desc = " ".join(parts[3:]) if len(parts) > 3 else ""
                print(add_task(name, title, desc))
            else:
                print("استخدم: مهمة [شخص] [العنوان] [الوصف]")

        elif action == "المهام" or action == "tasks":
            if len(parts) >= 2:
                print(list_tasks(person_name=parts[1]))
            else:
                print(list_tasks())

        elif action == "status" or action == "حالة":
            if len(parts) >= 3:
                print(update_task(parts[1], "status", parts[2]))
            else:
                print("استخدم: حالة [رقم المهمة] [pending/in_progress/done/cancelled]")

        elif action == "حذف" and len(parts) >= 2 and parts[1] == "مهمة":
            print(delete_task(parts[2]))

        elif action == "احصائيات" or action == "stats":
            print(stats())

        elif action == "خروج" or action == "exit":
            break

        else:
            print("الأوامر:\n  شخص [اسم]\n  الأشخاص\n  مهمة [شخص] [عنوان] [وصف]\n  المهام [شخص]\n  حالة [رقم] [status]\n  حذف شخص [اسم]\n  حذف مهمة [رقم]\n  احصائيات\n  خروج")
