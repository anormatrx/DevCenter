---
name: project-setup
description: تهيئة مشاريع جديدة بهيكل كامل: مجلدات، git, README, opencode
---

# مهارة تهيئة المشاريع

تهيئة مشاريع جديدة من الصفر بهيكل متكامل.

---

## 1. هيكل المشروع

### لمشروع Python:
```
project/
├── src/
│   └── main.py
├── tests/
│   └── __init__.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
├── AGENTS.md
├── opencode.json
└── README.md
```

### لمشروع ويب (React/Vue):
```
project/
├── src/
│   ├── components/
│   ├── pages/
│   ├── App.jsx
│   └── main.jsx
├── public/
├── package.json
├── vite.config.js
├── .gitignore
├── .env.example
├── AGENTS.md
├── opencode.json
└── README.md
```

### لمشروع Android:
```
project/
├── app/
│   ├── src/main/
│   ├── build.gradle.kts
│   └── proguard-rules.pro
├── gradle/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── .gitignore
├── AGENTS.md
├── opencode.json
└── README.md
```

---

## 2. ملف .gitignore

### Python:
```gitignore
__pycache__/
*.py[cod]
.env
.venv/
dist/
*.egg-info/
```

### Node/Web:
```gitignore
node_modules/
dist/
.env
.env.local
*.log
```

### Android:
```gitignore
*.iml
.gradle/
/local.properties
/.idea/
build/
*.apk
*.aab
```

---

## 3. ملف README.md

```markdown
# اسم المشروع

## الوصف
شرح مختصر للمشروع وماذا يفعل.

## التشغيل
\`\`\`bash
# Python
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
\`\`\`

## البنية
- src/ - الكود المصدري
- tests/ - الاختبارات
- docs/ - الوثائق

## الترخيص
MIT
```

---

## 4. إعداد OpenCode

### opencode.json:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "ollama/llama3.2:3b",
  "instructions": ["AGENTS.md"],
  "permission": {
    "skill": { "*": "allow" }
  }
}
```

### AGENTS.md:
```markdown
# اسم المشروع

## لغة
- الإدخال: عربي → تنفيذ فوري
- الإخراج: شرح عربي + كود إنجليزي

## المهارات
- `python-dev` - تطوير بايثون

## الهيكل
- src/ - الكود
- tests/ - الاختبارات
```

---

## 5. الأوامر النهائية لتهيئة المشروع

```bash
# 1. أنشئ المجلدات
mkdir -p src tests docs

# 2. أضف الملفات الأساسية
echo "# Project" > README.md
echo "__pycache__/\n.env\n.venv/" > .gitignore
echo "" > src/__init__.py
echo "" > tests/__init__.py

# 3. Python: virtualenv
python -m venv .venv

# 4. Git
git init
git add .
git commit -m "chore: تهيئة المشروع"
```
