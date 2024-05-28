# 2ème Projet :

**Création de KPI's et d'un site de recommandation de film pour un cinéma en perte de vitesse faisant appel à nos services.**

Aucun client n’a renseigné ses préférences, nous somme dans une situation de cold start. Le client nous donne une base de données de films basée sur la plateforme IMDb (site contenant les info sur le cinéma, serie, etc...)

1) Dans un premier temps, exploration des données sur Pandas, nettoyages des données (5 tables en tout à notre disposition).
2) On garde ensuite ce qui va être utilisé pour notre recommandation de film en jointant les tables en une seule grande table unique.
3) on entraine ensuite le modèle de machine learning knn neighbors afin de ressortir 3 films recommandés.
4) Mise en code sur streamlit afin de visualiser le site.
5) Plusieurs KPI's sur power BI :
   - Analyse des Genres en corrélation avec le CA générée par genre de film à partir des années 2000 à aujourd'hui.
   - Analayse de la popularité des films en corrélation avec le CA générée par ces films.
   - Analyse du nombre de vote en corrélation avec la popularité.
   - Analyse de la durée des films dans le temps et par genre de films.
   - Analyse de la population de la creuse (rapport officiel INSEE)
   - Analyse de la répartition des spectateurs de cinéma en France en 2022 (rapport et étude du Centre National du Cinéma - CNC)


6) Visualisation du projet du Streamlit :
   - L'utilisateur entre un film qu'il a aimé et l'algorythme lui ressort 3 films recommandés du même genre.
   - l'utilisateur peut choisir un film par acteur, actrice ou réalisateur.
   - une page des films à venir au cours de l'année.
   - une page de film old school les plus populaires entre les années 1950 et 1980. Classé par tranche d'âge de 10 en 10.
  
_______________________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________________
_______________________________________________________________________________________________________________________________

# 2nd Project:

**Creation of KPI's and a film recommendation site for a cinema in decline using our services.**

No customer has provided their preferences, we are in a cold start situation. The client gives us a database of films based on the IMDb platform (site containing information on cinema, series, etc.)

1) Firstly, data exploration on Pandas, data cleaning (5 tables in total at our disposal).
2) We then keep what will be used for our movie recommendation by joining the tables into a single large table.
3) we then train the knn neighbors machine learning model in order to bring out 3 recommended films.
4) Encoding on streamlit in order to visualize the site.
5) Several KPI's on power BI:
   - Analysis of Genres in correlation with the turnover generated by film genre from the 2000s to today.
   - Analysis of the popularity of films in correlation with the turnover generated by these films.
   - Analysis of the number of votes in correlation with popularity.
   - Analysis of the duration of films over time and by film genre.
   - Analysis of the population of La Creuse (official INSEE report)
   - Analysis of the distribution of cinema spectators in France in 2022 (report and study by the National Cinema Center - CNC)


6) Visualization of the Streamlit project:
   - The user enters a film they liked and the algorithm brings up 3 recommended films of the same genre.
   - user can choose a movie by actor, actress or director.
   - a page of upcoming films during the year.
   - a page of the most popular old school films between the 1950s and 1980s. Classified by age group from 10 to 10.
