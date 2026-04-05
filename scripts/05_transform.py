print("hello world")
import pandas as pd
import os
import google.generativeai as genai
import PIL.Image
import time

# --- 1. CONFIGURATION ---
# REMPLACE BIEN ICI PAR TA CLÉ ENTRE LES GUILLEMETS
API_KEY = 'AIzaSyBMn1bJL1onDWG1a0aVa8OqdYUCOvwrLBI'

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

INPUT_PATH = "data/processed/filtered_elysee.csv"
OUTPUT_PATH = "data/processed/transformed_elysee.csv"
IMG_DIR = "data/raw/images/"
TXT_DIR = "data/raw/texts/"

# --- 2. FONCTIONS DE DIAGNOSTIC ---

def ask_gemini_vision(img_path):
    """Analyse l'image avec gestion d'erreur détaillée."""
    if not os.path.exists(img_path):
        return f"Manquant: {os.path.basename(img_path)}"
    
    try:
        img = PIL.Image.open(img_path)
        # Prompt court pour économiser les tokens
        prompt = "Réponds par un seul mot : 'Industrialisé' (déco hôtel) ou 'Personnel' (déco habitée)."
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        # Affiche l'erreur réelle (Quota, API Key, etc.)
        return f"Erreur API: {str(e)[:50]}"

def ask_gemini_text(txt_path):
    """Analyse les commentaires avec gestion d'erreur détaillée."""
    if not os.path.exists(txt_path):
        return "Aucun avis"
    
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()[:1000] # On limite le texte pour la rapidité
        
        prompt = f"Analyse ces avis : {content}. Réponds par un seul mot : 'Professionnel' ou 'Humain'."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Erreur API: {str(e)[:50]}"

# --- 3. BOUCLE PRINCIPALE ---

def run_transform():
    print("--- 🪄 PHASE 05 : ENRICHISSEMENT IA (TRANSFORM) ---")
    
    if not os.path.exists(INPUT_PATH):
        print(f"❌ Erreur : Fichier {INPUT_PATH} non trouvé. Lance le script 04 d'abord.")
        return

    df = pd.read_csv(INPUT_PATH)

    # --- TEST DE SÉCURITÉ ---
    # On commence par les 5 premières lignes pour valider que ça marche
    # Une fois que ça marche, tu peux mettre : df_final = df.copy()
    print("NB: Test sur les 5 premières lignes pour valider la clé API...")
    df_final = df.head(5).copy() 

    std_scores = []
    impact_scores = []

    print(f"Lancement de l'analyse sur {len(df_final)} annonces...")

    for idx, row in df_final.iterrows():
        # On s'assure que l'ID est un entier propre pour le nom du fichier
        listing_id = str(int(row['id']))
        
        # A. Appel Vision
        img_file = os.path.join(IMG_DIR, f"{listing_id}.jpg")
        res_v = ask_gemini_vision(img_file)
        
        # B. Appel NLP
        txt_file = os.path.join(TXT_DIR, f"{listing_id}.txt")
        res_t = ask_gemini_text(txt_file)
        
        std_scores.append(res_v)
        impact_scores.append(res_t)
        
        print(f"📍 ID {listing_id} | Vision: {res_v} | Texte: {res_t}")
        
        # Pause de sécurité pour le quota gratuit (15 requêtes/min max environ)
        time.sleep(3) 

    # Ajout des colonnes
    df_final['Standardization_Score'] = std_scores
    df_final['Neighborhood_Impact'] = impact_scores

    # Sauvegarde
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_final.to_csv(OUTPUT_PATH, index=False)
    
    print("-" * 30)
    print(f"✅ Bilan : Fichier sauvegardé dans {OUTPUT_PATH}")
    

if __name__ == "__main__":
    run_transform()