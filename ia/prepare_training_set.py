import pickle
import string
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE

"""Les fonctions de ce fichier créent un set de données qui sera directement
utilisable par le modèle de deep-learning. Pour cela, on crée une liste
contenant deux colonnes:
- la première colonne contient les données qui seront traitées en entrée
par le modèle, sous forme d'un vecteur.
- la deuxième colonne contient la réultat attendu pour chaque paire de données.
ce résultat est stocké sous la forme d'un vecteur [1, 0] (top 50), ou [0, 1]
(pas top 50).

De plus, on utilise l'algorithme SMOTE pour faire du resampling. En effet, seules
50 musiques sur 500 000 sont labellisées "top 50", ce qui peut créer un
déséquilibre et affecter l'entraînement? SMOTE fait de l'augmentation de données
afin que les deux labels aient une part égale dans le set d'entraînement.
La liste générée est ensuite enregistrée avec pickle.

NOTE : les fonctions make_vocabulary et make_bag_of_words n'ont finalement pas
été utilisées pour des raisons techniques : nos ordinateurs n'ont pas la puissance
nécessaire pour vectoriser tout le texte présent dans la table en un temps 
raisonnable"""


def make_vocabulary_list():

    """Rassemble tous les mots des colonnes name, artists et artists genres dans
    une liste (chaque mot est unique) et l'enregistre dans un fichier Pickle"""

    filepath = "final_data.csv"
    df = pd.read_csv(filepath)


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

def make_bag_of_words(text, vocabulary):

    vector = []

    text = str(text).translate(str.maketrans("", "", string.punctuation))
    words = text.split()

    for w in words:
        for i in range(len(vocabulary)):
            if w.lower() == vocabulary[i].lower(): vector.append(1.0)
            else: vector.append(0.0)
    return vector

def prepare_training_set():

    """Prépare une liste qui contient deux listes (liste d'entrée, liste de sortie)
    et stocke le résultat dans un fichier Pickle"""

    training_set = []

    training_set = []
    training_set_x = []
    training_set_y = []
    filepath = "final_data.csv"
    df = pd.read_csv(filepath)

    lines_processed = 0

    for index, row in df.iterrows():

        #name_vec = make_bag_of_words(row["name"], vocabulary)
        #artists_vec = make_bag_of_words(row["artists"], vocabulary)
        #artists_genres_vec = make_bag_of_words(row["artists genres"], vocabulary)

        training_x = []
        training_y = []

        training_x.append(float(row["valence"]))
        training_x.append(float(row["acousticness"]))
        training_x.append(float(row["danceability"]))
        training_x.append(float(row["duration_ms"]))
        training_x.append(float(row["energy"]))
        training_x.append(float(row["explicit"]))
        training_x.append(float(row["instrumentalness"]))
        training_x.append(float(row["key"]))
        training_x.append(float(row["liveness"]))
        training_x.append(float(row["loudness"]))
        training_x.append(float(row["mode"]))
        training_x.append(float(row["release_date"]))
        training_x.append(float(row["speechiness"]))
        training_x.append(float(row["tempo"]))
        training_x.append(float(row["artists' popularity"]))
        training_x.append(float(row["genres' popularity"]))
        training_x.append(float(row["year_popularity"]))
        training_x.append(float(row["popularity"]))

        #training_x.extend(name_vec)
        #training_x.extend(artists_vec)
        #training_x.extend(artists_genres_vec)

        if float(row["top50"]) == 1.0: training_y = [1.0, 0.0]
        else: training_y = [0.0, 1.0]

        training_set_x.append(training_x)
        training_set_y.append(training_y)

        lines_processed += 1
        if lines_processed % 1000 == 0: print(f"{lines_processed} processed")


    print("Resampling to get the two labels in equal numbers")
    print("Shape of data before resampling:")
    training_set_x = np.array(training_set_x)
    training_set_y = np.array(training_set_y)
    print("x: ", np.shape(training_set_x))
    print("y: ", np.shape(training_set_y))
    x_resampled = []
    y_resampled = []
    
    # Le code ci-dessous resample les données en utilisant SMOTE

    x_resampled, y_resampled = SMOTE().fit_resample(training_set_x, training_set_y)
    print("Shape of data after resampling:")
    print("x: ", np.shape(x_resampled))
    print("y: ", np.shape(y_resampled))

    x_resampled = list(x_resampled)
    y_resampled = list(y_resampled)

    print(y_resampled[-1])

    for i in range(len(y_resampled)):
        if y_resampled[i][0] == 1: y_resampled[i] = np.append(y_resampled[i], 0)
        elif y_resampled[i][0] == 0: y_resampled[i] = np.append(y_resampled[i], 1)
        else: print("Error")
    print("Final shape of data:")
    print("x: ", np.shape(x_resampled))
    print("y: ", np.shape(y_resampled))
    print(y_resampled[-1])
    training_set.append(list(x_resampled))
    training_set.append(list(y_resampled))
    print("Done")
    with open("training_set.pkl", "wb") as training_set_file: pickle.dump(training_set, training_set_file)


#make_vocabulary_list()
prepare_training_set()
