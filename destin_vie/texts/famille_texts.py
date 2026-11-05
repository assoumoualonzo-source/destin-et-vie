"""Textes du produit « Famille ».

Variables : {a} pour l'adulte, {enf} pour l'enfant (prénoms usuels).
Les familles de nombres reprennent celles de la compatibilité : esprit (1, 5, 7), matière (2, 4, 8), cœur (3, 6, 9).
"""

FAMILY_NAME = {"esprit": "l'indépendance et la réflexion", "matière": "le concret et la sécurité",
               "cœur": "le cœur et l'expression"}

# Lien entre un adulte qui élève et un enfant, selon la famille de leurs chemins de vie.
LINK_SAME = ("{a} et {enf} fonctionnent de la même manière : ils se comprennent souvent sans avoir besoin de "
             "parler. Attention à ne pas projeter sur {enf} ses propres choix ; ce qui a réussi à {a} n'est pas "
             "forcément sa voie.")
LINK_IDENTICAL = ("Même chemin de vie : {enf} ressemble beaucoup à {a}, défauts compris. C'est un miroir précieux, "
                  "qui demande de la patience quand {enf} répète les erreurs que {a} connaît bien.")
LINK_CROSS = {
    frozenset(["esprit", "matière"]): (
        "{a} et {enf} n'avancent pas au même rythme : l'un a besoin de liberté et d'idées, l'autre de repères et "
        "de concret. Expliquer le pourquoi des règles, et laisser une part de choix, apaise la relation."),
    frozenset(["esprit", "cœur"]): (
        "L'un a besoin d'espace, l'autre de chaleur et d'échanges. {a} gagne à montrer son affection par des gestes "
        "et des mots, même simples ; {enf} y trouve la sécurité dont {il|elle} a besoin pour s'épanouir."),
    frozenset(["matière", "cœur"]): (
        "L'un apporte la stabilité, l'autre la sensibilité. C'est une belle complémentarité : {a} donne un cadre, "
        "{enf} y met de la vie. Veillez à ce que les obligations ne prennent pas toute la place face aux émotions."),
}

# Ce que la famille vit ensemble, selon la famille de nombres la plus représentée.
DOMINANT = {
    "esprit": ("Une famille d'indépendants", "Beaucoup de membres ont besoin d'espace et de liberté. La maison "
               "gagne à laisser chacun respirer, tout en gardant des rendez-vous communs : un repas, une sortie, "
               "un moment de parole chaque semaine."),
    "matière": ("Une famille de bâtisseurs", "Le sens du devoir, du travail et de la sécurité domine. C'est une "
                "base solide pour les enfants. Il faut juste veiller à garder du temps pour le jeu, le rire et "
                "la fantaisie."),
    "cœur": ("Une famille du cœur", "L'affection, l'expression et la générosité dominent. La maison est chaleureuse "
             "et vivante ; elle gagne à poser aussi quelques règles claires, pour que l'émotion ne décide pas "
             "de tout."),
}

# Nombre de la famille (somme réduite de tous les chemins de vie).
FAMILY_NUMBER = {
    1: "Une famille qui avance par l'initiative : elle réussit quand elle se fixe un projet commun.",
    2: "Une famille de solidarité : sa force est l'entraide et la douceur entre ses membres.",
    3: "Une famille joyeuse et expressive, qui aime se retrouver, fêter et partager.",
    4: "Une famille qui construit sur la durée : maison, études, patrimoine.",
    5: "Une famille en mouvement, ouverte aux voyages et aux changements.",
    6: "Une famille tournée vers le foyer, le soin et la transmission entre générations.",
    7: "Une famille de réflexion, attachée aux valeurs, à la foi ou à la connaissance.",
    8: "Une famille d'ambition, qui pousse ses membres à réussir.",
    9: "Une famille généreuse, souvent ouverte aux autres et aux enfants qui ne sont pas les siens.",
    11: "Une famille inspirée, où l'intuition et les valeurs comptent beaucoup.",
    22: "Une famille capable de grands projets communs, sur plusieurs générations.",
    33: "Une famille de dévouement, où l'on prend soin les uns des autres.",
}

ELEMENT_NOTE = {
    "Feu": "le Feu (élan, enthousiasme, impatience)",
    "Terre": "la Terre (sens pratique, constance, prudence)",
    "Air": "l'Air (curiosité, échanges, besoin de mouvement)",
    "Eau": "l'Eau (sensibilité, intuition, besoin de sécurité affective)",
}

RAISED_BY = ("En Afrique, un enfant est souvent élevé par plusieurs adultes : parents, oncles, tantes, "
             "grands-parents, grands frères ou grandes sœurs. Cette étude tient compte du lien réel que chacun "
             "occupe, et pas seulement de la filiation.")
