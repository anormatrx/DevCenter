# Smart Builder Skill 🧠⚡

## الوصف
Skill للبناء الذكي — يكتشف المشاكل ويحلها تلقائياً بدون سؤال المستخدم.

## متى تستخدم
- عندما يقول المستخدم "ابني مشروع" أو أي أمر بناء
- عندما تطلب المستخدم "حل المشكلة" أو "صلحه"
- عند تشغيل سيرفر/تطبيق جديد

## المسار التلقائي
1. plan → build → detect → fix → run → deliver

## دوال المساعدة
### detect_port_conflict(port: int) -> int
افحص إذا البورت مشغول، أرجع أول port فاضي.

### check_dependencies(path: str) -> list
اقرأ الـ imports واشوف إذا كل الباكجات موجودة.

### auto_fix_error(error_text: str, project_path: str) -> str
افهم الـ error، صلّح الملف، أرجع التقرير.

### detect_path_issue(expected: str, actual: str) -> bool
قارن المسار المتوقع مع الفعلي، لو غلط انقل الملفات.

## أمثلة
```
المستخدم: "ابني مشروع PC-Controller"
→ تلقائياً: 
  1. ينشئ الملفات
  2. يفحص port ← 5000 مشغول ← يحول لـ 5001
  3. يفحص المكتبات ← flask ناقص ← ثبته
  4. يشغل السيرفر ← يختبره
  5. يقول: "✅ تم على http://localhost:5001"
```
