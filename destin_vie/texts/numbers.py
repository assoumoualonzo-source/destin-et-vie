"""Textes d'interprétation numérologique.

Les textes sont rédigés à la troisième personne et acceptent ces variables :
{p} prénom usuel, {il}/{Il} pronom, {e} accord féminin (« né{e} »),
{masculin|féminin} choisit selon le sexe.
"""

# ---------------------------------------------------------------- Chemin de vie
LIFE_PATH = {
    1: dict(title="Le pionnier", traits="volonté, esprit d'initiative, besoin d'ouvrir sa propre voie et de décider.",
            vigilance="Impatience, entêtement, mal à demander ou à accepter de l'aide.",
            long="Le 1 avance seul et devant. {p} a besoin d'autonomie et de projets qu'{il} peut mener à sa façon. "
                 "Son chemin consiste à apprendre à diriger sans écraser, et à faire confiance aux autres."),
    2: dict(title="Le médiateur", traits="écoute, sensibilité, sens de l'harmonie et du travail à deux.",
            vigilance="Manque de confiance en soi, dépendance au regard des autres, peur du conflit.",
            long="Le 2 relie les personnes. {p} sent les ambiances, apaise les tensions et donne le meilleur dans le duo. "
                 "Son chemin consiste à oser prendre sa place et à dire ce qu'{il} pense."),
    3: dict(title="Le communicant", traits="imagination, besoin de s'exprimer, goût du jeu, de la parole et de la création.",
            vigilance="Dispersion, difficulté à finir ce qui est commencé, susceptibilité quand on ne l'écoute pas.",
            long="Le 3 avance par la parole et la création. {p} a besoin d'un public, d'échanges et de liberté créative. "
                 "Son chemin consiste à canaliser ce talent dans des projets menés jusqu'au bout."),
    4: dict(title="Le bâtisseur", traits="méthode, constance, sens du concret et du travail bien fait.",
            vigilance="Rigidité, inquiétude face à l'imprévu, excès de sérieux.",
            long="Le 4 construit pierre après pierre. {p} est fiable, organisé{e}, rassuré{e} par un cadre clair. "
                 "Son chemin consiste à garder cette solidité tout en apprenant la souplesse."),
    5: dict(title="L'explorateur", traits="curiosité, mouvement, soif d'expériences et de liberté.",
            vigilance="Instabilité, ennui rapide, difficulté à s'engager dans la durée.",
            long="Le 5 apprend en essayant. {p} a besoin de bouger, de voyager, de changer d'horizon. "
                 "Son chemin consiste à trouver la liberté dans l'engagement plutôt que dans la fuite."),
    6: dict(title="Le protecteur", traits="sens des responsabilités, attention aux proches, besoin d'harmonie au foyer.",
            vigilance="Oubli de soi, besoin d'approbation, tendance à tout porter.",
            long="Le 6 prend soin. {p} se sent responsable de l'équilibre de son entourage et y trouve du sens. "
                 "Son chemin consiste à aider sans s'oublier et à accepter que les autres fassent leurs propres choix."),
    7: dict(title="Le chercheur", traits="réflexion, intuition, goût de la connaissance et de la vérité.",
            vigilance="Repli, méfiance, difficulté à exprimer ses émotions, perfectionnisme.",
            long="Le 7 veut comprendre en profondeur. {p} a besoin de calme, de lecture, de temps pour soi. "
                 "Son chemin consiste à partager ce qu'{il} comprend au lieu de le garder pour soi."),
    8: dict(title="Le stratège", traits="ambition, sens de l'organisation, goût des responsabilités et de la réussite.",
            vigilance="Autoritarisme, rapport tendu à l'argent ou au pouvoir, surmenage.",
            long="Le 8 vise des résultats concrets. {p} a l'étoffe d'un{e} dirigeant{e} et le sens des affaires. "
                 "Son chemin consiste à équilibrer pouvoir et générosité, réussite et vie personnelle."),
    9: dict(title="L'humaniste", traits="générosité, ouverture au monde, idéal, sens du collectif.",
            vigilance="Dispersion dans les causes des autres, difficulté à tourner la page.",
            long="Le 9 voit large. {p} est sensible aux injustices et attiré{e} par ce qui dépasse sa propre vie. "
                 "Son chemin consiste à donner sans se perdre et à savoir clore les étapes."),
    11: dict(title="L'inspiré (nombre maître)", traits="intuition vive, capacité à inspirer, sensibilité hors du commun.",
             vigilance="Nervosité, hypersensibilité, anxiété quand l'idéal paraît hors d'atteinte.",
             long="Le 11 est un nombre maître, qui se vit aussi comme un 2. {p} capte beaucoup de choses et peut guider les autres. "
                  "Son chemin consiste à ancrer cette sensibilité dans le concret pour ne pas s'y épuiser."),
    22: dict(title="Le grand bâtisseur (nombre maître)", traits="capacité à donner forme à de grands projets, vision et sens pratique.",
             vigilance="Exigence écrasante envers soi, peur de ne pas être à la hauteur.",
             long="Le 22 est un nombre maître, qui se vit aussi comme un 4. {p} peut construire des choses durables et utiles au plus grand nombre. "
                  "Son chemin consiste à avancer par étapes, sans se laisser paralyser par l'ampleur de la tâche."),
    33: dict(title="Le guide (nombre maître)", traits="dévouement, sens de la transmission et du service.",
             vigilance="Sacrifice de soi, culpabilité, charge émotionnelle lourde.",
             long="Le 33 est un nombre maître, qui se vit aussi comme un 6. {p} a une vocation d'accompagnement et de transmission. "
                  "Son chemin consiste à prendre soin de soi autant que des autres."),
}

# ---------------------------------------------- Expression, Âme, Personnalité
EXPRESSION = {
    1: ("Le meneur", "volonté, esprit d'initiative, envie de faire les choses à sa façon.", "Impatience, mal à accepter la consigne."),
    2: ("Le diplomate", "tact, coopération, talent pour rapprocher les points de vue.", "Hésitation, difficulté à trancher."),
    3: ("Le créatif", "aisance à l'oral comme à l'écrit, sens artistique, sociabilité.", "Dispersion, légèreté dans les engagements."),
    4: ("L'organisateur", "rigueur, persévérance, goût des choses bien faites.", "Rigidité, routine pesante."),
    5: ("L'aventurier", "adaptabilité, vivacité, talent pour la nouveauté et le mouvement.", "Agitation, impatience."),
    6: ("Le conciliateur", "sens des responsabilités, esthétique, attention aux autres.", "Perfectionnisme, besoin de tout contrôler."),
    7: ("L'observateur", "esprit analytique, réflexion, intuition, goût du calme.", "Réserve, difficulté à montrer ce qu'{il} ressent."),
    8: ("Le gestionnaire", "efficacité, sens de l'organisation et des responsabilités.", "Dureté, rapport tendu au pouvoir."),
    9: ("L'altruiste", "ouverture, générosité, intérêt pour les autres cultures et les grandes causes.", "Idéalisme, dispersion."),
    11: ("L'inspirateur", "charisme discret, intuition, capacité à transmettre une vision.", "Nervosité, idéal trop élevé."),
    22: ("Le réalisateur", "capacité à concrétiser de grands projets avec méthode.", "Exigence excessive envers soi."),
    33: ("Le transmetteur", "pédagogie, dévouement, sens du service.", "Oubli de soi."),
}
SOUL = {
    1: ("Besoin d'autonomie", "désir profond de décider pour soi et d'être reconnu{e} pour ce qu'{il} accomplit.", "Orgueil blessé, peur de dépendre."),
    2: ("Besoin d'harmonie", "désir de paix, de complicité et d'être aimé{e} en douceur.", "Susceptibilité, besoin d'être rassuré{e}."),
    3: ("Cœur joyeux", "besoin profond de créer, de partager, d'être entendu{e}.", "Se froisser quand on ne {le|la} prend pas au sérieux."),
    4: ("Besoin de sécurité", "désir de stabilité, de repères clairs et de choses solides.", "Inquiétude face au changement."),
    5: ("Soif de liberté", "besoin de mouvement, de nouveauté, d'expériences concrètes.", "Ennui rapide, refus des routines."),
    6: ("Cœur protecteur", "besoin d'amour, de foyer et de prendre soin des siens.", "Oubli de soi, besoin d'approbation."),
    7: ("Besoin de sens", "désir de comprendre, de silence et de vie intérieure.", "Repli, sentiment d'être incompris{e}."),
    8: ("Besoin de réussir", "désir d'accomplissement, de reconnaissance et de maîtrise.", "Frustration quand les résultats tardent."),
    9: ("Cœur généreux", "besoin de donner, d'aider, de se sentir utile au monde.", "Déception face aux limites des autres."),
    11: ("Âme inspirée", "aspiration à un idéal, intuition profonde.", "Hypersensibilité."),
    22: ("Âme bâtisseuse", "désir de laisser une œuvre utile et durable.", "Pression intérieure."),
    33: ("Âme dévouée", "besoin profond de servir et de transmettre.", "Sacrifice de soi."),
}
PERSONALITY = {
    1: ("Image affirmée", "perçu{e} comme sûr{e} de soi, direct{e}, indépendant{e}.", "Peut paraître distant{e} ou autoritaire."),
    2: ("Image douce", "perçu{e} comme {gentil|gentille}, {attentif|attentive}, facile à vivre.", "Peut paraître effacé{e}."),
    3: ("Image vive", "perçu{e} comme drôle, {expressif|expressive}, sociable.", "Peut paraître {superficiel|superficielle}."),
    4: ("Image fiable", "perçu{e} comme {sérieux|sérieuse}, {soigneux|soigneuse}, raisonnable.", "Peut paraître rigide."),
    5: ("Image mobile", "perçu{e} comme {curieux|curieuse}, dynamique, toujours en mouvement.", "Peut paraître instable."),
    6: ("Image rassurante", "perçu{e} comme {chaleureux|chaleureuse}, fiable, {protecteur|protectrice}.", "Peut paraître envahissant{e}."),
    7: ("Image réservée", "perçu{e} comme {discret|discrète}, réfléchi{e}, un peu {mystérieux|mystérieuse}.", "Peut paraître froid{e}."),
    8: ("Image solide", "perçu{e} comme compétent{e}, déterminé{e}, à l'aise avec l'autorité.", "Peut impressionner."),
    9: ("Image ouverte", "perçu{e} comme bienveillant{e}, tolérant{e}, {généreux|généreuse}.", "Peut paraître lointain{e}."),
    11: ("Image lumineuse", "perçu{e} comme inspirant{e} et sensible.", "Peut paraître {nerveux|nerveuse}."),
    22: ("Image de bâtisseur", "perçu{e} comme quelqu'un sur qui on peut compter pour de grands projets.", "Peut paraître trop {sérieux|sérieuse}."),
    33: ("Image bienveillante", "perçu{e} comme une personne de confiance.", "Peut paraître trop dévoué{e}."),
}
BIRTHDAY = {
    1: ("Talent pour l'initiative et l'affirmation de soi.", "Peut vouloir tout faire seul{e}."),
    2: ("Talent pour l'écoute et la coopération.", "Peut douter de soi."),
    3: ("Talent pour l'expression et la créativité.", "Peut s'éparpiller."),
    4: ("Talent pour l'organisation et la régularité.", "Peut manquer de souplesse."),
    5: ("Talent pour l'adaptation et la découverte.", "Peut s'éparpiller."),
    6: ("Talent naturel pour l'entraide et l'attention aux proches.", "Peut chercher à faire plaisir pour être aimé{e}."),
    7: ("Talent pour l'analyse et l'intuition.", "Peut se replier."),
    8: ("Talent pour la gestion et la décision.", "Peut se montrer dur{e}."),
    9: ("Talent pour la compréhension des autres.", "Peut se disperser dans les causes des autres."),
    11: ("Intuition et sensibilité très vives.", "Nervosité."),
    22: ("Sens pratique au service de grandes idées.", "Exigence envers soi."),
}

# --------------------------------------------------------------- Leçons karmiques
KARMIC = {
    1: "le 1 manque : l'affirmation de soi et l'initiative s'apprendront par l'expérience.",
    2: "le 2 manque : la patience, la coopération et la diplomatie seront un terrain d'apprentissage.",
    3: "le 3 manque : oser s'exprimer et montrer sa créativité demandera un effort conscient.",
    4: "le 4 manque : la méthode, la régularité et l'organisation seront à construire.",
    5: "le 5 manque : accepter le changement et prendre des risques mesurés sera une leçon de vie.",
    6: "le 6 manque : la responsabilité, le sens du foyer et du service s'apprendront par l'expérience.",
    7: "le 7 manque : prendre du recul et cultiver sa vie intérieure demandera un effort.",
    8: "le 8 manque : le rapport à l'argent, au pouvoir et à l'autorité sera un terrain d'apprentissage.",
    9: "le 9 manque : l'ouverture aux autres et la tolérance seront à cultiver.",
}

MASTER_IN_NAME = {
    11: "l'inspirateur, intuition et capacité à guider",
    22: "le bâtisseur, capable de donner forme concrète à de grandes idées",
    33: "le guide, sens de la transmission et du service",
}

# --------------------------------------------------- Cycles, réalisations, défis
CYCLE = {1: "affirmation de soi", 2: "coopération, relations", 3: "expression, créativité",
         4: "travail, construction", 5: "liberté, changements", 6: "famille, responsabilités",
         7: "réflexion, intériorité", 8: "réussite matérielle, autorité", 9: "ouverture, générosité",
         11: "inspiration, sensibilité", 22: "grandes réalisations", 33: "transmission, service"}
REALIZATION = {1: "s'affirmer, prendre des initiatives", 2: "coopérer, s'associer",
               3: "s'exprimer, créer", 4: "construire, consolider", 5: "expérimenter, bouger",
               6: "prendre soin, s'engager", 7: "apprendre, approfondir", 8: "réussir, diriger",
               9: "transmettre, s'ouvrir au monde", 11: "inspirer, rayonner",
               22: "bâtir une œuvre durable", 33: "guider, enseigner"}
CHALLENGE = {0: "choisir sa voie parmi de nombreux talents", 1: "s'affirmer sans écraser",
             2: "gagner en confiance et en assurance", 3: "s'exprimer avec constance",
             4: "rigueur et patience", 5: "canaliser son besoin de liberté",
             6: "trouver l'équilibre entre soi et les autres", 7: "s'ouvrir et faire confiance",
             8: "maîtriser son rapport à l'argent et au pouvoir"}

# ------------------------------------------------------------- Année personnelle
PERSONAL_YEAR = {
    1: "une année de départ : nouveaux projets, affirmation, premiers pas dans un cycle de neuf ans.",
    2: "une année de patience et de relations : coopération, écoute, alliances à soigner.",
    3: "une année d'expression : rencontres, créativité, prise de parole.",
    4: "une année de construction : travail, organisation, fondations solides.",
    5: "une année de mouvement : changements, voyages, nouvelles expériences.",
    6: "une année centrée sur le foyer : famille, engagements, responsabilités affectives.",
    7: "une année plus intérieure : réflexion, apprentissage, besoin de calme.",
    8: "une année de structure et de résultats : affirmation, efforts récompensés, questions matérielles.",
    9: "une année de bilan : fin d'un cycle de neuf ans, tri, préparation du suivant.",
}

# --------------------------------------------------- Étiquettes pour la synthèse
TAGS = {
    1: {"affirmation", "indépendance", "action"}, 2: {"relation", "sensibilité", "harmonie"},
    3: {"expression", "créativité", "relation"}, 4: {"structure", "concret", "travail"},
    5: {"liberté", "mouvement", "curiosité"}, 6: {"soin", "famille", "harmonie"},
    7: {"réflexion", "intériorité", "curiosité"}, 8: {"ambition", "concret", "affirmation"},
    9: {"idéal", "ouverture", "soin"}, 11: {"sensibilité", "idéal", "intériorité"},
    22: {"structure", "ambition", "concret"}, 33: {"soin", "idéal", "famille"},
}
