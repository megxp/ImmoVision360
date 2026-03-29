import pandas as pd
import os

# --- CONFIGURATION ---
CSV_PATH = "data/raw/tabular/listings.csv"
IMAGES_DIR = "data/raw/images/"
TEXTS_DIR = "data/raw/texts/"
TARGET_NEIGHBORHOOD = "Élysée"

def run_sanity_check():
    print("--- 🏥 BILAN DE SANTÉ DU DATA LAKE : IMMOVISION 360 ---")
    
    # 1. Chargement et comptage théorique
    if not os.path.exists(CSV_PATH):
        print(f"❌ Erreur : Fichier source {CSV_PATH} introuvable.")
        return

    df = pd.read_csv(CSV_PATH)
    
    # On filtre pour l'Élysée comme dans le script 01 pour être cohérent
    df_elysee = df[df['neighbourhood_cleansed'] == TARGET_NEIGHBORHOOD]
    expected_ids = set(df_elysee['id'].astype(str))
    total_expected = len(expected_ids)

    # 2. Comptage Physique
    # On liste les fichiers sans l'extension pour comparer aux IDs
    downloaded_images = {f.replace('.jpg', '') for f in os.listdir(IMAGES_DIR) if f.endswith('.jpg')}
    downloaded_texts = {f.replace('.txt', '') for f in os.listdir(TEXTS_DIR) if f.endswith('.txt')}
    
    total_images = len(downloaded_images)
    total_texts = len(downloaded_texts)

    # 3. La Jointure Physique (Test Ultime)
    # On cherche quels IDs du CSV ne sont pas dans le dossier images
    missing_images = [id_ann for id_ann in expected_ids if id_ann not in downloaded_images]
    missing_texts = [id_ann for id_ann in expected_ids if id_ann not in downloaded_texts]

    # 4. Génération du Rapport
    completion_rate = (total_images / total_expected * 100) if total_expected > 0 else 0

    print(f"\n📊 RAPPORT D'AUDIT (Quartier : {TARGET_NEIGHBORHOOD})")
    print("-" * 40)
    print(f"✅ Annonces attendues (CSV)    : {total_expected}")
    print(f"🖼️  Images téléchargées (JPG)   : {total_images}")
    print(f"📝 Corpus textes créés (TXT)   : {total_texts}")
    print(f"📈 Taux de complétion images   : {completion_rate:.2f}%")
    print("-" * 40)

    # Liste des Orphelins
    if missing_images:
        print(f"⚠️  ALERTE : {len(missing_images)} images manquent à l'appel.")
        print(f"🔍 Top 5 des IDs orphelins : {missing_images[:5]}")
    else:
        print("🎉 Félicitations : Toutes les images attendues sont présentes !")

    if missing_texts:
        print(f"ℹ️  Note : {len(missing_texts)} annonces n'ont pas de fichier texte (souvent car aucun commentaire n'existe).")

    print("\n--- FIN DU BILAN ---")

if __name__ == "__main__":
    run_sanity_check()