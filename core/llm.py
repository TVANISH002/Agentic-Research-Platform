from __future__ import annotations

import json
import os
from pathlib import Path

import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv
from core.config import settings

# Load .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or settings.groq_api_key
GROQ_BASE_URL = settings.groq_base_url
GROQ_MODEL = settings.groq_model

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing")

CHAT_URL = f"{GROQ_BASE_URL}/chat/completions"


def _call_llm(payload):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        CHAT_URL,
        headers=headers,
        json=payload,
        timeout=60,   # increased from 20
    )

    if response.status_code != 200:
        raise Exception(f"LLM Error: {response.text}")

    return response.json()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(), reraise=True)
def chat_completion(system_prompt, user_prompt, temperature=0.2, model=None):
    payload = {
        "model": model or GROQ_MODEL,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    res = _call_llm(payload)
    return res["choices"][0]["message"]["content"]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(), reraise=True)
def chat_json(system_prompt, user_prompt, temperature=0.0, model=None):
    payload = {
        "model": model or GROQ_MODEL,
        "temperature": temperature,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    res = _call_llm(payload)
    return json.loads(res["choices"][0]["message"]["content"])