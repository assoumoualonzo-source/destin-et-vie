# Destin & Vie : mise en route (3 gestes)

Chaque commande validée sur le site déclenche aussitôt la génération. L'étude, en PDF et avec sa vidéo, t'arrive par mail en 2 à 3 minutes. Toutes les 10 minutes, une relève de secours rattrape les commandes manquées.

## 1. GitHub : déposer les fichiers
Ouvre le dépôt, clique sur **Add file → Upload files**, glisse tout le contenu du dossier dézippé, puis clique sur **Commit changes**.

## 2. GitHub : créer le jeton de déclenchement
1. Va sur **github.com/settings/personal-access-tokens/new**.
2. Nom : `netlify-destin-et-vie`. Expiration : 1 an.
3. Dans **Repository access**, choisis **Only select repositories**, puis `destin-et-vie`.
4. Dans **Permissions → Repository permissions → Actions**, choisis **Read and write**.
5. Clique sur **Generate token** et copie le jeton.

## 3. Netlify : relier le site au dépôt
1. Ouvre le projet, puis **Project configuration → Build & deploy → Link repository**. Choisis **GitHub**, puis `destin-et-vie`. Les réglages se remplissent seuls grâce à `netlify.toml`.
2. Va dans **Project configuration → Environment variables → Add a variable**. Nom : `GH_TOKEN`. Valeur : le jeton copié à l'étape 2.
3. Va dans **Deploys → Trigger deploy → Deploy site**.

Désormais, pour modifier le site, il suffit de modifier `site/index.html` dans GitHub : Netlify le publie tout seul.
