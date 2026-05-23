import asyncio, os, sys, subprocess, json, requests, datetime, re
from pathlib import Path

BOT_TOKEN = ""
CHAT_ID = ""
ALLOWED_USERS = []
DEVCENTER = "D:\\DevCenter"
AI_MODEL = "openrouter/free"
conversations = {}

def load_config():
    global BOT_TOKEN, CHAT_ID, ALLOWED_USERS
    env_path = Path(__file__).parent / ".env.comm"
    cfg = {}
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    cfg[k.strip()] = v.strip()
    BOT_TOKEN = cfg.get("TELEGRAM_BOT_TOKEN", "")
    CHAT_ID = cfg.get("TELEGRAM_CHAT_ID", "")
    ALLOWED_USERS = [CHAT_ID] if CHAT_ID else []

load_config()

def get_or_key():
    up = Path(os.environ.get("USERPROFILE", "C:/Users/anorm")) / ".config" / "opencode" / "opencode.json"
    if up.exists():
        try:
            cfg = json.loads(up.read_text(encoding="utf-8"))
            k = cfg.get("provider", {}).get("openrouter", {}).get("apiKey", "")
            if k: return k
        except: pass
    return os.environ.get("OPENROUTER_API_KEY", "")

SYSTEM_PROMPT = """أنت مساعد ذكي ومفيد اسمك DevCenter AI.

تصرفاتك:
- رد بالعربية دائماً
- كن طبيعياً وودوداً مثل محادثة حقيقية
- جاوب على أي سؤال بشكل مفصل ومفيد
- ساعد في البرمجة، التقنية، العلوم، وكل المواضيع
- إذا المستخدم طلب منك شي متعلق بجهازه (مثل: ابني مشروع، شغل السيرفر، حمل مكتبة)، أعد أمر JSON بهذا الشكل بالضبط:
{"cmd": "build_project", "name": "...", "type": "..."}
{"cmd": "run_server", "path": "..."}
{"cmd": "install_pkg", "pkg": "..."}
{"cmd": "search", "query": "..."}
{"cmd": "run_cmd", "cmd": "..."}
{"cmd": "list_dir", "path": "."}
{"cmd": "read_file", "path": "..."}

للأمر استخدم JSON فقط. للأسئلة والمحادثة رد بشكل طبيعي.

مثال:
المستخدم: "وش هي Python؟"
أنت: "Python هي لغة برمجة قوية وسهلة التعلم... [شرح طبيعي]"

المستخدم: "ابني مشروع ويب"
أنت: {"cmd": "build_project", "name": "new_web_app", "type": "web"}

المستخدم: "كيف أتعلم الذكاء الاصطناعي؟"
أنت: "لتعلم الذكاء الاصطناعي، ابدأ بتعلم Python ثم... [نصيحة]"

الأهم: كن طبيعياً، لا تكن آلياً."""

def ask_ai(messages):
    try:
        or_key = get_or_key()
        if not or_key: return None
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + or_key, "Content-Type": "application/json"},
            json={"model": AI_MODEL, "messages": messages, "max_tokens": 2000},
            timeout=60
        )
        if r.status_code == 200:
            msg = r.json()["choices"][0]["message"]
            return msg.get("content") or msg.get("reasoning") or msg.get("refusal") or ""
    except Exception as e:
        print("AI Error:", e)
    return None

async def execute_cmd(cmd_obj):
    cmd = cmd_obj.get("cmd", "")
    result = ""
    if cmd == "build_project":
        name = cmd_obj.get("name", "project")
        ptype = cmd_obj.get("type", "python")
        target = os.path.join(DEVCENTER, "WebApps", name)
        os.makedirs(target, exist_ok=True)
        result += "✅ تم إنشاء مشروع " + ptype + ": `" + name + "`\nالمسار: `" + target + "`"
    elif cmd == "run_server":
        path = cmd_obj.get("path", "server.py")
        full = ""
        for r, d, f in os.walk(DEVCENTER):
            if path in f: full = os.path.join(r, path); break
        if full:
            p = subprocess.Popen(["python", full], cwd=os.path.dirname(full))
            result += "✅ شغّل `" + path + "` PID: " + str(p.pid)
        else:
            result += "❌ ما لقيت `" + path + "`"
    elif cmd == "install_pkg":
        pkg = cmd_obj.get("pkg", "")
        r = subprocess.run(["pip", "install", pkg], capture_output=True, text=True, timeout=60)
        result += "✅ تم تثبيت `" + pkg + "`" if r.returncode == 0 else "❌ " + r.stderr[:300]
    elif cmd == "search":
        q = cmd_obj.get("query", "")
        try:
            r = requests.get("https://api.duckduckgo.com/?q=" + q + "&format=json&no_html=1", timeout=15)
            d = r.json()
            txt = d.get("AbstractText", "") or ""
            if not txt and d.get("RelatedTopics"):
                txt = d["RelatedTopics"][0].get("Text", "")
            if txt:
                result += "🔍 " + txt[:1500]
            else:
                r2 = requests.get("https://html.duckduckgo.com/html/?q=" + q, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
                sn = re.findall(r'class="result__snippet">(.*?)</a>', r2.text)
                result += "🔍 " + ("\n".join(s.strip() for s in sn[:5]) if sn else "(ما لقيت نتائج)")
        except Exception as e:
            result += "❌ " + str(e)
    elif cmd == "run_cmd":
        c = cmd_obj.get("cmd", "")
        r = subprocess.run(c, shell=True, capture_output=True, text=True, cwd=DEVCENTER, timeout=30)
        result += "$ " + c + "\n" + (r.stdout[-1500:] if r.stdout else r.stderr[-500:])
    elif cmd == "list_dir":
        p = cmd_obj.get("path", ".")
        t = os.path.join(DEVCENTER, p)
        if os.path.exists(t):
            result += "📁 `" + p + "`:\n"
            for item in sorted(os.listdir(t)):
                full = os.path.join(t, item)
                icon = "📁" if os.path.isdir(full) else "📄"
                sz = " (" + str(os.path.getsize(full)) + " B)" if os.path.isfile(full) else ""
                result += icon + " " + item + sz + "\n"
                if len(result) > 3000: result += "..."; break
        else:
            result += "❌ ما موجود"
    elif cmd == "read_file":
        p = cmd_obj.get("path", "")
        t = os.path.join(DEVCENTER, p) if not os.path.isabs(p) else p
        if os.path.exists(t):
            try:
                content = Path(t).read_text(encoding="utf-8")
                result += "📄 `" + p + "`:\n```\n" + content[:2000] + "```"
                if len(content) > 2000: result += "\n..."
            except:
                result += "❌ ما قدرت أقرأ"
        else:
            result += "❌ ما موجود"
    else:
        result += "🤔 الأمر مو معروف"
    return result[:4000]

async def handle_message(update):
    msg = update.get("message", {})
    chat_id = str(msg.get("chat", {}).get("id", ""))
    text = msg.get("text", "")

    if not ALLOWED_USERS:
        return "🤖 *DevCenter AI*\n\nchat_id تبعك: `" + chat_id + "`\nحطه في:\n`D:\\DevCenter\\Tools\\.env.comm`\nكـ `TELEGRAM_CHAT_ID=" + chat_id + "`"
    if chat_id not in ALLOWED_USERS:
        return "⚠️ غير مصرح"

    if text == "/start":
        return "🤖 *DevCenter AI* 🧠\n\nأنا مساعدك الذكي بالعربية — أسألني أي شيء!\n\n*أمثلة:*\n• وش هي Python؟\n• علمني الذكاء الاصطناعي\n• حل مسألة:\n• اشرح لي الكود\n• ابني مشروع ويب\n• شغل السيرفر\n\n`/reset` - امسح الذاكرة"

    if text == "/help":
        return await handle_message({"message": {"chat": {"id": chat_id}, "text": "/start"}})

    if text == "/reset":
        if chat_id in conversations: del conversations[chat_id]
        return "🧹 تم مسح الذاكرة. ابدأ من جديد!"

    # Conversation memory
    if chat_id not in conversations:
        conversations[chat_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    conversations[chat_id].append({"role": "user", "content": text})
    if len(conversations[chat_id]) > 21:
        conversations[chat_id] = [conversations[chat_id][0]] + conversations[chat_id][-20:]

    ai_reply = ask_ai(conversations[chat_id])

    if not ai_reply:
        conversations[chat_id].pop()
        return "⚠️ البوت مو قادر يتصل بالذكاء الاصطناعي حالياً. جرب بعد شوي."

    # Check if AI returned a command JSON
    cmd_obj = None
    try:
        match = re.search(r'\{[^}]*\}', ai_reply.replace('\n', ' '))
        if match:
            parsed = json.loads(match.group())
            if parsed.get("cmd"):
                cmd_obj = parsed
    except:
        pass

    if cmd_obj:
        result = await execute_cmd(cmd_obj)
        conversations[chat_id].append({"role": "assistant", "content": result})
        return result
    else:
        # Natural ChatGPT-style reply
        conversations[chat_id].append({"role": "assistant", "content": ai_reply})
        return ai_reply[:4000]

async def main():
    if not BOT_TOKEN:
        return print("TELEGRAM_BOT_TOKEN غير موجود")
    import aiohttp
    offset = 0
    print("🤖 DevCenter AI Bot شغال — ChatGPT بالعربية...")
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                url = "https://api.telegram.org/bot" + BOT_TOKEN + "/getUpdates"
                async with session.post(url, json={"offset": offset, "timeout": 30}) as r:
                    if r.status != 200: await asyncio.sleep(5); continue
                    data = await r.json()
                    for update in data.get("result", []):
                        offset = update["update_id"] + 1
                        reply = await handle_message(update)
                        if reply:
                            send_url = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
                            cid = update["message"]["chat"]["id"]
                            await session.post(send_url, json={"chat_id": cid, "text": reply, "parse_mode": "Markdown"})
            except asyncio.CancelledError: break
            except Exception as e:
                print("خطأ:", e)
                await asyncio.sleep(5)

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("\nتم الإيقاف")
