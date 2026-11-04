# Mise en route de la génération automatique

Toutes les 10 minutes, GitHub relève les nouvelles commandes du site. Pour chacune, il génère l'étude en PDF et sa capsule vidéo, puis te les envoie par mail. Tu vérifies le paiement Airtel (référence « DV + nom »), puis tu transmets les fichiers au client.

## 1. Déposer les fichiers

Sur la page du dépôt `destin-et-vie`, clique sur **Add file → Upload files**. Glisse **tout le contenu** du dossier dézippé (pas le dossier lui-même), puis clique sur **Commit changes**.

Le dossier `.github` est caché sous Windows. S'il ne part pas, crée le fichier à la main : **Add file → Create new file**, nom `.github/workflows/commandes.yml`, puis colle son contenu.

## 2. Créer les 4 secrets

Dans le dépôt, va dans **Settings → Secrets and variables → Actions → New repository secret** :

| Nom | Valeur |
|---|---|
| `NETLIFY_TOKEN` | Netlify : avatar → **User settings → Applications → Personal access tokens → New access token** |
| `GMAIL_USER` | l'adresse Gmail qui enverra les mails |
| `GMAIL_APP_PASSWORD` | Google : **myaccount.google.com/apppasswords** (la validation en 2 étapes doit être activée), 16 lettres, sans espaces |
| `DEST_EMAIL` | l'adresse qui reçoit les études (elle peut être la même) |

Ces valeurs sont confidentielles : ne les colle nulle part ailleurs.

## 3. Tester

Va dans **Actions → Commandes Destin & Vie → Run workflow**. Le premier passage prend environ 3 minutes, le temps de télécharger la voix. Fais ensuite une commande test sur le site : le mail arrive dans les 10 minutes.

## Bon à savoir

- Les packs **Compatibilité** et **Famille** concernent plusieurs personnes. Le mail te prévient, et c'est toi qui transmets les données à Claude.
- Si le lieu de naissance n'est pas reconnu, le mail te le signale. Ajoute la ville dans `destin_vie/places.py`.
- GitHub met en pause les tâches planifiées d'un dépôt inactif pendant 60 jours. Si plus aucune étude n'arrive, clique sur **Actions → Enable workflow**.
