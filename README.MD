# Angelia, le futur de la musique !

La société Mélomane souhaite développer une extension de leur outil (qui est aujourd'hui un plugin pour les navigateurs) afin d'aider les utilisateurs de solutions de streaming comme Spotify, Deezer ou encore Napster, à trouver les meilleurs titres pour leurs playlists.
Pour se faire, elle souhaite tout d'abord analyser les titres qui se trouvent sur la plateforme Spotify (genre principal, compositeurs, langues etc...) avant de se lancer dans un projet autour de l'intelligence articielle.
N'ayant pas de compétences IA dans leurs équipes, la société vous sollicite afin de mener à bien ce projet. Elle souhaite que **vous analysiez le jeu de données qu'elle vous fournit **(vous êtes libre sur l'analyse), ainsi que vous commenciez à créer le début d'un algorithme d'intelligence articielle qui trouve si un titre risque d'être dans le TOP 50 ou pas.

Ce projet se base sur un modèle d'IA utilisant la technique du deep learning, dans lequel les données sont analysées et nettoyées avant d'être utilisées pour entraîner l'IA.


# Jupyter :

Se trouve le fichier .ipynb contenant toute l'analyse de données 


# Python :

extract_from_csv : Ce code est fait pour trouver le minimum et le maximum dans tous les colonnes de fichier csv. permettant d'obtenir la valeur maximale et minimale des tables chansons et artistes 


get_data_min_max : "Ce fichier contient une fonction qui permet de calculer les valeurs minimum
et maximum dans une table de données. Ces valeurs seront ensuite utilisées pour 
faire des analyses de données et savoir s'il faut ou non normaliser certaines
colonnes.

merge_tables : Le code contenu dans ce fichier rassemble toutes les données pertinentes de 
la base de données dans un fichier csv unique. Dans ce fichier, chaque ligne
correspond à une musiqu

# Figures :

Dossier où se trouve toutes les données graphiques 

# ia :

angelia.py :

Un script qui demande à l'utilisateur d'entrer les données concernant une 
musique et réalise une prédiction en utilisant l'IA précédemment entraînée

prepare_training_set.py :

Les fonctions de ce fichier créent un set de données qui sera directement
utilisable par le modèle de deep-learning. Pour cela, on crée une liste
contenant deux colonnes:
- la première colonne contient les données qui seront traitées en entrée
par le modèle, sous forme d'un vecteur.
- la deuxième colonne contient la réultat attendu pour chaque paire de données.
ce résultat est stocké sous la forme d'un vecteur [1, 0] (top 50), ou [0, 1]
(pas top 50).

train_model.py :

Ce script entraîne le modèle de deep learning avec les données générées par 
prepare_script.py et affiche les métriques qui décrivent l'entraînement

# Bonne lecture !