import pickle
import string
import pandas as pd

def make_vocabulary_list():

    """Rassemble tous les mots des colonnes name, artists et artists genres dans
    une liste (chaque mot est unique) et l'enregistre dans un fichier Pickle"""

    filepath = "clean_data01.csv"
    df = pd.read_csv(filepath)

    vocabulary_list = []
    columns_with_text = []

    columns_with_text.append(df["name"])
    columns_with_text.append(df["artists"])
    columns_with_text.append(df["artists genres"])

    values_processed = 0

    for column in columns_with_text:

        print("Processing a new column...")
        for value in column:
            string_without_punctuation = str(value).translate(str.maketrans("", "", string.punctuation))
            words = string_without_punctuation.split()

            for w in words:
                if w in ("", " "): continue
                if str(w).lower() not in vocabulary_list: vocabulary_list.append(str(w).lower())
            values_processed += 1
            if values_processed%10000 == 0 : print(f"{values_processed} processed")

        print("Done")

    print(f"{len(vocabulary_list)} words saved")
    print("Sample:")
    cpt = 0
    while cpt < 50:
        print(vocabulary_list[cpt])
        cpt += 1
    with open("vocabulary_list.pkl", "wb") as voc_file: pickle.dump(vocabulary_list, voc_file)
    print("Done!")

def prepare_training_set():

    """Prépare une liste qui contient des tuples de cette forme : (vecteur
    d'entrée, valeur de sortie) et stocke le résultat dans un fichier Pickle"""

    voc = pickle.load("vocabulary_list.pkl")

    training_set = []
    filepath = "clean_data01.csv"
    df = pd.read_csv(filepath)

    for index, row in df.iterrows():
        ...

    for line in

make_vocabulary_list()
