import requests
import time
import re
from correct_title import correct_title
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import *

session = requests.Session()
retry = Retry(total=5, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}

def get_movie_context(title: str) -> list:
    title = correct_title(title)
    titleurl = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    for attempt in range(5):
        try:
            time.sleep(2)
            Movie = session.get(titleurl, headers=HEADERS)
            movie_ID = Movie.json()["results"][0]["id"]
            overview = Movie.json()["results"][0]["overview"]
            poster_path = Movie.json()["results"][0]["poster_path"]
            break
        except Exception as e:
            time.sleep(3)
            print(e)
            continue

    IDurl = "https://api.themoviedb.org/3/movie/"+str(movie_ID)+"/reviews?api_key="+TMDB_API_KEY
    revStr = ""
    for attemptAgain in range(5):
        try:
            time.sleep(2)
            rev = session.get(IDurl, headers=HEADERS)
            remaining = 8000 - len(overview)
            revStr = ""
            for i in rev.json()["results"]:
                cleaned = re.sub(r'<.*?>', '', i["content"])
                if len(revStr) + len(cleaned) > remaining:
                    break
                revStr += cleaned
            break
        except Exception as e:
            print(e)
            time.sleep(3)
            continue
    return [overview, revStr, poster_path]