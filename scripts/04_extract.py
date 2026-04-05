import pandas as pd
import os

# --- CONFIGURATION ---
RAW_CSV_PATH = "data/raw/tabular/listings.csv"
PROCESSED_DIR = "data/processed/"
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "filtered_elysee.csv")
TARGET_NEIGHBORHOOD = "Élysée"

# Colonnes à garder
COLS_TO_KEEP = [
    # 1. Identifiant (La clé de jointure)
    'id', 
    
    # 2. Hypothèse Économique (Industrialisation)
    'price', 
    'property_type', 
    'room_type', 
    'availability_365', 
    'calculated_host_listings_count', # Indicateur de multipropriété
    
    # 3. Hypothèse Sociale (Gestion Pro vs Particulier)
    'host_id',
    'host_response_time', 
    'host_response_rate',
    'host_is_superhost',
    'number_of_reviews',
    
    # 4. Localisation (Validation géographique)
    'neighbourhood_cleansed',
    'latitude',
    'longitude'
]

def run_extraction():
    print(f"---  EXTRACTION STRATÉGIQUE : {TARGET_NEIGHBORHOOD} ---")
    
    if not os.path.exists(RAW_CSV_PATH):
        print(f"❌ Erreur : Source {RAW_CSV_PATH} introuvable.")
        return

    # 1. Chargement optimisé (on ne lit que les colonnes utiles pour la RAM)
    try:
        df = pd.read_csv(RAW_CSV_PATH, usecols=COLS_TO_KEEP)
    except ValueError as e:
        print(f"❌ Erreur de colonnes : {e}")
        return

    # 2. Filtrage Géographique
    print(f"Filtrage sur le quartier : {TARGET_NEIGHBORHOOD}...")
    df_filtered = df[df['neighbourhood_cleansed'] == TARGET_NEIGHBORHOOD].copy()

    # 3. Nettoyage rapide du prix (enlever le signe $ et convertir en float)
    if 'price' in df_filtered.columns:
        df_filtered['price'] = df_filtered['price'].replace('[\$,]', '', regex=True).astype(float)

    # 4. Sauvegarde Idempotente
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df_filtered.to_csv(OUTPUT_FILE, index=False)
    
    print(f"✅ Extraction terminée !")
    print(f"📍 Fichier sauvegardé : {OUTPUT_FILE}")
    print(f"📊 Volume extrait : {df_filtered.shape[0]} annonces / {df_filtered.shape[1]} colonnes.")

if __name__ == "__main__":
    run_extraction()