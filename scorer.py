import requests
import json
import time
from tmdb import get_movie_context
from config import GROQ_API_KEY, GROQ_MODEL

def score_movie(context: list) -> dict:
    if context is None:
        return None
    else:
        prompt = """You are a movie expert. Use the overview of the movie as well as the given context to assign a score between 0 and 1 for thrill, action, romance, comedy, drama, and darkness. Respond ONLY with a JSON object in this exact format, no other text:
    {"thrill": 0.0, "action": 0.0, "romance": 0.0, "comedy": 0.0, "drama": 0.0, "darkness": 0.0}. You may search for the movie and do your own research, and use whatever information you gain to improve the scores. Limit your answer to 5500 characters.
    """ + " ".join(context)
        for attempt in range(5):
            time.sleep(2)
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0
                }
            )   

            if "choices" in response.json():
                break
            time.sleep(10)
        try:
            text = response.json()["choices"][0]["message"]["content"]
            if "<think>" in text:
                text = text.split("</think>")[-1].strip()
            return json.loads(text)
        except Exception as e:
            print('this model is currently overwhelmed. please try later', e)
            return None

