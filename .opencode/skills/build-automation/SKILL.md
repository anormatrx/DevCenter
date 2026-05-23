---
name: build-automation
description: أتمتة البناء: Taskfile, pre-commit, CI/CD, scripts, changelog
---

# مهارة أتمتة البناء

أتمتة سير العمل: فحص → بناء → اختبار → نشر.

---

## 1. Taskfile (أفضل من Makefile في Windows)

### Taskfile.yml:
```yaml
version: '3'
tasks:
  setup:
    desc: تثبيت المتطلبات
    cmds:
      - python -m venv .venv
      - .venv\Scripts\pip install -r requirements.txt

  lint:
    desc: فحص الكود
    cmds:
      - ruff check src/ tests/

  test:
    desc: تشغيل الاختبارات
    cmds:
      - pytest --cov=src/

  build:
    desc: بناء المشروع
    deps: [lint, test]
    cmds:
      - python -m build

  docker:
    desc: بناء Docker
    cmds:
      - docker build -t myapp .

  all:
    desc: كل شيء
    deps: [lint, test, build]
```

### التثبيت والتشغيل:
```bash
# تثبيت Task
winget install Task.Task

# تشغيل
task setup
task lint
task test
task build
task all
```

---

## 2. Pre-commit Hooks

### .pre-commit-config.yaml:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
      - id: ruff-format
```

### التثبيت:
```bash
pip install pre-commit
pre-commit install          # يتفعل مع كل commit
pre-commit run --all-files # فحص الملفات كلها
```

---

## 3. CI/CD خطوط الأنابيب

### GitHub Actions (متعدد المهارات):
```yaml
name: CI/CD
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install ruff
      - run: ruff check src/

  test:
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt pytest
      - run: pytest

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: echo "نشر..."
```

---

## 4. سكريبتات الأتمتة

### scripts/setup.ps1 (Windows):
```powershell
# إعداد المشروع بالكامل
Write-Host "إعداد المشروع..." -ForegroundColor Green

# 1. البيئة الافتراضية
python -m venv .venv
.venv\Scripts\pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt

# 2. pre-commit
.venv\Scripts\pip install pre-commit
.venv\Scripts\pre-commit install

# 3. Git hooks
git config core.hooksPath .githooks

Write-Host "تم الإعداد!" -ForegroundColor Green
```

### scripts/build.sh (Linux/Mac):
```bash
#!/bin/bash
set -e
echo "بناء المشروع..."
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install build
python -m build
echo "اكتمل البناء!"
```

---

## 5. Changelog (سجل التغييرات)

### CHANGELOG.md:
```markdown
# Changelog

## [1.1.0] - 2026-05-23
### Added
- إدارة المستخدمين (تسجيل، دخول)

## [1.0.0] - 2026-05-01
### Added
- الإصدار الأول: دردشة أساسية
```

### أتمتة الـ changelog:
```bash
# باستخدام git-cliff
pip install git-cliff
git cliff -o CHANGELOG.md
```

---

## 6. سير العمل الكامل

```bash
# عند بداية مشروع جديد:
# 1. إنشاء Taskfile.yml
# 2. إعداد pre-commit hooks
# 3. إنشاء scripts/setup.ps1
# 4. إعداد CI/CD (GitHub Actions)
# 5. إضافة CHANGELOG.md

# لكل commit:
# pre-commit يشتغل تلقائياً → يفحص الكود

# لكل push:
# GitHub Actions يشتغل → lint → test → build
```
