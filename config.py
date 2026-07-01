from dotenv import load_dotenv
import os
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "qwen/qwen3-32b" # To use Qwen AI
# GROQ_MODEL = "llama-3.3-70b-versatile" # To use Llama Versatile
# GROQ_MODEL = "llama-3.1-8b-instant" # LLaMa 3.1, fastest but not the best!
AXES = ["thrill", "action", "romance", "comedy", "drama", "darkness"] # genres. do not change
AXIS_GENRE_MAP = {
    "action": [28],
    "thrill": [53, 27], # Thrill and Horror
    "romance": [10749],
    "comedy": [35],
    "drama": [18],
    "darkness": [27, 80], # Horror and Crime
}
AXIS_THRESHOLD = 0.62 # Adjust this to your will
SIMILARITY_THRESHOLD = 0.6
PAGES_TO_SCAN = 3 # no of pages scanned