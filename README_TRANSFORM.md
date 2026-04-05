# 🪄 Transformation & Enrichissement IA (Zone Silver)

Ce document détaille les opérations de nettoyage et d'enrichissement effectuées par le script `05_transform.py`.

## 1. Stratégie de Nettoyage (Data Cleaning)
Avant l'enrichissement, les données ont été normalisées :
- **Prix :** Conversion de la chaîne `$xxx.xx` en `float`.
- **Valeurs manquantes (NaN) :** - Imputation par la médiane pour les scores de revues (`review_scores_rating`).
    - Remplacement par `0` pour `reviews_per_month` (logique : pas d'avis = 0 avis/mois).
- **Outliers :** Suppression des annonces avec un prix égal à 0€.

## 2. Enrichissement Multimodal (IA Gemini)
Nous avons utilisé l'API **Google Gemini 1.5 Flash** pour extraire des signaux métier à partir des données non structurées (images et textes).

### A. Feature : Standardization Score (Vision)
- **Source :** `data/raw/images/[ID].jpg`
- **Objectif :** Détecter si le logement est "Industrialisé" (style hôtelier) ou "Personnel" (habité).
- **Mapping :** `1` (Industrialisé), `0` (Personnel), `-1` (Erreur/Autre).

### B. Feature : Neighborhood Impact (NLP)
- **Source :** `data/raw/texts/[ID].txt` (Agrégation des commentaires)
- **Objectif :** Évaluer si l'expérience voyageur est "Professionnelle" ou "Humaine".
- **Mapping :** `1` (Professionnel), `0` (Humain), `-1` (Aucun avis).

## 3. Preuve de Concept (POC)
En raison des limitations de quota de l'API gratuite (15 RPM), l'IA a été sollicitée pour un échantillon représentatif de 5 annonces afin de valider le pipeline.

**Capture d'écran du terminal (Logs de transformation) :**
![Preuve Inférence IA]((./docs/analyse_datalake.png))

> *Note : Pour le reste du dataset (2620+ lignes), des valeurs aléatoires (-1, 0, 1) ont été générées conformément aux consignes, afin de permettre l'intégration complète dans le Data Warehouse PostgreSQL sans saturation de quota.*

## 4. Schéma de sortie
Le fichier final est stocké dans : `data/processed/transformed_elysee.csv`.