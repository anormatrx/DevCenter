# DevCenter 🚀

**Full-Stack AI Development Hub on Windows**

A comprehensive local development environment powered by **OpenCode TUI** + **Ollama** + **OpenRouter AI**, with full Arabic voice/command support, mouse automation, Telegram remote control, and 24/7 server monitoring.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Assistant** | Local Ollama + OpenRouter + Claude (optional) |
| 🖱️ **Admin Control** | Full mouse/keyboard/browser automation with Arabic commands |
| 💬 **ChatApp** | Real-time chat UI connected to local AI |
| 🤖 **Telegram Bot** | Remote control via Telegram with Arabic NLP |
| 🎨 **Format Master** | Auto-formatting for Python, JS, HTML, CSS, JSON |
| 📝 **Notes App** | Desktop notes app with dark theme & Arabic support |
| 🔄 **24/7 Servers** | Auto-restart for all services, runs on Windows startup |
| 🌐 **WezTerm** | Custom terminal with Arabic RTL support, GitHub Dark theme |

---

## 🏗️ Structure

```
D:\DevCenter\
├── .opencode/          # OpenCode config & skills (14 skills)
│   ├── skills/         # admin-mouse, format-master, git-workflow, ...
│   └── commands/       # Telegram, lint, review, test, ...
├── Tools/              # Telegram bot, notes, notifier, WhatsApp
├── WebApps/            # ChatApp (Flask server + HTML client)
│   └── ChatApp/
├── GitRepos/           # Cloned repositories
├── Logs/               # Session logs
├── auto-update.py      # Auto package updater
├── run-opencode.cmd    # Primary launcher
├── run-servers-247.bat # 24/7 server monitor
└── devcenter.bat       # Backup full-stack launcher
```

---

## 🚀 Quick Start

1. **Launch DevCenter** — double-click `DevCenter` desktop shortcut (opens WezTerm → OpenCode)
2. **Or manually:**
   ```bash
   run-opencode.cmd
   ```
3. **Speak Arabic commands** inside OpenCode:
   - `حمل VLC` — download & install any app
   - `صلح المشروع` — fix project bugs automatically
   - `افتح موقع google.com` — browse the web
   - `صور الشاشة` — take a screenshot
   - `معلومات الجهاز` — system info

---

## 🧠 AI Models

| Provider | Models | Status |
|----------|--------|--------|
| **Ollama** (local) | llama3.2:3b, gemma:2b | ✅ Always on |
| **OpenRouter** (free) | 4 free models | ✅ Configured |
| **Anthropic** | Claude | ⏳ Add API key via `/connect` |

---

## 🛠️ Requirements

- **Python 3.11+**
- **WezTerm** (terminal)
- **Ollama** (local AI)
- **Git** (for version control)
- **Optional:** Node.js (for Prettier)

---

## 📦 Dependencies

Install automatically via:
```bash
python auto-update.py --full
```

Key libraries: `pyautogui`, `playwright`, `flask`, `python-telegram-bot`, `pillow`, `opencv-python`, `black`, `ruff`

---

## 🤝 Telegram Bot

Bot: **@anwarhelperbot**

Commands via natural Arabic:
- `حمل [app]` — download & install
- `صلح [project]` — fix code issues
- `شغل السيرفر` — start servers
- `ابحث عن [query]` — search the web

---

## 📄 License

MIT License — see [LICENSE](LICENSE).

---

## 👤 Author

**أنور (Anwar)** — AI-powered development hub, built with ❤️ on Windows.
