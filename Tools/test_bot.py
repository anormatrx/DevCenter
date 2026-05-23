import requests, json, os
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
    exit(1)

# Test token
r = requests.get(f'https://api.telegram.org/bot{token}/getMe', timeout=15)
if r.status_code == 200:
    bot = r.json()['result']
    print('Bot OK: @' + bot['username'] + ' - ' + bot['first_name'])
else:
    print(f'Token ERR: {r.status_code} - {r.text[:200]}')
    exit(1)

# Check messages
r2 = requests.post(f'https://api.telegram.org/bot{token}/getUpdates', json={'timeout': 5}, timeout=10)
if r2.status_code == 200:
    updates = r2.json().get('result', [])
    print(f'Messages waiting: {len(updates)}')
    for u in updates:
        msg = u.get('message', {})
        chat_id = msg.get('chat', {}).get('id', '?')
        text = msg.get('text', '')
        print(f'  From {chat_id}: {text}')
else:
    print(f'getUpdates ERR: {r2.status_code}')
