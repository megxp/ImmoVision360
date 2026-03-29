import pandas as pd
import os
import re

# --- CONFIGURATION ---
INPUT_CSV = "data/raw/tabular/reviews.csv"
OUTPUT_DIR = "data/raw/texts/"

def clean_html(text):
    """Supprime les balises HTML simples et nettoie les espaces."""
    if not isinstance(text, str):
        return ""
    # Supprime <br/>, <p>, <div> etc.
    clean = re.sub(r'<.*?>', '', text)
    # Nettoie les sauts de ligne multiples et espaces superflus
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def ingest_texts(overwrite=False):
    if not os.path.exists(INPUT_CSV):
        print(f"Erreur : {INPUT_CSV} introuvable.")
        return

    print("Chargement des commentaires... (cela peut prendre un instant)")
    try:
        # On ne charge que les colonnes nécessaires pour économiser la RAM
        # On force listing_id en string pour éviter les problèmes de virgules/points
        df = pd.read_csv(INPUT_CSV, usecols=['listing_id', 'comments'], dtype={'listing_id': str})
    except Exception as e:
        print(f"Erreur critique lors de la lecture du CSV : {e}")
        return

    # Supprimer les lignes sans commentaire (données corrompues)
    df = df.dropna(subset=['comments'])

    # 1. Regroupement par annonce (listing_id)
    # On groupe tous les commentaires d'un même ID dans une liste
    print("Regroupement des commentaires par ID...")
    grouped = df.groupby('listing_id')['comments'].apply(list)

    print(f"Traitement de {len(grouped)} annonces distinctes...")

    success_count = 0
    skip_count = 0
    error_count = 0

    # 2. Boucle de création des fichiers
    for listing_id, comments_list in grouped.items():
        filename = f"{listing_id}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # --- Idempotence ---
        if os.path.exists(filepath) and not overwrite:
            skip_count += 1
            continue

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                # En-tête structuré
                f.write(f"Commentaires pour l'annonce {listing_id}:\n")
                f.write("="*40 + "\n")
                
                # 3. Nettoyage et Écriture sous forme de liste à puces
                for comment in comments_list:
                    cleaned_comment = clean_html(comment)
                    if cleaned_comment: # On n'écrit que si le texte n'est pas vide après nettoyage
                        f.write(f"* {cleaned_comment}\n")
            
            success_count += 1
        except Exception as e:
            # --- Robustesse : On loggue l'erreur et on continue ---
            print(f"Erreur sur l'ID {listing_id}: {e}")
            error_count += 1

    print("-" * 30)
    print(f"Fin de l'ingestion texte.")
    print(f"Fichiers créés/mis à jour : {success_count}")
    print(f"Fichiers ignorés (déjà existants) : {skip_count}")
    print(f"Erreurs rencontrées : {error_count}")

if __name__ == "__main__":
    # S'assurer que le dossier de destination existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Paramètre : mettre à True pour forcer la réécriture de tous les fichiers
    ingest_texts(overwrite=False)