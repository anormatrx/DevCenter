---
name: admin-mouse
description: تحكم كامل بالجهاز بأوامر عربية — متصفح، ماوس، كيبورد، ملفات، نظام، شبكة، OCR، صوت، صورة، AI، وغيرها
---

# مهارة التحكم الكامل — جميع خصائص التفاعل البشري

هذه المهارة تتيح لك التحكم بـ **كل شيء** في جهاز الكمبيوتر باستخدام أوامر عربية طبيعية.

## التفعيل

أي أمر عربي يتطلب تحكم بالجهاز:
- "حمل تطبيق VLC من النت وثبته"
- "صلح مشروع الدردشة"
- "ابني مشروع موقع شخصي"
- "اطفي الجهاز بعد 10 دقايق"
- "قفل الشاشة"
- "ارفع الصوت شوي"
- "ابحث عن Python tutorials"
- "سجل الشاشة 30 ثانية"
- "اقرأ النص من الشاشة"
- "معلومات الجهاز"

---

## المحتويات — 17 قسم

| # | القسم | الميزات |
|---|-------|---------|
| 1 | 🤖 **AI** | فهم عربي، محادثة حرة، تخطيط الخطوات |
| 2 | 🌐 **BROWSER** | متصفح مرئي، بحث، نقر، تعبئة، تحميل |
| 3 | 🖱️ **MOUSE** | تحريك، نقر، سحب، تمرير، يمين، وسط |
| 4 | ⌨️ **KEYBOARD** | كتابة، اختصارات، حافظة، نسخ/لصق/قص |
| 5 | 🪟 **WINDOWS** | تنشيط، تكبير، إرساء، نوافذ افتراضية |
| 6 | ⚙️ **SYSTEM** | إطفاء، إعادة تشغيل، قفل، صوت، سطوع، عمليات، خدمات |
| 7 | 📁 **FILES** | إنشاء، نسخ، حذف، بحث، ضغط، اختصارات |
| 8 | 🌍 **NETWORK** | IP، ping، WiFi، سرعة، DNS |
| 9 | 🖥️ **SCREEN** | تصوير، OCR، تسجيل، ألوان، مطابقة صور |
| 10 | 🔊 **AUDIO** | تشغيل، تسجيل، بيب، كلام، استماع |
| 11 | 🖼️ **IMAGE** | اقتصاص، تغيير حجم، فلاتر، كتابة على الصورة |
| 12 | 📊 **DATA** | CSV، JSON، SQLite، INI |
| 13 | 🔋 **POWER** | خطط الطاقة (متوازن، توفير، أداء عالي) |
| 14 | 🛠️ **DEV** | Git، pip، npm، Docker |
| 15 | ✈️ **TELEGRAM** | إرسال رسائل تلغرام |
| 16 | 🔄 **AUTOMATION** | تحميل تطبيقات، إصلاح مشاريع، بناء مشاريع |
| 17 | 🎯 **EXECUTE** | نقطة الدخول الرئيسية — افهم ونفذ |

---

## الاستخدام

### CLI مباشر:
```bash
python admin_mouse.py "حمل VLC"
python admin_mouse.py "صلح مشروع الدردشة"
python admin_mouse.py "اطفي الجهاز"
```

### من Python:
```python
from admin_mouse import AdminController
ctrl = AdminController()
ctrl.execute("ارفع الصوت")
# أو استخدم دوال مباشرة
ctrl.system_volume_set(70)
ctrl.keyboard_hotkey("win", "d")
ctrl.screen_screenshot("s.png")
ctrl.cleanup()
```

---

## الأقسام بالتفصيل

### 1. AI — الذكاء الاصطناعي
```python
ctrl.ai_understand("حمل VLC")       # -> dict
ctrl.ai_chat("What is Python?")     # -> str (محادثة)
```

### 2. BROWSER — المتصفح
```python
ctrl.browser_open()                 # فتح متصفح
ctrl.browser_search("query")        # بحث Google
ctrl.browser_click_text("Download") # نقر على نص
ctrl.browser_fill("#id", "value")   # تعبئة حقل
ctrl.browser_screenshot("s.png")    # تصوير
ctrl.browser_get_text("h1")         # قراءة نص
ctrl.browser_close()                # إغلاق
```

### 3. MOUSE — الماوس
```python
ctrl.mouse_move(x, y)               # تحريك
ctrl.mouse_click(x, y)              # نقر
ctrl.mouse_right_click(x, y)        # يمين
ctrl.mouse_double_click(x, y)       # دبل كلك
ctrl.mouse_drag(x1,y1, x2,y2)       # سحب
ctrl.mouse_scroll(-5)               # تمرير للأسفل
ctrl.mouse_pos()                    # موقع الماوس
```

### 4. KEYBOARD — لوحة المفاتيح
```python
ctrl.kb_type("Hello")               # كتابة
ctrl.kb_hotkey("ctrl", "c")         # اختصار
ctrl.kb_combination("ctrl+c")       # اختصار نصي
ctrl.kb_press("enter")              # ضغط زر
# الحافظة
ctrl.clipboard_set("text")          # وضع نص
ctrl.clipboard_get()                # أخذ نص
ctrl.clipboard_copy()               # نسخ التحديد
ctrl.clipboard_paste()              # لصق
ctrl.clipboard_select_all()         # تحديد الكل
ctrl.clipboard_cut()                # قص
```

### 5. WINDOWS — النوافذ
```python
ctrl.win_activate("Chrome")         # تنشيط
ctrl.win_maximize("Chrome")         # تكبير
ctrl.win_minimize("Chrome")         # تصغير
ctrl.win_close("Chrome")            # إغلاق
ctrl.win_list()                     # قائمة النوافذ
ctrl.win_get_active()               # النشطة حالياً
ctrl.win_snap_left()                # إرساء لليسار
ctrl.win_snap_right()               # إرساء لليمين
ctrl.win_show_desktop()             # إظهار سطح المكتب
ctrl.win_virtual_desktop_new()      # سطح مكتب جديد
ctrl.win_switch()                   # Alt+Tab
```

### 6. SYSTEM — النظام
```python
ctrl.system_shutdown(30)            # إطفاء
ctrl.system_restart(30)             # إعادة تشغيل
ctrl.system_lock()                  # قفل الشاشة
ctrl.system_sleep()                 # سبات
ctrl.system_hibernate()             # إسبات
ctrl.system_info()                  # معلومات كاملة
ctrl.system_battery()               # البطارية
ctrl.system_volume_set(50)          # ضبط الصوت
ctrl.system_volume_mute()           # كاتم
ctrl.system_brightness_set(70)      # ضبط السطوع
ctrl.system_process_list()          # قائمة العمليات
ctrl.system_process_kill("notepad") # قتل عملية
ctrl.system_service_start("name")   # بدء خدمة
ctrl.system_service_stop("name")    # إيقاف خدمة
ctrl.system_notification("عنوان", "نص")  # إشعار
```

### 7. FILES — الملفات
```python
ctrl.file_create("test.txt", "content")
ctrl.file_read("test.txt")
ctrl.file_copy("src.txt", "dst.txt")
ctrl.file_move("src.txt", "dst.txt")
ctrl.file_delete("test.txt")
ctrl.file_find("*.py", "C:\\Projects")
ctrl.file_find_text("function", "C:\\", "*.py")
ctrl.file_list("D:\\DevCenter")
ctrl.file_zip("folder")
ctrl.file_unzip("folder.zip")
ctrl.file_shortcut_create("target.exe", "shortcut.lnk")
ctrl.file_watch("folder")           # مراقبة تغييرات
```

### 8. NETWORK — الشبكة
```python
ctrl.net_ip()                       # IP عام + ipconfig
ctrl.net_ping("google.com")         # اختبار اتصال
ctrl.net_dns_lookup("google.com")   # تحليل DNS
ctrl.net_speedtest()                # اختبار سرعة
ctrl.net_wifi_networks()            # شبكات WiFi
ctrl.net_wifi_connect("SSID", "pass")
ctrl.net_wifi_disconnect()
ctrl.net_trace("google.com")        # تتبع المسار
```

### 9. SCREEN — الشاشة
```python
ctrl.screen_screenshot("s.png")            # تصوير
ctrl.screen_screenshot_annotated("s.png", "نص", [(10,10,100,100)])
ctrl.screen_region(x, y, w, h)              # منطقة
ctrl.screen_color(0, 0)                     # لون بكسل
ctrl.screen_matches("icon.png")             # بحث عن صورة
ctrl.screen_matches_all("icon.png")         # كل المواقع
ctrl.screen_ocr(lang="ara+eng")             # OCR
ctrl.screen_record(10, "rec.avi")           # تسجيل فيديو
ctrl.screen_pixel_search((255,0,0))         # بحث بلون
```

### 10. AUDIO — الصوت
```python
ctrl.audio_play("file.mp3")          # تشغيل
ctrl.audio_record(5, "rec.wav")      # تسجيل
ctrl.audio_beep(440, 500)            # بيب
ctrl.audio_tts("مرحبا")             # نص → كلام
ctrl.audio_stt(5)                    # كلام → نص
```

### 11. IMAGE — الصور
```python
ctrl.image_resize("img.png", 800, 600)
ctrl.image_convert("img.png", "jpg")
ctrl.image_crop("img.png", (x1,y1,x2,y2))
ctrl.image_rotate("img.png", 90)
ctrl.image_filter("img.png", "grayscale")
ctrl.image_draw_text("img.png", "نص", (50,50))
ctrl.image_info("img.png")
```

### 12. DATA — البيانات
```python
ctrl.data_csv_read("data.csv")
ctrl.data_csv_write("data.csv", [{...}])
ctrl.data_json_read("data.json")
ctrl.data_json_write("data.json", {...})
ctrl.data_sqlite_query("db.sqlite", "SELECT * FROM ...")
ctrl.data_sqlite_execute("db.sqlite", "INSERT INTO ...")
ctrl.data_ini_read("config.ini")
```

### 13. POWER — الطاقة
```python
ctrl.power_plan_get()               # الخطة الحالية
ctrl.power_plan_set("balanced")     # متوازن
ctrl.power_plan_set("high performance")  # أداء عالي
ctrl.power_plan_set("power saver")  # توفير طاقة
```

### 14. DEV — التطوير
```python
ctrl.dev_git_status()
ctrl.dev_git_commit("update")
ctrl.dev_git_push()
ctrl.dev_git_pull()
ctrl.dev_git_clone("url")
ctrl.dev_pip_install("package")
ctrl.dev_pip_list()
ctrl.dev_docker_ps()
```

### 15. TELEGRAM
```python
ctrl.telegram_send("مرحبا من DevCenter")
```

### 16. AUTOMATION
```python
ctrl.download_app("VLC")            # تحميل وتثبيت
ctrl.fix_project("ChatApp")         # إصلاح مشروع
ctrl.build_project("MySite")        # بناء مشروع
```

### 17. EXECUTE — نقطة الدخول الرئيسية
```python
ctrl.execute("حمل VLC")
# نفس: ai_understand → توجيه → تنفيذ → تقرير
```

---

## أوامر عربية مدعومة

| المجموعة | أمثلة |
|----------|-------|
| **تحميل** | حمل VLC, نزل Firefox, تحميل Node.js |
| **إصلاح** | صلح المشروع, أصلح التطبيق, Fix ChatApp |
| **بناء** | ابني موقع, Build project, أنشئ تطبيق |
| **فتح** | افتح كروم, شغل المفكرة, Open notepad |
| **بحث** | ابحث عن Python, دور على React, Google AI |
| **نظام** | اطفي الجهاز, ريستارت, قفل الشاشة, سبات |
| **صوت** | ارفع الصوت, اخفض, كاتم, Mute |
| **شاشة** | اقرأ الشاشة, صور الشاشة, سجل الشاشة |
| **معلومات** | معلومات الجهاز, البطارية, بطارية |
| **شبكة** | IP, ping google.com, سرعة النت |
| **ملفات** | احذف, انسخ, انقل, ضغط, فك الضغط |
| **أخرى** | ترجم, طقس, احسب, اشغل سيرفر |

---

## ARABIC TO EXECUTION MAP

```
"حمل تطبيق VLC"
  ↓ AI Understand
  {action: "download_app", target: "VLC"}
  ↓
  1. browser_open()          ← فتح متصفح
  2. browser_search("VLC")   ← بحث
  3. browser_click("Download") ← نقر
  4. wait_download()          ← انتظار
  5. run_installer()          ← تشغيل
  6. keyboard_navigation()    ← تثبيت
  7. screenshot()             ← توثيق

"صلح مشروع ChatApp"
  ↓
  {action: "fix_app", target: "ChatApp"}
  ↓
  1. قراءة ملفات المشروع
  2. كشف المكتبات الناقصة
  3. تثبيت المكتبات
  4. تشغيل السيرفر
  5. اختبار API
  6. screenshot

"اطفي الجهاز"
  ↓
  {action: "shutdown"}
  ↓
  system_shutdown(30)

"قفل الشاشة"
  ↓
  {action: "lock_screen"}
  ↓
  kb_hotkey("win", "l")
```

---

## الملفات

- `admin_mouse.py` — الموديل الكامل (17 قسم، دوال لكل تفاعل بشري + CLI)
- `SKILL.md` — هذا الملف

## المكتبات المطلوبة

تم تثبيتها تلقائياً عند أول تشغيل:
`pyautogui, pygetwindow, keyboard, pyperclip, Pillow, psutil, requests, plyer`

اختيارية (تثبت عند الاستخدام):
`playwright, pytesseract, opencv-python, sounddevice, soundfile, pyttsx3, speechrecognition, speedtest-cli, winshell`
