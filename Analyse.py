import sqlite3
def get_min_and_max(tablename):

    try:
        dico = {}

        # 1 - Connexion à la base de données sqlite #
        conn = sqlite3.connect("Sources_data.db")
        
        # 2 - Création du cursor qui permettra d'effectuer des requêtes sql #
        cur = conn.cursor()
        cur2 = conn.cursor()

        print("START....")

        # 3 - Selection des chansons par la popularité décroissante #
        musics_data = f"PRAGMA table_info({tablename})"
    

        # 4 - execution de la requête #
        cur.execute(musics_data)
        
        # 5 - recupération de la réponse #
        res = cur.fetchall()
        liste_headers = []
        cpt = 0

        # 6 - parcours de la liste + affichage des chansons #
    
        for col in res:
            liste_headers.append(col[1])
            dico[col[1]]=()

        
        for header in liste_headers:

            req = f"SELECT {header} FROM {tablename}"
            

            content = [cell[0] for cell in cur2.execute(req)]
            print("1",len(content))
            while cpt < len(content):
                if (not type(content[cpt]) in (int,str,float)) or (not content[cpt]):
                    print("2",len(content))
                    content.pop(cpt)
                cpt+=1
            
            minimum = min(content)
            maximum = max(content)
            """
            print(header)
            print("min",minimum)
            print("max",maximum)
            """
            dico[header] = (" min : " + str(minimum),  "max : " +  str(maximum))
        for h in dico : print(h, dico[h])
        # 6 - fermeture du cursor et de la bdd pour éviter les conflits
        cur.close()
        conn.close()
        print("....END")

    except sqlite3.Error as error:
        print("Erreur lors de la connexion à SQLite", error)

get_min_and_max("artistes")