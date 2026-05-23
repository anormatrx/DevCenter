---
description: تشغيل مدقق الكود (linter) واكتشاف الأداة المناسبة تلقائياً
agent: build
subtask: true
---

# تشغيل Linter

## ماذا يفعل؟
1. يكتشف لغة المشروع ونوع الـ linter المناسب
2. يركّب الأداة إذا ما مثبتة
3. يشغّل الفحص ويصحح الأخطاء تلقائياً

## الـ linters حسب اللغة:
- **Python**: `ruff check src/ tests/` أو `flake8`
- **JavaScript/TypeScript**: `npx eslint src/`
- **CSS**: `npx stylelint "src/**/*.css"`
- **HTML**: `npx html-validate src/`
- **Python format**: `ruff format src/ tests/`
- **Pre-commit**: `pre-commit run --all-files`

## خطوات التنفيذ
1. افحص وجود ملفات المشروع (Python, JS, CSS...)
2. اختر الـ linter المناسب
3. شغّل الفحص
4. حلّ الأخطاء إن وجدت (أو استخدم `--fix`)
5. أبلغ المستخدم بالنتيجة

## أمثلة
- `/lint` → يكتشف النوع ويشغّل الفحص
- `/lint --fix` → يصحح الأخطاء التلقائية
