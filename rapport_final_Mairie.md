---
title: "ImmOvision 360° Paris - Quartier Élysée"
subtitle: "Analyse exploratoire des annonces Airbnb"
author: " BEDOUME Mégane"
date: "Janvier 2025"
geometry: margin=2.5cm
fontsize: 11pt
---

# RÉSUMÉ EXÉCUTIF

**Contexte** : La Mairie de Paris souhaite comprendre les dynamiques locatives 
dans le quartier de l'Élysée pour éclairer sa politique de régulation du tourisme.

**Objectif** : Analyser 3 hypothèses concernant la transformation du quartier :
1. **Standardisation** : les logements deviennent-ils des "produits financiers" ?
2. **Déshumanisation** : le lien social est-il rompu par l'hôtellerie de masse ?
3. **Concentration** : une minorité d'acteurs contrôle-t-elle l'offre ?

**Résultats clés** :
- ✅ **Hypothèse 2 validée** : 59% des descriptions adoptent un vocabulaire "hôtelier"
- ⚠️ **Hypothèse 1 partiellement validée** : 57% de standardisation (seuil 80% non atteint)
- ⚠️ **Hypothèse 3 modérée** : 42% de l'offre contrôlée par 5% d'hôtes (concentration significative mais sous seuil 60%)

**Conclusion** : Le quartier présente des signes de professionnalisation (rupture du lien social, 
concentration mesurable) sans basculement total vers un modèle industriel.

---

\newpage

# 1. CONTEXTE ET PROBLÉMATIQUE

## 1.1 Demande de la Mairie

Le quartier de l'Élysée fait face à des tensions liées à la location de courte durée :
- Plaintes de riverains sur la transformation du voisinage
- Suspicion de concentration de l'offre entre peu d'acteurs
- Inquiétude sur la disparition du lien social

La Maire demande une analyse factuelle basée sur les données Airbnb pour :
- Quantifier le phénomène (pas seulement des impressions)
- Identifier les acteurs (particuliers vs professionnels)
- Mesurer l'impact sur le tissu social

## 1.2 Périmètre de l'étude

**Zone géographique** : Quartier Élysée (8e arrondissement, Paris)

**Source de données** : Inside Airbnb (données publiques, snapshot décembre 2024)

**Variables analysées** :
- Images (analyse IA : style "catalogue" vs "personnel")
- Textes (NLP : vocabulaire "hôtelier" vs "humain")
- Métadonnées (disponibilité, réactivité, concentration)

**Période** : Photo instantanée (pas de suivi temporel)

---

# 2. DONNÉES ET MÉTHODOLOGIE

## 2.1 Chaîne de traitement
DATA LAKE │ --> │ EXTRACTION │ --> │ TRANSFORMATION│ --> │ EDA │


### Étape 1 : Data Lake (Bronze)
- **Fichiers bruts** : `listings.csv`, images (JPG), descriptions (TXT)
- **Volumétrie** : [X] annonces initiales dans Paris
- **Qualité** : Valeurs manquantes, formats hétérogènes

### Étape 2 : Extraction (Silver)
- **Filtrage géographique** : Conservation uniquement du quartier Élysée
- **Résultat** : [Y] annonces retenues
- **Script** : `04_extract.py` (Pandas)

### Étape 3 : Transformation (Silver → Gold)
- **Analyse d'images** : Modèle IA détecte le style "industrialisé" vs "personnel"
  - Score = 1 : décoration catalogue (Ikea, murs blancs)
  - Score = 0 : traces de vie (livres, photos personnelles)
  - Score = -1 : erreur/non disponible

- **Analyse de texte** : NLP détecte le vocabulaire "hôtelier" vs "naturel"
  - Score = 1 : "code", "boîte à clés", "agence"
  - Score = 0 : "accueil", "conseils", "rencontre"
  - Score = -1 : ambigu/absent

- **Script** : `05_transform.py` (TensorFlow, spaCy)

### Étape 4 : Chargement
- **Base de données** : PostgreSQL (`immovision.elysee_tabular`)
- **Variables finales** : 8 colonnes (id, disponibilité, scores...)
- **Script** : `06_load.py` (SQLAlchemy)

## 2.2 Traitement des données manquantes

**Convention** : Toutes les valeurs NULL remplacées par **-1**

| Variable | % de -1 | Traitement |
|----------|---------|------------|
| `standardization_score` | [X]% | Exclusion pour calcul de % |
| `neighborhood_impact_score` | [X]% | Exclusion pour calcul de % |
| `host_response_rate_num` | [X]% | Affiché mais non interprété |

**Impact** : Les pourcentages sont calculés sur l'effectif **valide** (hors -1) 
pour éviter de compter les erreurs techniques comme une catégorie métier.

---

\newpage

# 3. RÉSULTATS

## 3.1 Hypothèse 1 : Standardisation → Produits financiers

### Question posée
*"Les appartements du quartier Élysée présentent-ils massivement un style 
'industrialisé' révélateur d'une transformation en produits financiers ?"*

### Résultats

![Distribution standardisation](q1_standardisation_repartition.png){ width=75% }

**Chiffres clés** (N = [X] annonces valides) :
- **57.0%** d'annonces avec décoration "industrialisée"
- **43.0%** d'annonces avec décoration "personnelle"

**Test d'hypothèse** :
- Seuil attendu : ≥80% pour valider la transformation totale
- **Verdict** : ⚠️ NON VALIDÉE (57% < 80%)

**Croisement avec type de logement** :

![Standardisation par type](q2_standardisation_par_type.png){ width=70% }

- Logements entiers : **56.9%** industrialisés
- Chambres privées : **59.7%** industrialisées
- **Écart faible** (2.8 points) → pas de différence marquée

### Interprétation

✅ **Ce que nous observons** :
- Une majorité relative (57%) adopte un style "catalogue"
- Phénomène présent mais **non écrasant**

⚠️ **Limites** :
- Le style "neutre" peut être un choix marketing, pas forcément la preuve d'un achat par investisseur
- Absence de données : statut juridique du propriétaire, date d'achat
- Facteur commun possible : Airbnb recommande la décoration neutre à tous

---

## 3.2 Hypothèse 2 : Déshumanisation → Bris du lien social

### Question posée
*"Les descriptions révèlent-elles une logique 'hôtelière' (absence d'hôte) 
plutôt qu'un partage entre habitants ?"*

### Résultats

![Analyse des textes](q3_deshumanisation_textes.png){ width=75% }

**Chiffres clés** (N = [X] annonces valides) :
- **59.1%** de descriptions "hôtelisées" (vocabulaire froid)
- **40.9%** de descriptions "naturelles" (vocabulaire humain)

**Test d'hypothèse** :
- Seuil attendu : >50% pour valider la rupture sociale
- **Verdict** : ✅ **VALIDÉE** (59.1% > 50%)

**Croisement avec multi-annonces** :

![Multi-annonceurs](q5_multi_annonceurs_hotelisation.png){ width=70% }

- Mono-annonce : **53.9%** hôtélisés
- Multi (>10 annonces) : **59.1%** hôtélisés
- **Gradient faible** (+5.2 points) mais cohérent

### Interprétation

✅ **Ce que nous observons** :
- La majorité des annonces utilisent un vocabulaire **déshumanisé**
- Mots-clés dominants : "code", "accès autonome", "géré par"
- Compatible avec l'hypothèse d'une **rupture du lien social**

⚠️ **Limites** :
- Un texte "hôtelier" ne prouve pas l'hostilité des voisins
- Facteur commun : professionnalisation → templates imposés par agences
- Pas de données sur les plaintes effectives de riverains

---

## 3.3 Hypothèse 3 : Machine à cash → Concentration

### Question posée
*"Une minorité de propriétaires (5%) contrôle-t-elle la majorité (≥60%) 
de l'offre locative ?"*

### Résultats

![Courbe de Lorenz](q4_concentration_lorenz.png){ width=80% }

**Chiffres clés** :
- **Coefficient de Gini : 0.851** (concentration élevée)
- **Top 5% des hôtes** contrôlent **41.8%** de l'offre

**Répartition** :
- Mono-annonce (= 1) : [X]% des annonces
- Multi (2-10) : [X]% des annonces
- Multi (>10) : [X]% des annonces

**Test d'hypothèse** :
- Seuil attendu : ≥60% contrôlés par 5% d'hôtes
- **Verdict** : ⚠️ NON VALIDÉE (41.8% < 60%)

### Interprétation

✅ **Ce que nous observons** :
- **Concentration significative** : 42% de l'offre entre 5% d'acteurs
- Gini élevé (0.85) confirme une **inégalité forte**
- Présence d'acteurs professionnels avec portefeuilles importants

⚠️ **Limites** :
- 42% reste élevé (4 annonces sur 10 contrôlées par une minorité)
- Absence de données **prix** → impossible de calculer les revenus concentrés
- Facteur commun : quartier touristique attire naturellement les investisseurs
- Pas de distinction juridique (particulier vs société)

---

\newpage

# 4. SYNTHÈSE ET RECOMMANDATIONS

## 4.1 Bilan des 3 hypothèses

| Hypothèse | Indicateur | Seuil | Résultat | Statut |
|-----------|-----------|-------|----------|--------|
| **1. Standardisation** | % industrialisé | ≥80% | 57.0% | ⚠️ Partiel |
| **2. Déshumanisation** | % hôtélisé | >50% | 59.1% | ✅ Validée |
| **3. Concentration** | Top 5% contrôle | ≥60% | 41.8% | ⚠️ Modérée |

### Interprétation globale

Le quartier Élysée présente des **signes nets de professionnalisation** :
- ✅ Rupture du lien social confirmée (vocabulaire déshumanisé majoritaire)
- ⚠️ Standardisation présente mais non écrasante (57%, pas 80%)
- ⚠️ Concentration significative mais pas extrême (42%, pas 60%)

**Conclusion** : Le quartier n'est **pas encore totalement transformé** en "usine à touristes", 
mais le processus est **engagé et mesurable**.

## 4.2 Limites de l'étude

### Données manquantes
- ❌ **Pas de prix** : impossible de calculer les revenus concentrés
- ❌ **Pas de temporalité** : photo instantanée, pas d'évolution dans le temps
- ❌ **Pas de statut juridique** : impossible de distinguer particulier/société

### Biais méthodologiques
- **Corrélation ≠ causalité** : les liaisons observées peuvent résulter de facteurs communs
  - Ex : professionnalisation → templates + décoration neutre
- **Échantillon** : uniquement Airbnb (pas Booking, Abritel...)
- **Algorithmes IA** : marge d'erreur non quantifiée (15-25% de scores -1)

### Généralisation
- Résultats valables pour le **quartier Élysée uniquement**
- Pas de groupe témoin (quartier résidentiel non touristique)

## 4.3 Recommandations pour la Mairie

### Actions immédiates (données disponibles)
1. **Cibler les multi-annonceurs (>10 logements)** :
   - Identifier juridiquement les acteurs
   - Vérifier la conformité réglementaire (120 jours/an max)

2. **Enquête qualitative complémentaire** :
   - Sonder les riverains sur le ressenti (nuisances, perte de lien)
   - Croiser avec les données de plaintes effectives

### Actions moyen terme (collecte de données)
3. **Enrichir avec les prix** :
   - Scraper les tarifs Airbnb pour calculer les revenus concentrés
   - Comparer avec les loyers longue durée du quartier

4. **Suivi temporel** :
   - Répéter l'analyse dans 12 mois
   - Mesurer l'évolution (aggravation ou stabilisation ?)

5. **Comparaison avec quartier témoin** :
   - Analyser un quartier résidentiel (ex : 15e arrondissement)
   - Valider que les 59% d'hôtélisation sont spécifiques à l'Élysée

---

# 5. ANNEXES

## 5.1 Méthodologie technique

**Langages** : Python 3.10, SQL (PostgreSQL 14)

**Bibliothèques** :
- Pandas, NumPy (manipulation données)
- TensorFlow/Keras (analyse images)
- spaCy (analyse texte NLP)
- Matplotlib, Seaborn (visualisations)

**Infrastructure** :
- Base PostgreSQL locale
- Pipeline ETL documenté (6 scripts Python)
- Notebook Jupyter pour EDA

## 5.2 Matrice de corrélations

![Corrélations Spearman](complementaire_correlations.png){ width=85% }

**Observations** :
- Corrélations globalement **faibles à modérées** (|ρ| < 0.5)
- Pas de liaison forte entre standardisation et concentration
- Compatible avec des phénomènes **multifactoriels**

---

# GLOSSAIRE

- **Data Lake** : Stockage brut des fichiers Airbnb sans transformation
- **ETL** : Extract-Transform-Load (chaîne de traitement des données)
- **Gini** : Coefficient mesurant l'inégalité (0 = égalité, 1 = concentration maximale)
- **NLP** : Natural Language Processing (analyse automatique de texte)
- **Proxy** : Variable de substitution approximant un concept non mesurable directement
- **Score -1** : Convention indiquant une donnée manquante/non disponible

---

  
**Code source** : https://github.com/megxp/ImmoVision360.git
