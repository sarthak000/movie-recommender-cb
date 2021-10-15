import streamlit as st
import pickle
import pandas as pd
import requests


def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=5992ba032612a5765954990e52a6ff6c'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    actual_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return actual_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_posters.append(get_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies,recommended_movie_posters


movies_dict = pickle.load(open('movie_list_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Simple Content Based Movie Recommendation System')

selected_movie_name = st.selectbox('Choose movies from below or type', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie[4])
        st.image(recommended_movie_posters[4])


# add links to more information of these movies and add sentiment of reviews