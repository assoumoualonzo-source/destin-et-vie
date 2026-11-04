# Destin & Vie — moteur de génération des études

Génère automatiquement une étude PDF à partir des données d'un acte de naissance.

| `--produit` | Pack sur le site | Contenu |
|---|---|---|
| `prevision_2027` | Prévision 2027 | année personnelle 2027, 12 mois personnels, temps forts, vigilance, conseils (4 pages) |
| `chemin_de_vie` | Découverte | étude individuelle complète, numérologie + thème astral (6 pages) |
| `essentiel` | Essentiel | chemin de vie + prévision 2027 + bonus : lecture croisée chemin de vie × 2027 (9 pages) |
| `compatibilite` | Compatibilité amoureuse | lecture du couple (nombres, synastrie, forces, frictions, conseils) + les deux chemins de vie (12 pages). Deux adultes. |

Ajouter `--video` génère aussi la capsule de 20 à 30 secondes (même nom, en .mp4).

À venir : `famille`.

## Installation

```bash
pip install ephem reportlab
# polices : paquet fonts-liberation (Linux) ou copier les .ttf Liberation dans destin_vie/fonts/
```

Python 3.10 ou plus récent (utilise `zoneinfo`).

## Générer une étude

```bash
python3 generate.py --prenoms "Thimy Akam Matungiatia" --nom "Mbadinga Ella" \
    --sexe M --date 2021-01-24 --heure 15:30 --lieu "Akanda, Gabon" \
    --ref DV-0001 -o etude.pdf
```

ou à partir d'une commande au format JSON (voir `exemples/commande_exemple.json`) :

```bash
python3 generate.py --json exemples/commande_exemple.json -o etude.pdf
python3 generate.py --produit prevision_2027 --json exemples/commande_exemple.json -o prevision.pdf
python3 generate.py --produit essentiel --json exemples/commande_exemple.json -o essentiel.pdf
```

Pour la compatibilité, la commande contient une liste `personnes` (voir `exemples/commande_couple.json`).

La prévision 2027 n'utilise que les noms, le sexe et la date ; l'heure et le lieu restent demandés
pour garder un seul format de commande.

| Champ | Obligatoire | Remarque |
|---|---|---|
| `prenoms` | oui | tous les prénoms de l'acte, dans l'ordre |
| `nom` | oui | noms de famille |
| `sexe` | oui | `M` ou `F`, pour les accords du texte |
| `date` | oui | `AAAA-MM-JJ` |
| `heure` | non | `HH:MM`. Sans heure : pas d'ascendant ni de maisons, la Lune est signalée comme indicative |
| `lieu` | oui | texte libre ; la ville est cherchée dans `destin_vie/places.py` |
| `lat`, `lon`, `tz` | non | pour un lieu absent de la table (fuseau IANA, ex. `Africa/Douala`) |
| `prenom_usuel` | non | sinon, le premier prénom |
| `ref` | non | référence de commande imprimée en couverture |

Le programme affiche le lieu retenu : vérifiez qu'il correspond à l'acte avant de livrer.

## Ce que contient l'étude

1. Couverture et note de méthode (avec mise en garde : lecture symbolique, sans valeur scientifique)
2. Profil numérologique : chemin de vie, expression, âme, personnalité, jour de naissance, nombres maîtres,
   leçons karmiques, détail des calculs, lecture d'ensemble, grille d'inclusion
3. Cycles de vie, réalisations, défis et année personnelle
4. Thème natal : planètes, Nœud Nord, ascendant, Milieu du Ciel, maisons Placidus, alerte si l'ascendant
   change de signe à moins de 20 minutes de l'heure indiquée
5. Lecture du thème : Soleil, Lune, ascendant, concentrations de planètes, Mercure-Vénus-Mars, éléments,
   aspects les plus serrés, Milieu du Ciel
6. Synthèse croisée numérologie / astrologie
7. Pistes concrètes : activités et manière d'apprendre (moins de 16 ans) ou forces, domaines et année en cours (adultes)

## Organisation du code

```
destin_vie/
  numerology.py        calculs numérologiques (fonctions pures, détail des calculs)
  astro.py             éphéméride, maisons Placidus, aspects, phase lunaire
  places.py            villes (Gabon, Afrique, diaspora) et fuseaux horaires
  reading.py           assemble calculs + textes en paragraphes et tableaux
  texts/numbers.py     textes par nombre
  texts/astro_texts.py textes par signe, maison, aspect
  texts/guidance.py    pistes enfant / adulte
  pdf_style.py         charte graphique (encre et laiton, Liberation)
  products/            un module par produit, enregistré dans products/__init__.py
generate.py            ligne de commande
```

Les textes sont rédigés à la troisième personne avec des variables :
`{p}` prénom, `{il}`/`{Il}`, `{lui}`, `{e}` (accord féminin) et `{masculin|féminin}`
pour les mots qui changent (`{curieux|curieuse}`). Pour modifier une interprétation,
il suffit d'éditer le texte concerné.

## Ajouter les autres produits

Chaque produit réutilise `reading.build(person)` et `pdf_style`. Il suffit d'ajouter un module
dans `products/` et de l'enregistrer dans `PRODUCTS` :

- **compatibilite** : deux lectures, puis comparaison des nombres, des éléments et des aspects
  entre les deux thèmes
- **prevision_2027** : année personnelle 2027, mois personnels, passages planétaires majeurs
- **famille** : jusqu'à 6 lectures, puis les liens (nombres partagés, éléments complémentaires,
  conseils pour les enfants)

## Capsule résumé (`capsule/slide.py`) — format retenu

Une seule diapositive animée, 9:16, 15 à 20 secondes, environ 2 Mo.
- **À l'écran** : « Chemin de vie », le prénom et le nom (écrits uniquement), le nombre et son titre, puis une
  carte pastel avec les points de la conclusion (une icône chacun) et le point à cultiver.
- **À la voix** : uniquement le titre de l'étude (« Chemin de vie »). Le reste défile en musique, sans paroles.
  Les noms des clients ne sont jamais prononcés.
- **Contenu** : tiré de `reading.synthesis_points()`, c'est-à-dire de la même synthèse que le PDF.
- **Fond** : illustration pastel « Sparkling night sky with a purple moon and pink clouds » (Severina Seidl,
  Unsplash, licence Unsplash). **Icônes** : Phosphor Icons (MIT). Musique et voix : comme ci-dessous.
- Disponible pour `chemin_de_vie` ; les autres produits utilisent encore l'ancien gabarit.

## Ancien gabarit multi-scènes (`capsule/capsule.py`)

Format vertical 9:16, 1080×1920, 20 à 30 secondes, environ 7 Mo (compatible statut WhatsApp, TikTok, Reels).

- **Fond** : le ciel étoilé du site (`assets/fond_site.jpg`, photo Unsplash de Nathan Anderson, licence Unsplash).
- **Contenu** : uniquement le résumé de l'étude du client (chemin de vie, forces, défi, année 2027 ; ou nombre du
  couple, force, point à travailler, conseil), puis la signature « Destin & Vie », sans message promotionnel.
- **Emplacements** : grand titre, PRÉNOM, NOM, grand chiffre dans l'emblème, sous-titre de la voix off.
- **Scripts** : `capsule/modeles.json`, un modèle par produit (variantes enfant pour le chemin de vie et la
  prévision). Les textes se modifient sans toucher au code ; les variables sont remplies par le moteur.
- **Voix off** : Piper, voix française `fr_FR-siwis-medium` (licence libre), téléchargée au premier lancement.
- **Musique** : « Kalimba Relaxation Music », Kevin MacLeod, publiée sur FreePD en domaine public (CC0),
  copie conservée par Internet Archive (archive.org/details/freepd). Aucune attribution requise. Elle est
  automatiquement baissée sous la voix.

Dépendances supplémentaires : `pip install piper-tts numpy pillow`, et `ffmpeg`.

## Conventions de calcul de la Prévision 2027

- Année personnelle = jour réduit + mois réduit + 2027 réduit (2+0+2+7 = 11 → 2). Si le total brut vaut 11 ou 22,
  il est présenté comme nombre maître, vécu comme 2 ou 4.
- L'année couvre l'année civile, du 1er janvier au 31 décembre 2027. Le chemin de vie applique la même règle
  à son paragraphe « Année personnelle ».
- Mois personnel = chiffre de base de l'année + numéro du mois réduit (octobre = 1, novembre = 2, décembre = 3).
- Temps forts : mois 1 et 8, et le mois dont le chiffre égale celui du chemin de vie. Vigilance : mois 4, 7 et 9.
- Moins de 16 ans : textes adaptés (conseils aux parents, pas de vocabulaire professionnel ou financier).

## Précision et limites

- Positions planétaires à la minute d'arc près (PyEphem) ; Nœud Nord moyen.
- Coordonnées des villes au kilomètre près, suffisant pour l'ascendant.
- Une ville absente de la table bloque la génération : ajoutez-la dans `places.CITIES`
  ou passez `lat`, `lon`, `tz`.
