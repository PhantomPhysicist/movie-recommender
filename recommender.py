from scorer import score_movie
from tmdb import get_movie_context
from config import *
from utils import cosine
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=5, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}

def build_user_profile(movies: dict) -> dict:
    total_weight = sum(rating/5 for rating in movies.values())
    UserProfile = dict()
    for axis in AXES:
        UserProfile[axis] = 0
    
    for key, value in movies.items():
        context = get_movie_context(key)
        score = score_movie(context)
        if score is None:
            raise Exception("AI model unavailable. Please try again later.")
        for key2, value2 in score.items():
            score[key2] = (value/5)*value2
        for axis in AXES:
            UserProfile[axis] += score[axis]
        time.sleep(2)

    for key, value in UserProfile.items():
        UserProfile[key] = UserProfile[key]/total_weight
    
    return UserProfile

def get_candidate_movies(language: str, min_rating: float, include_adult: bool, page_offset: int = 0) -> dict:
    MovieDict = dict()
    for page in range(1 + page_offset, PAGES_TO_SCAN + 1 + page_offset):
        movies = []
        time.sleep(3)
        for attempt in range(5):
            try:
                url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_original_language={language}&vote_average.gte={min_rating}&include_adult={include_adult}&sort_by=popularity.desc&page={page}"
                time.sleep(2)
                link = session.get(url, headers=HEADERS)
                movies = link.json()['results']
                break
            except Exception as e:
                time.sleep(3)
                print(e)
        for movie in movies:
            MovieDict[movie['title']] = [movie['vote_average'], movie['overview'], movie['genre_ids'], movie['poster_path']]
    
    # print(MovieDict[0].get('poster_path'))
    return MovieDict

def filter_candidates(user_profile: dict, candidates: dict):
    Major = []
    for key, value in user_profile.items():
        if value >= (AXIS_THRESHOLD-0.05):
            Major.append(key)
    
    I_Axes = []
    for axis in Major:
        I_Axes.append(AXIS_GENRE_MAP[axis])
    
    I_Axes = [g for genres in I_Axes for g in genres]
    
    filtered_candidates = dict()
    for key, value in candidates.items():
        if any(g in I_Axes for g in value[2]):
            filtered_candidates[key] = [value[0], value[1], value[3]]
    
    return filtered_candidates

def find_similar_movies(user_profile: dict, candidates: dict, user_movies: dict, N: int) -> dict:
    filtered = filter_candidates(user_profile, candidates)
    similarities = []

    for title, value in filtered.items():
        if title in user_movies:
            continue
        else:
            score = score_movie([value[1]])
            if score is None:
                raise Exception("AI model unavailable. Please try again later.")
            cos = cosine(user_profile, score)
            similarities.append((title, cos, value[0], value[1], value[2]))
            time.sleep(4)

    similarities.sort(key=lambda x: x[1], reverse=True)
    similarities = similarities[:N]

    RecommendedMovies = dict()
    for pair in similarities:
        if pair[1] > SIMILARITY_THRESHOLD:
            RecommendedMovies[pair[0]] = {"Rating": pair[2], "Overview": pair[3], "Poster": pair[4]}
        else:
            continue
    #   print(RecommendedMovies)    
    return RecommendedMovies

