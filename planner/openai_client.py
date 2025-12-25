import os
import openai

openai.api_key = os.environ.get('OPENAI_API_KEY')

class OpenAIClient:
    @staticmethod
    def categorize_expense(description: str):
        if not openai.api_key:
            return {'category': 'unknown', 'confidence': 0}
        prompt = f"Categorize this expense description into a spending category: '{description}'\nReturn JSON: { '{' }"category": string, "confidence": float{ '}' }"
        resp = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            max_tokens=60,
            temperature=0
        )
        text = resp.choices[0].text.strip()
        # Best-effort parse
        try:
            import json
            return json.loads(text)
        except Exception:
            return {'category': text, 'confidence': 0}

    @staticmethod
    def suggest_budget(user_context: str):
        if not openai.api_key:
            return {'suggestion': 'No API key configured'}
        prompt = f"Given this user context, suggest a monthly budget plan: {user_context}" 
        resp = openai.Completion.create(
            model='text-davinci-003',
            prompt=prompt,
            max_tokens=200,
            temperature=0.6
        )
        return {'suggestion': resp.choices[0].text.strip()}
