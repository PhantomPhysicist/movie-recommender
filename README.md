# Movie Recommender

A personalized movie recommendation system that uses LLMs to score movies on emotional/genre axes and finds the best matches for your taste using cosine similarity.

## Features
- **Mode A:** Get movie recommendations based on movies you've watched
- **Mode B:** Check if you would enjoy a specific movie
- Weighted user taste profiles
- Genre filtering
- Typo correction
- Movie posters

## Tech Stack
- Python, Streamlit
- TMDB API (movie data)
- Groq API with Qwen/LLaMA (LLM scoring)
- Cosine Similarity (matching)

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file:
TMDB_API_KEY=your_key
GROQ_API_KEY=your_key
4. Modify the config file to your wishes:
- at times, the AI model being used may be down/out of tokens. try switch to a different AI model. a couple of AI models' tags are given in the config file.
- AXIS_THRESHOLD is a variable that if an axis's score is above, that genre must be mandatory in the movie. for instance, if AXIS_THRESHOLD = 0.6, and "thrill" for a movie is 0.8, the algorithm only sifts through thriller movies.
- SIMILARITY_THRESHOLD is a variable that determines what the similarity between two movies must be for it to make the final cut. you can make it as high/low as you want!
- PAGES_TO_SCAN: the algorithm goes through the TMDB database page-by-page. this variable tells the algorithm how many pages to scan to get suitable candidates, before conducting the final comparison.
5. Run: `streamlit run main.py`

## How It Works
1. Input movies you've watched + ratings
2. LLM scores each on 6 axes: Thrill, Action, Romance, Comedy, Drama, Darkness
3. Weighted average builds your taste profile
4. Candidate movies are fetched from TMDB and filtered by genre
5. Cosine similarity finds the closest matches 

## Notes
- You will need your own [TMDB API key](https://www.themoviedb.org/settings/api) and [Groq API key](https://console.groq.com). Both of these can be obtained easily, for free.
- First run may be slow as the LLM scores multiple movies