import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ce2b1780c9ff54fee6c5449ca686d4d6')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_overviews = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=ce2b1780c9ff54fee6c5449ca686d4d6&language=en-US')
        data = response.json()
        recommended_movies.append(data['title'])
        recommended_overviews.append(data['overview'])
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_overviews, recommended_movies_posters

st.set_page_config(page_title='Movie Recommender', page_icon='🎬')

st.title('Movie Recommender System')
st.write("Discover movies similar to your favorite!")

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    st.subheader('Recommended Movies:')

    names, overviews, posters = recommend(selected_movie_name)

    # Display recommended movies in a linear list covering the whole page
    for i in range(len(names)):
        expander = st.expander(f"**{names[i]}**", expanded=False)
        expander.image(posters[i], width=150, caption=names[i])  # Adjust width as needed
        expander.write(overviews[i])

st.markdown("---")
st.write("Created by Samir Tamang")
