---
name: messaging
description: 🚀 تحكم كامل عن بعد عبر Telegram + WhatsApp مع AI - فهم عربي وتنفيذ
---

# مهارة التحكم عن بعد (Telegram + WhatsApp)

تحكم بمشاريعك كاملة من أي مكان في العالم عبر Telegram.
**تكلم عربي والبوت يفهم وينفذ!**

---

## 1. الإعدادات

عدّل ملف `Tools/.env.comm`:
```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...     # من @BotFather
TELEGRAM_CHAT_ID=123456789                # من @userinfobot
WHATSAPP_NUMBER=96650xxxxxxx              # رقم مع مفتاح الدولة
```

---

## 2. تشغيل البوت الذكي

```bash
# تشغيل عادي
python D:\DevCenter\Tools\telegram_bot.py

# تشغيل 24/7 مع auto-restart
D:\DevCenter\Tools\run-telegram-bot.bat
```

---

## 3. الأوامر اللي تفهمها (بالعربي الفصيح والعامي)

### بناء المشاريع
| تقول | يطبق |
|------|------|
| "ابني مشروع ويب اسمه myapp" | ينشئ مجلد وهيكل مشروع ويب |
| "ابني مشروع بايثون اسمه analyzer" | ينشئ مجلد project-setup |
| "شغّل السيرفر" | يشغّل Flask server |
| "شغّل مشروع الدردشة" | يشغّل ChatApp server |

### تثبيت وتحكم
| تقول | يطبق |
|------|------|
| "حمل مكتبة requests" | pip install requests |
| "نصّب flask" | pip install flask |
| "اختبر المشروع" | pytest --tb=short -q |
| "حلل المشروع" | يشغّل ai_assistant.py |

### بحث وتصفح
| تقول | يطبق |
|------|------|
| "جيبلي موضوع عن الذكاء الاصطناعي" | يبحث في DuckDuckGo ويرد عليك |
| "ابحث عن Python tutorials" | بحث ويب |
| "أظهر لي الملفات" | يعرض مجلد DevCenter |
| "عرض محتويات المجلد" | يعرض محتويات أي مجلد |

### قراءة ملفات
| تقول | يطبق |
|------|------|
| "اقرأ ملف server.py" | يعرض محتوى الملف |
| "أظهر لي الكود" | يقرأ ويعرض الكود |

### أوامر مباشرة
| تقول | يطبق |
|------|------|
| "شغّل git status" | ينفذ الأمر في التيرمنل |
| "شغّل npm install" | ينفذ npm install |
| "كيف حالة المشروع؟" | يعرض حالة Git |

---

## 4. إرسال إشعارات من الكود

```python
from Tools.notifier import notify

notify("بناء المشروع اكتمل بنجاح!")
notify("فشل الاختبار: خطأ في login.py")
```

أو من الأمر:
```bash
python D:\DevCenter\Tools\notifier.py "رسالتي هنا"
```

---

## 5. إرسال واتساب

### مباشر:
```bash
python D:\DevCenter\Tools\whatsapp_sender.py "الرسالة"
```

### مجدول (في وقت محدد):
```python
from Tools.whatsapp_sender import send_later
send_later("تذكير: اجتماع بعد ساعة", 14, 30)
```

---

## 6. كيف يشتغل؟

```
Telegram (تلفونك)
  ↓ تكتب عربي
AI (OpenRouter/Ollama)
  ↓ يفهم القصد
DevCenter (جهازك)
  ↓ ينفذ الأمر
  ↓ يرد عليك بالنتيجة
Telegram (تلفونك)
```

---

## 7. ملاحظات

- البوت يستخدم **الذكاء الاصطناعي** (OpenRouter) لفهم كلامك
- ما يحتاج أوامر محددة — **تكلم عربي طبيعي**
- البوت يشتغل 24/7 مع `run-telegram-bot.bat` (auto-restart)
- كل الأوامر تنفذ محلياً على جهازك
- آمن: بس المستخدم المصرح له يقدر يستخدم البوت
