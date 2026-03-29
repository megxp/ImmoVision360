import pandas as pd
import requests
import os
import time
from PIL import Image
from io import BytesIO

# --- CONFIGURATION DES CHEMINS ---
CSV_PATH = "data/raw/tabular/listings.csv"
OUTPUT_DIR = "data/raw/images/"
TARGET_NEIGHBORHOOD = "Élysée" # Filtrage pour éviter le Big Data inutile
IMAGE_SIZE = (320, 320)        # Redimensionnement exigé
SLEEP_TIME = 0.5               # Courtoisie serveur (0.5 seconde entre chaque image)

# --- CONFIGURATION RESEAU (User-Agent) ---
# On s'identifie comme un navigateur pour éviter d'être bloqué comme un robot anonyme
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def ingest_images():
    # 1. Lecture du catalogue
    if not os.path.exists(CSV_PATH):
        print(f"Erreur : Le fichier {CSV_PATH} est introuvable.")
        return

    df = pd.read_csv(CSV_PATH)

    # 2. Filtrage (Réduction de la matière première)
    # On ne garde que le quartier de l'Élysée et les lignes avec une URL d'image
    df_filtered = df[(df['neighbourhood_cleansed'] == TARGET_NEIGHBORHOOD) & (df['picture_url'].notna())]
    
    print(f"Extraction lancée pour {len(df_filtered)} annonces dans le quartier : {TARGET_NEIGHBORHOOD}")

    # 3. Boucle d'ingestion
    for index, row in df_filtered.iterrows():
        id_annonce = str(int(row['id']))
        url_image = row['picture_url']
        filename = f"{id_annonce}.jpg"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # --- Règle d'Idempotence ---
        if os.path.exists(filepath):
            # print(f"Saut : L'image {filename} existe déjà.")
            continue

        # --- Scraping avec Gestion des Exceptions ---
        try:
            # Téléchargement
            response = requests.get(url_image, headers=HEADERS, timeout=10)
            response.raise_for_status() # Déclenche une erreur si 404 ou 500

            # Traitement de l'image (Pixels)
            img = Image.open(BytesIO(response.content))
            
            # Conversion en RGB (pour éviter les erreurs avec les formats RGBA/PNG en JPG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Redimensionnement (320*320)
            img = img.resize(IMAGE_SIZE)

            # Sauvegarde
            img.save(filepath, "JPEG")
            print(f"Succès : Image {filename} enregistrée.")

            # --- Courtoisie Serveur (Rate Limiting) ---
            time.sleep(SLEEP_TIME)

        except requests.exceptions.RequestException as e:
            print(f"Lien mort ou erreur réseau pour l'ID {id_annonce} : {e}")
        except Exception as e:
            print(f"Erreur lors du traitement de l'image {id_annonce} : {e}")

    print("Fin du processus d'ingestion.")

if __name__ == "__main__":
    # S'assurer que le dossier de destination existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ingest_images()