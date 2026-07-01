from config import *
import requests

def get_language_code(language: str) -> str:
    try:
        prompt = f"Convert '{language}' to its ISO 639-1 two-letter language code. Return only the code, nothing else."
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            }
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except:
        print('this model is overwhelmed. please try later')

def correct_title(title: str) -> str:
    try:
        correction_prompt = f"The user typed '{title}' as a movie name. If this looks like a typo or misspelling, return only the correct movie title. If it's already correct, return it as-is. Return only the title, nothing else."
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": correction_prompt}],
                "temperature": 0
            }
        )
        return response.json()["choices"][0]["message"]["content"].strip()
    except:
        print('this model is overwhelmed. please try later')