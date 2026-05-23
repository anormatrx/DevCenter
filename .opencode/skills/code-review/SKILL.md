---
name: code-review
description: مراجعة الكود: أخطاء، أمان، أداء، type hints، اختبارات
---

# مهارة مراجعة الكود

قائمة فحص شاملة لمراجعة جودة الكود.

---

## 1. الأخطاء المنطقية

- [ ] هل فيه **حلقات لا نهائية** (while True بدون break)؟
- [ ] هل المتغيرات **مستخدمة قبل تعريفها**؟
- [ ] هل المقارنات صحيحة (`==` وليس `=` في الشرط)؟
- [ ] هل ترجع الدالة القيمة المتوقعة في **كل المسارات**؟
- [ ] هل يتعامل مع **الحالات الحدية** (empty list, None, 0)؟

---

## 2. نوع البيانات (Type Hints)

```python
# ✅ صح
def add(a: int, b: int) -> int:
    return a + b

# ❌ خطأ
def add(a, b):       # بدون type hints
    return a + b
```

- [ ] كل الدوال العامة عندها type hints
- [ ] تستخدم `Optional[X]` للقيم اللي ممكن تكون None
- [ ] تستخدم `List[X]`, `Dict[K, V]` بدل list, dict

---

## 3. معالجة الأخطاء

```python
# ✅ صح
try:
    data = api_call()
except requests.Timeout:
    print("الطلب تجاوز الوقت")
except requests.RequestException as e:
    print(f"خطأ في الطلب: {e}")
    raise

# ❌ خطأ
try:
    data = api_call()
except Exception:  # واسع جداً
    pass            # يخفي الخطأ
```

- [ ] الـ try/except **محدد** (يختار استثناءات معينة)
- [ ] ما في `except:` بدون تحديد
- [ ] الأخطاء الحقيقية **تتسجل** (logging) مش `pass`
- [ ] الموارد تتقفل (file close, db close) في `finally`

---

## 4. الأداء

- [ ] لا توجد **حلقات متداخلة غير ضرورية** (O(n²) ويمكن O(n))
- [ ] **قراءة/كتابة الملفات** مرة واحدة (بدل تكرار fopen/fclose)
- [ ] **استعلامات قاعدة البيانات** مركبة (بدل N+1 queries)
- [ ] استخدام **generators** للبيانات الكبيرة بدل loading الكل في RAM

### مقارنة:
```python
# ❌ بطيء - يحمل كل الملف
with open("large.txt") as f:
    lines = f.readlines()
    for line in lines:
        process(line)

# ✅ سريع - يقرأ سطر سطر
with open("large.txt") as f:
    for line in f:
        process(line)
```

---

## 5. الأمان

- [ ] **API keys** مخزنة في `.env` مش في الكود
- [ ] **SQL injection** محمي (استخدام parameterized queries)
- [ ] **XSS** محمي (تشفير المخرجات HTML)
- [ ] **CSRF tokens** في النماذج
- [ ] **صلاحيات الملفات** مضبوطة (لا 777 للملفات الحساسة)
- [ ] **كلمات المرور** مشفرة (bcrypt, argon2)

### SQL:
```python
# ❌ خطير
cursor.execute(f"SELECT * FROM users WHERE id = {user_input}")

# ✅ آمن
cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
```

---

## 6. الاختبارات

- [ ] **اختبارات الوحدة** (unit tests) للدوال المهمة
- [ ] **الحالات الحدية** مختبرة (empty, null, negative)
- [ ] **الأخطاء المتوقعة** مختبرة (تتأكد أن الدالة ترمي الخطأ الصحيح)
- [ ] **التغطية** كافية (على الأقل 70%-80%)

---

## 7. النمط والتنظيم

- [ ] الكود يتبع **PEP 8** (Python) أو **Standard** (JavaScript)
- [ ] **أسماء المتغيرات** واضحة (لا `x`, `tmp` إلا في حلقات صغيرة)
- [ ] **الدوال** صغيرة (أقل من 30 سطر)
- [ ] **التعليقات** بالعربية أو الإنجليزية (لا تعليقات قديمة محذوفة)
- [ ] **المكتبات الخارجية** محددة في requirements.txt / package.json

---

## 8. قائمة الفحص السريع

| الرقم | البند | ✅ / ❌ |
|-------|-------|---------|
| 1 | نوع البيانات (type hints) | |
| 2 | معالجة الأخطاء (try/except) | |
| 3 | الأداء (حلقات، استعلامات) | |
| 4 | الأمان (API keys, SQL, XSS) | |
| 5 | الاختبارات (unit + edge cases) | |
| 6 | النمط (PEP 8, أسماء واضحة) | |
| 7 | الوثائق (README, docstrings) | |
| 8 | المكتبات (requirements.txt) | |
