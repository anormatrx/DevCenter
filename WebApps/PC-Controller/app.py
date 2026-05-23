import os, io, base64, subprocess, socket, sys
from flask import Flask, render_template, request, jsonify, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'pc-controller-secret-2026'
PASSWORD = "1234"

def find_free_port(start=5000):
    while start < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', start)) != 0:
                return start
        start += 1
    return 5000

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data and data.get('password') == PASSWORD:
        session['logged_in'] = True
        return jsonify({'success': True})
    return jsonify({'error': 'كلمة المرور خطأ'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'success': True})

@app.route('/api/check-auth')
def check_auth():
    return jsonify({'authenticated': session.get('logged_in', False)})

@app.route('/api/shutdown', methods=['POST'])
@login_required
def shutdown():
    subprocess.Popen('shutdown /s /t 5', shell=True)
    return jsonify({'message': 'سيتم إيقاف التشغيل بعد 5 ثواني'})

@app.route('/api/restart', methods=['POST'])
@login_required
def restart():
    subprocess.Popen('shutdown /r /t 5', shell=True)
    return jsonify({'message': 'سيتم إعادة التشغيل بعد 5 ثواني'})

@app.route('/api/lock', methods=['POST'])
@login_required
def lock():
    subprocess.Popen('rundll32.exe user32.dll,LockWorkStation', shell=True)
    return jsonify({'message': 'تم قفل الجهاز'})

@app.route('/api/screenshot', methods=['POST'])
@login_required
def screenshot():
    try:
        import pyautogui
        img = pyautogui.screenshot()
        buf = io.BytesIO()
        img.save(buf, 'PNG')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode()
        return jsonify({'image': img_base64})
    except ImportError:
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            buf = io.BytesIO()
            img.save(buf, 'PNG')
            buf.seek(0)
            img_base64 = base64.b64encode(buf.getvalue()).decode()
            return jsonify({'image': img_base64})
        except ImportError:
            return jsonify({'error': 'يلزم تثبيت pyautogui: pip install pyautogui'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/volume/up', methods=['POST'])
@login_required
def volume_up():
    try:
        subprocess.run(['powershell', '-Command',
            '(New-Object -ComObject WScript.Shell).SendKeys([char]175)'],
            check=True, capture_output=True)
        return jsonify({'message': '✓ رفع الصوت'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/volume/down', methods=['POST'])
@login_required
def volume_down():
    try:
        subprocess.run(['powershell', '-Command',
            '(New-Object -ComObject WScript.Shell).SendKeys([char]174)'],
            check=True, capture_output=True)
        return jsonify({'message': '✓ خفض الصوت'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/volume/mute', methods=['POST'])
@login_required
def volume_mute():
    try:
        subprocess.run(['powershell', '-Command',
            '(New-Object -ComObject WScript.Shell).SendKeys([char]173)'],
            check=True, capture_output=True)
        return jsonify({'message': '✓ تم كتم الصوت'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/open-app', methods=['POST'])
@login_required
def open_app():
    data = request.get_json()
    app_name = data.get('app', '').strip()
    if not app_name:
        return jsonify({'error': 'الرجاء إدخال اسم التطبيق'}), 400
    try:
        subprocess.Popen(f'start "" "{app_name}"', shell=True)
        return jsonify({'message': f'✓ تم فتح {app_name}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cmd', methods=['POST'])
@login_required
def cmd():
    data = request.get_json()
    command = data.get('command', '').strip()
    if not command:
        return jsonify({'error': 'الرجاء إدخال الأمر'}), 400
    try:
        result = subprocess.run(
            ['powershell', '-Command', command],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        return jsonify({'output': output or '✓ تم التنفيذ بنجاح'})
    except subprocess.TimeoutExpired:
        return jsonify({'output': '⌛ انتهت المهلة (30 ثانية)'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cancel-shutdown', methods=['POST'])
@login_required
def cancel_shutdown():
    subprocess.run('shutdown /a', shell=True, capture_output=True)
    return jsonify({'message': '✓ تم إلغاء الإيقاف'})

if __name__ == '__main__':
    port = find_free_port(5000)
    host = '0.0.0.0'
    print("=" * 50)
    print("  PC-Controller Server")
    print(f"  http://{host}:{port}")
    print("  Password: 1234")
    print("=" * 50)
    app.run(host=host, port=port, debug=True)
