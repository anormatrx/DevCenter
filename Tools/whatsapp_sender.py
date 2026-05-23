import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from notifier import CONFIG

NUMBER = CONFIG.get("WHATSAPP_NUMBER", "")

def send_now(message: str):
    if not NUMBER:
        print("WHATSAPP_NUMBER غير موجود في .env.comm")
        return False
    try:
        import pywhatkit as kit
        kit.sendwhatmsg_instantly(NUMBER, message, wait_time=15, tab_close=True)
        print(f"تم إرسال واتساب: {message[:50]}")
        return True
    except Exception as e:
        print(f"خطأ واتساب: {e}")
        return False

def send_later(message: str, hour: int, minute: int):
    if not NUMBER:
        print("WHATSAPP_NUMBER غير موجود في .env.comm")
        return False
    try:
        import pywhatkit as kit
        kit.sendwhatmsg(NUMBER, message, hour, minute, wait_time=15)
        print(f"سيتم الإرسال في {hour}:{minute}")
        return True
    except Exception as e:
        print(f"خطأ واتساب: {e}")
        return False

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "رسالة من DevCenter"
    send_now(msg)