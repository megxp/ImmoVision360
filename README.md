# 🏘️ ImmoVision 360 - Phase 1 : Ingénierie du Data Lake (Zone Bronze)

## 📌 Context
Ce projet vise à construire la couche "Bronze" (Raw Data) d'un Data Lake dédié à l'analyse de la gentrification dans le quartier de l'Élysée à Paris. L'objectif est de collecter, stocker et certifier des données massives provenant d'Inside Airbnb (listings et commentaires) de manière reproductible et éthique.

## 📂 Structure du Répertoire
L'arborescence respecte les standards d'ingénierie de données pour séparer la logique (scripts) de la matière première (data) :

```text
/ImmoVision360_DataLake
├── /data
│   └── /raw
│       ├── /tabular        # Fichiers CSV sources (listings, reviews)
│       ├── /images         # Photos d'appartements (320x320 px)
│       └── /texts          # Commentaires regroupés par ID (.txt)
├── /scripts
│   ├── 00_data.ipynb       # Exploration initiale
│   ├── 01_ingestion_images.py # Scraping & Redimensionnement
│   ├── 02_ingestion_textes.py # Extraction NLP & Nettoyage HTML
│   └── 03_sanity_check.py     # Audit Qualité & Rapport
├── .gitignore              # Protection du dépôt contre les fichiers lourds
└── README.md               # Documentation technique

##Notice d'execution 

Pour reproduire ce Data Lake, suivez ces étapes :

Environnement : Créez et activez votre environnement virtuel (python -m venv myenv).

Dépendances : Installez les bibliothèques requises :
pip install pandas requests pillow tqdm

Sources : Placez listings.csv et reviews.csv dans data/raw/tabular/.

Ingestion Images : Lancez python scripts/01_ingestion_images.py (Filtre : Élysée).

Ingestion Textes : Lancez python scripts/02_ingestion_textes.py pour générer le corpus NLP.

Audit : Lancez python scripts/03_sanity_check.py pour valider l'intégrité du stockage.

##Audit des Données
📊 RAPPORT D'AUDIT (Quartier : Élysée)
----------------------------------------
✅ Annonces attendues (CSV)    : 2625
🖼️  Images téléchargées (JPG)   : 2495
📝 Corpus textes créés (TXT)   : 63893
📈 Taux de complétion images   : 95.05%
----------------------------------------
⚠️  ALERTE : 130 images manquent à l'appel.

##Analyse des pertes

Lors de l'ingestion, une déperdition mineure peut être observée entre le catalogue CSV et le stockage physique. Voici les raisons techniques identifiées :

Instabilité des URLs (404/Expired) : Les liens picture_url fournis par Airbnb sont parfois temporaires ou supprimés par l'hôte, rendant le téléchargement impossible.

Rate Limiting & Timeouts : Malgré l'usage de pauses (sleep), certains serveurs de contenu (muscache.com) peuvent rejeter des requêtes lors de micro-coupures réseau.

Absence de Commentaires : Pour les fichiers textes, le nombre peut différer des annonces car certaines nouvelles propriétés n'ont pas encore reçu d'avis clients, elles sont donc légitimement exclues du corpus NLP.g