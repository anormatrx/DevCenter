# DevCenter

## المستخدم
- الاسم: أنور (Anwar)
- ناديه باسمه "أنور" دائماً

## وضع المشرف الكامل (Admin Full Control)
عندما يقول المستخدم "أنت أدمن" أو "تحكم بالماوس" أو "تولى البناء" أو "ابني المشروع":
- استخدم مهارة `admin-mouse` فوراً
- أول شيء: **اسأل "وين تريد يتم البناء؟ في أي مجلد؟"** إذا ما حدد المسار
- ثبّت المكتبات القوية: `playwright` + `pyautogui` + `pygetwindow` + `keyboard` + `pyperclip`
- افتح المتصفح **بشكل مرئي** (ليس headless) عشان المستخدم يشوف
- **تحكم كامل:**
  - 🖱️ تحريك الماوس ونقر على الأزرار
  - 🔤 تعبئة الحقول (fill forms, type)
  - 🌐 التنقل بين الصفحات (goto, back, forward)
  - 📸 تصوير الشاشة للتأكيد
  - 🪟 التحكم بالنوافذ (تكبير، تصغير، تنشيط)
  - ⌨️ اختصارات لوحة المفاتيح (Ctrl+C/V, Alt+Tab)
- أبلغ المستخدم بكل خطوة بالعربي
- إذا فشلت، جرّب المكتبة الثانية — **لا تستسلم**

## اللغة + وضع الترجمة التنفيذية
- **الإدخال**: المستخدم يكتب بالعربية — افهمها ونفذها
- **الإخراج**: الرد بالعربية، الكود بالإنجليزية
- **التنفيذ**: حول العربية لأوامر فعلية
- المستخدم: "اعمل مجلد" → تنفيذ فوري
- المستخدم: "شغّل الاختبارات" → تنفيذ الأمر مباشرة
- لا تسأل توضيح — نفذ على طول

## الأوامر المخصصة
- `/test [path]` - تشغيل الاختبارات (يكتشف الإطار المناسب تلقائياً: pytest, vitest, Gradle...)
- `/analyze [file]` - تحليل البيانات (CSV, Excel, JSON) مع رسوم بيانية وتقارير
- `/init-project <type> <name>` - تهيئة مشروع جديد (python, web, android, cli, library)
- `/review` - مراجعة الكود (أخطاء، أمان، أداء)
- `/lint` - تشغيل الـ linter
- `/telegram` - تشغيل بوت التحكم عن بعد عبر Telegram

## المهارات المتاحة (اختر المناسب للمهمة)

### تطوير وبناء
- `python-dev` - Python كامل: type hints, PEP 8, testing, logging, دوال مساعدة
- `python-build` - بناء Python: venv, install, build, pytest coverage, Docker, CI/CD
- `web-dev` - 🆕 تطوير ويب كامل: فتح متصفح، جلب مكتبات، بناء دردشة، ربط بالسيرفر
- `web-build` - بناء ويب: npm, vite, webpack, env vars, deploy (Vercel, Netlify, Pages)
- `android-build` - بناء Android: Gradle, APK, AAB, signing, Google Play
- `build-automation` - أتمتة: Taskfile, pre-commit hooks, CI/CD, scripts, changelog

### تحليل وذكاء اصطناعي
- `data-analysis` - تحليل بيانات: pandas, matplotlib, numpy, sklearn, تنظيف، تصور، تقارير
- `ai-development` - تطوير AI: Ollama, LangChain, Streaming, Fallback, Evaluation, API keys

### أدوات
- `git-workflow` - Git كامل: commits, branches, merge, rebase, cherry-pick, stash, bisect, حل تعارضات
- `code-review` - مراجعة كود: أخطاء منطقية، أمان، أداء، type hints، SQL injection، XSS، checklist
- `project-setup` - تهيئة مشاريع: هيكل كامل (Python/Web/Android), .gitignore, README, opencode config

### تواصل (تحكم عن بعد)
- `messaging` - 🆕 تحكم كامل من Telegram + WhatsApp: فهم عربي بالذكاء الاصطناعي، تنفيذ أوامر، بناء مشاريع، بحث ويب، قراءة ملفات (يتطلب API key من @BotFather)

### تحكم وإدارة
- **`admin-mouse`** - 🆕 تحكم كامل: ماوس + متصفح + نقر + تنقل + تعبئة حقول + بناء مشاريع + إصلاح

## المشاريع
### نشط
- `GitRepos/MyApp/` - تحليل بيانات + AI (Python)
- `PythonAI/AI_Assistant/` - بيئة تطوير AI

### قيد الإنشاء
- `AndroidProjects/` - مشاريع Android
- `WebApps/` - تطبيقات ويب (ChatApp server شغال + ملاحظات)
- `Tools/` - أدوات و scripts (notes.py جاهز)
- `Logs/` - سجلات وملفات (logger.py + start-session.ps1)

## التشغيل 24/7
- `run-opencode-247.bat` - شغّل OpenCode بدون انقطاع (يمنع السكون + auto-restart)
- `install-opencode-247.ps1` - ثبّت المهمة في Task Scheduler للبدء مع الويندوز (شغّله كـ Administrator)
- `start-opencode.bat` - تشغيل عادي

## ملاحظات
- افتح opencode داخل مجلد المشروع المحدد
- استخدم `/init` لتحديث AGENTS.md لكل مشروع
- المهارات تحمل تلقائياً حسب السياق
