---
name: format-master
description: تنسيق احترافي للكود والواجهات — ترتيب، محاذاة، أناقة، تناسق، جماليات
---

# مهارة التنسيق الاحترافي (Format Master)

تنسيق كل شيء بشكل احترافي: كود، واجهات، نصوص، ملفات، تقارير.

## متى تفعّل
- "نسق الكود"
- "رتب الواجهة"
- "حسن الشكل"
- "خله احترافي"
- "ظبط التنسيق"
- "حسن الخطوط والألوان"
- "نسق الملفات"
- أي أمر يتعلق بالشكل والترتيب والجماليات

---

## 1. تنسيق الكود (Code Formatting)

### 1.1 Python — Black + Ruff
```bash
# تنسيق تلقائي كامل
pip install black ruff
black .                      # نسق كل ملفات Python
black file.py --line-length 100  # بطول سطر 100

# فحص الجودة
ruff check .                 # فحص سريع
ruff check . --fix           # اصلاح تلقائي
ruff format .                # تنسيق مثل Black
```

### 1.2 JavaScript/TypeScript — Prettier
```bash
npm install -g prettier
prettier --write "src/**/*.{js,ts,jsx,tsx}"
prettier --write "*.{json,css,md}"
```

### 1.3 HTML/CSS — Prettier + Stylelint
```bash
prettier --write "**/*.html" --parser html
prettier --write "**/*.css"
npx stylelint "**/*.css" --fix
```

### 1.4 قواعد التنسيق الأساسية

```python
# ✅ احترافي
def calculate_total(items: list, discount: float = 0.0) -> float:
    """حساب المجموع مع الخصم"""
    subtotal = sum(item.price * item.quantity for item in items)
    return subtotal * (1 - discount)


# ❌ غير مهذب
def calc(items,discount=0):
    x=0
    for i in items:x+=i.price*i.quantity
    return x*(1-discount)
```

```javascript
// ✅ احترافي
function formatDate(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// ❌ غير مهذب
function formatDate(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')}
```

### 1.5 Config Files

**`.prettierrc`** — تنسيق موحد لكل المشروع:
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 100,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

**`pyproject.toml`** — للـ Python:
```toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "single"
```

---

## 2. تنسيق الواجهات (UI Formatting)

### 2.1 المسافات والتناسق — CSS Methodology

```css
/* ✅ منهجية احترافية: System Design Tokens */
:root {
  /* Spacing scale */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* Typography */
  --font-sans: 'Segoe UI', 'Noto Sans Arabic', system-ui, sans-serif;
  --font-mono: 'Cascadia Code', 'JetBrains Mono', 'Consolas', monospace;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 20px;
  --text-xl: 24px;
  --text-2xl: 32px;

  /* Colors */
  --color-bg: #0d1117;
  --color-surface: #161b22;
  --color-border: #30363d;
  --color-text: #e6edf3;
  --color-text-secondary: #8b949e;
  --color-accent: #3fb950;
  --color-danger: #f85149;
  --color-warning: #d29922;
  --color-info: #58a6ff;

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.3);
}

/* ✅ Composition - building blocks */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
}

.card:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow-md);
}

/* ✅ RTL support */
[dir="rtl"] .icon-left {
  margin-left: var(--space-sm);
  margin-right: 0;
}
```

```css
/* ❌ فوضوي */
*{margin:0;padding:0}
div{border:1px solid #ccc;background:#fff;padding:10px;margin:5px;border-radius:5px}
.a{color:blue;font-size:14px}
.b{color:red;font-size:16px}
```

### 2.2 مكونات متسقة — Component Pattern

```html
<!-- ✅ منسق ومنظم -->
<div class="card">
  <div class="card-header">
    <h3 class="card-title">عنوان البطاقة</h3>
    <span class="card-badge">جديد</span>
  </div>
  <div class="card-body">
    <p>نموذج نصي يمثل محتوى البطاقة بشكل منسق ومرتب.</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-primary">حفظ</button>
    <button class="btn btn-secondary">إلغاء</button>
  </div>
</div>
```

```css
/* ✅ BEM methodology */
.card { }
.card__header { }
.card__title { }
.card__body { }
.card__footer { }
.card--featured { }
.card--disabled { }
```

### 2.3 ألوان متناسقة — Color System

```css
/* ✅ نظام ألوان متكامل */
:root {
  /* Primary */
  --primary-50: #e6f7ed;
  --primary-100: #c3ebd4;
  --primary-200: #9ddfb9;
  --primary-300: #6ed09a;
  --primary-400: #4ac482;
  --primary-500: #3fb950;   /* Main */
  --primary-600: #34a545;
  --primary-700: #288f38;
  --primary-800: #1d7a2c;
  --primary-900: #0f5e1e;

  /* Neutral grays */
  --gray-50: #f0f2f5;
  --gray-100: #d0d5db;
  --gray-200: #b0b8c4;
  --gray-300: #8b949e;
  --gray-400: #6e7681;
  --gray-500: #555d68;
  --gray-600: #3d444e;
  --gray-700: #30363d;
  --gray-800: #21262d;
  --gray-900: #161b22;
  --gray-950: #0d1117;
}
```

---

## 3. تنسيق الملفات (File Organization)

### 3.1 هيكل المشروع الاحترافي

```
my-project/
├── src/                    # كود المصدر
│   ├── components/         # مكونات الواجهة
│   ├── services/           # خدمات API
│   ├── styles/             # أنماط CSS
│   ├── utils/              # دوال مساعدة
│   └── types/              # أنواع البيانات
├── tests/                  # اختبارات
├── public/                 # ملفات ثابتة
├── server/                 # Backend (إن وجد)
├── scripts/                # سكريبتات مساعدة
├── docs/                   # توثيق
├── .github/                # CI/CD
├── .vscode/                # إعدادات المحرر
├── .prettierrc
├── .eslintrc.js
├── tsconfig.json
├── package.json
├── README.md
└── LICENSE
```

### 3.2 ترتيب الأكواد داخل الملف

```python
# ✅ ترتيب مثالي
"""
module docstring
"""
from __future__ import annotations

# 1. المكتبات الأساسية
import os
import sys
from pathlib import Path

# 2. مكتبات خارجية
import requests
from flask import Flask

# 3. مكتبات محلية
from .utils import helper
from .models import BaseModel

# 4. ثوابت
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# 5. كلاسات
class Service:
    """وصف الكلاس"""
    pass

# 6. دوال
def main():
    """وصف الدالة"""
    pass

# 7. نقطة الدخول
if __name__ == "__main__":
    main()
```

```javascript
// ✅ ترتيب مثالي
'use strict';

// 1. المكتبات
import React from 'react';
import { useState, useEffect } from 'react';

// 2. المكونات المحلية
import Header from './Header';
import Footer from './Footer';

// 3. ثوابت
const API_URL = process.env.REACT_APP_API_URL;

// 4. Types
interface Props {
  title: string;
  children: React.ReactNode;
}

// 5. المكون الرئيسي
export function Card({ title, children }: Props) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
}
```

---

## 4. تنسيق التقارير والمخرجات (Output Formatting)

### 4.1 Markdown احترافي

```markdown
# عنوان رئيسي

## عنوان ثانوي

### عنوان ثالثي

**نص عريض** | *نص مائل* | ~~نص مشطوب~~ | `كود` 

> اقتباس مهم: هذا النص مقتبس من مصدر موثوق.

- عنصر قائمة غير مرقمة
- عنصر آخر
  - عنصر فرعي

1. خطوة أولى
2. خطوة ثانية
3. خطوة ثالثة

| الاسم     |  العمر  |  المدينة  |
|----------|:-------:|:---------:|
| أحمد     |   25    |  الرياض  |
| سارة     |   30    |  جدة     |
| محمد     |   28    |  الدمام   |

```python
def hello():
    print("مرحباً")
```

[رابط إلى Google](https://google.com)

![صورة](image.png)
```

### 4.2 تنسيق مخرجات الطرفية

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from rich.syntax import Syntax

console = Console()

# ✅ جداول جميلة
table = Table(title="المشاريع")
table.add_column("الاسم", style="cyan")
table.add_column("الحالة", style="green")
table.add_column("الحجم")
table.add_row("DevCenter", "✅ شغال", "12MB")
table.add_row("ChatApp", "✅ شغال", "4MB")
console.print(table)

# ✅ أكواد ملونة
code = Syntax('print("Hello")', "python", theme="monokai")
console.print(code)

# ✅ شريط تقدم
with Progress() as progress:
    task = progress.add_task("تحميل...", total=100)
    for _ in range(100):
        progress.update(task, advance=1)
        time.sleep(0.02)
```

### 4.3 تنسيق JSON

```python
# ✅ منسق ومقروء
import json

data = {"name": "DevCenter", "version": "1.0", "services": ["api", "web"]}
print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
# {
#   "name": "DevCenter",
#   "services": ["api", "web"],
#   "version": "1.0"
# }
```

---

## 5. دوال مساعدة للتنسيق

### 5.1 تنسيق تلقائي للمشروع كامل

```python
import subprocess
from pathlib import Path

def format_project(path: str = "."):
    """تنسيق كل ملفات المشروع بشكل احترافي"""
    path = Path(path)
    results = []

    # Python
    if list(path.rglob("*.py")):
        subprocess.run(["black", str(path), "--line-length", "100"], capture_output=True)
        subprocess.run(["ruff", "check", str(path), "--fix"], capture_output=True)
        results.append("✅ Python: Black + Ruff")

    # JS/TS
    if list(path.rglob("*.{js,ts,jsx,tsx}")):
        subprocess.run(["prettier", "--write", f"{path}/**/*.{js,ts,jsx,tsx}"], capture_output=True)
        results.append("✅ JS/TS: Prettier")

    # HTML/CSS
    if list(path.rglob("*.{html,css}")):
        subprocess.run(["prettier", "--write", f"{path}/**/*.html", "--parser", "html"], capture_output=True)
        subprocess.run(["prettier", "--write", f"{path}/**/*.css"], capture_output=True)
        results.append("✅ HTML/CSS: Prettier")

    # JSON
    if list(path.rglob("*.json")):
        subprocess.run(["prettier", "--write", f"{path}/**/*.json"], capture_output=True)
        results.append("✅ JSON: Prettier")

    return results
```

### 5.2 تنسيق نص عربي

```python
import re

def format_arabic_text(text: str) -> str:
    """تنسيق النص العربي — محاذاة، تشكيل، ترقيم"""
    # إزالة المسافات الزائدة
    text = re.sub(r' +', ' ', text)
    # تأكيد اتجاه RTL
    text = f"\u202B{text}\u202C"
    # توحيد علامات الترقيم
    text = text.replace('?', '؟').replace(',', '،').replace(';', '؛')
    # مسافات بعد علامات الترقيم
    text = re.sub(r'([،؛؟!])([^\s])', r'\1 \2', text)
    return text.strip()


def align_table(data: list, headers: list) -> str:
    """جدول منسق بالعربي"""
    col_widths = [len(h) for h in headers]
    for row in data:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    lines = []
    sep = " | ".join("-" * w for w in col_widths)
    lines.append(" | ".join(h.ljust(w) for h, w in zip(headers, col_widths)))
    lines.append(sep)
    for row in data:
        cells = [str(c).ljust(w) for c, w in zip(row, col_widths)]
        lines.append(" | ".join(cells))
    return "\n".join(lines)
```

### 5.3 CSS Minifier / Formatter

```python
import re

def minify_css(css: str) -> str:
    """تصغير CSS للإنتاج"""
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)  # إزالة التعليقات
    css = re.sub(r'\s+', ' ', css)             # مسافات مفردة
    css = re.sub(r'\s*([{};:,])\s*', r'\1', css)  # مسافات حول الرموز
    return css.strip()


def beautify_css(css: str) -> str:
    """تجميل CSS للقراءة"""
    css = re.sub(r'\{', ' {\n  ', css)
    css = re.sub(r';', ';\n  ', css)
    css = re.sub(r'\}', '\n}\n\n', css)
    return css.strip()
```

### 5.4 إنشاء ملف الإعدادات الموحد

```python
def create_format_config(path: str = "."):
    """إنشاء ملفات إعدادات التنسيق للمشروع"""
    path = Path(path)

    # .prettierrc
    prettier = {
        "semi": True,
        "singleQuote": True,
        "tabWidth": 2,
        "trailingComma": "all",
        "printWidth": 100,
        "arrowParens": "always",
        "endOfLine": "lf",
    }
    (path / ".prettierrc").write_text(json.dumps(prettier, indent=2))

    # pyproject.toml
    toml = """[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "single"
"""
    (path / "pyproject.toml").write_text(toml)

    # .editorconfig
    editorconfig = """root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4
"""
    (path / ".editorconfig").write_text(editorconfig)

    return "✅ تم إنشاء: .prettierrc, pyproject.toml, .editorconfig"
```

---

## 6. أمثلة عملية

### 6.1 تنسيق مشروع كامل

```bash
# من سطر الأوامر
python D:\DevCenter\.opencode\skills\format-master\format.py "D:\DevCenter\WebApps\ChatApp"
```

```python
# من الكود
from format import format_project

results = format_project("D:/DevCenter/WebApps/ChatApp")
for r in results:
    print(r)
# ✅ Python: Black + Ruff
# ✅ HTML/CSS: Prettier
# ✅ JSON: Prettier
```

### 6.2 تنسيق ملف واحد

```python
# Black لملف Python واحد
import subprocess
subprocess.run(["black", "server.py", "--line-length", "100"])

# Prettier لملف HTML
subprocess.run(["prettier", "--write", "index.html", "--parser", "html"])
```

### 6.3 تحسين واجهة HTML/CSS

```python
from format import beautify_css, create_format_config

# جمّل ملف CSS
css = Path("style.css").read_text()
Path("style.css").write_text(beautify_css(css))

# أنشئ إعدادات التنسيق
create_format_config()
```

---

## 7. قائمة التنسيق السريعة

| المهمة | الأمر/الكود |
|--------|------------|
| 🐍 Python | `black . && ruff check --fix .` |
| 📜 JS/TS | `prettier --write "src/**/*.{js,ts}"` |
| 🌐 HTML | `prettier --write "**/*.html" --parser html` |
| 🎨 CSS | `prettier --write "**/*.css"` |
| 📄 JSON | `prettier --write "**/*.json"` |
| 📝 Markdown | `prettier --write "**/*.md" --parser markdown` |
| 🔧 إنشاء إعدادات | `create_format_config()` |
| 📏 قياس الجودة | `ruff check .` |
| 🧹 تنظيف المسافات | `editorconfig` + Prettier |
| 🎯 محاذاة عربي | `format_arabic_text()` |
| 🖼️ واجهة منسقة | Design Tokens + BEM |

---

## 8. المبادئ الذهبية للتنسيق

1. **التناسق أهم من الصحة** — اختر أسلوباً واحداً والتزم به
2. **Design Tokens** — كل القيم في متغيرات في مكان واحد
3. **Spacing Scale** — 4, 8, 16, 24, 32, 48 (مضاعفات 4)
4. **BEM Methodology** — `block__element--modifier`
5. **RTL First** — `margin-inline-start` بدل `margin-left`
6. **80/100 خط** — لا تتجاوز 100 حرف بالسطر
7. **أسماء معبرة** — `calculateTotal` لا `calc`
8. **تعليقات مفيدة** — `# WHY:` لا `# what:`
9. **فراغات منظمة** — سطر فارغ بين sections
10. **أوتوماتيكياً** — استخدم formatter دائماً، لا تنسق يدوياً
