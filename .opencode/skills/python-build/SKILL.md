---
name: python-build
description: بناء Python: venv, install, build, pytest, Docker, CI/CD
---

# مهارة بناء Python

سير عمل كامل لبناء وتثبيت واختبار مشاريع Python.

---

## 1. البيئة الافتراضية

```bash
# إنشاء
python -m venv .venv

# تفعيل (Windows)
.venv\Scripts\activate

# تفعيل (Linux/Mac)
source .venv/bin/activate

# إيقاف
deactivate
```

---

## 2. تثبيت المتطلبات

```bash
# من ملف
pip install -r requirements.txt

# تثبيت المشروع للتطوير
pip install -e .

# تجميد المتطلبات
pip freeze > requirements.txt
```

### pyproject.toml (مفضل):
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "flask>=3.0",
    "pandas>=2.0",
]
```

---

## 3. بناء الحزمة

```bash
# تثبيت build
pip install build

# بناء
python -m build

# النتيجة في dist/
# dist/myapp-0.1.0.tar.gz
# dist/myapp-0.1.0-py3-none-any.whl
```

---

## 4. الاختبارات

```bash
# pytest مع التغطية
pip install pytest pytest-cov
pytest --cov=src/ --cov-report=html

# فتح تقرير التغطية
start htmlcov/index.html
```

### ملف pytest.ini:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v --cov=src/ --cov-report=term-missing
```

---

## 5. الفحص (Linting)

```bash
pip install ruff
ruff check src/ tests/
ruff format --check src/
```

---

## 6. بناء Docker

### Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "src/main.py"]
```

### البناء والتشغيل:
```bash
docker build -t myapp .
docker run -p 5000:5000 myapp
```

---

## 7. CI/CD مع GitHub Actions

### .github/workflows/python.yml:
```yaml
name: Python CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov ruff
      - run: ruff check src/
      - run: pytest --cov=src/
```

---

## 8. سير العمل الكامل

```bash
# 1. بيئة
python -m venv .venv
.venv\Scripts\activate

# 2. تثبيت
pip install -r requirements.txt
pip install -e .

# 3. فحص
ruff check src/ tests/

# 4. اختبار
pytest --cov=src/

# 5. بناء
python -m build

# 6. (اختياري) Docker
docker build -t myapp .
```
