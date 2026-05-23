async function apiCall(url, data) {
    const opts = { method: 'POST', headers: { 'Content-Type': 'application/json' } };
    if (data) opts.body = JSON.stringify(data);
    const r = await fetch(url, opts);
    return r.json();
}

async function login() {
    const pwd = document.getElementById('password-input').value;
    const r = await apiCall('/api/login', { password: pwd });
    if (r.success) {
        document.getElementById('login-screen').style.display = 'none';
        document.getElementById('main-screen').style.display = 'block';
    } else {
        document.getElementById('login-error').textContent = r.error || 'كلمة المرور خطأ';
    }
}
document.getElementById('password-input').addEventListener('keydown', e => { if (e.key === 'Enter') login(); });

async function logout() {
    await apiCall('/api/logout');
    document.getElementById('main-screen').style.display = 'none';
    document.getElementById('login-screen').style.display = 'flex';
}

function confirmAction(type) {
    const msgs = { shutdown: '⏻ تأكيد إيقاف التشغيل?', restart: '🔄 تأكيد إعادة التشغيل?' };
    if (!confirm(msgs[type] || 'تأكيد?')) return;
    apiCall('/api/' + type).then(r => alert(r.message || r.error));
}

async function takeScreenshot() {
    const r = await apiCall('/api/screenshot');
    if (r.image) {
        document.getElementById('screenshot-img').src = 'data:image/png;base64,' + r.image;
        document.getElementById('screenshot-modal').style.display = 'flex';
    } else {
        alert(r.error || 'فشل');
    }
}
function closeScreenshot() { document.getElementById('screenshot-modal').style.display = 'none'; }

async function openApp() {
    const app = document.getElementById('app-input').value.trim();
    if (!app) return;
    const r = await apiCall('/api/open-app', { app });
    alert(r.message || r.error);
}

async function runCmd() {
    const cmd = document.getElementById('cmd-input').value.trim();
    if (!cmd) return;
    document.getElementById('cmd-output').textContent = '⏳ جاري التنفيذ...';
    const r = await apiCall('/api/cmd', { command: cmd });
    document.getElementById('cmd-output').textContent = r.output || r.error || 'تم';
}
document.getElementById('cmd-input').addEventListener('keydown', e => { if (e.key === 'Enter') runCmd(); });

async function checkAuth() {
    try {
        const r = await fetch('/api/check-auth');
        const d = await r.json();
        if (d.authenticated) {
            document.getElementById('login-screen').style.display = 'none';
            document.getElementById('main-screen').style.display = 'block';
        }
    } catch(e) {}
}
checkAuth();
