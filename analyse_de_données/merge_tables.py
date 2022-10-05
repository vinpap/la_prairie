import pandas as pd
import sqlite3

"""Le code contenu dans ce fichier rassemble toutes les données pertinentes de 
la base de données dans un fichier csv unique. Dans ce fichier, chaque ligne
correspond à une musique"""

connection = sqlite3.connect("Sources_data.db")
cursor = connection.cursor()

def retrieve_years_popularities(songs_df):
    
    """Récupère la colonne popularity de la table par_annees_o et l'intègre à 
    notre table finale. Cette colonne correspond à la popularité moyenne de 
    chaque année de sortie."""

    songs_year_popularities = []
    processed_songs = 0

    print("Retrieving songs' year popularity...")
    # Ci-dessous, on récupère l'année de chaque musique puis on va chercher la
    # popularité correspondante à cette année dans par_annees_o
    for index, row in songs_df.iterrows():
        song_year = row["release_date"]
        try:
            year_popularity = pd.read_sql_query(f"SELECT popularity from par_annees_o WHERE year = {song_year}", connection)["popularity"].iat[0]
        except IndexError: continue
        songs_year_popularities.append(year_popularity)
        processed_songs += 1
        if processed_songs % 10000 == 0: print(f"{processed_songs} songs processed")

    songs_year_popularities_df = pd.DataFrame(songs_year_popularities, columns=["year_popularity"])
    songs_df.reset_index(inplace=True, drop=True)
    songs_df = pd.concat([songs_df, songs_year_popularities_df], axis=1)

    print("Done")
    return songs_df

def retrieve_artists_data(songs_df):
    
    """Cette fonction récupère toutes les informations concernant les artistes
    pour chaque musique : nom des artistes, genres des artistes, popularité
    moyenne de ces genres, popularité et nombre de followers des artistes"""

    print("Retrieving artists' data...")
    artists_genres_list = []
    artists_followers_list = []
    artists_popularity_list = []
    genres_popularity_list = []
    processed_songs = 0

    for index, row in songs_df.iterrows():
        song_artists = row["artists"]
        artists_list = song_artists.split(",")
        if artists_list != [] :
            artists_list[0] = artists_list[0].lstrip("[").strip()
            artists_list[-1] = artists_list[-1].rstrip("]").strip()


        artists_genres = []
        nb_genres = 0
        total_genres_popularity = 0
        for a in artists_list:

            genres_mean_popularity = 0
            # Looking for the artists genres
            try:
                artist_genres = pd.read_sql_query(f"SELECT genres from par_artistes_o WHERE artists = {a}", connection)["genres"].iat[0]
            except (IndexError, pd.io.sql.DatabaseError):
                try:
                    artist_genres = pd.read_sql_query(f"SELECT genres from artistes WHERE artists = {a}", connection)["genres"].iat[0]
                except (IndexError, pd.io.sql.DatabaseError): continue

            artist_genres = artist_genres.lstrip("[")
            artist_genres = artist_genres.rstrip("]").strip()
            if artist_genres == "" : continue
            artist_genres = artist_genres.split(",")

            for i in range(len(artist_genres)):
                artist_genres[i] = artist_genres[i].strip()
                nb_genres += 1
                # Looking for the artists' genres' popularity
                pop = pd.read_sql_query(f"SELECT popularity from par_genres_o WHERE genres = {artist_genres[i]}", connection)["popularity"].iat[0]
                nb_genres += 1
                total_genres_popularity += pop
            artists_genres.extend(artist_genres)

        if nb_genres != 0: genres_mean_popularity = total_genres_popularity/nb_genres
        else: genres_mean_popularity = ""

        nb_artists = 0
        total_artists_popularity = 0

        for a in artists_list:
            # Looking for the artists mean popularity
            try:
                pop = pd.read_sql_query(f"SELECT popularity from par_artistes_o WHERE artists = {a}", connection)["popularity"].iat[0]
            except (IndexError, pd.io.sql.DatabaseError):
                try:
                    pop = pd.read_sql_query(f"SELECT popularity from artistes WHERE artists = {a}", connection)["popularity"].iat[0]
                except (IndexError, pd.io.sql.DatabaseError): continue

            total_artists_popularity += pop
            nb_artists += 1

        if nb_artists != 0: artists_mean_popularity = total_artists_popularity/nb_artists
        else: artists_mean_popularity = ""

        nb_artists = 0
        total_artists_followers = 0

        for a in artists_list:
            # On cherche la moyenne du nombre de followers des artistes
            try:
                followers = pd.read_sql_query(f"SELECT followers from par_artistes_o WHERE artists = {a}", connection)["followers"].iat[0]
            except (IndexError, pd.io.sql.DatabaseError):
                try:
                    followers = pd.read_sql_query(f"SELECT followers from artistes WHERE artists = {a}", connection)["followers"].iat[0]
                except (IndexError, pd.io.sql.DatabaseError): continue
            total_artists_followers += followers
            nb_artists += 1

        if nb_artists != 0: artists_mean_followers = total_artists_followers/nb_artists
        else: artists_mean_followers = ""

        artists_followers_list.append(str(artists_mean_followers))
        artists_popularity_list.append(str(artists_mean_popularity))
        genres_popularity_list.append(str(genres_mean_popularity))
        artists_genres_list.append(str(artists_genres))


        processed_songs += 1
        if processed_songs % 10000 == 0: print(f"{processed_songs} songs processed")


    with_headers = {"artists genres": artists_genres_list,
            "artists' popularity": artists_popularity_list,
            "artists' followers": artists_followers_list,
            "genres' popularity": genres_popularity_list}

    artists_df = pd.DataFrame(with_headers)
    songs_df.reset_index(inplace=True, drop=True)
    songs_df = pd.concat([songs_df, artists_df], axis=1)
    print("Done")
    return songs_df

def make_table():
    
    """Ici, on crée et on sauvegarde la table finale"""

    final_df = None
    # csv_filepath stocke le chemin vers le fichier où l'on souhaite enregistrer 
    # la table csv
    csv_filepath = "clean_data.csv"

    chansons_query = """SELECT id, name, valence, acousticness, danceability,
                    duration_ms, energy, explicit, instrumentalness, key,
                    liveness, loudness, mode, popularity, release_date,
                    speechiness, tempo, artists from chansons"""
    donnees_o_query = """SELECT id, name, valence, acousticness, danceability,
                    duration_ms, energy, explicit, instrumentalness, key,
                    liveness, loudness, mode, popularity, release_date,
                    speechiness, tempo, artists from donnees_o"""

    print("Retrieving base information...")
    chansons_df = pd.read_sql_query(chansons_query, connection)
    donnees_o_df = pd.read_sql_query(donnees_o_query, connection)

    # Adding data from chansons and donnees_o
    chansons_df = pd.concat([chansons_df, donnees_o_df], axis=0)
    # Truncating release dates so we only keep years
    chansons_df["release_date"] = chansons_df["release_date"].str.slice(0, 4)
    print("Done")

    chansons_df = retrieve_artists_data(chansons_df)
    chansons_df = retrieve_years_popularities(chansons_df)


    final_df = chansons_df
    print(final_df.info())

    # Saving as csv
    print(f"Saving clean data table in {csv_filepath}")
    final_df.to_csv(csv_filepath, sep=",")



make_table()
connection.close()
