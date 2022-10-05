from keras.models import load_model
import numpy as np

"""Un script qui demande à l'utilisateur d'entrer les données concernant une 
musique et réalise une prédiction en utilisant l'IA précédemment entraînée"""

ia_model = load_model("IA_model.h5")
keep_up = True

print("Hi!")

while keep_up:
    input_vector = []
    print("Enter the values associated with your song:")
    input_vector.append(float(input("song's popularity: ")))

    input_vector.append(float(input("acousticness: ")))
    input_vector.append(float(input("artists' popularity: ")))
    input_vector.append(float(input("danceability: ")))
    input_vector.append(float(input("duration in ms: ")))
    input_vector.append(float(input("energy: ")))
    input_vector.append(float(input("explicit: ")))
    input_vector.append(float(input("genres' popularity: ")))
    input_vector.append(float(input("instrumentalness: ")))
    input_vector.append(float(input("key: ")))
    input_vector.append(float(input("liveness: ")))
    input_vector.append(float(input("loudness: ")))
    input_vector.append(float(input("mode: ")))
    input_vector.append(float(input("speechiness: ")))
    input_vector.append(float(input("tempo: ")))
    input_vector.append(float(input("valence: ")))
    input_vector.append(float(input("release year: ")))
    input_vector.append(float(input("year's popularity: ")))


    prediction = ia_model.predict(np.array([input_vector]))
    
    if prediction[0][0] == 1: print("Top 50!")
    else: print("Cette musique ne sera pas un hit...")
    print(f"Valeurs en sortie de l'IA: {prediction}")
    
    keep_up = input("Faire une autre prédiction? (y/n)")
    if keep_up == "n": keep_up = False
