"""Textes d'interprétation astrologique (mêmes variables que numbers.py)."""

SUN = {
    "Bélier": "Le Soleil en Bélier donne un tempérament direct, courageux et impatient. {p} aime commencer, relever des défis et passer à l'action sans attendre. Sa force est l'élan ; sa difficulté, la persévérance quand la nouveauté s'émousse.",
    "Taureau": "Le Soleil en Taureau donne un tempérament stable, patient et sensuel. {p} construit lentement mais solidement, aime le confort, la nature et les choses concrètes. Sa force est la constance ; sa difficulté, l'entêtement face au changement.",
    "Gémeaux": "Le Soleil en Gémeaux donne un esprit vif, curieux et bavard. {p} apprend vite, aime échanger, jongler entre plusieurs activités et comprendre comment tout fonctionne. Sa force est l'agilité ; sa difficulté, la dispersion.",
    "Cancer": "Le Soleil en Cancer donne une nature sensible, protectrice et attachée aux siens. {p} a besoin d'un foyer sûr et d'une famille unie pour s'épanouir. Sa force est la mémoire du cœur ; sa difficulté, la susceptibilité.",
    "Lion": "Le Soleil en Lion donne de la présence, de la chaleur et de la fierté. {p} aime briller, créer et être reconnu{e} pour ce qu'{il} fait. Sa force est la générosité ; sa difficulté, le besoin d'admiration.",
    "Vierge": "Le Soleil en Vierge donne un esprit précis, observateur et serviable. {p} remarque les détails, aime que les choses soient à leur place et se rend utile. Sa force est la rigueur ; sa difficulté, l'autocritique.",
    "Balance": "Le Soleil en Balance donne le sens de l'harmonie, de la justice et de la relation. {p} cherche l'équilibre, l'esthétique et le dialogue. Sa force est la diplomatie ; sa difficulté, l'indécision.",
    "Scorpion": "Le Soleil en Scorpion donne une nature intense, profonde et déterminée. {p} ressent fort, va au fond des choses et ne lâche pas facilement. Sa force est la ténacité ; sa difficulté, la méfiance.",
    "Sagittaire": "Le Soleil en Sagittaire donne de l'enthousiasme, de l'optimisme et le goût des horizons lointains. {p} aime apprendre, voyager et partager ses convictions. Sa force est la confiance ; sa difficulté, l'excès.",
    "Capricorne": "Le Soleil en Capricorne donne de l'ambition, du sérieux et le sens du long terme. {p} avance avec patience vers des objectifs élevés. Sa force est la persévérance ; sa difficulté, la dureté envers soi.",
    "Verseau": "Le Soleil en Verseau donne un esprit indépendant, original et attaché à l'équité. {p} pense autrement, aime le groupe mais garde sa liberté, et supporte mal l'autorité arbitraire. Sa force est l'inventivité ; sa difficulté, la distance affective.",
    "Poissons": "Le Soleil en Poissons donne une grande sensibilité, de l'imagination et de la compassion. {p} capte les ambiances et vit beaucoup de choses intérieurement. Sa force est l'empathie ; sa difficulté, se protéger des émotions des autres.",
}

MOON = {
    "Bélier": "Sa vie émotionnelle est vive et spontanée : {il} réagit vite, s'emporte parfois, mais oublie aussi vite. {Il} a besoin d'action pour évacuer ses tensions.",
    "Taureau": "Sa vie émotionnelle est calme et stable : {il} a besoin de repères, de confort et de régularité pour se sentir en sécurité. Les changements brusques l'inquiètent.",
    "Gémeaux": "Sa vie émotionnelle passe par les mots : {il} se calme en parlant, en posant des questions, en racontant. Le silence et l'ennui lui pèsent.",
    "Cancer": "Sa vie émotionnelle est profonde et tournée vers la famille : {il} a besoin de tendresse, de présence et d'un foyer chaleureux.",
    "Lion": "Sa vie émotionnelle a besoin de chaleur et de reconnaissance : {il} s'épanouit quand on remarque ses efforts et qu'on lui fait confiance.",
    "Vierge": "Sa vie émotionnelle passe par l'utile et le concret : {il} se rassure en organisant, en aidant, en comprenant. {Il} peut s'inquiéter pour des détails.",
    "Balance": "Sa vie émotionnelle a besoin d'harmonie : les disputes l'affectent beaucoup, et {il} se sent bien dans une atmosphère douce et équitable.",
    "Scorpion": "Sa vie émotionnelle est intense et discrète : {il} ressent fort, garde beaucoup pour soi et accorde sa confiance lentement, mais pour longtemps.",
    "Sagittaire": "Sa vie émotionnelle est optimiste et a besoin d'espace : {il} se ressource dans la découverte, le mouvement et les projets.",
    "Capricorne": "Sa vie émotionnelle est pudique et responsable : {il} montre peu ses sentiments et se rassure par la maîtrise et l'effort.",
    "Verseau": "Sa vie émotionnelle a besoin d'indépendance : {il} aime ses proches à sa manière, sans être étouffé{e}, et se sent bien entouré{e} d'amis.",
    "Poissons": "Sa vie émotionnelle est très perméable : {il} ressent les émotions des autres comme les siennes et a besoin de moments de calme et de rêverie.",
}

ASC = {
    "Bélier": "L'ascendant Bélier donne une allure énergique et franche : {p} se lance, réagit vite et ne passe pas inaperçu{e}.",
    "Taureau": "L'ascendant Taureau donne une présence posée et rassurante : {p} prend son temps, avance sûrement et apprécie les plaisirs simples.",
    "Gémeaux": "L'ascendant Gémeaux donne une allure vive, mobile et joueuse : {p} communique facilement et s'adapte vite.",
    "Cancer": "L'ascendant Cancer donne une approche douce et protectrice : {p} observe avant de s'ouvrir et crée vite un climat familial.",
    "Lion": "L'ascendant Lion donne de la présence et de la chaleur : {p} a un certain sens de la scène et aime qu'on {le|la} remarque quand {il} réussit.",
    "Vierge": "L'ascendant Vierge donne une approche discrète et soignée : {p} observe, analyse et se rend utile avant de se mettre en avant.",
    "Balance": "L'ascendant Balance donne de la grâce et du tact : {p} cherche à plaire, à apaiser et à créer du lien.",
    "Scorpion": "L'ascendant Scorpion donne une présence intense et magnétique : {p} se protège derrière une certaine réserve et perce vite les gens à jour.",
    "Sagittaire": "L'ascendant Sagittaire donne une allure ouverte et enthousiaste : {p} va vers les autres et voit les choses en grand.",
    "Capricorne": "L'ascendant Capricorne donne une allure sérieuse et maîtrisée : {p} paraît plus mûr{e} que son âge et inspire confiance.",
    "Verseau": "L'ascendant Verseau donne une allure originale et indépendante : {p} surprend, pense autrement et défend sa liberté.",
    "Poissons": "L'ascendant Poissons donne une présence douce et rêveuse : {p} est très {réceptif|réceptive} à son environnement et à l'humeur des autres.",
}

HOUSE = {
    1: "la maison 1, celle de la personnalité et de l'image de soi",
    2: "la maison 2, celle des ressources, des talents et de la sécurité matérielle",
    3: "la maison 3, celle de la communication, des apprentissages et de la fratrie",
    4: "la maison 4, celle du foyer, de la famille et des racines",
    5: "la maison 5, celle de la créativité, du jeu et du plaisir",
    6: "la maison 6, celle du quotidien, du travail et de la santé",
    7: "la maison 7, celle des relations, du couple et des partenaires",
    8: "la maison 8, celle des transformations et de ce qui est caché",
    9: "la maison 9, celle des études, des voyages et des grandes idées",
    10: "la maison 10, celle de la vocation, de la réussite et du rôle social",
    11: "la maison 11, celle des amis, des groupes et des projets",
    12: "la maison 12, celle de la vie intérieure et de ce qui se joue en coulisses",
}
HOUSE_SUN = {
    1: "son identité est très visible, {il} s'affirme par sa personne même.",
    2: "{il} se construit en développant ses talents et une sécurité concrète.",
    3: "{il} s'épanouit dans l'apprentissage, l'échange et les déplacements.",
    4: "la famille et le foyer sont au centre de sa construction.",
    5: "{il} brille par la créativité, le jeu et l'expression personnelle.",
    6: "{il} se réalise en se rendant utile et en perfectionnant ses méthodes.",
    7: "{il} se construit beaucoup à travers les autres et les partenariats.",
    8: "{il} voudra comprendre ce qui est caché, comment fonctionnent les choses et pourquoi.",
    9: "{il} cherche le sens, les connaissances et les horizons lointains.",
    10: "la réussite et le rôle social comptent beaucoup pour {lui}.",
    11: "les amis, le groupe et les projets collectifs {le|la} portent.",
    12: "une part de sa force agit en coulisses, et {il} a besoin de retrait pour se ressourcer.",
}

# Style d'un signe, pour composer Mercure / Vénus / Mars.
STYLE = {
    "Bélier": "rapide, directe et parfois impatiente", "Taureau": "lente, concrète et tenace",
    "Gémeaux": "vive, curieuse et changeante", "Cancer": "sensible, protectrice et intuitive",
    "Lion": "chaleureuse, fière et généreuse", "Vierge": "précise, analytique et soigneuse",
    "Balance": "diplomate, élégante et soucieuse d'équilibre", "Scorpion": "intense, profonde et secrète",
    "Sagittaire": "enthousiaste, franche et tournée vers le large", "Capricorne": "sérieuse, structurée et prudente",
    "Verseau": "originale, indépendante et inventive", "Poissons": "intuitive, imaginative et douce",
}
DOMAIN = {
    "Mercure": "Mercure en {sign} : sa façon de penser et de communiquer est {style}.",
    "Vénus": "Vénus en {sign} : sa manière d'aimer et ce qui lui plaît sont marqués par une sensibilité {style}.",
    "Mars": "Mars en {sign} : sa manière d'agir et de se défendre est {style}.",
}

MC = {
    "Bélier": "le sport, l'entrepreneuriat, les métiers d'action", "Taureau": "la finance, l'agriculture, l'artisanat, les arts",
    "Gémeaux": "la communication, l'enseignement, le commerce", "Cancer": "le soin, l'éducation, l'immobilier",
    "Lion": "la création, la direction, les métiers de scène", "Vierge": "la santé, l'analyse, les métiers de précision",
    "Balance": "le droit, la médiation, le design", "Scorpion": "la recherche, la psychologie, la gestion de crise",
    "Sagittaire": "l'international, l'enseignement, le droit", "Capricorne": "la gestion, l'administration, l'ingénierie",
    "Verseau": "les technologies, l'innovation, l'associatif", "Poissons": "les arts, le soin, l'accompagnement",
}

ELEMENT_DOMINANT = {
    "Feu": "L'élément Feu domine : énergie, enthousiasme, besoin d'agir et d'être reconnu{e}.",
    "Terre": "L'élément Terre domine : sens du concret, patience, besoin de résultats tangibles.",
    "Air": "L'élément Air domine : curiosité, communication, besoin d'idées et d'échanges.",
    "Eau": "L'élément Eau domine : sensibilité, intuition, besoin de liens affectifs profonds.",
}
ELEMENT_MISSING = {
    "Feu": "Le Feu est peu présent : l'élan et la confiance en soi gagneront à être encouragés.",
    "Terre": "La Terre est peu présente : le sens pratique et la régularité seront à cultiver.",
    "Air": "L'Air est peu présent : prendre du recul et mettre des mots sur les choses demandera un effort.",
    "Eau": "L'Eau est peu présente : exprimer ses émotions ne viendra pas toujours naturellement.",
}

PLANET_KW = {
    "Soleil": "l'identité", "Lune": "les émotions", "Mercure": "l'intelligence", "Vénus": "l'affection",
    "Mars": "l'énergie", "Jupiter": "la confiance", "Saturne": "la rigueur", "Uranus": "l'originalité",
    "Neptune": "l'imaginaire", "Pluton": "l'intensité", "Ascendant": "l'image de soi", "Milieu du Ciel": "la vocation",
}
ASPECT_TXT = {
    "conjonction": "{A} et {B} sont réunis : {ka} et {kb} agissent ensemble et se renforcent.",
    "trigone": "{A} forme un trigone à {B} : {ka} et {kb} s'accordent naturellement, c'est une facilité.",
    "sextile": "{A} forme un sextile à {B} : entre {ka} et {kb}, un soutien discret, une ressource à cultiver.",
    "carré": "{A} forme un carré à {B} : {ka} et {kb} se frottent, ce qui crée des tensions mais aussi de la motivation.",
    "opposition": "{A} s'oppose à {B} : {ka} et {kb} tirent dans deux directions, l'enjeu est de trouver l'équilibre.",
}

PHASE_NOTE = "{p} est né{e} en {phase}."

TAGS = {
    "Bélier": {"action", "affirmation", "indépendance"}, "Taureau": {"concret", "structure", "harmonie"},
    "Gémeaux": {"expression", "curiosité", "mouvement"}, "Cancer": {"famille", "soin", "sensibilité"},
    "Lion": {"expression", "créativité", "affirmation"}, "Vierge": {"concret", "structure", "soin"},
    "Balance": {"relation", "harmonie", "créativité"}, "Scorpion": {"intériorité", "sensibilité", "ambition"},
    "Sagittaire": {"liberté", "idéal", "ouverture"}, "Capricorne": {"ambition", "structure", "travail"},
    "Verseau": {"indépendance", "idéal", "liberté"}, "Poissons": {"sensibilité", "idéal", "intériorité"},
}
TAG_LABEL = {
    "affirmation": "un caractère affirmé", "indépendance": "un fort besoin d'indépendance",
    "action": "le goût de l'action", "relation": "l'importance des relations", "sensibilité": "une grande sensibilité",
    "harmonie": "le besoin d'harmonie", "expression": "le besoin de s'exprimer", "créativité": "la créativité",
    "structure": "le sens de la structure", "concret": "le sens du concret", "travail": "le goût de l'effort",
    "liberté": "le besoin de liberté", "mouvement": "le besoin de mouvement", "curiosité": "la curiosité",
    "soin": "l'attention aux autres", "famille": "l'attachement à la famille", "réflexion": "le goût de la réflexion",
    "intériorité": "une riche vie intérieure", "ambition": "l'ambition", "idéal": "l'idéalisme",
    "ouverture": "l'ouverture au monde",
}
