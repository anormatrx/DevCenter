---
description: تشغيل الاختبارات واكتشاف وتثبيت إطار الاختبار المناسب
agent: build
---

# تشغيل الاختبارات

## الاستخدام
`/test` أو `/test <path>`

## ماذا يفعل؟
1. يكتشف إطار الاختبار المناسب للمشروع
2. يركّب الأدوات إذا ما مثبتة
3. يشغّل الاختبارات ويعرض النتائج

## خطوات التنفيذ
1. **اكتشاف نوع المشروع**:
   - Python: هل في pytest, unittest, أو nose؟
   - Node: هل في vitest, jest, أو mocha؟
   - Android: هل في Gradle test؟

2. **إذا ما في إطار اختبار**:
   - Python: ثبّت pytest + pytest-cov
   - Node: ثبّت vitest
   - Android: استخدم Gradle

3. **تشغيل الاختبارات**:
   - Python: `pytest -v --cov=src/`
   - Node: `npm test` أو `npx vitest run`
   - Android: `./gradlew test`

4. **عرض التقرير**:
   - اعرض عدد النجاح/الفشل
   - اعرض نسبة التغطية (coverage)
   - حدد الاختبارات الفاشلة إن وجدت

## أمثلة
- `/test` → يشغّل كل الاختبارات في المشروع
- `/test tests/test_main.py` → يشغّل ملف محدد
- `/test tests/` → يشغّل مجلد اختبارات محدد
