import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Moive Recommendation System')

#movies_list = pickle.load(open('movies.pkl', 'rb'))
#movies_list = movies_list['title'].values



##option = st.selectbox(
##     'How would you like to be contacted?',
##     ('Email', 'Home phone', 'Mobile phone'))

#option = st.selectbox(
#    'How would you like to be contacted?',
#   movies_list)


movies_dict = pickle.load(open('moviedict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

option = st.selectbox(
     'How would you like to be contacted?',
movies['title'].values)

# option will have the movie name selected by the user

selected_movie_name = option


similarity = pickle.load(open('similarity.pkl', 'rb'))


# to hit API, we need a library called requests
# inside requests, we have get, inside wchich we have to give url
def fetch_poster(movie_id) :
     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
     #convert response to json
     data = response.json()
     #st.text(data)
     #st.text('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
     #print(data)
     #return data['poster_path']  # this is not the complete path
     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommend(movie_name) :
     movie_index = movies[movies['title'] == movie_name].index[0]
     distances = similarity[movie_index]
     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
     recommend_movies = []
     recommend_movies_poster = []
     for i in movies_list:
          #print(movies.iloc[i[0]].title)  # add this line after reading the below cod, to give the names of the movies, instead of indexes
          movie_id = movies.iloc[i[0]].movie_id;


          recommend_movies.append(movies.iloc[i[0]].title);

          # fetch poster from API
          recommend_movies_poster.append(fetch_poster(movie_id));

     return recommend_movies, recommend_movies_poster

#if st.button('Recommend'):
#     recommendations = recommend(selected_movie_name)
#     for i in recommendations :
#          st.write(i)

# to show both names and postersm we use layout your app

if st.button('Recommend'):
     recommendations_names, recommendations_posters = recommend(selected_movie_name)
     col1, col2, col3, col4, col5 = st.columns(5)

     with col1:
          st.text(recommendations_names[0])
          st.image(recommendations_posters[0])
     with col2:
          st.text(recommendations_names[1])
          st.image(recommendations_posters[1])
     with col3:
          st.text(recommendations_names[2])
          st.image(recommendations_posters[2])
     with col4:
          st.text(recommendations_names[3])
          st.image(recommendations_posters[3])
     with col5:
          st.text(recommendations_names[4])  # can use st.header but it will show bigger text
          st.image(recommendations_posters[4])

# for poster of movies
# when we recommend movies