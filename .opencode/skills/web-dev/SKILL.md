---
name: web-dev
description: تطوير ويب كامل - فتح متصفح، جلب مكتبات، ربط بالسيرفر، بناء تطبيقات
---

# مهارة تطوير الويب الكاملة

## 1. فتح المتصفح والاختبار
- استخدم `webfetch` أو `bash` لفتح المتصفح عند الحاجة
- اختبر الواجهة في المتصفح المحلي: `http://localhost:XXXX`
- تأكد أن السيرفر يشغل قبل فتح المتصفح

## 2. جلب المكتبات المطلوبة
- اقرأ الكود الموجود وحدد المكتبات الناقصة
- استخدم `npm install <package>` أو `pip install <package>` حسب المشروع
- أضف المكتبات تلقائياً لـ `package.json` أو `requirements.txt`

### مكتبات شائعة حسب المشروع:
- **React:** `npm install react react-dom react-router-dom`
- **Vue:** `npm install vue vue-router pinia`
- **Node/Express:** `npm install express cors dotenv mongoose socket.io`
- **Python/Flask:** `pip install flask flask-cors python-dotenv flask-socketio`
- **Python/FastAPI:** `pip install fastapi uvicorn websockets`

## 3. بناء تطبيقات واجهة دردشة (Chat)
اذا كان المشروع **واجهة دردشة** تأكد من:
- [ ] النموذج (AI model) مربوط بالواجهة (API endpoint)
- [ ] السيرفر شغال ومستقبل للطلبات
- [ ] رسائل الدردشة ترسل وتستقبل بشكل صحيح
- [ ] WebSocket أو SSE شغال للردود المباشرة
- [ ] الأزرار (إرسال، مسح، إعدادات) مرتبطة بالدوال الصحيحة

### هيكل دردشة نموذجي:
```
project/
├── client/          # واجهة المستخدم (React/Vue)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Chat.jsx       # مكون الدردشة
│   │   ├── Settings.jsx   # إعدادات النموذج
│   │   └── api.js         # ربط مع السيرفر
│   └── package.json
├── server/          # السيرفر (Node/Python)
│   ├── index.js        # نقطة البداية
│   ├── routes/chat.js  # مسارات الدردشة
│   └── models/         # ربط مع AI model
└── README.md
```

## 4. البناء والتشغيل
- بناء الواجهة: `cd client && npm run build`
- تشغيل السيرفر: `cd server && npm start` أو `python server.py`
- ربط السيرفر مع النموذج عبر API key

## 5. التأكد من الربط
- إذا المشروع فيه **AI model**، تأكد من ربط API key في ملف `.env`
- إذا في **WebSocket**، تأكد من الاتصال بين client و server
- اختبر الإرسال والاستقبال يدوياً

## 6. التعلم من الأخطاء
- سجل الأخطاء في ملف log
- حل المشكلة واختبرها مرة ثانية
- لا تكرر نفس الخطأ — ارجع للكود وتأكد من الحل

## 7. الأزرار والإعدادات
- زر الإرسال ← يربط بـ API/WebSocket
- زر المسح ← يمسح المدخلات
- زر الإعدادات ← يفتح نافذة تعديل (API key, model, theme)
- تأكد من ربط كل زر بالدالة المناسبة
