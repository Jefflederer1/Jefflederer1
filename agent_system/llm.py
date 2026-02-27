from __future__ import annotations

import json
import os
from typing import List, Dict
from urllib import request
from urllib.error import URLError, HTTPError


class LLMClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def complete(self, messages: List[Dict[str, str]], role_hint: str) -> str:
        if not self.enabled:
            return self._fallback(messages, role_hint)

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }

        req = request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=60) as res:
                data = json.loads(res.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"].strip()
        except (HTTPError, URLError, TimeoutError, KeyError, json.JSONDecodeError) as exc:
            return (
                "LLM API call failed; using fallback output.\n"
                f"Error: {exc}\n\n"
                f"{self._fallback(messages, role_hint)}"
            )

    def _fallback(self, messages: List[Dict[str, str]], role_hint: str) -> str:
        user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        return (
            f"[{role_hint} fallback mode]\n"
            "Plan summary:\n"
            "1) Clarify scope and constraints from prompt.\n"
            "2) Define Salesforce integration contracts (auth, objects, API limits).\n"
            "3) Define UI parity map (views, components, interactions).\n"
            "4) Ship in thin slices with validation gates.\n\n"
            f"Prompt excerpt:\n{user_message[:500]}"
        )
