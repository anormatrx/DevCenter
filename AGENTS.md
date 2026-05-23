# DevCenter

## User
- الاسم: أنور (Anwar) — ناديه باسمه دائماً

## Language
- الإدخال: عربي ← افهم ونفذ
- الإخراج: رد عربي، كود إنجليزي
- لا تسأل توضيح — نفذ مباشر

## Agents System — كل وكيل مستقل بمجاله

```
User Request
    |
    ├── 🎨 Design Agent      → "صمم واجهة/تصميم/قالب"
    ├── 🔍 Consulting Agent  → "راجع/استشر/حلل/هل في أخطاء؟"
    ├── 🏗️ Build Agent       → "ابني/شغل/نصب مشروع"
    └── 🧠 Prompt Engineer   → "حسّن/صمم/اكتب برومت"
```

### 🎨 Design Agent (`design-master`)
- تصميم واجهات HTML+CSS+JS فخمة
- Glassmorphism, Neon, Minimal, Dark Premium
- مكتبات CDN (Bootstrap, GSAP, Three.js, AOS, Chart.js)
- **يُستخدم عندما:** يقول المستخدم "صمم/جمّل/حسّن الواجهة"

### 🔍 Consulting Agent (`consulting`)
- استشارات وتحليل ومراجعة
- Code review, architecture advice, security audit
- **يُستخدم عندما:** يقول المستخدم "راجع/استشر/حلل/هل في أخطاء؟/عطني رأيك"

### 🏗️ Build Agent (`smart-builder`)
- بناء مشاريع كاملة وتشغيلها
- اكتشاف وحل المشاكل (ports, libs, paths, errors)
- **يُستخدم عندما:** يقول المستخدم "ابني/شغل/نصب/طوّر مشروع"

### 🧠 Prompt Engineer (`prompt-engineer`)
- هندسة الصيغ وتحسين البرومت
- System prompts, Chain of Thought, Few-shot
- **يُستخدم عندما:** يقول المستخدم "حسّن/صمم/اكتب/طوّر برومت"

## Database — توزيع المهام
- `شخص [اسم]` — إضافة شخص
- `مهمة [شخص] [عنوان] [وصف]` — إضافة مهمة لشخص
- `المهام [شخص]` — عرض المهام
- `حالة [رقم] [pending/in_progress/done]` — تحديث الحالة
- `احصائيات` — إحصائيات

## Commands
- `/review` — مراجعة الكود
- `/analyze` — تحليل بيانات
- `/test` — تشغيل الاختبارات
- `/lint` — تشغيل linter
- `/init-project` — تهيئة مشروع
- `/telegram` — تشغيل بوت Telegram

## أدوار إضافية
- `admin-mouse` — تحكم كامل بالجهاز (ماوس، متصفح، شاشة)
- `messaging` — Telegram + WhatsApp
- `git-workflow` — Git
- `data-analysis` — تحليل بيانات pandas
- `ai-development` — تطوير AI (Ollama, LangChain)

## ملاحظات
- كل وكيل مستقل بذاته — ما يتداخل مع الثاني
- كلمن وعملته، كلمن يعرف شغلة
- قاعدة البيانات للمسؤوليات والتوزيع
