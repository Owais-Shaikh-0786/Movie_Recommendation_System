import requests
import streamlit as st
import pickle
import pandas as pd


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=72e610e123c2422f74a4178c3d426b5e'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie, movies_df):
    movie_lower = movie.lower()
    movie_indices = movies_df[movies_df['title'].str.lower() == movie_lower].index
    if len(movie_indices) > 0:
        movie_index = movie_indices[0]
        movie_list = sorted(enumerate(similarity[movie_index]), key=lambda x: x[1], reverse=True)[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for j in movie_list:
            movie_id = movies_df.iloc[j[0]].movie_id
            recommended_movies.append(movies_df.iloc[j[0]].title.capitalize())
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    else:
        return ["Movie not found."]


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


# Increase the font size for the title
st.markdown('<h1 style="font-size:36px;">Movie Recommender System</h1>', unsafe_allow_html=True)

selected_movie_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend'):
    names, poster = recommend(selected_movie_name, movies)
    cols = st.columns(5)
    for i in range(len(names)):
        with cols[i % 5]:
            # Adjust the font size for the subheader
            st.markdown(names[i])

            # Adjust the image display size
            st.image(poster[i])
