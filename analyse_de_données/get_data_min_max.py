import sqlite3

"""Ce fichier contient une fonction qui permet de calculer les valeurs minimum
et maximum dans une table de données. Ces valeurs seront ensuite utilisées pour 
faire des analyses de données et savoir s'il faut ou non normaliser certaines
colonnes."""


def get_min_and_max(tablename):
    

    try:
        columns_min_max = {}

        # 1 - Connexion à la base de données sqlite
        conn = sqlite3.connect("Sources_data.db")
        
        # 2 - Création du cursor qui permettra d'effectuer des requêtes sql
        cur = conn.cursor()
        cur2 = conn.cursor()

        print("START....")

        # 3 - Création de la requête pour récupérer les headers des colonnes
        musics_data = f"PRAGMA table_info({tablename})"
    
        # 4 - execution de la requête 
        cur.execute(musics_data)
        
        # 5 - recupération de la réponse
        res = cur.fetchall()
        liste_headers = []
        cpt = 0

        # 6 - parcours de la liste + affichage des chansons
        
        
        for col in res:
            liste_headers.append(col[1])
            columns_min_max[col[1]]=()

        # 7 - On stocke dans le dictionnaire columns_min_max les valeurs minimum
        # et maximum de chaque colonne (pour les valeurs numériques)
        for header in liste_headers:

            req = f"SELECT {header} FROM {tablename}"
            

            content = [cell[0] for cell in cur2.execute(req)]
            while cpt < len(content):
                if (not type(content[cpt]) in (int,str,float)) or (not content[cpt]):
                    content.pop(cpt)
                cpt+=1
            
            minimum = min(content)
            maximum = max(content)

            columns_min_max[header] = (" min : " + str(minimum),  "max : " +  str(maximum))
        for h in columns_min_max : print(h, columns_min_max[h])
        # 8 - fermeture du cursor et de la bdd pour éviter les conflits
        cur.close()
        conn.close()
        print("....END")

    except sqlite3.Error as error:
        print("Erreur lors de la connexion à SQLite", error)

get_min_and_max("artistes")