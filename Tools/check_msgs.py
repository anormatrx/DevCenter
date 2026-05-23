import requests, os
from pathlib import Path

env_path = Path(__file__).parent / '.env.comm'
token = ''
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.startswith('TELEGRAM_BOT_TOKEN='):
            token = line.split('=', 1)[1].strip()
token = token or os.environ.get('TELEGRAM_BOT_TOKEN', '')
if not token:
    print('⚠️ TELEGRAM_BOT_TOKEN غير موجود. ضبطه في Tools\.env.comm')
    exit()

r = requests.post(f'https://api.telegram.org/bot{token}/getUpdates', json={'timeout': 2}, timeout=10)
if r.status_code == 200:
    msgs = r.json().get('result', [])
    if msgs:
        for u in msgs:
            m = u.get('message', {})
            print(f'From {m.get("chat",{}).get("id")}: {m.get("text","")}')
    else:
        print('No messages. Send /start to @anor777_bot on Telegram')
else:
    print(f'Error: {r.status_code}')
