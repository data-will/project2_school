import streamlit as st
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from streamlit_option_menu import option_menu
from fuzzywuzzy import fuzz
from sklearn.neighbors import NearestNeighbors
from datetime import datetime
import locale
from cachetools import cached, TTLCache

# cache de 1h pour améliorer les perfs de l'api
cache = TTLCache(maxsize=100, ttl=3600)



# fonction pour api tmdb
@cached(cache)
def get_movie_info(title):
    api_key = '7870f5a9017c0c9f2f46377646b75a64'
    base_url = 'https://api.themoviedb.org/3'
    search_url = f"{base_url}/search/movie?api_key={api_key}&query={title}&language=fr-FR"
    response = requests.get(search_url).json()
    
    if response['results']:
        movie_id = response['results'][0]['id']
        movie_details_url = f"{base_url}/movie/{movie_id}?api_key={api_key}&append_to_response=videos&language=fr-FR"
        movie_details = requests.get(movie_details_url).json()
        genres = ", ".join([genre['name'] for genre in movie_details['genres']])
        movie_details['genres'] = genres
        return movie_details
    else:
        return None

# fonction Will similar movie avec fuzz
def find_similar_movie(movie_name, df_filtre):
    max_similarity = -2
    most_similar_movie = None
    for movie in df_filtre['titre_du_film']:
        similarity = fuzz.ratio(movie_name.lower(), movie.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_movie = movie
    return most_similar_movie

# fonction de recommandation de Will pour films avec weight
def recommandation(film, df_ml):
    df_filtre = df_ml.groupby('titre_du_film').first().reset_index()   # groupby.first permet de garder seulement la première ligne quand il y a doublon d'id.
    
    X = df_filtre.select_dtypes(include='number').drop(['birthYear', 'deathYear', 'month', 'year', 'actor', 'actress', 'director', 'producer', 'writer'], axis=1, errors='ignore')
    
    weights = X.drop(['budget', 'popularity', 'revenue', 'vote_count', 'durée_du_film', 'moyenne_vote'], axis=1)
    
    weights *= 2
    
    X_weighted = pd.concat([X[['budget', 'popularity', 'revenue', 'vote_count', 'durée_du_film', 'moyenne_vote']], weights], axis=1)
    
    distanceKNN = NearestNeighbors(n_neighbors=5).fit(X_weighted)
    
    corrected_movie_name = find_similar_movie(film, df_filtre)
    
    st.write("Film recherché :", corrected_movie_name)
    
    user_df = df_filtre.loc[df_filtre['titre_du_film'] == corrected_movie_name, X.columns]
    
    distance, indices = distanceKNN.kneighbors(user_df)
    
    recommended_movies = []
    for idx in indices[0][1:]:
        recommended_movies.append(df_filtre.iloc[idx]['titre_du_film'])
    return recommended_movies

import pandas as pd
from sklearn.neighbors import NearestNeighbors



# csv
df_ml = pd.read_csv('C:\\Users\\33660\\Desktop\\PROJET 2\\df_ml.csv')
st.set_page_config(page_title="G4Cinema", layout="wide")

# logo
st.markdown(f'<div id="logo-container" style="display: flex; justify-content: center; margin-bottom: 20px;"><img src="https://i.ibb.co/DpcPy4T/G4-Cinema-V2.png" alt="G4 Cinema Logo" width="200"></div>', unsafe_allow_html=True)

#style css 
background1 = '''
<style>
.stApp {
    background-image: url("https://i.ibb.co/D9QfmJt/CineG42.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
.stApp .main .block-container {
    background-color: rgba(0, 0, 0, 0.9);  /* Fond semi-transparent */
    padding: 10px;  
    border-radius: 10px;  
}
.stApp .sidebar .sidebar-content {
    background-color: rgba(0, 0, 0, 0.6);  
    border-radius: 10px;
    padding: 10px;
}
</style>
'''
st.markdown(background1, unsafe_allow_html=True)
#son demarrage du streamlit
st.markdown("""
    <audio autoplay>
        <source src="https://jmp.sh/s/uM8lCruZFMosOjR0lh3d" type="audio/wav"></audio>
    """, unsafe_allow_html=True)

#dates fr
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

#



# menu
selected = option_menu(
    menu_title=None,
    options=["Accueil", "Par Acteur", "Par Réal.", "Prochainement", "Films Rétro", "Animation"],
    icons=["house", "star", "camera-reels", "clock", "film", "emoji-smile"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#262730"},
        "icon": {"color": "#cb9c5e", "font-size": "25px", "display": "inline-block", "vertical-align": "middle"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px", "--hover-color": "#4C4C4C", "display": "inline-flex", "align-items": "center", "justify-content": "flex-start"},
        "nav-link-selected": {"background-color": "#4C4C4C"},
        "nav-link-text": {"margin-left": "5px", "vertical-align": "middle"}
    },
)

# fonction film en colonnes
def moviesColumns(movies):
    num_cols = 4
    cols = st.columns(num_cols)
    for idx, movie in enumerate(movies):
        with cols[idx % num_cols]:
            st.image(movie['poster'], width=200)
            st.markdown(f"<h2 style='font-weight: bold;'>{movie['title']}</h2>", unsafe_allow_html=True)
            st.write(f"**Durée :** {movie['runtime']} minutes")
            st.write(f"**Note :** {movie['vote_average']} / 10")
            st.write(f"**Genres :** {movie['genres']}")
            st.write(movie['overview'])
            if 'trailer' in movie:
                st.video(movie['trailer'])




# Onglet Accueil
if selected == "Accueil":
    st.header("Mentionnez un film que vous avez aimé, et nous vous proposerons une recommandation adaptée !")
    film = st.text_input("Entrez le nom d'un film :")
    
    if st.button("Recommander"):
        if film:
            recommendations = recommandation(film, df_ml)
            movies_to_display = []
            for movie in recommendations:
                movie_info = get_movie_info(movie)
                if movie_info:
                    movie_dict = {
                        'title': movie_info['title'],
                        'poster': f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}",
                        'overview': movie_info.get('overview', 'Pas de synopsis disponible.'),
                        'runtime': movie_info.get('runtime', 'N/A'),
                        'vote_average': round(movie_info.get('vote_average', 0), 1),
                        'genres': movie_info.get('genres', 'N/A')
                    }
                    for video in movie_info['videos']['results']:
                        if video['type'] == 'Trailer':
                            movie_dict['trailer'] = f"https://www.youtube.com/watch?v={video['key']}"
                    movies_to_display.append(movie_dict)
            moviesColumns(movies_to_display)
        else:
            st.write("Veuillez entrer un titre de film.")

# Code pour l'onglet "Par Acteur"
elif selected == "Par Acteur":
    st.header("Vous avez un acteur fétiche ? Ça tombe bien, on peut vous aider !")
    
    # Champ de texte pour entrer le nom d'un acteur
    actor_name = st.text_input("Entrez le nom d'un acteur :")
    
    # Bouton pour lancer la recherche
    if st.button("Rechercher par acteur"):
        if actor_name:
            # Filtrer les films par nom d'acteur
            filtered_films = df_ml[df_ml['primaryName'].str.contains(actor_name, case=False, na=False)]
            if not filtered_films.empty:
                # Liste pour stocker les informations des films à afficher
                movies_to_display = []
                for index, row in filtered_films.iterrows():
                    # Obtenir les informations du film
                    movie_info = get_movie_info(row['titre_du_film'])
                    # Stocker les informations du film dans un dictionnaire
                    movie_dict = {
                        'title': movie_info['title'],
                        'poster': f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}",
                        'overview': movie_info.get('overview', 'Pas de synopsis disponible.'),
                        'runtime': movie_info.get('runtime', 'N/A'),
                        'vote_average': round(movie_info.get('vote_average', 0), 1),
                        'genres': movie_info.get('genres', 'N/A')
                    }
                    # Ajouter le lien de la bande-annonce si disponible
                    for video in movie_info['videos']['results']:
                        if video['type'] == 'Trailer':
                            movie_dict['trailer'] = f"https://www.youtube.com/watch?v={video['key']}"
                    # Ajouter le dictionnaire à la liste des films à afficher
                    movies_to_display.append(movie_dict)
                # Appeler la fonction pour afficher les films
                moviesColumns(movies_to_display)
            else:
                # Message si aucun film n'est trouvé pour l'acteur
                st.write("Aucun film trouvé pour cet acteur.")
        else:
            # Message si le champ de texte est vide
            st.write("Veuillez entrer le nom d'un acteur.")
            
# Onglet realisateur

elif selected == "Par Réal.":
    st.header("Vous avez un réalisateur dont vous appréciez le style ? Aucun souci, nous avons ce qu'il vous faut")
    director_name = st.text_input("Entrez le nom d'un réalisateur :")
    
    if st.button("Rechercher par réalisateur"):
        if director_name:
            filtered_films = df_ml[df_ml['primaryName'].str.contains(director_name, case=False, na=False)]
            if not filtered_films.empty:
                movies_to_display = []
                for index, row in filtered_films.iterrows():
                    movie_info = get_movie_info(row['titre_du_film'])
                    if movie_info:
                        movie_dict = {
                            'title': movie_info['title'],
                            'poster': f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}",
                            'overview': movie_info.get('overview', 'Pas de synopsis disponible.'),
                            'runtime': movie_info.get('runtime', 'N/A'),
                            'vote_average': round(movie_info.get('vote_average', 0), 1),
                            'genres': movie_info.get('genres', 'N/A')
                        }
                        for video in movie_info['videos']['results']:
                            if video['type'] == 'Trailer':
                                movie_dict['trailer'] = f"https://www.youtube.com/watch?v={video['key']}"
                        movies_to_display.append(movie_dict)
                moviesColumns(movies_to_display)
            else:
                st.write("Aucun film trouvé pour ce réalisateur.")
        else:
            st.write("Entrer le nom d'un réalisateur.")


# Onglet prochainement
if selected == "Prochainement":
    st.header("Retrouvez les films qui feront l'actu prochainement dans les salles obscures!")

    # Convertir les colonnes year et month en datetime
    df_films = pd.read_csv('C:\\Users\\33660\\Desktop\\PROJET 2\\df_ml.csv')
    df_filtre = df_films.groupby('titre_du_film').first().reset_index()
    df_filtre['release_date'] = pd.to_datetime(df_filtre[['year', 'month']].assign(day=1), errors='coerce')

    #trouver les films avec datetime
    today = datetime.today()
    upcoming_films = df_filtre[df_filtre['release_date'] > today]

    # trier les films
    upcoming_films = upcoming_films.sort_values(by='release_date').head(10)

    # grouper les films
    upcoming_films['year_month'] = upcoming_films['release_date'].dt.strftime('%Y-%m')
    grouped_films = upcoming_films.groupby('year_month')

    # Afficher les films à venir
    if not upcoming_films.empty:
        for group, data in grouped_films:
            year, month = group.split('-')
            month_name = datetime.strptime(month, "%m").strftime("%B")
            st.markdown(f"""
            <div style='border: 2px solid #cb9c5e; padding: 10px; margin: 10px 0; text-align: center;'>
                <h2 style='color: #cb9c5e;'>{month_name} {year}</h2>
            </div>
            """, unsafe_allow_html=True)


            movies_to_display = []
            for index, row in data.iterrows():
                movie_info = get_movie_info(row['titre_du_film'])
                if movie_info:
                    movie_dict = {
                        'title': movie_info['title'],
                        'poster': f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}",
                        'overview': movie_info.get('overview', 'Pas de synopsis disponible.'),
                        'runtime': movie_info.get('runtime', 'N/A'),
                        'vote_average': round(movie_info.get('vote_average', 0), 1),
                        'genres': movie_info.get('genres', 'N/A')
                    }
                    for video in movie_info['videos']['results']:
                        if video['type'] == 'Trailer':
                            movie_dict['trailer'] = f"https://www.youtube.com/watch?v={video['key']}"
                    movies_to_display.append(movie_dict)
            moviesColumns(movies_to_display)





# Onglet film retro
elif selected == "Films Rétro":
    st.header("Ces classiques intemporels pourraient captiver votre intérêt !")
    df_filtre = df_ml.groupby('titre_du_film').first().reset_index()
    df_filtre['year'] = pd.to_numeric(df_filtre['year'], errors='coerce')
    df_filtre['decade'] = (df_filtre['year'] // 10) * 10
    decades = [1950, 1960, 1970, 1980]
    selected_decade = st.selectbox("Sélectionnez une décennie", decades)

    st.title(f"Top 4 des films les plus populaires de {selected_decade} à {selected_decade + 9}")

    start_year = selected_decade
    end_year = selected_decade + 9

    df_decade = df_filtre[(df_filtre['year'] >= start_year) & (df_filtre['year'] <= end_year)]
    top_films = df_decade.sort_values(by='budget', ascending=False).head(4)
    
    if not top_films.empty:
        movies_to_display = []
        for index, row in top_films.iterrows():
            movie_info = get_movie_info(row['titre_du_film'])
            if movie_info:
                movie_dict = {
                    'title': movie_info['title'],
                    'poster': f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}",
                    'overview': movie_info.get('overview', 'Pas de synopsis disponible.'),
                    'runtime': movie_info.get('runtime', 'N/A'),
                    'vote_average': round(movie_info.get('vote_average', 0), 1),
                    'genres': movie_info.get('genres', 'N/A')
                }
                for video in movie_info['videos']['results']:
                    if video['type'] == 'Trailer':
                        movie_dict['trailer'] = f"https://www.youtube.com/watch?v={video['key']}"
                movies_to_display.append(movie_dict)
        moviesColumns(movies_to_display)
    else:
        st.write(f"Aucun film trouvé pour la décennie {start_year} à {end_year}.")


# Onglet Animation
elif selected == "Animation":
    st.header("Une suggestion parfaitement adaptée aux jeunes et aux amateurs d'animation !")

    # selection de films d'animation occi et jp
    occiAnim = ["Frozen", "Toy Story 4", "Coco", "Zootopia"]
    jpAnim = ["Spirited Away", "Your Name", "Mononoke", "My Neighbor Totoro"]

    selectAnim = occiAnim + jpAnim

    if selectAnim:
        movies_to_display = []
        for title in selectAnim:
            movie_info = get_movie_info(title)
            if movie_info:
                movie_dict = {
                    'title': movie_info['title'],
                    'poster': f"https://image.tmdb.org/t/p/w500{movie_info['poster_path']}",
                    'overview': movie_info.get('overview', 'Pas de synopsis disponible.'),
                    'runtime': movie_info.get('runtime', 'N/A'),
                    'vote_average': round(movie_info.get('vote_average', 0), 1),
                    'genres': movie_info.get('genres', 'N/A')
                }
                for video in movie_info['videos']['results']:
                    if video['type'] == 'Trailer':
                        movie_dict['trailer'] = f"https://www.youtube.com/watch?v={video['key']}"
                movies_to_display.append(movie_dict)
        moviesColumns(movies_to_display)