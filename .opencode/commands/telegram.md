---
description: تشغيل بوت التحكم عن بعد عبر Telegram (فهم عربي بالذكاء الاصطناعي)
agent: build
---

# التحكم عن بعد عبر Telegram

## الاستخدام
`/telegram` - تشغيل بوت Telegram

## قبل التشغيل
عدّل ملف `Tools/.env.comm`:
- `TELEGRAM_BOT_TOKEN` — من @BotFather في Telegram
- `TELEGRAM_CHAT_ID` — من @userinfobot في Telegram

## ما تسوي عن بعد؟
- "ابني مشروع ويب اسمه myapp" → يبني مشروع
- "شغّل السيرفر" → يشغّل Flask
- "حمل مكتبة requests" → pip install
- "جيبلي موضوع عن الذكاء الاصطناعي" → بحث ويب
- "حلل المشروع" → تحليل كود
- "اقرأ ملف server.py" → يعرض الملف
- "أظهر لي الملفات" → يعرض المجلدات
- "اختبر المشروع" → تشغيل pytest

## للتشغيل 24/7
شغّل ملف `Tools\run-telegram-bot.bat`
