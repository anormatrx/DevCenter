---
description: تهيئة مشروع جديد بهيكل متكامل (مجلدات، git, README, config)
agent: build
---

# تهيئة مشروع جديد

## الاستخدام
`/init-project <type> <name>`
- `type`: python, web, android, cli, library
- `name`: اسم المشروع

## مثال
`/init-project python myapp` → يهيئ مشروع Python في مجلد `myapp/`

## ماذا يفعل؟
1. ينشئ مجلد المشروع
2. ينشئ هيكل المجلدات (src/, tests/, docs/)
3. ينشئ الملفات الأساسية:
   - requirements.txt أو package.json
   - .gitignore مناسب للغة
   - README.md
   - AGENTS.md
   - opencode.json
4. يشغّل `git init`
5. يضيف أول commit

## خطوات التنفيذ
1. أسأل المستخدم عن نوع المشروع إذا ما specified
2. استخدم مهارة `project-setup` لتهيئة الهيكل
3. أنشئ الملفات حسب النوع (Python, Web, Android...)
4. اختبر أن كل شيء شغال (virtualenv, npm install)
5. أضف أول commit في Git

## أنواع المشاريع
- `python` - تطبيق بايثون مع virtualenv + pytest
- `web` - تطبيق ويب مع React/Vue + Vite
- `android` - تطبيق Android مع Gradle
- `cli` - أداة سطر أوامر Python
- `library` - مكتبة Python قابلة للنشر
