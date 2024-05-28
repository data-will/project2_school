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
