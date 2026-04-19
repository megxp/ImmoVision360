from weasyprint import HTML
import os

# Define the HTML content based on the user's report structure
# I've added professional styling for a "City Hall" report feel.
html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 20mm;
            background-color: #ffffff;
            @bottom-right {
                content: counter(page);
                font-size: 9pt;
                color: #666;
            }
        }

        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #333;
            text-align: justify;
        }

        /* Front Page */
        .title-page {
            height: 250mm;
            display: block;
            text-align: center;
            padding-top: 50mm;
            page-break-after: always;
        }

        .title-page h1 {
            font-size: 28pt;
            color: #1a3a5a;
            margin-bottom: 10mm;
            text-transform: uppercase;
            border-bottom: 3px solid #1a3a5a;
            display: inline-block;
            padding-bottom: 5mm;
        }

        .title-page h2 {
            font-size: 18pt;
            color: #4a6a8a;
            margin-top: 0;
        }

        .title-page .meta {
            margin-top: 80mm;
            font-size: 12pt;
            color: #666;
        }

        /* Section Styling */
        h1 {
            color: #1a3a5a;
            font-size: 18pt;
            border-left: 5px solid #1a3a5a;
            padding-left: 10px;
            margin-top: 30pt;
            page-break-before: always;
        }

        h2 {
            color: #2c5282;
            font-size: 14pt;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 5px;
            margin-top: 20pt;
        }

        h3 {
            color: #4a5568;
            font-size: 12pt;
            font-weight: bold;
        }

        .summary-box {
            background-color: #f7fafc;
            border: 1px solid #edf2f7;
            padding: 15px;
            border-radius: 8px;
            margin: 20pt 0;
        }

        .highlight-green { color: #2f855a; font-weight: bold; }
        .highlight-orange { color: #c05621; font-weight: bold; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20pt 0;
        }

        th {
            background-color: #1a3a5a;
            color: white;
            padding: 10px;
            text-align: left;
            font-size: 10pt;
        }

        td {
            border-bottom: 1px solid #e2e8f0;
            padding: 10px;
            font-size: 10pt;
        }

        .chart-placeholder {
            background-color: #f1f5f9;
            border: 1px dashed #cbd5e0;
            padding: 40px;
            text-align: center;
            font-style: italic;
            color: #718096;
            margin: 15pt 0;
        }

        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 9pt;
            font-weight: bold;
            text-transform: uppercase;
        }
        .badge-validated { background-color: #c6f6d5; color: #22543d; }
        .badge-warning { background-color: #feebc8; color: #744210; }

        /* Prevent widows/orphans */
        p, li { orphans: 3; widows: 3; }
        h2, h3 { page-break-after: avoid; }
    </style>
</head>
<body>

    <div class="title-page">
        <h1>ImmoVision 360° : Paris Élysée</h1>
        <h2>Rapport d'analyse des dynamiques locatives</h2>
        <div class="meta">
            <p>Destinataire : Mairie de Paris</p>
            <p>Auteur : Mégane Legnigha - IABD</p>
            <p>Date : 19 Avril 2026</p>
        </div>
    </div>

    <h1>RÉSUMÉ EXÉCUTIF</h1>
    <div class="summary-box">
        <p><strong>Contexte</strong> : La Mairie de Paris souhaite comprendre les dynamiques locatives dans le quartier de l'Élysée pour éclairer sa politique de régulation du tourisme.</p>
        <p><strong>Résultats clés</strong> :</p>
        <ul>
            <li><span class="highlight-green">Hypothèse 2 validée</span> : 59% des descriptions adoptent un vocabulaire "hôtelier".</li>
            <li><span class="highlight-orange">Hypothèse 1 partiellement validée</span> : 57% de standardisation (seuil 80% non atteint).</li>
            <li><span class="highlight-orange">Hypothèse 3 modérée</span> : 42% de l'offre contrôlée par 5% d'hôtes.</li>
        </ul>
        <p><strong>Conclusion</strong> : Le quartier présente des signes de professionnalisation (rupture du lien social, concentration mesurable) sans basculement total vers un modèle industriel.</p>
    </div>

    <h1>1. CONTEXTE ET PROBLÉMATIQUE</h1>
    <h2>1.1 Demande de la Mairie</h2>
    <p>Le quartier de l'Élysée (8e arrondissement) fait face à des tensions croissantes liées à la location de courte durée. Les riverains signalent une dégradation de la vie de quartier et une transformation des immeubles d'habitation en structures quasi-hôtelières.</p>
    
    <h2>1.2 Périmètre de l'étude</h2>
    <p>Cette analyse se base sur les données extraites d'Inside Airbnb (Décembre 2024). Nous avons utilisé des techniques de <strong>Computer Vision</strong> pour analyser les photos et de <strong>NLP (Natural Language Processing)</strong> pour scruter les descriptions afin de différencier le partage résidentiel de l'exploitation commerciale.</p>

    <h1>2. DONNÉES ET MÉTHODOLOGIE</h1>
    <h2>2.1 Chaîne de traitement</h2>
    <p>Le projet suit une architecture de données rigoureuse divisée en trois zones : <strong>Bronze</strong> (données brutes), <strong>Silver</strong> (données filtrées et nettoyées) et <strong>Gold</strong> (données enrichies par IA pour l'analyse décisionnelle).</p>
    
    <h3>Analyse par Intelligence Artificielle</h3>
    <ul>
        <li><strong>Standardisation</strong> : Détection automatisée du style "catalogue" (murs blancs, mobilier type IKEA, absence d'effets personnels).</li>
        <li><strong>Déshumanisation</strong> : Analyse sémantique recherchant des marqueurs de gestion déléguée ("code d'accès", "conciergerie", "gestionnaire").</li>
    </ul>

    <h2>2.2 Fiabilité des données</h2>
    <p>Pour garantir l'honnêteté scientifique, les valeurs manquantes ou inexploitables par l'IA ont été codées <strong>-1</strong> et exclues des calculs de pourcentages afin de ne pas biaiser les résultats.</p>

    <h1>3. RÉSULTATS DÉTAILLÉS</h1>
    <h2>3.1 Standardisation visuelle</h2>
    <div class="chart-placeholder">[Graphique : Répartition Standardisation (Industrialisé vs Personnel)]</div>
    <p>Nous observons que <strong>57%</strong> des annonces présentent un caractère industrialisé. Bien que majoritaire, ce chiffre reste inférieur au seuil critique de 80% que nous avions fixé pour qualifier une transformation "massive" du parc immobilier.</p>

    <h2>3.2 Rupture du lien social</h2>
    <div class="chart-placeholder">[Graphique : Analyse des Textes (Hôtélisé vs Naturel)]</div>
    <p>C'est le point le plus saillant de l'étude : <strong>59,1%</strong> des textes de présentation sont dénués de toute trace d'accueil humain personnalisé. Le vocabulaire hôtelier domine, confirmant une rupture du lien social traditionnel de l'économie de partage.</p>

    <h2>3.3 Concentration de l'offre</h2>
    <div class="chart-placeholder">[Graphique : Courbe de Lorenz - Indice de Gini 0.85]</div>
    <p>L'indice de Gini s'établit à <strong>0.851</strong>. Une minorité de 5% des hôtes contrôle 41,8% des annonces. Bien que sous le seuil de 60% attendu, ce niveau d'inégalité témoigne d'une forte professionnalisation du secteur au détriment des petits propriétaires locaux.</p>

    <h1>4. CONCLUSION ET RECOMMANDATIONS</h1>
    <h2>4.1 Bilan</h2>
    <table>
        <thead>
            <tr>
                <th>Hypothèse</th>
                <th>Résultat</th>
                <th>Statut</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Standardisation (Produit financier)</td>
                <td>57.0%</td>
                <td><span class="badge badge-warning">Partiel</span></td>
            </tr>
            <tr>
                <td>Déshumanisation (Lien social)</td>
                <td>59.1%</td>
                <td><span class="badge badge-validated">Validée</span></td>
            </tr>
            <tr>
                <td>Concentration (Machine à cash)</td>
                <td>41.8%</td>
                <td><span class="badge badge-warning">Modérée</span></td>
            </tr>
        </tbody>
    </table>

    <h2>4.2 Recommandations</h2>
    <ol>
        <li><strong>Renforcer les contrôles</strong> sur les hôtes possédant plus de 10 annonces (31,1% de l'offre totale).</li>
        <li><strong>Favoriser les résidences principales</strong> par une distinction fiscale ou réglementaire plus marquée entre les annonces "Naturelles" et "Hôtélisées".</li>
        <li><strong>Étude d'impact</strong> : Réaliser une analyse croisée avec les données de prix pour identifier les zones de spéculation immobilière.</li>
    </ol>

</body>
</html>
"""

# Remplace la fin de ton script par ceci :
with open("rapport_final_Mairie.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("Fichier HTML généré avec succès !")