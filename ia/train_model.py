
import pickle
import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

"""Ce script entraîne le modèle de deep learning avec les données générées par 
prepare_script.py et affiche les métriques qui décrivent l'entraînement."""

def plot_training(training_history):

    """Cette fonction affiche les résultats de l'entraînement (précision et loss)"""

    plt.plot(training_history.history['accuracy'])
    plt.plot(training_history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()


    plt.plot(training_history.history['loss'])
    plt.plot(training_history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

words = []
lines = []

training_set = pickle.load(open("training_set.pkl", "rb"))

train_x = training_set[0]
train_y = training_set[1]

full_list = list(zip(train_x, train_y))
random.shuffle(full_list)
train_x, train_y = zip(*full_list)

print(len(train_x))
print(len(train_x[0]))
print(len(train_y))
print(len(train_y[0]))


print("Creating neural network...")

# Crée un modèle à une couche cachée de 128 neurones
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dense(len(train_y[0]), activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=1e-3), metrics=['accuracy'])
model.summary()

print("Starting training...")
# entraînement et sauvegarde du modèle
hist = model.fit(np.array(train_x), np.array(train_y), validation_split=0.33, epochs=3, batch_size=100, verbose=1)
model.save('IA_model.h5', hist)
print("Training complete. Visualizing training data...")
plot_training(hist)
