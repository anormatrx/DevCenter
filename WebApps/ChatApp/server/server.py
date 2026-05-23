from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

messages = []
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")

def ask_ollama(message: str) -> str:
    """إرسال رسالة إلى Ollama المحلي واستقبال الرد."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": message}],
                "stream": False,
                "options": {"temperature": 0.7}
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["message"]["content"]
        return f"عذراً، النموذج مشغول (حالة: {response.status_code})"
    except requests.ConnectionError:
        return "عذراً، Ollama غير شغال. شغّل `ollama serve` أولاً."
    except Exception as e:
        return f"حدث خطأ: {str(e)}"

@app.route("/")
def home():
    return "Chat Server شغال ومرتبط بـ Ollama ✅"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    user = data.get("user", "User")
    
    reply = ask_ollama(msg)
    
    entry = {
        "user": user,
        "message": msg,
        "reply": reply,
        "time": datetime.now().isoformat()
    }
    messages.append(entry)
    
    return jsonify(entry)

@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(messages[-50:])

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": MODEL, "ollama_connected": True, "messages": len(messages)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Server running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
