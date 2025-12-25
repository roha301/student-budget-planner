import hashlib
import json
import os
import time

import openai
from django.conf import settings
from django.core.cache import cache

openai.api_key = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")


class OpenAIClient:
    @staticmethod
    def _make_key(prefix, payload_obj):
        payload = json.dumps(payload_obj, sort_keys=True, ensure_ascii=False)
        h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return f"openai:{prefix}:{h}"

    @staticmethod
    def _chat(messages, max_tokens=300, temperature=0.4, cache_prefix=None):
        cache_key = None
        if cache_prefix:
            cache_key = OpenAIClient._make_key(
                cache_prefix,
                {
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
            )
            cached = cache.get(cache_key)
            if cached:
                return cached
        if not openai.api_key:
            raise RuntimeError("OpenAI API key not set")
        # simple retry/backoff
        backoff = 1
        for attempt in range(3):
            try:
                resp = openai.ChatCompletion.create(
                    model=MODEL,
                    messages=messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                out = resp.choices[0].message.content.strip()
                if cache_key:
                    ttl = getattr(settings, "OPENAI_CACHE_SECONDS", 3600)
                    cache.set(cache_key, out, ttl)
                return out
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(backoff)
                backoff *= 2

    @staticmethod
    def categorize_expense(description: str):
        try:
            system = (
                "You are an assistant that categorizes short expense descriptions into simple "
                "spending categories like Food, Transport, Rent, Entertainment, Utilities, "
                "Utilities, Groceries, Education, Other. "
                'Reply only with a JSON object: {"category": string, "confidence": number (0-1)}'
            )
            user = f'Categorize this expense: "{description}"'
            cache_key = f"cat:{hash(description)}"
            out = OpenAIClient._chat(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=60,
                temperature=0,
                cache_prefix=cache_key,
            )
            return json.loads(out)
        except Exception:
            return {"category": "Other", "confidence": 0}

    @staticmethod
    def suggest_budget(summary: str):
        try:
            system = (
                "You are a financial assistant for students. Given a brief summary of recent "
                "spending, return a concise monthly budget plan as JSON: "
                '{"monthly_income": number, '
                '"allocations": [{"category": string, "amount": number}], '
                '"notes": string}'
            )
            user = (
                f"User spending summary:\n{summary}\nProvide a recommended monthly budget in the "
                "specified JSON format. Keep allocations reasonable for a student."
            )
            cache_key = f"suggest:{hash(summary)}"
            out = OpenAIClient._chat(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=400,
                temperature=0.6,
                cache_prefix=cache_key,
            )
            return json.loads(out)
        except Exception:
            return {"error": "Unable to generate suggestion"}

    @staticmethod
    def forecast_expenses(history_summary: str, months=3):
        try:
            system = (
                "You are an assistant that forecasts monthly spending totals by category "
                "based on recent history. Return JSON: "
                '{"forecasts": [{"month": string, "category": string, '
                '"amount": number}], "notes": string}'
            )
            user = (
                f"History summary:\n{history_summary}\nForecast spending for the next {months} "
                "months and return the JSON."
            )
            cache_key = f"forecast:{hash(history_summary)}:{months}"
            out = OpenAIClient._chat(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=500,
                temperature=0.4,
                cache_prefix=cache_key,
            )
            return json.loads(out)
        except Exception:
            return {"error": "Unable to forecast"}

    @staticmethod
    def answer_nl_query(context: str, query: str):
        try:
            system = (
                "You are a helpful financial assistant for a single student's data. Use the "
                "provided context (spending summaries, budgets) and answer the user's "
                "natural language question. Reply in JSON: {\"answer\": string, \"followup\": string}"
            )
            user = (
                f"Context:\n{context}\n\nQuestion: {query}\nRespond in JSON."
            )
            cache_key = f"nlq:{hash(context)}:{hash(query)}"
            out = OpenAIClient._chat(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=400,
                temperature=0.3,
                cache_prefix=cache_key,
            )
            return json.loads(out)
        except Exception:
            return {"error": "Unable to answer"}
