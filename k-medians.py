import pandas as pd
import numpy as np
import folium
import random
import re
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from sklearn.preprocessing import StandardScaler
from folium.plugins import MarkerCluster
import webbrowser

# Étape 1 : Charger le jeu de données
chemin_fichier = "Electric_Vehicle_Population_Data.csv"
df = pd.read_csv(chemin_fichier)

# Étape 2 : Nettoyage des données
# Vérifier que 'Vehicle Location' existe et n'est pas vide
df = df.dropna(subset=['Vehicle Location'])

# Fonction pour extraire la latitude et la longitude à partir du format 'POINT (long lat)'
def extraire_coordonnees(location):
    correspondance = re.search(r"POINT \((-?\d+\.\d+) (-?\d+\.\d+)\)", location)
    if correspondance:
        longitude, latitude = float(correspondance.group(1)), float(correspondance.group(2))
        return latitude, longitude
    return None, None

# Appliquer la fonction pour extraire les coordonnées
df[['Latitude', 'Longitude']] = df['Vehicle Location'].apply(lambda loc: pd.Series(extraire_coordonnees(loc)))

# Supprimer les lignes avec des valeurs manquantes pour la latitude ou la longitude
df = df.dropna(subset=['Latitude', 'Longitude'])

# Sauvegarder les données nettoyées
fichier_nettoye = "cleaned_ev_data.csv"
df.to_csv(fichier_nettoye, index=False)
print(f"✅ Données nettoyées enregistrées sous {fichier_nettoye}")

# Étape 3 : Convertir latitude et longitude en tableau NumPy
X = df[['Latitude', 'Longitude']].to_numpy()

# Normalisation des données pour le clustering
scaler = StandardScaler()
X_normalise = scaler.fit_transform(X)

# Étape 4 : Fonction de clustering K-Median
def k_median(X, k, max_iters=100, tol=1e-4):
    # Initialiser aléatoirement k médianes
    medians = X[random.sample(range(len(X)), k)]
    
    for _ in range(max_iters):
        # Calculer la distance de Manhattan jusqu'aux médianes
        distances = np.array([[np.sum(np.abs(point - median)) for median in medians] for point in X])
        mediane_plus_proche = np.argmin(distances, axis=1)
        
        # Mettre à jour les médianes
        nouvelles_medians = []
        for i in range(k):
            points_du_cluster = X[mediane_plus_proche == i]
            if len(points_du_cluster) > 0:
                nouvelles_medians.append(np.median(points_du_cluster, axis=0))
            else:
                nouvelles_medians.append(medians[i])  # Conserver l'ancienne médiane si vide
        
        nouvelles_medians = np.array(nouvelles_medians)
        
        # Vérifier la convergence
        if np.max(np.abs(nouvelles_medians - medians)) < tol:
            break
        
        medians = nouvelles_medians

    return medians, mediane_plus_proche

# **Exécuter le clustering et afficher les résultats**
def executer_clustering():
    k = int(k_dropdown.get())
    print(f"🔍 Exécution du clustering avec k = {k}...")

    # Appliquer le clustering K-Median
    medians, etiquettes_clusters = k_median(X_normalise, k)

    # Convertir les médianes à l'échelle originale
    emplacements_optimaux = scaler.inverse_transform(medians)

    # Sauvegarder les emplacements optimaux
    fichier_optimal = "optimal_ev_stations.csv"
    optimal_df = pd.DataFrame(emplacements_optimaux, columns=['Latitude', 'Longitude'])
    optimal_df.to_csv(fichier_optimal, index=False)
    print(f"📍 Emplacements optimaux des bornes de recharge enregistrés sous {fichier_optimal}")

    # **Créer une carte interactive avec Folium**
    centre_lat, centre_lon = df['Latitude'].median(), df['Longitude'].median()
    carte_ev = folium.Map(location=[centre_lat, centre_lon], zoom_start=8)
    cluster_marqueurs = MarkerCluster().add_to(carte_ev)

    # Ajouter les emplacements des véhicules électriques en bleu
    for _, ligne in df.iterrows():
        folium.CircleMarker(
            location=[ligne['Latitude'], ligne['Longitude']],
            radius=1,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacité=0.5,
        ).add_to(cluster_marqueurs)

    # Ajouter les emplacements optimaux des stations de recharge en rouge
    for lat, lon in emplacements_optimaux:
        folium.Marker(
            location=[lat, lon],
            popup=f"Station de recharge optimale\nLat: {lat:.6f}, Lon: {lon:.6f}",
            icon=folium.Icon(color="red", icon="bolt"),
        ).add_to(carte_ev)

    # Enregistrer et ouvrir la carte dans un navigateur
    carte_output = "ev_charging_map.html"
    carte_ev.save(carte_output)
    webbrowser.open(carte_output)  # Ouvrir le fichier HTML dans le navigateur par défaut

    # **Afficher le graphique du clustering**
    plt.figure(figsize=(10, 6))
    plt.scatter(X[:, 1], X[:, 0], c=etiquettes_clusters, cmap='viridis', marker='o', alpha=0.5, label="Emplacements des véhicules électriques")
    plt.scatter(emplacements_optimaux[:, 1], emplacements_optimaux[:, 0], c='red', marker='x', s=100, label="Stations optimales")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(f"Emplacements optimaux des bornes de recharge (k={k})")
    plt.legend()
    plt.show()

# **Fonction pour quitter le programme**
def quitter_programme():
    print("Fermeture du programme... 🛑")
    root.destroy()

# **Créer une interface graphique avec Tkinter**
root = tk.Tk()
root.title("Analyse des stations de recharge EV")
root.geometry("400x300")

# Titre
titre_label = tk.Label(root, text="Clustering des stations de recharge EV", font=("Arial", 14, "bold"))
titre_label.pack(pady=10)

# Menu déroulant
tk.Label(root, text="Sélectionnez le nombre de stations de recharge (k) :", font=("Arial", 11)).pack()
k_dropdown = ttk.Combobox(root, values=[3, 5, 7, 10, 15])
k_dropdown.pack()
k_dropdown.set(5)  # Valeur par défaut

# Bouton pour exécuter le clustering
bouton_executer = tk.Button(root, text="Lancer le clustering", command=executer_clustering, font=("Arial", 12), bg="green", fg="white")
bouton_executer.pack(pady=10)

# **Bouton de sortie**
bouton_sortie = tk.Button(root, text="Quitter", command=quitter_programme, font=("Arial", 12), bg="red", fg="white")
bouton_sortie.pack(pady=10)

# Lancer l'interface graphique Tkinter
root.mainloop()