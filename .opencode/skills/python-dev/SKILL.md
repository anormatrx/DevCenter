---
name: python-dev
description: تطوير Python كامل: type hints, pep 8, testing, project templates
---

# مهارة تطوير Python

إرشادات كاملة لكتابة Python نظيف وقوي.

---

## 1. هيكل المشروع القياسي

```
project-name/
├── src/
│   ├── __init__.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
├── .venv/
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

---

## 2. Type Hints (إلزامي من Python 3.10+)

```python
from typing import Optional, List, Dict, Union

def greet(name: str, age: Optional[int] = None) -> str:
    """ترحيب بالمستخدم."""
    if age:
        return f"مرحباً {name}، عمرك {age}"
    return f"مرحباً {name}"
```

---

## 3. نمط الكود (PEP 8)

```python
# ✅ صح
def calculate_total(items: List[float]) -> float:
    return sum(items)

# ❌ خطأ
def calculate_total(items): return sum(items)  # لا type hints
```

### أدوات الفحص:
```bash
pip install black ruff
black src/ tests/            # تنسيق تلقائي
ruff check src/ tests/        # فحص الأخطاء
ruff format src/ tests/       # تنسيق مثل black
```

---

## 4. إدارة المكتبات

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
pip freeze > requirements.txt # بعد إضافة مكتبات
```

### requirements.txt:
```
flask>=3.0
pandas>=2.0
pytest>=8.0
ruff>=0.5
```

---

## 5. الاختبارات (Testing)

```python
# tests/test_main.py
import pytest
from src.main import calculate_total

def test_calculate_total():
    assert calculate_total([1, 2, 3]) == 6
    assert calculate_total([]) == 0
    assert calculate_total([-1, 1]) == 0

def test_calculate_total_float():
    result = calculate_total([1.5, 2.5])
    assert result == 4.0
```

### التشغيل:
```bash
pytest                    # كل الاختبارات
pytest -v                 # مع تفاصيل
pytest --cov=src/         # مع تغطية
pytest -k "test_calc"     # اختبار معين
```

---

## 6. معالجة الأخطاء

```python
# ✅ try/except محدد
try:
    result = risky_operation()
except ValueError as e:
    print(f"خطأ في القيمة: {e}")
except Exception as e:
    print(f"خطأ غير متوقع: {e}")
    raise  # أعد رفع الخطأ إذا ما تعرف تتعامل معه

# ❌ try/except عام بدون معالجة
try:
    result = risky_operation()
except:  # ياخذ كل الأخطاء!
    pass  # يخفي الخطأ!
```

---

## 7. دوال مساعدة جاهزة

```python
import json, os
from pathlib import Path

def read_json(path: str) -> dict:
    """قراءة ملف JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path: str, data: dict) -> None:
    """كتابة ملف JSON."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ensure_dir(path: str) -> Path:
    """تأكد من وجود المجلد."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
```

---

## 8. Logging بدلاً من print

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("التطبيق شغال")
logger.error("حدث خطأ!")
```
