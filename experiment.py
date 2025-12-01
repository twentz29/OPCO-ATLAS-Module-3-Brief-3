from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Input
import matplotlib.pyplot as plt
import numpy as np

# Données synthétiques
X, y = make_regression(n_samples=500, n_features=6, noise=0.1, random_state=42)
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === MODELE 1 (3 features) ===
X_train_old = X_train[:, :3]
X_test_old = X_test[:, :3]

model1 = Sequential([
    Input(shape=(3,), name='input_3f'),
    Dense(16, activation='relu', name='dense_1'),
    Dense(8, activation='relu', name='dense_2'),
    Dense(1, name='output')
])
model1.compile(optimizer='adam', loss='mse')

history1 = model1.fit(X_train_old, y_train, epochs=30, batch_size=16, validation_split=0.2, verbose=0)

# Sauvegarde du modèle complet
model1.save("model1.keras")

# Courbes d'apprentissage modèle 1
plt.figure(figsize=(10, 5))
plt.plot(history1.history['loss'], label='train_loss')
plt.plot(history1.history['val_loss'], label='val_loss')
plt.title("Modèle 1 - 3 features")
plt.xlabel("Époques")
plt.ylabel("MSE Loss")
plt.legend()
plt.grid(True)
plt.savefig("loss_model1.jpg")
plt.close()

# === MODELE 2 (6 features) ===
model2 = Sequential([
    Input(shape=(6,), name='input_6f'),
    Dense(16, activation='relu', name='dense_1'),
    Dense(8, activation='relu', name='dense_2'),
    Dense(1, name='output')
])

# Charger le modèle 1 et transférer les poids compatibles
model1_loaded = tf.keras.models.load_model("model1.keras")

for layer in model2.layers:
    try:
        old_layer = model1_loaded.get_layer(layer.name)
        layer.set_weights(old_layer.get_weights())
        print(f"✅ Poids transférés pour : {layer.name}")
    except ValueError:
        print(f"⛔ Incompatible ou nouvelle couche : {layer.name}")

model2.compile(optimizer='adam', loss='mse')

# Entraînement du modèle avec les 6 features
history2 = model2.fit(X_train, y_train, epochs=30, batch_size=16, validation_split=0.2, verbose=0)

# Courbes d'apprentissage modèle 2
plt.figure(figsize=(10, 5))
plt.plot(history2.history['loss'], label='train_loss')
plt.plot(history2.history['val_loss'], label='val_loss')
plt.title("Modèle 2 - 6 features (avec transfert)")
plt.xlabel("Époques")
plt.ylabel("MSE Loss")
plt.legend()
plt.grid(True)
plt.savefig("loss_model2.jpg")
plt.close()
