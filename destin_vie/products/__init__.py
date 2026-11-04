"""Catalogue des produits Destin & Vie.

Chaque produit expose `render(...)`. Les produits à venir réutilisent
reading.build() et les gabarits de pdf_style :
- compatibilite : deux Person -> deux lectures + comparaison (nombres, éléments, aspects croisés)
- prevision_2027 : une Person -> année personnelle 2027 et mois personnels + transits majeurs
- famille : jusqu'à 6 Person -> une lecture chacun + liens (nombres partagés, éléments, rôles)
"""
from . import chemin_de_vie, compatibilite, essentiel, prevision_2027

PRODUCTS = {
    "prevision_2027": prevision_2027.render,   # pack Prévision 2027
    "chemin_de_vie": chemin_de_vie.render,     # pack Découverte
    "essentiel": essentiel.render,             # pack Essentiel (les deux + bonus)
    "compatibilite": compatibilite.render,     # pack Compatibilité amoureuse (2 personnes)
}

# Nombre de personnes attendu par produit (1 par défaut).
MULTI = {"compatibilite": 2}
