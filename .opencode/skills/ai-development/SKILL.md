---
name: ai-development
description: تطوير AI: Ollama, LangChain, API keys, streaming, evaluation
---

# مهارة تطوير AI

سير عمل كامل لتطوير تطبيقات الذكاء الاصطناعي.

---

## 1. الاتصال بالنماذج المحلية (Ollama)

```python
import requests
import json

OLLAMA_URL = "http://localhost:11434/api"

def chat_ollama(prompt: str, model: str = "llama3.2:3b") -> str:
    """إرسال رسالة إلى نموذج Ollama محلي."""
    response = requests.post(
        f"{OLLAMA_URL}/chat",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    )
    return response.json()["message"]["content"]

def list_models() -> list:
    """عرض النماذج المتاحة محلياً."""
    response = requests.get(f"{OLLAMA_URL}/tags")
    return [m["name"] for m in response.json()["models"]]
```

---

## 2. استخدام LangChain

```python
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# نموذج
llm = Ollama(model="llama3.2:3b", temperature=0.7)

# قالب
prompt = PromptTemplate(
    input_variables=["topic"],
    template="اكتب مقالاً عن {topic} بالعربية:"
)

# سلسلة
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run("الذكاء الاصطناعي")
print(result)
```

---

## 3. إدارة API Keys بأمان

### .env:
```
OPENAI_API_KEY=sk-xxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxx
OLLAMA_BASE_URL=http://localhost:11434
```

### في الكود:
```python
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

if not openai_key:
    raise ValueError("OPENAI_API_KEY غير موجود في .env")
```

---

## 4. التدفق (Streaming)

```python
# مع Ollama
def chat_stream(prompt: str, model: str = "llama3.2:3b"):
    """إرسال رسالة مع استقبال الرد بشكل متدفق."""
    response = requests.post(
        f"{OLLAMA_URL}/chat",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        },
        stream=True
    )
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if "message" in data:
                yield data["message"]["content"]

# الاستخدام
for chunk in chat_stream("اكتب قصة"):
    print(chunk, end="", flush=True)
```

---

## 5. التبديل بين النماذج (Fallback)

```python
def smart_chat(prompt: str) -> str:
    """محاولة مع النموذج المحلي، والرجوع إلى API إذا فشل."""
    models = [
        ("ollama", "llama3.2:3b"),
        ("ollama", "gemma:2b"),
        ("anthropic", "claude-3-haiku"),
    ]
    
    for provider, model in models:
        try:
            if provider == "ollama":
                return chat_ollama(prompt, model)
            elif provider == "anthropic":
                # استخدم Anthropic API
                pass
        except Exception as e:
            print(f"{model} فشل: {e}")
            continue
    
    return "عذراً، جميع النماذج غير متاحة."
```

---

## 6. تقييم النموذج (Evaluation)

```python
def evaluate_model(model: str, test_cases: list) -> dict:
    """تقييم دقة النموذج في مهام محددة."""
    results = []
    for case in test_cases:
        prompt = case["prompt"]
        expected = case["expected"]
        response = chat_ollama(prompt, model)
        is_correct = expected.lower() in response.lower()
        results.append({
            "prompt": prompt,
            "expected": expected,
            "response": response[:100],
            "correct": is_correct
        })
    
    accuracy = sum(r["correct"] for r in results) / len(results)
    return {
        "model": model,
        "accuracy": f"{accuracy:.0%}",
        "details": results
    }
```

---

## 7. واجهة بسيطة (Streamlit)

### app.py:
```python
import streamlit as st
import requests

st.title("🤖 المساعد الذكي")

model = st.selectbox("اختر النموذج", ["llama3.2:3b", "gemma:2b"])
prompt = st.text_input("اكتب سؤالك:")

if st.button("إرسال") and prompt:
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={"model": model, "messages": [{"role": "user", "content": prompt}]}
    )
    st.write(response.json()["message"]["content"])
```

### التشغيل:
```bash
pip install streamlit
streamlit run app.py
```

---

## 8. التسجيل (Logging)

```python
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ai_logs.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ai_dev")

logger.info(f"طلب: {prompt}")
logger.info(f"الرد: {response}")
logger.error(f"خطأ مع النموذج {model}: {e}")
```
