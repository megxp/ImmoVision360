# 🔍 Stratégie d'Extraction - ImmoVision 360

Ce document justifie la sélection des données pour le passage de la zone **Bronze** (Raw) à la zone **Silver** (Processed).

##  Sélection des Features

### A. Hypothèse Économique : Industrialisation
* **`calculated_host_listings_count`** : Variable clé pour identifier les "multi-hébergeurs". Un score élevé trahit une gestion hôtelière plutôt qu'un partage de résidence.
* **`price` & `availability_365`** : Permet de calculer le rendement potentiel. Un bien disponible 365 jours par an n'est plus une habitation, mais un produit financier.

### B. Hypothèse Sociale : Déshumanisation
* **`host_response_time` & `rate`** : Les professionnels utilisent des outils d'automatisation (Channel Managers) garantissant des réponses en moins d'une heure à 100%.
* **`number_of_reviews`** : Mesure l'intensité du flux de voyageurs dans l'immeuble (nuisances potentielles).

### C. Données de Structure
* **`id`** : Préservé pour garantir la jointure avec les images (`.jpg`) et les textes (`.txt`) lors de la phase de transformation IA.
* **`latitude/longitude`** : Pour la cartographie précise de la gentrification dans l'Élysée.

## ⚙️ Processus Technique
L'extraction est **idempotente** : le script peut être relancé sans doublons. Le prix est nettoyé nativement (conversion string -> float) pour faciliter les calculs statistiques immédiats.