import streamlit as st
import pickle
import pandas as pd
import requests
st.markdown(
    """
    <style>
    .stApp {
        background-color: #6a0dad; /* Deep purple */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# @st.cache_resource
@st.cache(allow_output_mutation=True)
def load_pickle_from_url(url):
    response = requests.get(url)
    return pickle.loads(response.content)


dict_url = "https://huggingface.co/datasets/medha28/movie_recommender_files/resolve/main/movies.pkl"
sim_url = "https://huggingface.co/datasets/medha28/movie_recommender_files/resolve/main/similarity.pkl"

movies_dict = load_pickle_from_url(dict_url)
similarity = load_pickle_from_url(sim_url)



def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2526febf427e18fa30bbb4c76131002b&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']

def recommend(movie):
    movie_index= movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse= True, key=lambda x: x[1])[1:6]
    recommend_movies= []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_poster
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')
selected_movie = st.selectbox('Select the movies', movies['title'].values)

if st.button('Recommend'):
   names, posters = recommend(selected_movie)
   st.subheader("🎬 Top 5 Recommendations")
   col1, col2, col3, col4, col5 =  st.columns(5)
   cols = st.columns(5)
   for idx, col in enumerate(cols):
       with col:
           st.markdown(f"**{names[idx]}**")
           st.image(posters[idx], use_column_width=True)


