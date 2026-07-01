import streamlit as st
from correct_title import *
from scorer import *
from recommender import *
from tmdb import *
from predict import predict_movie

st.markdown("""
<style>
::selection {
    background-color: #64E1E7;
    color: black;
}
</style>
""", unsafe_allow_html=True)

st.title("Movie Recommender")
st.subheader("Movies you've watched")

if "movies" not in st.session_state:
    st.session_state.movies = {}

if "page_offset" not in st.session_state:
    st.session_state.page_offset = 0

with st.form("add_movie_form", clear_on_submit=True):
    movie_input = st.text_input("Movie title")
    rating_input = st.slider("Your rating out of 5", 1.0, 5.0, 3.0, 0.1)
    submitted = st.form_submit_button("Add Movie")
    if submitted and movie_input:
        st.session_state.movies[movie_input] = rating_input

for movie in list(st.session_state.movies.keys()):
    col1, col2 = st.columns([4, 1])
    col1.write(f"{movie} — {st.session_state.movies[movie]}")
    if col2.button("Remove", key=f"remove_{movie}"):
        del st.session_state.movies[movie]
        st.rerun()
    with st.expander(f"Modify {movie}"):
        new_name = st.text_input("New title", value=movie, key=f"name_{movie}")
        new_rating = st.slider("New rating", 1.0, 5.0, st.session_state.movies[movie], 0.1, key=f"rating_{movie}")
        if st.button("Update", key=f"update_{movie}"):
            del st.session_state.movies[movie]
            st.session_state.movies[new_name] = new_rating
            st.rerun()

st.subheader("Filters")
language_input = st.text_input("Language (e.g. English, Tamil, French)", "English")
min_rating = st.slider("Minimum TMDB rating", 0.0, 10.0, 7.0, 0.5)
include_adult = st.checkbox("Include adult content", value=False)
st.subheader("What would you like to do?")

predict_input = st.text_input("Movie Name (to check if you'll like). Leave blank for recommendations.")

col1, col2 = st.columns(2)
find_movies = col1.button("🎬 Find Movies for Me")
predict = col2.button("🤔 Will I like this movie?")

if predict and predict_input:
    if "results" in st.session_state:
        del st.session_state.results
    with st.spinner("Analyzing..."):
        profile = build_user_profile(st.session_state.movies)
        result = predict_movie(predict_input, profile)
    if result is None:
        st.error("Something went wrong. Please try again.")
    else:
        st.title(predict_input.upper())
        if result.get('Poster'):
            st.image(f"https://image.tmdb.org/t/p/w500{result['Poster']}", width=300)
        st.write(f"**Similarity:** {result['similarity']:.2f}")
        st.write(result['explanation'])

if find_movies:
    try:
        with st.spinner("Converting language..."):
            lang_code = get_language_code(language_input)
        with st.spinner("Fetching candidate movies..."):
            candidates = get_candidate_movies(lang_code, min_rating, include_adult, st.session_state.page_offset)
            st.session_state.page_offset += PAGES_TO_SCAN
        with st.spinner("Building your taste profile..."):
            profile = build_user_profile(st.session_state.movies)
        with st.spinner("Finding similar movies..."):
            results = find_similar_movies(profile, candidates, st.session_state.movies, 5)
            st.session_state.results = results
    except Exception as e:
        st.error(str(e))

if "results" in st.session_state:
    for title, info in st.session_state.results.items():
        st.subheader(title)
        if info.get('Poster'):
            st.image(f"https://image.tmdb.org/t/p/w500{info['Poster']}", width=300)
        st.write(f"⭐ {info['Rating']}")
        st.write(info['Overview'])
        st.divider()
    if st.button("Show More"):
        try:
            with st.spinner("Fetching more movies..."):
                lang_code = get_language_code(language_input)
                candidates = get_candidate_movies(lang_code, min_rating, include_adult, st.session_state.page_offset)
                profile = build_user_profile(st.session_state.movies)
                new_results = find_similar_movies(profile, candidates, st.session_state.movies, 5)
                st.session_state.results.update(new_results)
                st.session_state.page_offset += PAGES_TO_SCAN
        except Exception as e:
            st.error(str(e))