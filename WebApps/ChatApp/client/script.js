(function () {
  'use strict';

  const API_BASE = 'http://localhost:5000';

  const form = document.getElementById('chat-form');
  const input = document.getElementById('message-input');
  const sendBtn = document.getElementById('send-btn');
  const messagesEl = document.getElementById('messages');
  const welcomeEl = document.getElementById('welcome');
  const statusDot = document.getElementById('status-dot');
  const statusText = document.getElementById('status-text');
  const toast = document.getElementById('toast');

  let isLoading = false;

  /* ---- Utility ---- */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function getTime() {
    return new Date().toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
  }

  function showToast(msg, duration) {
    toast.textContent = msg;
    toast.classList.remove('hidden');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.add('hidden'), duration || 3000);
  }

  function setStatus(state, text) {
    statusDot.className = 'status-dot ' + state;
    statusText.textContent = text;
  }

  /* ---- Markdown Render ---- */
  function renderMarkdown(text) {
    if (!text) return '';

    const blocks = [];
    let remaining = text;

    // Code blocks ```
    const codeBlockRegex = /```(\w*)\n?([\s\S]*?)```/g;
    let lastIdx = 0;
    let match;

    while ((match = codeBlockRegex.exec(text)) !== null) {
      if (match.index > lastIdx) {
        blocks.push({ type: 'text', content: text.slice(lastIdx, match.index) });
      }
      blocks.push({ type: 'code', lang: match[1], content: match[2] });
      lastIdx = match.index + match[0].length;
    }
    if (lastIdx < text.length) {
      blocks.push({ type: 'text', content: text.slice(lastIdx) });
    }

    if (blocks.length === 0) {
      blocks.push({ type: 'text', content: text });
    }

    return blocks.map(block => {
      if (block.type === 'code') {
        const langAttr = block.lang ? ` class="language-${escapeHtml(block.lang)}"` : '';
        return `<pre><code${langAttr}>${escapeHtml(block.content.trim())}</code></pre>`;
      }
      return renderInline(block.content);
    }).join('\n');
  }

  function renderInline(text) {
    if (!text) return '';
    let html = escapeHtml(text);

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Bold
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // Italic
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    // Line breaks
    html = html.replace(/\n/g, '<br>');

    return html;
  }

  /* ---- Message DOM ---- */
  function addMessage(role, text, time) {
    welcomeEl.style.display = 'none';

    const avatar = role === 'user' ? 'أنت' : '🤖';
    const div = document.createElement('div');
    div.className = 'message ' + role;

    if (role === 'bot' && text === '__typing__') {
      div.classList.add('typing');
      div.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-body">
          <span class="dot"></span>
          <span class="dot"></span>
          <span class="dot"></span>
        </div>
      `;
      messagesEl.appendChild(div);
      scrollToBottom();
      return div;
    }

    const rendered = renderMarkdown(text);
    div.innerHTML = `
      <div class="message-avatar">${avatar}</div>
      <div class="message-body">${rendered}</div>
    `;

    const timeEl = document.createElement('div');
    timeEl.className = 'message-time';
    timeEl.textContent = time || getTime();
    div.querySelector('.message-body').appendChild(timeEl);

    messagesEl.appendChild(div);
    scrollToBottom();
    return div;
  }

  function scrollToBottom() {
    const container = document.getElementById('chat-container');
    requestAnimationFrame(() => {
      container.scrollTop = container.scrollHeight;
    });
  }

  function removeTyping() {
    const typing = messagesEl.querySelector('.message.typing');
    if (typing) typing.remove();
  }

  /* ---- API Calls ---- */
  async function sendMessage(text) {
    if (isLoading) return;
    isLoading = true;
    sendBtn.disabled = true;

    addMessage('user', text);
    input.value = '';
    addMessage('bot', '__typing__');

    try {
      const res = await fetch(API_BASE + '/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      removeTyping();

      if (!res.ok) {
        const errText = await res.text().catch(() => '');
        addMessage('bot', '⚠️ **خطأ في السيرفر:** ' + (errText || res.statusText));
        return;
      }

      const data = await res.json();
      addMessage('bot', data.reply || data.response || 'لم يتم استلام رد');
    } catch (err) {
      removeTyping();
      addMessage('bot', '⚠️ **فشل الاتصال بالسيرفر.**\n\nهل السيرفر شغال؟ تأكد من:\n1. `python server/server.py` في `WebApps/ChatApp/`\n2. Ollama شغال');
    } finally {
      isLoading = false;
      sendBtn.disabled = false;
      input.focus();
    }
  }

  async function checkHealth() {
    try {
      const res = await fetch(API_BASE + '/api/health');
      if (res.ok) {
        setStatus('online', 'متصل');
      } else {
        setStatus('offline', 'غير متاح');
      }
    } catch {
      setStatus('offline', 'غير متصل');
    }
  }

  async function loadHistory() {
    try {
      const res = await fetch(API_BASE + '/api/history');
      if (!res.ok) return;
      const data = await res.json();
      const history = data.history || data.messages || [];
      if (history.length === 0) return;

      welcomeEl.style.display = 'none';
      history.forEach(msg => {
        const isUser = msg.role === 'user' || msg.user === 'User';
        addMessage(
          isUser ? 'user' : 'bot',
          isUser ? (msg.content || msg.message || '') : (msg.reply || msg.content || ''),
          msg.time ? new Date(msg.time).toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' }) : undefined
        );
      });
    } catch {
      // silent — history is best-effort
    }
  }

  /* ---- Events ---- */
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const text = input.value.trim();
    if (!text || isLoading) return;
    sendMessage(text);
  });

  /* ---- Init ---- */
  checkHealth();
  loadHistory();
  setInterval(checkHealth, 15000);

  input.focus();
})();