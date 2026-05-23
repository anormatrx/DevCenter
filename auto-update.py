#!/usr/bin/env python3
"""
auto-update.py — التحديث التلقائي لـ DevCenter
==============================================
فحص وتثبيت جميع المكتبات والإضافات عند بدء التشغيل.
تشتغل مرة وحدة كل 24 ساعة (تسجل آخر تحديث في ملف).
"""
import os, sys, subprocess, json, time
from datetime import datetime, timedelta
from pathlib import Path

DEVICENTER = Path(__file__).parent
STATE_FILE = DEVICENTER / ".opencode" / "last_update.json"

# قائمة جميع المكتبات المطلوبة
REQUIRED_PACKAGES = {
    # التحكم بالجهاز (admin-mouse)
    "pyautogui": "pyautogui",
    "pygetwindow": "pygetwindow",
    "keyboard": "keyboard",
    "pyperclip": "pyperclip",
    "psutil": "psutil",
    "requests": "requests",
    "Pillow": "Pillow",
    "winshell": "winshell",
    "plyer": "plyer",

    # المتصفح (Playwright)
    "playwright": "playwright",

    # السيرفرات
    "flask": "flask",
    "flask_cors": "flask-cors",

    # تلغرام
    "telegram": "python-telegram-bot",

    # OCR
    "pytesseract": "pytesseract",

    # الصوت
    "sounddevice": "sounddevice",
    "soundfile": "soundfile",
    "pyttsx3": "pyttsx3",
    "speech_recognition": "SpeechRecognition",

    # الفيديو
    "cv2": "opencv-python",
    "numpy": "numpy",

    # السرعة
    "speedtest": "speedtest-cli",

    # النظام
    "wmi": "wmi",
    "win10toast": "win10toast",
}

# قائمة أدوات CLI المطلوبة
REQUIRED_TOOLS = {
    "black": ("pip", "black"),
    "ruff": ("pip", "ruff"),
    "prettier": ("npm", "prettier"),
}

# إضافات اختيارية (تحتاج تثبيت يدوي)
OPTIONAL_PACKAGES = {
    "pycaw": "pycaw",
}

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def should_update() -> bool:
    """هل نحتاج تحديث؟ (مرة كل 24 ساعة)"""
    if not STATE_FILE.exists():
        return True
    try:
        data = json.loads(STATE_FILE.read_text(encoding='utf-8'))
        last = datetime.fromisoformat(data.get("last_update", "2000-01-01"))
        return datetime.now() - last > timedelta(hours=24)
    except:
        return True

def save_update_time():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({
        "last_update": datetime.now().isoformat(),
        "status": "ok"
    }, ensure_ascii=False, indent=2), encoding='utf-8')

def install_pip(package_name: str):
    """تثبيت باكج Python"""
    try:
        log(f"  📦 تثبيت: {package_name}")
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name, "--quiet", "--upgrade"],
            capture_output=True, text=True, timeout=120
        )
        if r.returncode == 0:
            log(f"     ✅ {package_name}")
            return True
        else:
            log(f"     ⚠️  خطأ: {r.stderr[:100]}")
            return False
    except Exception as e:
        log(f"     ⚠️  {e}")
        return False

def check_pip_package(module_name: str, pip_name: str) -> bool:
    """فحص باكج Python وتثبيته إذا ناقص"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        log(f"  ❌ {module_name} غير موجود")
        return install_pip(pip_name)

def check_tool(name: str, source: str, pkg: str) -> bool:
    """فحص أداة CLI وتثبيتها إذا ناقصة"""
    try:
        if source == "pip":
            subprocess.run([name, "--version"], capture_output=True, timeout=10)
        elif source == "npm":
            subprocess.run(["npx", name, "--version"], capture_output=True, timeout=10)
        return True
    except:
        log(f"  ❌ {name} غير موجود")
        if source == "pip":
            return install_pip(pkg)
        elif source == "npm":
            try:
                log(f"  📦 تثبيت: npm install -g {pkg}")
                r = subprocess.run(["npm", "install", "-g", pkg],
                                   capture_output=True, text=True, timeout=120)
                if r.returncode == 0:
                    log(f"     ✅ {name}")
                    return True
                log(f"     ⚠️  فشل تثبيت npm: {r.stderr[:100]}")
            except:
                log(f"     ⚠️  npm غير متاح")
            return False

def install_playwright():
    """تثبيت متصفحات Playwright"""
    try:
        from playwright.sync_api import sync_playwright
        # اختبر إذا المتصفح مثبت
        with sync_playwright() as p:
            p.chromium.launch(headless=True).close()
        return True
    except:
        log("  📦 تثبيت متصفحات Playwright...")
        r = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True, text=True, timeout=180
        )
        if r.returncode == 0:
            log("     ✅ Chromium مثبت")
            return True
        log(f"     ⚠️  فشل: {r.stderr[:200]}")
        return False

def auto_update(full: bool = False):
    """تشغيل التحديث التلقائي"""
    log("=" * 50)
    log("  DevCenter — التحديث التلقائي")
    log("=" * 50)
    log("")

    if not full and not should_update():
        log("⏳ آخر تحديث خلال 24 ساعة. تخطي...")
        log("   (استخدم --full للإجبار)")
        log("")
        return

    log("🔍 فحص المكتبات...")
    log("")

    # 1. مكتبات Python الأساسية
    log("[1/4] مكتبات Python...")
    installed = 0
    failed = 0
    for module, pip_name in REQUIRED_PACKAGES.items():
        if check_pip_package(module, pip_name):
            installed += 1
        else:
            failed += 1
    log(f"     {installed} موجودة، {failed} فشلت")
    log("")

    # 2. أدوات CLI
    log("[2/4] أدوات CLI...")
    cli_ok = 0
    cli_fail = 0
    for name, (source, pkg) in REQUIRED_TOOLS.items():
        if check_tool(name, source, pkg):
            cli_ok += 1
        else:
            cli_fail += 1
    log(f"     {cli_ok} موجودة، {cli_fail} فشلت")
    log("")

    # 3. متصفحات Playwright
    log("[3/4] متصفحات Playwright...")
    pw_ok = install_playwright()
    log(f"     {'✅' if pw_ok else '⚠️'}")
    log("")

    # 4. إضافات اختيارية
    log("[4/4] إضافات اختيارية...")
    for module, pip_name in OPTIONAL_PACKAGES.items():
        check_pip_package(module, pip_name)
    log("")

    # حفظ وقت التحديث
    save_update_time()

    # ملخص
    total = len(REQUIRED_PACKAGES) + len(REQUIRED_TOOLS)
    ok_count = installed + cli_ok + (1 if pw_ok else 0)
    log("=" * 50)
    log(f"  ✅ {ok_count}/{total} مكونات محدثة")
    log("=" * 50)
    log("")

if __name__ == "__main__":
    full = "--full" in sys.argv or "-f" in sys.argv
    auto_update(full=full)
