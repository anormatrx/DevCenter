import os, json, asyncio
from pathlib import Path
from datetime import datetime

ENV_PATH = Path(__file__).parent / ".env.comm"
CONFIG = {}

def load_config():
    if not ENV_PATH.exists():
        return
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                CONFIG[k.strip()] = v.strip()

load_config()

class Notifier:
    def __init__(self):
        self.telegram = None
        self.log_path = Path(__file__).parent.parent / "Logs" / "notifications.log"

    def log(self, channel, status, msg):
        entry = f"[{datetime.now().isoformat()}] {channel}: {status} - {msg}\n"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    async def send_telegram(self, message: str):
        token = CONFIG.get("TELEGRAM_BOT_TOKEN", "")
        chat_id = CONFIG.get("TELEGRAM_CHAT_ID", "")
        if not token or not chat_id:
            self.log("telegram", "SKIP", "لا يوجد توكن أو chat_id في .env.comm")
            return False
        try:
            import aiohttp
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}) as r:
                    if r.status == 200:
                        self.log("telegram", "OK", message[:50])
                        return True
                    self.log("telegram", f"ERR {r.status}", await r.text())
                    return False
        except Exception as e:
            self.log("telegram", "ERROR", str(e))
            return False

    def send_whatsapp(self, message: str):
        number = CONFIG.get("WHATSAPP_NUMBER", "")
        if not number:
            self.log("whatsapp", "SKIP", "لا يوجد رقم في .env.comm")
            return False
        try:
            import pywhatkit as kit
            kit.sendwhatmsg_instantly(number, message, wait_time=15, tab_close=True)
            self.log("whatsapp", "OK", message[:50])
            return True
        except Exception as e:
            self.log("whatsapp", "ERROR", str(e))
            return False

    def send_all(self, message: str):
        asyncio.run(self.send_telegram(message))
        self.send_whatsapp(message)

def notify(message: str):
    n = Notifier()
    n.send_all(f"DevCenter: {message}")
    return n

if __name__ == "__main__":
    import sys
    msg = " ".join(sys.argv[1:]) or "اختبار الإشعارات"
    notify(msg)
    print(f"تم إرسال: {msg}")