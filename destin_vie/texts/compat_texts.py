"""Textes du produit « Compatibilité amoureuse ».

Variables : {a} et {b} pour les prénoms des deux partenaires.
Les textes restent neutres quant au genre des partenaires.
"""

# Les trois familles de nombres (concordances classiques) : 1-5-7, 2-4-8, 3-6-9.
FAMILY = {1: "esprit", 5: "esprit", 7: "esprit", 2: "matière", 4: "matière", 8: "matière",
          3: "cœur", 6: "cœur", 9: "cœur"}
FAMILY_LABEL = {
    "esprit": "les nombres de l'indépendance et de la réflexion (1, 5, 7)",
    "matière": "les nombres du concret et de la sécurité (2, 4, 8)",
    "cœur": "les nombres du cœur et de l'expression (3, 6, 9)",
}
SAME_FAMILY = ("Leurs chemins de vie appartiennent à la même famille, {fam}. {a} et {b} se comprennent "
               "sans avoir besoin de tout expliquer : ils partagent la même façon d'aborder la vie, ce qui crée "
               "une complicité rapide. Le revers est qu'ils peuvent aussi partager les mêmes angles morts.")
CROSS_FAMILY = {
    frozenset(["esprit", "matière"]): (
        "L'un avance par les idées et la liberté, l'autre par la sécurité et le concret. C'est une "
        "complémentarité utile : l'un ouvre des portes, l'autre construit derrière. Elle demande d'accepter que "
        "le rythme de l'autre ne soit pas le sien."),
    frozenset(["esprit", "cœur"]): (
        "L'un a besoin d'espace et de réflexion, l'autre d'échanges et de chaleur. Ensemble, ils mêlent "
        "profondeur et générosité. Le point d'attention est la distance : ce qui est respect de l'espace pour "
        "l'un peut ressembler à de la froideur pour l'autre."),
    frozenset(["matière", "cœur"]): (
        "L'un apporte la stabilité, l'autre la tendresse et l'expression. C'est souvent une association solide "
        "pour fonder un foyer. Il faudra veiller à ce que le sens pratique de l'un ne prenne pas toute la place "
        "face aux élans de l'autre."),
}
SAME_NUMBER = ("Même chemin de vie : {a} et {b} se reconnaissent l'un dans l'autre. C'est une force et un "
               "piège, car un même défaut se trouve alors multiplié par deux.")

SOUL_SAME = ("Âmes en résonance : au fond, {a} et {b} désirent la même chose. C'est l'un des meilleurs signes "
             "de durée pour un couple.")
SOUL_FAMILY = ("Leurs Âmes sont de la même famille : leurs besoins profonds sont proches, même s'ils ne "
               "s'expriment pas de la même manière.")
SOUL_DIFF = ("Leurs Âmes diffèrent : ce qui nourrit l'un ({sa}) n'est pas ce qui nourrit l'autre ({sb}). "
             "Le dire clairement évite bien des malentendus.")

COUPLE = {
    1: ("Un couple de projets", "Ce couple avance quand il a un but commun. Ensemble, {a} et {b} osent davantage "
        "que seuls ; le danger serait que chacun veuille diriger."),
    2: ("Un couple de tendresse", "Ce couple vit de complicité, de petites attentions et de dialogue. Sa force "
        "est la douceur ; sa faiblesse, la peur d'aborder les sujets qui fâchent."),
    3: ("Un couple joyeux", "Ce couple aime sortir, rire, recevoir. Il rayonne en société. Il gagne à se garder "
        "aussi des moments seuls à deux, loin du bruit."),
    4: ("Un couple bâtisseur", "Ce couple construit : maison, épargne, projets durables. Il est fiable et "
        "rassurant ; il doit veiller à ne pas laisser la routine éteindre la fantaisie."),
    5: ("Un couple d'aventure", "Ce couple a besoin de mouvement, de voyages, de nouveauté. La liberté de chacun "
        "est la condition de sa durée."),
    6: ("Un couple de foyer", "Ce couple est tourné vers la famille, les enfants, la maison. Il donne beaucoup "
        "aux autres ; il doit aussi se donner du temps à lui-même."),
    7: ("Un couple de complicité intellectuelle", "Ce couple partage des idées, des lectures, une recherche de "
        "sens. Il a besoin de calme et de confiance ; le non-dit est son principal ennemi."),
    8: ("Un couple d'ambition", "Ce couple réussit ensemble : carrière, affaires, patrimoine. Il doit partager "
        "le pouvoir de décision et ne pas laisser l'argent devenir un sujet de rivalité."),
    9: ("Un couple ouvert sur le monde", "Ce couple est généreux, tourné vers les autres et les grandes causes. "
        "Il doit veiller à ne pas s'oublier lui-même."),
}

# Synastrie : contacts entre les deux thèmes.
PAIR_TOPIC = {
    ("Soleil", "Lune"): "l'identité de l'un et la sensibilité de l'autre",
    ("Lune", "Lune"): "leurs besoins émotionnels",
    ("Vénus", "Mars"): "le désir et l'attirance",
    ("Vénus", "Vénus"): "leur façon d'aimer et leurs goûts",
    ("Soleil", "Soleil"): "leurs personnalités",
    ("Mercure", "Mercure"): "leur façon de se parler",
    ("Soleil", "Vénus"): "l'affection et l'admiration",
    ("Lune", "Vénus"): "la tendresse au quotidien",
    ("Mars", "Mars"): "leur énergie et leur manière de se disputer",
}
ASPECT_FEEL = {
    "conjonction": "se rejoignent directement : un lien fort, immédiat, presque évident",
    "trigone": "s'accordent naturellement : une harmonie qui ne demande pas d'effort",
    "sextile": "se soutiennent : une entente facile à cultiver",
    "carré": "se frottent : de l'attraction et des tensions, qui obligent à se parler",
    "opposition": "se font face : une attirance des contraires, qui demande des compromis",
}

ELEMENT_PAIR = {
    "same": "Leurs Soleils sont du même élément ({e}) : même tempo, mêmes réflexes.",
    frozenset(["Feu", "Air"]): "Feu et Air s'entretiennent : l'un donne l'élan, l'autre l'oxygène des idées.",
    frozenset(["Terre", "Eau"]): "Terre et Eau se complètent : l'un donne la forme, l'autre la sensibilité.",
    frozenset(["Feu", "Terre"]): "Feu et Terre avancent à des vitesses différentes : l'un fonce, l'autre consolide.",
    frozenset(["Feu", "Eau"]): "Feu et Eau s'attirent et se heurtent : passion d'un côté, émotion de l'autre.",
    frozenset(["Air", "Terre"]): "Air et Terre doivent traduire leurs langages : l'un pense, l'autre fait.",
    frozenset(["Air", "Eau"]): "Air et Eau se cherchent : l'un raisonne, l'autre ressent.",
}

ADVICE = {
    "esprit": "Respecter le besoin d'espace de chacun, et prévoir des projets communs qui donnent une direction.",
    "matière": "S'accorder sur l'argent et l'organisation dès le départ, et garder de la place pour l'imprévu.",
    "cœur": "Se dire les choses avec tendresse mais clairement, et préserver du temps pour le couple seul.",
}
ADVICE_TENSION = ("Les aspects tendus entre leurs thèmes ne sont pas des signes d'échec : ce sont les endroits "
                  "où le couple apprend le plus. Ils demandent surtout de la parole.")
