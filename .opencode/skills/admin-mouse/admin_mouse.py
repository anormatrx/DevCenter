#!/usr/bin/env python3
"""
admin_mouse.py — تحكم كامل بالجهاز باللغة العربية
=================================================
جميع خصائص التفاعل البشري مع الكمبيوتر في موديل واحد:
متصفح، ماوس، كيبورد، ملفات، نظام، شبكة، صوت، صورة، OCR، AI، وغيرها
"""
import os, sys, time, json, subprocess, re, io, base64, shutil, zipfile
import tempfile, webbrowser, ctypes, platform, uuid, hashlib, csv
import sqlite3, configparser, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Union, List, Tuple
from dataclasses import dataclass, field
import collections

# ================================================================
# التثبيت التلقائي للمكتبات المفقودة
# ================================================================
_REQUIRED_LIBS = {
    'pyautogui': 'pyautogui',
    'pygetwindow': 'pygetwindow',
    'keyboard': 'keyboard',
    'pyperclip': 'pyperclip',
    'PIL': 'Pillow',
    'requests': 'requests',
    'psutil': 'psutil',
}

def _auto_install(pkg_name: str):
    try:
        __import__(pkg_name)
    except ImportError:
        pip_name = _REQUIRED_LIBS.get(pkg_name, pkg_name)
        subprocess.run([sys.executable, "-m", "pip", "install", pip_name], check=True, capture_output=True)

for _mod in _REQUIRED_LIBS:
    _auto_install(_mod)

import pyautogui
import pygetwindow as gw
import keyboard
import pyperclip
import psutil
from PIL import Image, ImageDraw, ImageFont, ImageGrab

# إضافات اختيارية (نحاول نستوردها، ما نوقف إذا فشلت)
try:
    import requests
except ImportError:
    requests = None

try:
    from plyer import notification
except ImportError:
    notification = None

# ================================================================
# AdminController — الموديل الرئيسي
# ================================================================
class AdminController:
    """
    تحكم كامل بالجهاز — كل ما يفعله الإنسان أمام الكمبيوتر.

    الأقسام:
      1. AI      — الفهم والتخطيط بالعربية
      2. BROWSER — فتح, بحث, نقر, تعبئة, تحميل
      3. MOUSE   — تحريك, نقر, سحب, تمرير
      4. KEYBOARD— كتابة, اختصارات, حافظة
      5. WINDOWS — تنشيط, تكبير, تصغير, إغلاق
      6. FILES   — إنشاء, نسخ, حذف, بحث, ضغط
      7. SYSTEM  — إيقاف, إعادة تشغيل, عمليات, خدمات
      8. NETWORK — IP, ping, wifi, سرعة
      9. SCREEN  — تصوير, OCR, تسجيل
     10. AUDIO   — صوت, كلام, تسجيل
     11. IMAGE   — معالجة, تحديد, تحويل
     12. DATA    — CSV, Excel, JSON, قاعدة بيانات
     13. TASKS   — مؤقت, تذكير, جدولة
     14. SPEECH  — كلام إلى نص, نص إلى كلام
     15. EMAIL   — إرسال بريد
     16. DEV     — Git, Docker, باكجات
     17. UTILITY — حاسبة, عملة, طقس, ترجمة
    """

    def __init__(self, ai_api_key: str = ""):
        self.ai_api_key = ai_api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self.ai_model = "google/gemini-2.0-flash-lite-001"
        # Browser
        self.browser = None
        self.page = None
        self._playwright = None
        self._playwright_cm = None
        # Audio
        self._recognizer = None
        self._tts_engine = None

    # ═══════════════════════════════════════════════════════════
    # SECTION 1 — AI: الذكاء الاصطناعي
    # ═══════════════════════════════════════════════════════════
    def ai_understand(self, text: str) -> dict:
        """فهم أمر عربي وتحويله إلى خطة"""
        if self.ai_api_key and requests:
            return self._ai_api(text)
        return self._ai_fallback(text)

    def _ai_api(self, text: str) -> dict:
        prompt = f"""أنت مساعد تحكم بالويندوز. حلل الأمر:
الأمر: {text}
أعد JSON بهذه الحقول فقط:
- action: download_app, open_app, fix_app, build_project, search_web,
         navigate, click_element, type_text, run_command, install_package,
         take_screenshot, check_status, send_email, shutdown, restart,
         lock_screen, volume_up, volume_down, mute, open_file, delete_file,
         copy_file, move_file, zip_file, unzip_file, list_files, find_file,
         system_info, battery_status, wifi_on, wifi_off, ip_config,
         ping_test, task_manager, kill_process, service_start, service_stop,
         calendar, reminder, timer, calculator, translate, weather,
         ocr_screen, record_audio, play_audio, image_edit, open_website
         or unknown
- target: الشيء المستهدف
- details: تفاصيل إضافية

رد: JSON فقط"""
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.ai_api_key}", "Content-Type": "application/json"},
                json={"model": self.ai_model, "messages": [{"role": "user", "content": prompt}],
                      "temperature": 0.1, "max_tokens": 300}, timeout=15)
            if r.status_code == 200:
                c = r.json()["choices"][0]["message"]["content"]
                c = re.sub(r'^```(?:json)?\n?|```$', '', c.strip())
                return json.loads(c)
        except: pass
        return self._ai_fallback(text)

    def _ai_fallback(self, text: str) -> dict:
        text_lower = text.lower()
        kw = collections.OrderedDict([
            # === الماوس أولاً ===
            ("mouse_double_click", ["دبل كلك","دبل","double click","نقرتين","زوج","doubleclick"]),
            ("mouse_right_click", ["نقر يمين","right click","زر يمين","كلك يمين","click right"]),
            ("mouse_click", ["نقر","click","دق","كلك","خبط","نقرة"]),
            ("mouse_move", ["حرك الماوس","حرك المؤشر","حرك","حول المؤشر","pointer","cursor","اذهب"]),
            ("mouse_drag", ["سحب","إفلات","drag","drop","جر","اسحب"]),
            ("mouse_scroll", ["سكرول","scroll","مرر","لف","ادر","دير"]),
            # === الشاشة ===
            ("screenshot", ["صور الشاشة","تصوير","screenshot","snap","التقط","كام","كاميرا","صور"]),
            ("ocr_screen", ["ocr","اقرأ الشاشة","screen","قراءة"]),
            ("screen_record", ["سجل الشاشة","record","تسجيل","فيديو"]),
            # === الكيبورد — الكتابة ===
            ("type_text", ["اكتب","type","كتابة","أكتب","طبع","اطبع"]),
            # === الكيبورد — التنقل (الأكثر تحديداً أولاً) ===
            ("keyboard_new_tab", ["تبويب جديد","new tab","فتح تبويب","صفحة جديدة","ctrl t"]),
            ("keyboard_close_tab", ["أغلق التبويب","close tab","اغلق التبويب","أغلق التبويب","قفل التبويب"]),
            ("keyboard_tab_next", ["التبويب التالي","التبويب بعد","بعد التبويب","يمين التبويب","تاب التالي","next tab","تبديل التبويب"]),
            ("keyboard_tab_prev", ["التبويب السابق","التبويب قبل","قبل التبويب","يسار التبويب","تاب السابق","prev tab","السابق التبويب","رجوع التبويب"]),
            ("keyboard_back", ["الى الخلف","الصفحة السابقة","previous page","رجوع","back"]),
            ("keyboard_forward", ["الى الامام","الصفحة التالية","next page","next tab","تقدم","forward"]),
            ("keyboard_refresh", ["تحديث","refresh","reload","اعادة تحميل","ريفرش"]),
            ("keyboard_shortcut", ["اختصار","shortcut"]),
            # === التحميل والبناء ===
            ("download_app", ["حمل","نزل","download","تحميل","تنزيل"]),
            ("build_project", ["ابني","build","بناء","أنشئ","create","إنشاء"]),
            ("fix_app", ["صلح","أصلح","fix","إصلاح","تصليح"]),
            # === التطبيقات ===
            ("open_website", ["افتح موقع","افتح http","افتح https","www.","http://","افتح الرابط","افتح لينك","website","رابط"]),
            ("open_app", ["افتح","شغل","run","تشغيل","open"]),
            # === النظام ===
            ("shutdown", ["اطفي","shutdown","إيقاف","طف","أطفى"]),
            ("restart", ["restart","إعادة تشغيل","ريستارت","اعادة تشغيل","ريست"]),
            ("lock_screen", ["lock","قفل","تأمين","امن"]),
            ("volume_up", ["ارفع الصوت","volume up","عل الصوت","رفع صوت","صخب"]),
            ("volume_down", ["اخفض الصوت","volume down","خفض صوت","وطي الصوت"]),
            ("mute", ["mute","كاتم","صامت","سكت"]),
            ("system_info", ["معلومات الجهاز","system info","مواصفات","جهازي"]),
            ("battery_status", ["بطارية","battery","شحن","battery"]),
            # === الشبكة ===
            ("ip_config", ["ip","ايبي","اي بي","اتش"]),
            ("ping_test", ["ping","بينج","اتصال","نت"]),
            # === الملفات ===
            ("open_file", ["افتح ملف"]),
            ("delete_file", ["احذف","delete","مسح","حذف","ازل"]),
            ("copy_file", ["انسخ","copy","نسخ"]),
            ("move_file", ["انقل","move","نقل ملف"]),
            ("zip_file", ["zip","ضغط ملف","ضغط مجلد","ضغط الملف","ضغط المجلد"]),
            ("unzip_file", ["فك ضغط","unzip","استخراج"]),
            # === العمليات ===
            ("kill_process", ["kill","قتل","process","عملية","انهاء"]),
            # === أخرى ===
            ("search_web", ["بحث","search","دور","google","ابحث"]),
            ("calculator", ["حساب","calc","آلة","حاسبة","math","رياضيات"]),
            ("translate", ["ترجم","translate","ترجمة"]),
            ("weather", ["طقس","weather","جو"]),
            ("navigate", ["اتجه","نافذة","تبديل","window","switch","تعال"]),
            ("browser_zoom_in", ["تكبير","zoom in","كبّر"]),
            ("browser_zoom_out", ["تصغير","zoom out","صغّر","صغير"]),
            ("browser_fullscreen", ["ملء الشاشة","fullscreen","كامل","شاشة كاملة","تكبير الشاشة"]),
        ])
        skip_words = ["تطبيق","من","النت","على","ال","مشروع","جديد","عن","في","و","ثم","الى","إلى"]
        for action, words in kw.items():
            if any(w in text_lower for w in words):
                target = text
                for w in words + skip_words:
                    target = target.replace(w, "")
                target = re.sub(r'\s+', ' ', target).strip().strip("،,.-_ ")
                if not target or len(target) < 2:
                    target = text.split()[-1] if len(text.split()) > 1 else text
                return {"action": action, "target": target[:50], "details": "", "language": "ar"}
        return {"action": "unknown", "target": text[:50], "details": "", "language": "ar"}

    def ai_chat(self, message: str) -> str:
        """محادثة حرة مع AI (بدون تنفيذ)"""
        if not self.ai_api_key or not requests:
            return "⚠️ ما في مفتاح API. عشان تستخدم AI، ضبط الـ API key."
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.ai_api_key}", "Content-Type": "application/json"},
                json={"model": "google/gemini-2.0-flash-lite-001",
                      "messages": [{"role": "user", "content": message}],
                      "temperature": 0.7, "max_tokens": 1000}, timeout=30)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            return f"⚠️ خطأ API: {r.status_code}"
        except Exception as e:
            return f"⚠️ فشل الاتصال: {e}"

    # ═══════════════════════════════════════════════════════════
    # SECTION 2 — BROWSER: المتصفح (Playwright)
    # ═══════════════════════════════════════════════════════════
    def _ensure_playwright(self):
        try:
            from playwright.sync_api import sync_playwright
            return sync_playwright
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True, capture_output=True)
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True, capture_output=True)
            from playwright.sync_api import sync_playwright
            return sync_playwright

    def browser_open(self, url: str = "https://www.google.com"):
        """فتح متصفح مرئي"""
        self.browser_close()
        sp = self._ensure_playwright()
        self._playwright_cm = sp()
        self._playwright = self._playwright_cm.__enter__()
        self.browser = self._playwright.chromium.launch(headless=False, args=["--start-maximized"])
        ctx = self.browser.new_context(no_viewport=True)
        self.page = ctx.new_page()
        self.page.goto(url, wait_until="domcontentloaded")
        time.sleep(1)
        return self.page

    def browser_close(self):
        try:
            if self.page: self.page.close()
        except: pass
        try:
            if self.browser: self.browser.close()
        except: pass
        try:
            if self._playwright_cm: self._playwright_cm.__exit__(None, None, None)
        except: pass
        self.page = None; self.browser = None; self._playwright = None; self._playwright_cm = None

    def browser_goto(self, url: str):
        if not self.page: self.browser_open(url)
        else: self.page.goto(url, wait_until="domcontentloaded")

    def browser_search(self, query: str):
        self.browser_goto("https://www.google.com/search?q=" + requests.utils.quote(query))
        time.sleep(1.5)

    def browser_click_text(self, text: str) -> bool:
        if not self.page: return False
        try:
            self.page.get_by_text(text, exact=False).first.click(); time.sleep(1); return True
        except:
            try:
                self.page.locator(f"text={text}").first.click(); time.sleep(1); return True
            except:
                return False

    def browser_click(self, selector: str) -> bool:
        if not self.page: return False
        try:
            self.page.click(selector); time.sleep(0.5); return True
        except:
            return False

    def browser_fill(self, selector: str, value: str) -> bool:
        if not self.page: return False
        try:
            self.page.fill(selector, value); return True
        except:
            return False

    def browser_wait(self, selector: str, timeout: int = 5000) -> bool:
        if not self.page: return False
        try:
            self.page.wait_for_selector(selector, timeout=timeout); return True
        except:
            return False

    def browser_screenshot(self, path: str = "browser.png") -> str:
        if self.page:
            self.page.screenshot(path=path, full_page=False)
        return path

    def browser_get_text(self, selector: str) -> str:
        if not self.page: return ""
        try:
            return self.page.text_content(selector) or ""
        except:
            return ""

    # ═══════════════════════════════════════════════════════════
    # SECTION 3 — MOUSE: تحكم بالماوس
    # ═══════════════════════════════════════════════════════════
    mo = pyautogui  # alias

    def mouse_pos(self) -> Tuple[int, int]:
        """موقع الماوس الحالي"""
        return self.mo.position()

    def mouse_move(self, x: int, y: int, duration: float = 0.3):
        self.mo.moveTo(x, y, duration=duration)

    def mouse_move_rel(self, dx: int, dy: int, duration: float = 0.3):
        self.mo.moveRel(dx, dy, duration=duration)

    def mouse_click(self, x=None, y=None, button='left', clicks=1):
        if x is not None and y is not None:
            self.mo.click(x, y, button=button, clicks=clicks)
        else:
            self.mo.click(button=button, clicks=clicks)
        time.sleep(0.2)

    def mouse_right_click(self, x=None, y=None):
        self.mouse_click(x, y, button='right')

    def mouse_double_click(self, x=None, y=None):
        self.mouse_click(x, y, clicks=2)

    def mouse_middle_click(self, x=None, y=None):
        self.mouse_click(x, y, button='middle')

    def mouse_drag(self, x1, y1, x2, y2, duration=0.5):
        self.mo.moveTo(x1, y1, duration=0.2)
        self.mo.drag(x2 - x1, y2 - y1, duration=duration)

    def mouse_scroll(self, clicks=-5):
        self.mo.scroll(clicks)

    def mouse_hscroll(self, clicks=5):
        self.mo.hscroll(clicks)

    def mouse_drag_to(self, x, y, duration=0.5):
        """سحب وإفلات من الموضع الحالي"""
        self.mo.drag(x, y, duration=duration)

    # ═══════════════════════════════════════════════════════════
    # SECTION 4 — KEYBOARD: لوحة المفاتيح
    # ═══════════════════════════════════════════════════════════
    def kb_type(self, text: str, interval: float = 0.05):
        """كتابة نص"""
        self.mo.write(text, interval=interval)

    def kb_press(self, key: str):
        """ضغط زر واحد"""
        self.mo.press(key)

    def kb_hotkey(self, *keys):
        """اختصار: ctrl+c, alt+tab, win+r, ..."""
        self.mo.hotkey(*keys)

    def kb_combination(self, combo: str):
        """اختصار نصي: 'ctrl+c', 'win+r', 'alt+f4'"""
        parts = combo.lower().split('+')
        self.mo.hotkey(*parts)

    def kb_key_down(self, key: str):
        self.mo.keyDown(key)

    def kb_key_up(self, key: str):
        self.mo.keyUp(key)

    def kb_hold_and_type(self, hold_key: str, text: str):
        """مسك زر وكتابة (مثل Ctrl+C)"""
        self.mo.keyDown(hold_key)
        self.mo.write(text)
        self.mo.keyUp(hold_key)

    # Clipboard
    def clipboard_get(self) -> str:
        return pyperclip.paste()

    def clipboard_set(self, text: str):
        pyperclip.copy(text)

    def clipboard_copy(self):
        """نسخ التحديد الحالي إلى الحافظة"""
        self.kb_hotkey('ctrl', 'c')
        time.sleep(0.2)
        return self.clipboard_get()

    def clipboard_paste(self):
        """لصق من الحافظة"""
        self.kb_hotkey('ctrl', 'v')

    def clipboard_cut(self):
        """قص التحديد الحالي"""
        self.kb_hotkey('ctrl', 'x')
        time.sleep(0.2)
        return self.clipboard_get()

    def clipboard_select_all(self):
        """تحديد الكل"""
        self.kb_hotkey('ctrl', 'a')

    def clipboard_append(self, text: str):
        """إضافة نص إلى الحافظة"""
        current = self.clipboard_get()
        self.clipboard_set(current + text)

    def clipboard_history(self, max_items: int = 10) -> List[str]:
        """محاولة استعراض تاريخ الحافظة (آخر n عناصر)"""
        import win32clipboard
        history = []
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            try:
                for _ in range(max_items):
                    data = win32clipboard.GetClipboardData()
                    if data and (not history or data != history[-1]):
                        history.append(data)
                        win32clipboard.ChangeClipboardChain(win32clipboard.GetClipboardOwner(), 0)
                    else:
                        break
            except: pass
            win32clipboard.CloseClipboard()
        except: pass
        return history or [self.clipboard_get()]

    # ═══════════════════════════════════════════════════════════
    # SECTION 5 — WINDOWS: التحكم بالنوافذ
    # ═══════════════════════════════════════════════════════════
    def win_activate(self, title: str) -> bool:
        try:
            wins = gw.getWindowsWithTitle(title)
            if wins:
                wins[0].activate(); time.sleep(0.2); return True
        except: pass
        return False

    def win_maximize(self, title: str):
        try:
            wins = gw.getWindowsWithTitle(title)
            if wins: wins[0].maximize()
        except: pass

    def win_minimize(self, title: str):
        try:
            wins = gw.getWindowsWithTitle(title)
            if wins: wins[0].minimize()
        except: pass

    def win_restore(self, title: str):
        try:
            wins = gw.getWindowsWithTitle(title)
            if wins: wins[0].restore()
        except: pass

    def win_close(self, title: str):
        try:
            wins = gw.getWindowsWithTitle(title)
            if wins: wins[0].close()
        except: pass

    def win_resize(self, title: str, width: int, height: int):
        try:
            wins = gw.getWindowsWithTitle(title)
            if wins: wins[0].resizeTo(width, height)
        except: pass

    def win_move(self, title: str, x: int, y: int):
        try:
            wins = gw.getWindowsWithTitle(title)
            if wins: wins[0].moveTo(x, y)
        except: pass

    def win_list(self) -> List[dict]:
        """قائمة بجميع النوافذ المفتوحة"""
        result = []
        for w in gw.getAllWindows():
            if w.title.strip():
                result.append({"title": w.title, "x": w.left, "y": w.top,
                               "w": w.width, "h": w.height, "visible": w.visible})
        return result

    def win_get_active(self) -> str:
        """عنوان النافذة النشطة"""
        try:
            return gw.getActiveWindow().title
        except:
            return ""

    def win_snap_left(self, title: str = ""):
        """إرساء النافذة لليسار"""
        if title: self.win_activate(title)
        self.kb_hotkey('win', 'left')

    def win_snap_right(self, title: str = ""):
        if title: self.win_activate(title)
        self.kb_hotkey('win', 'right')

    def win_minimize_all(self):
        self.kb_hotkey('win', 'd')

    def win_switch(self):
        """Alt+Tab"""
        self.kb_hotkey('alt', 'tab')

    def win_show_desktop(self):
        self.kb_hotkey('win', 'd')

    def win_task_view(self):
        self.kb_hotkey('win', 'tab')

    def win_virtual_desktop_new(self):
        self.kb_hotkey('win', 'ctrl', 'd')

    def win_virtual_desktop_switch(self, direction: str = "right"):
        if direction == "right":
            self.kb_hotkey('win', 'ctrl', 'right')
        else:
            self.kb_hotkey('win', 'ctrl', 'left')

    def win_virtual_desktop_close(self):
        self.kb_hotkey('win', 'ctrl', 'f4')

    # ═══════════════════════════════════════════════════════════
    # SECTION 6 — SYSTEM: تحكم بالنظام
    # ═══════════════════════════════════════════════════════════
    def system_shutdown(self, seconds: int = 30):
        subprocess.run(f"shutdown /s /t {seconds}", shell=True)

    def system_restart(self, seconds: int = 30):
        subprocess.run(f"shutdown /r /t {seconds}", shell=True)

    def system_logoff(self):
        subprocess.run("shutdown /l", shell=True)

    def system_lock(self):
        """قفل الشاشة (Win+L)"""
        self.kb_hotkey('win', 'l')

    def system_sleep(self):
        subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

    def system_hibernate(self):
        subprocess.run("shutdown /h", shell=True)

    def system_abort_shutdown(self):
        subprocess.run("shutdown /a", shell=True)

    def system_info(self) -> dict:
        """معلومات كاملة عن الجهاز"""
        import platform as pf
        info = {
            "system": pf.system(),
            "node": pf.node(),
            "release": pf.release(),
            "version": pf.version(),
            "machine": pf.machine(),
            "processor": pf.processor(),
            "cpu_count": os.cpu_count(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_total": psutil.virtual_memory().total,
            "ram_available": psutil.virtual_memory().available,
            "ram_percent": psutil.virtual_memory().percent,
            "disk_total": psutil.disk_usage('/').total,
            "disk_free": psutil.disk_usage('/').free,
            "disk_percent": psutil.disk_usage('/').percent,
            "python_version": sys.version,
            "user": os.environ.get("USERNAME", ""),
            "computer": os.environ.get("COMPUTERNAME", ""),
        }
        return info

    def system_battery(self) -> dict:
        battery = psutil.sensors_battery()
        if not battery:
            return {"status": "no battery"}
        return {
            "percent": battery.percent,
            "plugged": battery.power_plugged,
            "time_left": str(timedelta(seconds=battery.secsleft)) if battery.secsleft != -1 else "calculating",
        }

    def system_process_list(self) -> List[dict]:
        """قائمة بجميع العمليات"""
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                procs.append(p.info)
            except: pass
        return sorted(procs, key=lambda x: x.get('cpu_percent', 0) or 0, reverse=True)

    def system_process_kill(self, name_or_pid: Union[str, int]):
        """قتل عملية بالاسم أو PID"""
        killed = []
        if isinstance(name_or_pid, int) or name_or_pid.isdigit():
            try:
                p = psutil.Process(int(name_or_pid))
                p.terminate()
                killed.append(str(name_or_pid))
            except: pass
        else:
            for p in psutil.process_iter(['pid', 'name']):
                try:
                    if name_or_pid.lower() in p.info['name'].lower():
                        p.terminate()
                        killed.append(f"{p.info['name']}({p.info['pid']})")
                except: pass
        return killed

    def system_process_start(self, name: str):
        """تشغيل عملية"""
        try:
            subprocess.Popen(name, shell=True)
            return True
        except:
            return False

    def system_service_list(self) -> List[dict]:
        """قائمة الخدمات"""
        result = []
        try:
            out = subprocess.run("sc query", shell=True, capture_output=True, text=True).stdout
            for line in out.split('\n'):
                if 'SERVICE_NAME' in line:
                    name = line.split(':')[1].strip()
                    result.append({"name": name})
        except: pass
        return result

    def system_service_start(self, name: str):
        subprocess.run(f"net start \"{name}\"", shell=True, capture_output=True)

    def system_service_stop(self, name: str):
        subprocess.run(f"net stop \"{name}\"", shell=True, capture_output=True)

    def system_service_restart(self, name: str):
        self.system_service_stop(name)
        time.sleep(1)
        self.system_service_start(name)

    def system_volume_get(self) -> int:
        """مستوى الصوت (0-100)"""
        try:
            import pycaw.pycaw
        except:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "pycaw"], check=True, capture_output=True)
            except:
                pass
            try:
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                return int(volume.GetMasterVolumeLevelScalar() * 100)
            except:
                pass
        return -1

    def system_volume_set(self, level: int):
        """ضبط مستوى الصوت (0-100)"""
        level = max(0, min(100, level))
        for _ in range(50):
            if level > self.system_volume_get():
                self.kb_hotkey('volumeup')
            else:
                self.kb_hotkey('volumedown')
            time.sleep(0.05)

    def system_volume_mute(self):
        self.kb_hotkey('volumemute')

    def system_brightness_get(self) -> int:
        """مستوى السطوع (0-100)"""
        try:
            import wmi
            c = wmi.WMI()
            for b in c.WmiMonitorBrightness():
                return b.CurrentBrightness
        except:
            pass
        return -1

    def system_brightness_set(self, level: int):
        """ضبط السطوع"""
        try:
            import wmi
            c = wmi.WMI()
            methods = c.WmiMonitorBrightnessMethods()[0]
            methods.WmiSetBrightness(level, 0)
        except:
            try:
                subprocess.run(["powershell", "-c", f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness({level},0)"], shell=True)
            except:
                pass

    def system_notification(self, title: str, message: str, duration: int = 5):
        """إرسال إشعار ويندوز"""
        try:
            notification.notify(title=title, message=message, timeout=duration, app_name="DevCenter")
        except:
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=duration, threaded=True)
            except:
                print(f"🔔 {title}: {message}")

    def system_screen_off(self):
        """إطفاء الشاشة"""
        subprocess.run("powershell -c (Add-Type '[DllImport(\\\"user32\\\")]^public static extern int SendMessage(int hWnd,int hMsg,int wParam,int lParam);' -Name a -Pas).SendMessage(-1,0x0112,0xF170,2)", shell=True)

    def system_screen_on(self):
        """تشغيل الشاشة"""
        self.kb_press('volumeup')

    # ═══════════════════════════════════════════════════════════
    # SECTION 7 — FILES: الملفات والمجلدات
    # ═══════════════════════════════════════════════════════════
    def file_create(self, path: str, content: str = ""):
        """إنشاء ملف"""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return str(p.absolute())

    def file_read(self, path: str) -> str:
        """قراءة ملف"""
        return Path(path).read_text(encoding='utf-8', errors='ignore')

    def file_write(self, path: str, content: str):
        Path(path).write_text(content, encoding='utf-8')

    def file_append(self, path: str, content: str):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(content)

    def file_copy(self, src: str, dst: str):
        shutil.copy2(src, dst)

    def file_move(self, src: str, dst: str):
        shutil.move(src, dst)

    def file_delete(self, path: str, permanent: bool = False):
        path = Path(path)
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()

    def file_rename(self, path: str, new_name: str):
        p = Path(path)
        p.rename(p.parent / new_name)

    def file_exists(self, path: str) -> bool:
        return Path(path).exists()

    def file_size(self, path: str) -> int:
        return Path(path).stat().st_size

    def file_info(self, path: str) -> dict:
        p = Path(path)
        s = p.stat()
        return {
            "name": p.name, "path": str(p.absolute()), "dir": str(p.parent),
            "size": s.st_size, "created": datetime.fromtimestamp(s.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(s.st_mtime).isoformat(),
            "is_dir": p.is_dir(), "is_file": p.is_file(),
            "ext": p.suffix,
        }

    def file_find(self, pattern: str, root: str = "C:\\") -> List[str]:
        """بحث عن ملفات بالـ pattern"""
        results = []
        try:
            for p in Path(root).rglob(pattern):
                results.append(str(p))
                if len(results) >= 100: break
        except: pass
        return results

    def file_find_text(self, text: str, root: str = "C:\\", ext: str = "*.py") -> List[str]:
        """بحث عن نص داخل ملفات"""
        results = []
        try:
            for p in Path(root).rglob(ext):
                try:
                    if text in p.read_text(encoding='utf-8', errors='ignore'):
                        results.append(str(p))
                        if len(results) >= 50: break
                except: pass
        except: pass
        return results

    def file_list(self, path: str = ".") -> List[dict]:
        """قائمة محتويات مجلد"""
        p = Path(path)
        if not p.exists(): return []
        items = []
        for item in p.iterdir():
            try:
                s = item.stat()
                items.append({
                    "name": item.name, "path": str(item.absolute()),
                    "size": s.st_size, "is_dir": item.is_dir(),
                    "modified": datetime.fromtimestamp(s.st_mtime).isoformat(),
                })
            except: pass
        return items

    def file_mkdir(self, path: str):
        Path(path).mkdir(parents=True, exist_ok=True)

    def file_zip(self, source: str, output: str = ""):
        """ضغط ملف/مجلد"""
        source = Path(source)
        if not output:
            output = str(source.parent / (source.stem + ".zip"))
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
            if source.is_dir():
                for f in source.rglob("*"):
                    zf.write(f, f.relative_to(source.parent))
            else:
                zf.write(source, source.name)
        return output

    def file_unzip(self, zip_path: str, output_dir: str = ""):
        """فك ضغط"""
        zip_path = Path(zip_path)
        if not output_dir:
            output_dir = str(zip_path.parent / zip_path.stem)
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(output_dir)
        return output_dir

    def file_watch(self, path: str, callback=None, interval: float = 1.0):
        """مراقبة تغييرات الملف"""
        import hashlib
        path = Path(path)
        old = {}
        try:
            while True:
                for f in path.rglob("*"):
                    if f.is_file():
                        h = hashlib.md5(f.read_bytes()).hexdigest()
                        if f not in old: old[f] = h
                        elif old[f] != h:
                            if callback: callback(str(f), "modified")
                            old[f] = h
                time.sleep(interval)
        except KeyboardInterrupt:
            pass

    def file_shortcut_create(self, target: str, shortcut_path: str, args: str = ""):
        """إنشاء اختصار على سطح المكتب"""
        import winshell
        try:
            import winshell
        except:
            subprocess.run([sys.executable, "-m", "pip", "install", "winshell"], check=True, capture_output=True)
            import winshell
        shortcut_path = Path(shortcut_path)
        if shortcut_path.suffix != '.lnk':
            shortcut_path = shortcut_path.with_suffix('.lnk')
        with winshell.shortcut(str(shortcut_path)) as sc:
            sc.path = target
            sc.arguments = args
            sc.working_directory = str(Path(target).parent)
        return str(shortcut_path)

    # ═══════════════════════════════════════════════════════════
    # SECTION 8 — NETWORK: الشبكة
    # ═══════════════════════════════════════════════════════════
    def net_ip(self) -> dict:
        """معلومات IP"""
        info = {}
        try:
            info["public"] = requests.get("https://api.ipify.org?format=json", timeout=5).json()["ip"]
        except:
            info["public"] = "unknown"
        try:
            out = subprocess.run("ipconfig", shell=True, capture_output=True, text=True).stdout
            info["ipconfig"] = out[:2000]
        except:
            pass
        return info

    def net_ping(self, host: str = "8.8.8.8", count: int = 4) -> str:
        """اختبار اتصال"""
        try:
            out = subprocess.run(f"ping -n {count} {host}", shell=True, capture_output=True, text=True, timeout=30)
            return out.stdout
        except:
            return "فشل الاتصال"

    def net_dns_lookup(self, domain: str) -> str:
        """تحليل DNS"""
        try:
            out = subprocess.run(f"nslookup {domain}", shell=True, capture_output=True, text=True)
            return out.stdout
        except:
            return "فشل"

    def net_speedtest(self) -> dict:
        """اختبار سرعة النت"""
        try:
            import speedtest
        except:
            subprocess.run([sys.executable, "-m", "pip", "install", "speedtest-cli"], check=True, capture_output=True)
            import speedtest
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            dl = st.download() / 1_000_000
            ul = st.upload() / 1_000_000
            return {"download_mbps": round(dl, 2), "upload_mbps": round(ul, 2)}
        except Exception as e:
            return {"error": str(e)}

    def net_wifi_networks(self) -> List[str]:
        """قائمة شبكات WiFi"""
        try:
            out = subprocess.run("netsh wlan show networks", shell=True, capture_output=True, text=True).stdout
            networks = re.findall(r'SSID \d+ : (.+)', out)
            return networks
        except:
            return []

    def net_wifi_connect(self, ssid: str, password: str = ""):
        """الاتصال بشبكة WiFi"""
        profile = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig><SSID><name>{ssid}</name></SSID></SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM><security><authEncryption><authentication>WPA2PSK</authentication><encryption>AES</encryption></authEncryption>
    <sharedKey><keyType>passPhrase</keyType><protected>false</protected><keyMaterial>{password}</keyMaterial></sharedKey></security></MSM>
</WLANProfile>"""
        path = os.path.join(tempfile.gettempdir(), f"{ssid}.xml")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(profile)
        subprocess.run(f'netsh wlan add profile filename="{path}"', shell=True, capture_output=True)
        subprocess.run(f'netsh wlan connect name="{ssid}"', shell=True, capture_output=True)

    def net_wifi_disconnect(self):
        subprocess.run("netsh wlan disconnect", shell=True)

    def net_wifi_current(self) -> str:
        try:
            out = subprocess.run("netsh wlan show interfaces", shell=True, capture_output=True, text=True).stdout
            m = re.search(r'SSID\s*:\s*(.+)', out)
            return m.group(1).strip() if m else "غير متصل"
        except:
            return "غير معروف"

    def net_trace(self, host: str = "google.com") -> str:
        try:
            r = subprocess.run(f"tracert -h 15 {host}", shell=True, capture_output=True, text=True, timeout=60)
            return r.stdout
        except:
            return "فشل"

    # ═══════════════════════════════════════════════════════════
    # SECTION 9 — SCREEN: الشاشة
    # ═══════════════════════════════════════════════════════════
    def screen_screenshot(self, path: str = "screenshot.png", region: tuple = None) -> str:
        """تصوير الشاشة"""
        if region:
            img = pyautogui.screenshot(region=region)
        else:
            img = pyautogui.screenshot()
        img.save(path)
        return path

    def screen_screenshot_annotated(self, path: str = "annotated.png", text: str = "", boxes: list = None):
        """تصوير مع تعليقات"""
        img = pyautogui.screenshot()
        draw = ImageDraw.Draw(img)
        if boxes:
            for box in boxes:
                draw.rectangle(box[:4], outline="red", width=3)
                if len(box) > 4:
                    draw.text((box[0], box[1] - 15), box[4], fill="red")
        if text:
            draw.text((10, 10), text, fill="red")
        img.save(path)
        return path

    def screen_region(self, x: int, y: int, w: int, h: int) -> Image.Image:
        """تصوير منطقة محددة"""
        return pyautogui.screenshot(region=(x, y, w, h))

    def screen_color(self, x: int, y: int) -> Tuple[int, int, int]:
        """لون البكسل في الموقع"""
        return pyautogui.pixel(x, y)

    def screen_matches(self, image_path: str, confidence: float = 0.8) -> Tuple[int, int]:
        """البحث عن صورة على الشاشة"""
        try:
            pos = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if pos:
                return pyautogui.center(pos)
        except:
            pass
        return None

    def screen_matches_all(self, image_path: str, confidence: float = 0.8) -> List[Tuple[int, int]]:
        """كل مواقع الصورة على الشاشة"""
        try:
            positions = list(pyautogui.locateAllOnScreen(image_path, confidence=confidence))
            return [pyautogui.center(p) for p in positions]
        except:
            return []

    def screen_ocr(self, region: tuple = None, lang: str = "ara+eng") -> str:
        """قراءة نص من الشاشة (OCR)"""
        try:
            import pytesseract
        except:
            subprocess.run([sys.executable, "-m", "pip", "install", "pytesseract"], check=True, capture_output=True)
            import pytesseract
        # محاولة تحديد مسار Tesseract
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            os.environ.get("TESSERACT_PATH", ""),
        ]
        for p in tesseract_paths:
            if p and os.path.exists(p):
                pytesseract.pytesseract.tesseract_cmd = p
                break
        if region:
            img = self.screen_region(*region)
        else:
            img = pyautogui.screenshot()
        try:
            return pytesseract.image_to_string(img, lang=lang)
        except:
            return "⚠️ Tesseract غير مثبت. حمله من: https://github.com/UB-Mannheim/tesseract/wiki"

    def screen_record(self, duration: int = 10, output: str = "recording.avi") -> str:
        """تسجيل الشاشة"""
        try:
            import cv2
            import numpy as np
        except:
            subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python", "numpy"], check=True, capture_output=True)
            import cv2
            import numpy as np
        screen = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output, fourcc, 10.0, screen)
        for _ in range(duration * 10):
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
        out.release()
        return output

    def screen_pixel_search(self, color: Tuple[int, int, int], tolerance: int = 10) -> List[Tuple[int, int]]:
        """البحث عن بكسل بلون محدد"""
        img = pyautogui.screenshot()
        found = []
        for x in range(img.width):
            for y in range(img.height):
                px = img.getpixel((x, y))
                if all(abs(px[i] - color[i]) <= tolerance for i in range(3)):
                    found.append((x, y))
                    if len(found) >= 50: break
            if len(found) >= 50: break
        return found

    # ═══════════════════════════════════════════════════════════
    # SECTION 10 — AUDIO: الصوت
    # ═══════════════════════════════════════════════════════════
    def audio_play(self, path: str):
        """تشغيل ملف صوتي"""
        os.startfile(path) if os.name == 'nt' else subprocess.run(["xdg-open", path])

    def audio_record(self, duration: int = 5, output: str = "recording.wav") -> str:
        """تسجيل صوت من المايكروفون"""
        try:
            import sounddevice as sd
            import soundfile as sf
        except:
            subprocess.run([sys.executable, "-m", "pip", "install", "sounddevice", "soundfile"], check=True, capture_output=True)
            import sounddevice as sd
            import soundfile as sf
        samplerate = 16000
        print(f"🎤 تسجيل {duration} ثوان...")
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
        sd.wait()
        sf.write(output, recording, samplerate)
        return output

    def audio_beep(self, frequency: int = 440, duration: int = 500):
        """إصدار صوت بيب"""
        import winsound
        winsound.Beep(frequency, duration)

    def audio_tts(self, text: str, lang: str = "ar"):
        """نص إلى كلام"""
        try:
            import pyttsx3
        except:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyttsx3"], check=True, capture_output=True)
            import pyttsx3
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except:
            # Fallback: استخدام winsound
            print(f"🗣️ {text}")

    def audio_stt(self, duration: int = 5) -> str:
        """كلام إلى نص (استماع من المايكروفون)"""
        try:
            import speech_recognition as sr
        except:
            subprocess.run([sys.executable, "-m", "pip", "install", "SpeechRecognition"], check=True, capture_output=True)
            import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 استماع...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=duration)
        try:
            text = r.recognize_google(audio, language="ar-SA")
            return text
        except sr.UnknownValueError:
            return "⚠️ ما فهمت الكلام"
        except sr.RequestError:
            return "⚠️ خطأ في الاتصال بخدمة التعرف"

    # ═══════════════════════════════════════════════════════════
    # SECTION 11 — IMAGE: معالجة الصور
    # ═══════════════════════════════════════════════════════════
    def image_open(self, path: str) -> Image.Image:
        return Image.open(path)

    def image_resize(self, path: str, width: int, height: int, output: str = ""):
        img = Image.open(path)
        img = img.resize((width, height))
        if not output: output = path
        img.save(output)
        return output

    def image_convert(self, path: str, fmt: str = "png", output: str = ""):
        img = Image.open(path)
        if not output:
            p = Path(path)
            output = str(p.parent / f"{p.stem}.{fmt}")
        img.save(output, fmt.upper())
        return output

    def image_crop(self, path: str, box: Tuple[int, int, int, int], output: str = ""):
        img = Image.open(path)
        img = img.crop(box)
        if not output: output = path
        img.save(output)
        return output

    def image_rotate(self, path: str, degrees: float, output: str = ""):
        img = Image.open(path)
        img = img.rotate(degrees, expand=True)
        if not output: output = path
        img.save(output)
        return output

    def image_filter(self, path: str, filter_type: str = "grayscale", output: str = ""):
        from PIL import ImageFilter
        img = Image.open(path)
        filters = {
            "grayscale": lambda i: i.convert("L"),
            "blur": lambda i: i.filter(ImageFilter.BLUR),
            "sharpen": lambda i: i.filter(ImageFilter.SHARPEN),
            "edge": lambda i: i.filter(ImageFilter.FIND_EDGES),
            "emboss": lambda i: i.filter(ImageFilter.EMBOSS),
            "contour": lambda i: i.filter(ImageFilter.CONTOUR),
            "smooth": lambda i: i.filter(ImageFilter.SMOOTH),
        }
        if filter_type in filters:
            img = filters[filter_type](img)
        if not output: output = path
        img.save(output)
        return output

    def image_draw_text(self, path: str, text: str, position: tuple = (10, 10), color: str = "red", size: int = 30, output: str = ""):
        img = Image.open(path)
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", size)
        except:
            font = ImageFont.load_default()
        draw.text(position, text, fill=color, font=font)
        if not output: output = path
        img.save(output)
        return output

    def image_info(self, path: str) -> dict:
        img = Image.open(path)
        return {"format": img.format, "mode": img.mode, "size": img.size,
                "width": img.width, "height": img.height, "path": path}

    # ═══════════════════════════════════════════════════════════
    # SECTION 12 — DATA: معالجة البيانات
    # ═══════════════════════════════════════════════════════════
    def data_csv_read(self, path: str) -> List[dict]:
        with open(path, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def data_csv_write(self, path: str, data: List[dict]):
        if not data: return
        with open(path, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=data[0].keys())
            w.writeheader()
            w.writerows(data)

    def data_json_read(self, path: str) -> Union[dict, list]:
        return json.loads(Path(path).read_text(encoding='utf-8'))

    def data_json_write(self, path: str, data: Union[dict, list]):
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    def data_sqlite_query(self, db_path: str, query: str) -> List[dict]:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query)
        results = [dict(row) for row in cur.fetchall()]
        conn.close()
        return results

    def data_sqlite_execute(self, db_path: str, query: str):
        conn = sqlite3.connect(db_path)
        conn.execute(query)
        conn.commit()
        conn.close()

    def data_ini_read(self, path: str) -> dict:
        config = configparser.ConfigParser()
        config.read(path, encoding='utf-8')
        return {s: dict(config.items(s)) for s in config.sections()}

    def data_ini_write(self, path: str, data: dict):
        config = configparser.ConfigParser()
        for section, items in data.items():
            config[section] = items
        with open(path, 'w', encoding='utf-8') as f:
            config.write(f)

    # ═══════════════════════════════════════════════════════════
    # SECTION 13 — POWER: الطاقة
    # ═══════════════════════════════════════════════════════════
    def power_plan_get(self) -> str:
        try:
            out = subprocess.run("powercfg /getactivescheme", shell=True, capture_output=True, text=True).stdout
            m = re.search(r'\{[^}]+\}', out)
            return m.group(0) if m else "غير معروف"
        except:
            return "غير معروف"

    def power_plan_set(self, plan: str = "balanced"):
        plans = {
            "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
            "power saver": "a1841308-3541-4fab-bc81-f71556f20b4a",
            "high performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
        }
        if plan.lower() in plans:
            subprocess.run(f"powercfg /setactive {plans[plan.lower()]}", shell=True)

    # ═══════════════════════════════════════════════════════════
    # SECTION 14 — DEV: أدوات التطوير
    # ═══════════════════════════════════════════════════════════
    def dev_git_status(self, repo_path: str = ".") -> str:
        try:
            r = subprocess.run("git status", shell=True, capture_output=True, text=True, cwd=repo_path)
            return r.stdout
        except:
            return "⚠️ Git غير متاح"

    def dev_git_commit(self, msg: str, repo_path: str = "."):
        subprocess.run(f'git commit -am "{msg}"', shell=True, cwd=repo_path)

    def dev_git_push(self, repo_path: str = "."):
        subprocess.run("git push", shell=True, cwd=repo_path)

    def dev_git_pull(self, repo_path: str = "."):
        subprocess.run("git pull", shell=True, cwd=repo_path)

    def dev_git_clone(self, url: str, dest: str = ""):
        subprocess.run(f"git clone {url} {dest}", shell=True)

    def dev_pip_install(self, package: str):
        subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

    def dev_pip_list(self) -> List[str]:
        r = subprocess.run([sys.executable, "-m", "pip", "list", "--format=columns"], capture_output=True, text=True)
        return [l.strip() for l in r.stdout.split('\n') if l.strip()]

    def dev_npm_install(self, package: str = ""):
        subprocess.run(f"npm install {package}".strip(), shell=True)

    def dev_docker_ps(self) -> str:
        try:
            r = subprocess.run("docker ps -a", shell=True, capture_output=True, text=True)
            return r.stdout or "⚠️ Docker غير شغال"
        except:
            return "⚠️ Docker غير مثبت"

    def dev_docker_compose_up(self, path: str = "."):
        subprocess.run("docker-compose up -d", shell=True, cwd=path)

    # ═══════════════════════════════════════════════════════════
    # SECTION 15 — TELEGRAM: التلغرام
    # ═══════════════════════════════════════════════════════════
    def telegram_send(self, message: str, token: str = "", chat_id: str = ""):
        """إرسال رسالة تلغرام"""
        if not token:
            token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        if not chat_id:
            chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
        if not token or not chat_id: return "⚠️ عيّن TELEGRAM_BOT_TOKEN و TELEGRAM_CHAT_ID"
        try:
            r = requests.get(f"https://api.telegram.org/bot{token}/sendMessage",
                            params={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})
            return "✅ تم الإرسال" if r.status_code == 200 else f"⚠️ خطأ: {r.text}"
        except Exception as e:
            return f"⚠️ فشل: {e}"

    # ═══════════════════════════════════════════════════════════
    # SECTION 16 — AUTOMATION: سير العمل المتقدم
    # ═══════════════════════════════════════════════════════════
    def download_app(self, app_name: str):
        """تحميل وتثبيت تطبيق من النت تلقائياً"""
        self.log(f"🔍 بدء تحميل: {app_name}")
        self.browser_open()
        self.browser_search(f"{app_name} download official")
        time.sleep(1.5)
        self.browser_click_text(app_name)
        time.sleep(2)
        for sel in [
            'a[href*="download"]', 'a[href*=".exe"]', 'a[href*=".msi"]',
            'button:has-text("Download")', '[class*="download"] a'
        ]:
            if self.browser_click(sel):
                break
        if not self.browser_click_text("Download") and not self.browser_click_text("تحميل"):
            self.log("⚠️ ما لقيت زر تحميل")
        time.sleep(5)
        self._wait_download()
        downloads = Path(os.path.expanduser("~")) / "Downloads"
        for f in sorted(downloads.glob("*.exe"), key=lambda f: f.stat().st_mtime, reverse=True)[:3]:
            os.startfile(str(f))
            self.log(f"📦 تشغيل المثبت: {f.name}")
            time.sleep(3)
            for _ in range(2): self.kb_press("tab"); time.sleep(0.2)
            self.kb_press("enter"); time.sleep(1)
            for _ in range(2): self.kb_press("tab"); time.sleep(0.2)
            self.kb_press("enter")
            time.sleep(10)
            break
        self.browser_screenshot("download_done.png")
        self.log("✅ تم التحميل")

    def _wait_download(self, timeout: int = 30):
        downloads = Path(os.path.expanduser("~")) / "Downloads"
        before = set(downloads.glob("*.exe")) | set(downloads.glob("*.msi"))
        for _ in range(timeout):
            time.sleep(1)
            now = set(downloads.glob("*.exe")) | set(downloads.glob("*.msi"))
            new = now - before
            if new:
                for f in new:
                    s1 = f.stat().st_size
                    time.sleep(2)
                    if f.exists() and f.stat().st_size == s1 and s1 > 1000:
                        self.log(f"✅ تحميل: {f.name}")
                        return f
        return None

    def fix_project(self, path_or_name: str):
        """إصلاح مشروع كامل — ذكي واتوماتيكي"""
        base = Path(path_or_name)
        if not base.exists():
            base = Path("D:/DevCenter") / path_or_name
        if not base.exists():
            base = self._ensure_correct_path(str(base))
            base = Path(base)
        if not base.exists():
            self.log(f"❌ المسار غير موجود: {path_or_name}")
            return False
        self.log(f"🔧 إصلاح: {base}")

        # 1. Fix path and dependencies
        os.chdir(str(base))
        missing = self._check_dependencies(str(base))
        if missing:
            self.log(f"📦 مكتبات ناقصة: {missing}")
            self._auto_install_missing(missing)

        # 2. Try running the server
        server = base / "server" / "server.py"
        if not server.exists():
            for f in base.rglob("*.py"):
                if f.name in ("app.py", "server.py", "main.py"):
                    server = f
                    break
        if server.exists():
            self.log("🚀 تشغيل السيرفر...")
            port = self._detect_port_conflict(5000)
            p = subprocess.Popen([sys.executable, str(server)], cwd=str(server.parent),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(3)
            if p.poll() is not None:
                err = p.stderr.read().decode('utf-8', errors='ignore')
                self.log(f"❌ السيرفر طفى: {err[:100]}")
                fix = self._auto_fix_error(err, str(base))
                self.log(fix)
                if "غيّرت port" in fix:
                    p = subprocess.Popen([sys.executable, str(server)], cwd=str(server.parent))
                    time.sleep(3)
                    if p.poll() is None:
                        self.log(f"✅ السيرفر اشتغل بعد الإصلاح!")
            else:
                self.log(f"✅ السيرفر شغال!")
            try:
                r = requests.get(f"http://localhost:{port}/api/health", timeout=5)
                self.log(f"✅ استجابة: {r.json()}")
            except:
                try:
                    r = requests.get("http://localhost:5000/api/health", timeout=5)
                    self.log(f"✅ استجابة: {r.json()}")
                except:
                    self.log("⚠️ السيرفر شغال لكن ما استجاب للـ health check")
            self.browser_open(f"http://localhost:{port}")
            self.browser_screenshot("fix_done.png")
        self.log("✅ تم الإصلاح")
        return True

    def build_project(self, name: str, project_type: str = "web", details: str = ""):
        """بناء مشروع جديد — يستخدم الذكاء الاصطناعي للبناء حسب الطلب"""
        base_path = Path("D:/DevCenter/WebApps") / name
        base_path.mkdir(parents=True, exist_ok=True)

        # Use AI to generate project based on details
        if details:
            prompt = f"""ابني مشروع {project_type} اسمه {name}.
التفاصيل: {details}

أعد قائمة الملفات المطلوبة (ملف واحد لكل أمر write):
1. اكتب اسم الملف
2. المحتوى الكامل

المشروع يكون في: {base_path}"""
            self.log(f"🧠 أستخدم الذكاء الاصطناعي لبناء '{name}'...")
            try:
                r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.ai_api_key}", "Content-Type": "application/json"},
                    json={"model": self.ai_model,
                          "messages": [{"role": "system", "content": "أنت مبرمج تبني مشاريع كاملة. اكتب كود نظيف وجاهز للتشغيل."},
                                       {"role": "user", "content": prompt}],
                          "temperature": 0.3, "max_tokens": 4000}, timeout=60)
                if r.status_code == 200:
                    content = r.json()["choices"][0]["message"]["content"]
                    # Try to extract and create files from response
                    files = re.findall(r'`([^`]+)`\s*\n```\w*\n(.*?)```', content, re.DOTALL)
                    if files:
                        for fname, fcontent in files:
                            fpath = base_path / fname
                            fpath.parent.mkdir(parents=True, exist_ok=True)
                            fpath.write_text(fcontent.strip(), encoding='utf-8')
                            self.log(f"  📄 {fname}")
                        self.log(f"✅ بني المشروع بـ AI: {base_path}")
                        return base_path
            except Exception as e:
                self.log(f"⚠️ AI فشل: {e}")

        # Fallback: template
        (base_path / "index.html").write_text(f"""<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8"><title>{name}</title>
<link rel="stylesheet" href="style.css"></head><body>
<h1>{name}</h1><p>بني بواسطة DevCenter AI</p>
<script src="script.js"></script></body></html>""")
        (base_path / "style.css").write_text("*{margin:0;padding:0;box-sizing:border-box}body{font-family:sans-serif;background:#0d1117;color:#e6edf3;display:flex;justify-content:center;align-items:center;min-height:100vh}h1{color:#3fb950}p{color:#8b949e}")
        (base_path / "script.js").write_text("console.log('DevCenter AI');")
        sv = base_path / "server" / "server.py"
        sv.parent.mkdir(exist_ok=True)
        sv.write_text(f'from flask import Flask,jsonify\nfrom flask_cors import CORS\napp=Flask(__name__)\nCORS(app)\n@app.route("/")\ndef home():\n    return jsonify({{"status":"ok","project":"{name}"}})\n@app.route("/api/health")\ndef health():\n    return jsonify({{"status":"ok"}})\nif __name__=="__main__":\n    import socket\n    port=5000\n    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:\n        while s.connect_ex(("127.0.0.1",port))==0:\n            port+=1\n    app.run(host="0.0.0.0",port=port,debug=True)\n')
        self.log(f"✅ بني: {base_path}")
        sp = subprocess.Popen([sys.executable, str(sv)], cwd=str(sv.parent))
        time.sleep(2)
        self.browser_open("http://localhost:5000")
        self.browser_screenshot(f"{name}_built.png")
        self.log(f"✅ http://localhost:5000")
        return base_path

    # ═══════════════════════════════════════════════════════════
    # SECTION 17 — EXECUTE: التنفيذ المباشر
    # ═══════════════════════════════════════════════════════════
    def _browser_active(self) -> bool:
        """هل المتصفح مفتوح؟"""
        return self.page is not None and self.browser is not None

    def _ensure_browser_open(self, url: str = "https://www.google.com"):
        """فتح متصفح إذا ما هو مفتوح"""
        if not self._browser_active():
            self.browser_open(url)

    def _type_in_browser(self, text: str):
        """يكتب في المتصفح مثل الإنسان: يركز على الحقل ويكتب"""
        if self._browser_active():
            try:
                # جرب يستخدم focus على العنصر النشط
                self.page.keyboard.type(text, delay=50)
                self.log(f"⌨️ كتب في المتصفح: {text}")
                return
            except:
                pass
        # Fallback: PyAutoGUI
        self.kb_type(text, interval=0.05)
        self.log(f"⌨️ كتب: {text}")

    def _click_in_browser(self, target_text: str = ""):
        """نقر في المتصفح مثل الإنسان"""
        if self._browser_active() and target_text:
            if self.browser_click_text(target_text):
                self.log(f"🖱️ نقر على: {target_text}")
                return True
        # Mouse click at current position
        self.mouse_click()
        self.log("🖱️ نقرت")
        return True

    # ═══════════════════════════════════════════════════════════════
    # SMARTER BUILDER — الباني الذكي
    # ═══════════════════════════════════════════════════════════════

    def _detect_port_conflict(self, port: int) -> int:
        """فحص البورت واستخدام أول بورت فاضي"""
        import socket
        while port < 65535:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('127.0.0.1', port)) != 0:
                    return port
            port += 1
        return 5000

    def _check_dependencies(self, path: str) -> list:
        """فحص المكتبات المطلوبة في المشروع"""
        missing = []
        if not os.path.exists(path): return missing
        imports = set()
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith('.py'):
                    with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as fh:
                        for line in fh:
                            m = re.match(r'^\s*import\s+(\w+)', line)
                            if m: imports.add(m.group(1))
                            m = re.match(r'^\s*from\s+(\w+)', line)
                            if m: imports.add(m.group(1))
        stl = {'os','sys','re','time','json','math','random','datetime','pathlib','subprocess','io','base64','typing'}
        for imp in imports:
            if imp in stl: continue
            try: __import__(imp)
            except: missing.append(imp)
        return missing

    def _auto_install_missing(self, missing: list) -> str:
        """تثبيت المكتبات الناقصة تلقائياً"""
        if not missing: return "✅ كل المكتبات موجودة"
        result = []
        for pkg in missing:
            r = subprocess.run(f"pip install {pkg}", shell=True, capture_output=True, text=True, timeout=60)
            if r.returncode == 0: result.append(f"✅ {pkg}")
            else: result.append(f"❌ {pkg}: {r.stderr[:50]}")
        return "\n".join(result)

    def _auto_fix_error(self, error_text: str, project_path: str) -> str:
        """فهم الخطأ وإصلاحه تلقائياً"""
        fixes = []
        # Port in use
        if "Address already in use" in error_text or "OSError" in error_text:
            for root, dirs, files in os.walk(project_path):
                for f in files:
                    if f.endswith('.py'):
                        fp = os.path.join(root, f)
                        with open(fp, 'r', encoding='utf-8') as fh:
                            content = fh.read()
                        m = re.search(r'port\s*=\s*(\d+)|port\s*(\d+)', content)
                        if m:
                            old_port = int(m.group(1) or m.group(2))
                            new_port = self._detect_port_conflict(old_port + 1)
                            content = content.replace(str(old_port), str(new_port))
                            with open(fp, 'w', encoding='utf-8') as fh:
                                fh.write(content)
                            fixes.append(f"🔧 غيّرت port من {old_port} إلى {new_port} (كان مشغول)")
                            break
        # Module not found
        if "ModuleNotFoundError" in error_text:
            m = re.search(r"ModuleNotFoundError: No module named '(\w+)'", error_text)
            if m:
                pkg = m.group(1)
                r = subprocess.run(f"pip install {pkg}", shell=True, capture_output=True, text=True, timeout=60)
                fixes.append(f"📦 ثبّت مكتبة {pkg}" + (" ✅" if r.returncode == 0 else " ❌"))
        # File not found
        if "FileNotFoundError" in error_text:
            m = re.search(r"FileNotFoundError.*'(.*?)'", error_text)
            if m:
                fixes.append(f"📂 الملف {m.group(1)} مفقود")
        return "\n".join(fixes) if fixes else "⚠️ ما عرفت أصلح الخطأ تلقائياً"

    def _ensure_correct_path(self, target: str) -> str:
        """تأكد أن المسار داخل DevCenter"""
        base = "D:\\DevCenter"
        if not target.startswith(base):
            name = os.path.basename(target.rstrip('\\'))
            correct = os.path.join(base, target.replace(':', '').lstrip('\\') if ':\\' in target else "WebApps", name)
            self.log(f"📍 المسار غلط، ينقل من {target} إلى {correct}")
            if os.path.exists(target) and not os.path.exists(correct):
                os.makedirs(os.path.dirname(correct), exist_ok=True)
                try:
                    import shutil
                    shutil.copytree(target, correct, dirs_exist_ok=True)
                    self.log(f"✅ نقلت المشروع إلى {correct}")
                except:
                    pass
            return correct
        return target

    def smart_build(self, name: str, project_type: str = "web", details: str = ""):
        """بناء ذكي — يخطط، يبني، يكتشف المشاكل، يحلها، يشغل"""
        self.log(f"🧠 ببدأ بناء: {name} ({project_type})")

        # 1. Ensure correct path
        base = os.path.join("D:\\DevCenter", "WebApps", name)
        os.makedirs(base, exist_ok=True)

        # 2. Detect port before building
        free_port = self._detect_port_conflict(5000)
        if free_port != 5000:
            self.log(f"⚠️ البورت 5000 مشغول، راح أستخدم {free_port}")

        # 3. Build project
        self.build_project(name, project_type, details)

        # 4. Check dependencies
        missing = self._check_dependencies(base)
        if missing:
            self.log(f"📦 مكتبات ناقصة: {missing}")
            self._auto_install_missing(missing)

        # 5. Fix port in built files
        if free_port != 5000:
            for root, dirs, files in os.walk(base):
                for f in files:
                    if f.endswith('.py'):
                        fp = os.path.join(root, f)
                        with open(fp, 'r', encoding='utf-8') as fh:
                            content = fh.read()
                        if '5000' in content:
                            content = content.replace('port=5000', f'port={free_port}')
                            content = content.replace(':5000', f':{free_port}')
                            with open(fp, 'w', encoding='utf-8') as fh:
                                fh.write(content)

        # 6. Try running
        self.log(f"🚀 أحاول أشغل المشروع...")
        server_file = None
        for root, dirs, files in os.walk(base):
            for f in files:
                if f in ('app.py', 'server.py', 'main.py'):
                    server_file = os.path.join(root, f)
                    break
            if server_file: break

        if server_file:
            try:
                proc = subprocess.Popen(
                    ["python", server_file],
                    cwd=os.path.dirname(server_file),
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                import time as _time
                _time.sleep(3)
                if proc.poll() is not None:
                    err = proc.stderr.read().decode('utf-8', errors='ignore')[:500]
                    self.log(f"❌ السيرفر طفى: {err[:100]}")
                    fix = self._auto_fix_error(err, base)
                    self.log(fix)
                    # Try again
                    proc = subprocess.Popen(
                        ["python", server_file],
                        cwd=os.path.dirname(server_file),
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                    _time.sleep(3)
                    if proc.poll() is None:
                        self.log(f"✅ السيرفر اشتغل بعد الإصلاح! PID: {proc.pid}")
                    else:
                        self.log("❌ السيرفر لسّه ما اشتغل. شوف اللوق")
                else:
                    self.log(f"✅ السيرفر شغال! PID: {proc.pid}")
            except Exception as e:
                self.log(f"❌ خطأ في التشغيل: {e}")
        else:
            self.log("⚠️ ما لقيت ملف سيرفر (app.py, server.py, main.py)")

        self.log(f"✅ تم بناء {name} في {base}")
        return base

    def execute(self, command: str):
        """
        النقطة الرئيسية — افهم أمر عربي ونفذه
        يدعم كل الـ actions المذكورة في ai_understand
        """
        self.log(f"🤖 {command}")
        intent = self.ai_understand(command)
        self.log(f"🧠 {json.dumps(intent, ensure_ascii=False)}")
        action = intent.get("action", "unknown")
        target = intent.get("target", "")

        # ====== ACTIONS ======
        if action in ("download_app",):
            return self.download_app(target)

        elif action in ("open_app",):
            self.open_app(target)

        elif action in ("fix_app",):
            return self.fix_project(target)

        elif action in ("build_project",):
            return self.smart_build(target)

        elif action in ("search_web",):
            self._ensure_browser_open()
            self.browser_search(target)
            self.browser_screenshot("search.png")
            return True

        elif action in ("open_website", "navigate"):
            url = target if "://" in target else f"https://{target}"
            self._ensure_browser_open(url)
            return True

        elif action in ("shutdown",):
            self.system_shutdown()
            return True

        elif action in ("restart",):
            self.system_restart()
            return True

        elif action in ("lock_screen",):
            self.system_lock()
            return True

        elif action in ("volume_up",):
            self.system_volume_set(min(100, self.system_volume_get() + 10))
            return True

        elif action in ("volume_down",):
            self.system_volume_set(max(0, self.system_volume_get() - 10))
            return True

        elif action in ("mute",):
            self.system_volume_mute()
            return True

        elif action in ("system_info",):
            info = self.system_info()
            self.log(json.dumps(info, ensure_ascii=False, indent=2))
            return info

        elif action in ("battery_status",):
            batt = self.system_battery()
            self.log(json.dumps(batt, ensure_ascii=False, indent=2))
            return batt

        elif action in ("ip_config",):
            ip = self.net_ip()
            self.log(json.dumps(ip, ensure_ascii=False, indent=2))
            return ip

        elif action in ("ping_test",):
            result = self.net_ping(target or "8.8.8.8")
            self.log(result)
            return result

        elif action in ("kill_process",):
            killed = self.system_process_kill(target)
            self.log(f"🔪 قتلت: {killed}")
            return killed

        elif action in ("take_screenshot", "screenshot"):
            p = self.screen_screenshot(f"cmd_{int(time.time())}.png")
            self.log(f"📸 {p}")
            return p

        elif action in ("ocr_screen",):
            text = self.screen_ocr()
            self.log(f"📖 {text[:500]}")
            return text

        elif action in ("mouse_move",):
            dirs = {"يمين": (200,0), "يسار": (-200,0), "فوق": (0,-200), "تحت": (0,200),
                    "right": (200,0), "left": (-200,0), "up": (0,-200), "down": (0,200)}
            tl = target.lower()
            if tl in dirs:
                dx, dy = dirs[tl]
                cx, cy = self.mouse_pos()
                self.mouse_move(cx+dx, cy+dy)
                self.log(f"🖱️ حركت الماوس {target}")
            elif target.replace(","," ").replace("."," ").split()[0].isdigit():
                parts = target.replace(","," ").split()
                if len(parts) >= 2:
                    try:
                        self.mouse_move(int(parts[0]), int(parts[1]))
                        self.log(f"🖱️ الماوس إلى ({parts[0]}, {parts[1]})")
                    except: pass
            else:
                self.log(f"🖱️ ما عرفت الموقع: {target}")
            return True

        elif action in ("mouse_click",):
            self._click_in_browser()
            return True

        elif action in ("mouse_right_click",):
            self.mouse_right_click()
            self.log("🖱️ نقرت يمين")
            return True

        elif action in ("mouse_double_click",):
            self.mouse_double_click()
            self.log("🖱️ دبل كلك")
            return True

        elif action in ("mouse_drag",):
            self.mouse_drag(300, 300, 600, 300)
            self.log("🖱️ سحبت")
            return True

        elif action in ("mouse_scroll",):
            self.mouse_scroll(-5)
            self.log("🖱️ سكرول للأسفل")
            return True

        elif action in ("type_text", "click_element"):
            if action == "click_element":
                self._click_in_browser(target)
            else:
                self._type_in_browser(target)
            return True

        elif action in ("keyboard_shortcut",):
            parts = target.split()
            if parts:
                self.kb_hotkey(*parts)
                self.log(f"⌨️ اختصار: {target}")
            return True

        elif action in ("keyboard_tab_next",):
            self.kb_hotkey("ctrl", "tab")
            self.log("📑 تبويب التالي")
            return True

        elif action in ("keyboard_tab_prev",):
            self.kb_hotkey("ctrl", "shift", "tab")
            self.log("📑 تبويب السابق")
            return True

        elif action in ("keyboard_new_tab",):
            self.kb_hotkey("ctrl", "t")
            self.log("📑 تبويب جديد")
            return True

        elif action in ("keyboard_close_tab",):
            self.kb_hotkey("ctrl", "w")
            self.log("📑 أغلق التبويب")
            return True

        elif action in ("keyboard_back",):
            self.kb_hotkey("alt", "left")
            self.log("🔙 رجوع للصفحة السابقة")
            return True

        elif action in ("keyboard_forward",):
            self.kb_hotkey("alt", "right")
            self.log("🔜 تقدم للصفحة التالية")
            return True

        elif action in ("keyboard_refresh",):
            self.kb_hotkey("ctrl", "r")
            self.log("🔄 تحديث الصفحة")
            return True

        elif action in ("browser_zoom_in",):
            self.kb_hotkey("ctrl", "add")
            self.log("🔍 تكبير")
            return True

        elif action in ("browser_zoom_out",):
            self.kb_hotkey("ctrl", "subtract")
            self.log("🔍 تصغير")
            return True

        elif action in ("browser_fullscreen",):
            self.kb_hotkey("f11")
            self.log("🖥️ ملء الشاشة")
            return True

        elif action in ("open_file",):
            self.file_open(target)
            return True

        elif action in ("delete_file",):
            self.file_delete(target)
            return True

        elif action in ("copy_file",):
            parts = target.split(" إلى ")
            if len(parts) == 2:
                self.file_copy(parts[0].strip(), parts[1].strip())
            return True

        elif action in ("move_file",):
            parts = target.split(" إلى ")
            if len(parts) == 2:
                self.file_move(parts[0].strip(), parts[1].strip())
            return True

        elif action in ("zip_file",):
            self.file_zip(target)
            return True

        elif action in ("unzip_file",):
            self.file_unzip(target)
            return True

        elif action in ("list_files",):
            files = self.file_list(target or ".")
            self.log(f"📂 {len(files)} عنصر")
            return files

        elif action in ("find_file",):
            found = self.file_find(target)
            self.log(f"🔍 {len(found)} نتيجة")
            return found

        elif action in ("calculator",):
            try:
                result = eval(target)
                self.log(f"🧮 {target} = {result}")
                return result
            except:
                self.log(f"⚠️ ما قدرت أحسب: {target}")
                return None

        elif action in ("translate",):
            return self.ai_chat(f"Translate this to Arabic and explain: {target}")

        elif action in ("weather",):
            return self.ai_chat(f"What's the weather like for {target}? Give a brief answer in Arabic.")

        elif action in ("run_command",):
            out = subprocess.run(target, shell=True, capture_output=True, text=True)
            self.log(f"💻 {out.stdout[:1000]}")
            return out.stdout

        elif action in ("install_package",):
            self.dev_pip_install(target)
            return True

        elif action in ("record_audio",):
            p = self.audio_record(int(target) if target.isdigit() else 5)
            self.log(f"🎤 {p}")
            return p

        elif action in ("screen_record",):
            p = self.screen_record(int(target) if target.isdigit() else 10)
            self.log(f"🎬 {p}")
            return p

        else:
            self.log(f"⚠️ ما عرفت الإجراء: {action}")
            self.log("بجرب التنفيذ المباشر...")
            return self._execute_direct(command)

    def _execute_direct(self, command: str):
        """آخر محاولة — تنفيذ مباشر"""
        c = command.lower()
        if "حمل" in c or "نزل" in c:
            for w in command.split():
                if w not in ["حمل","نزل","تحميل","تطبيق","من","النت","على"]:
                    return self.download_app(w)
        if "صلح" in c or "fix" in c:
            for w in command.split():
                if w not in ["صلح","أصلح","fix","مشروع","التطبيق","ال"]:
                    return self.fix_project(w)
        if "ابني" in c or "build" in c or "أنشئ" in c:
            for w in command.split():
                if w not in ["ابني","build","أنشئ","create","مشروع","جديد"]:
                    return self.build_project(w)
        if "افتح" in c or "شغل" in c:
            for w in command.split():
                if self.open_app(w):
                    return True
        if "بحث" in c or "دور" in c:
            for w in command.split():
                if w not in ["بحث","دور","عن","على","google"] and len(w) > 2:
                    self.browser_open(); self.browser_search(w); return True
        if "اطفي" in c or "إيقاف" in c:
            self.system_shutdown(); return True
        if "صوت" in c:
            if "ارفع" in c: self.system_volume_set(min(100, self.system_volume_get() + 20))
            elif "اخفض" in c: self.system_volume_set(max(0, self.system_volume_get() - 20))
            return True
        self.log("🔍 والله ما فهمت. بفتح متصفح عشان نشوف")
        self.browser_open()
        self.screen_screenshot(f"unknown_{int(time.time())}.png")
        self.log("📸 صور الشاشة. شوف وش المطلوب")
        return False

    def open_app(self, name: str) -> bool:
        """فتح تطبيق على الجهاز"""
        name_lower = name.lower().strip()
        arabic = {"كروم":"chrome","متصفح":"chrome","فايرفوكس":"firefox","إيدج":"edge",
                   "مفكرة":"notepad","الحاسبة":"calc","المستكشف":"explorer",
                   "الطرفية":"wt","cmd":"cmd","poweshell":"powershell"}
        name_lower = arabic.get(name_lower, name_lower)
        paths = {
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "notepad": "notepad.exe", "cmd": "cmd.exe", "powershell": "powershell.exe",
            "calc": "calc.exe", "explorer": "explorer.exe", "paint": "mspaint.exe",
            "taskmgr": "taskmgr.exe", "wt": "wt.exe",
            "wezterm": r"C:\Program Files\WezTerm\wezterm.exe",
            "code": "code.cmd", "notepad++": "notepad++.exe",
        }
        if name_lower in paths:
            subprocess.Popen(paths[name_lower], shell=True); time.sleep(1); return True
        try:
            subprocess.Popen(f"start {name_lower}", shell=True); time.sleep(1); return True
        except:
            pass
        for folder in [r"C:\Program Files", r"C:\Program Files (x86)"]:
            for root, dirs, files in os.walk(folder):
                for f in files:
                    if name_lower in f.lower() and f.endswith(".exe"):
                        subprocess.Popen(os.path.join(root, f)); time.sleep(1); return True
                if root.count(os.sep) > 4: break
        return False

    def file_open(self, path: str):
        """فتح ملف بالتطبيق الافتراضي"""
        os.startfile(path)

    def log(self, msg: str):
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] {msg}")

    def screenshot(self, path: str = "admin.png") -> str:
        self.browser_screenshot(path)
        return path

    def cleanup(self):
        self.browser_close()


# ═══════════════════════════════════════════════════════════════
# CLI — واجهة سطر الأوامر
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  DevCenter — Admin Controller")
    print("  تحكم كامل بالجهاز بأوامر عربية")
    print("  > جميع خصائص التفاعل البشري <")
    print("=" * 60)
    print()
    print("  الأوامر: حمل, نزل, صلح, ابني, ابحث, افتح,")
    print("           اطفي, ريستارت, قفل, صوت, اقرأ, سجل...")
    print()

    ctrl = AdminController()
    try:
        if len(sys.argv) > 1:
            cmd = " ".join(sys.argv[1:])
            ctrl.execute(cmd)
        else:
            while True:
                cmd = input("👤 أنور: ").strip()
                if cmd.lower() in ("exit", "خروج", "quit", "q"):
                    break
                if cmd:
                    ctrl.execute(cmd)
                print()
    finally:
        ctrl.cleanup()
