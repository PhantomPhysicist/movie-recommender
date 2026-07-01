from config import *
from tmdb import get_movie_context
from utils import cosine
from scorer import score_movie
from recommender import build_user_profile
import requests
import json


def predict_movie(title: str, user_profile: dict) -> dict:
    try:
        context = get_movie_context(title)
        print(context[0])
        print(context[1])
        score = score_movie(context[0:2])
        print(score)
        poster = context[2]

        cos = cosine(user_profile, score)
        print(cos)

        prompt = f"""Given this user's taste profile: {user_profile}
    This movie's scores on six genres/axes: {score}
    And the cosine similarity between them: {cos}

    In 2-3 sentences, explain whether this user would enjoy '{title}' and why. Be specific about which aspects match or clash."""

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
        )
        explanation = response.json()["choices"][0]["message"]["content"]
        if "<think>" in explanation:
            explanation = explanation.split("</think>")[-1].strip()


        return {
            "similarity": cos,
            "explanation": explanation,
            "Poster": poster
        }
    except Exception as e:
        if score is None:
            raise Exception("AI model unavailable. Please try again later.")
            print(e)
            return None