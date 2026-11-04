"""Assemble les calculs et les textes en une lecture structurée, prête à mettre en page.

Ce module ne connaît pas le PDF : il produit des données (titres, paragraphes,
tableaux) que les gabarits de produits réutilisent.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime

from . import astro, numerology, places
from .texts import astro_texts as AT
from .texts import guidance as GD
from .texts import numbers as NT


# ------------------------------------------------------------------ personne
@dataclass
class Person:
    prenoms: str
    nom: str
    sexe: str                       # "M" ou "F", comme sur l'acte
    naissance: date
    heure: str | None               # "HH:MM" ou None si inconnue
    lieu: str                       # texte libre, ex. « Akanda, Gabon »
    prenom_usuel: str | None = None
    lat: float | None = None        # pour un lieu absent de la table
    lon: float | None = None
    tz: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.prenoms} {self.nom}".strip()

    @property
    def first(self) -> str:
        return (self.prenom_usuel or self.prenoms.split()[0]).strip().capitalize()

    @property
    def feminine(self) -> bool:
        return self.sexe.upper().startswith("F")

    def place(self) -> places.Place:
        if self.lat is not None and self.lon is not None:
            return places.Place(self.lieu, self.lat, self.lon, self.tz or "Africa/Libreville")
        return places.resolve(self.lieu)

    def age(self, today: date) -> int:
        b = self.naissance
        return today.year - b.year - ((today.month, today.day) < (b.month, b.day))


_ALT = re.compile(r"\{([^{}|]*)\|([^{}]*)\}")


def g(text: str, person: Person) -> str:
    """Accorde un texte au sexe de la personne et insère son prénom."""
    f = person.feminine
    text = _ALT.sub(lambda m: m.group(2) if f else m.group(1), text)
    return (text.replace("{p}", person.first)
                .replace("{Il}", "Elle" if f else "Il")
                .replace("{il}", "elle" if f else "il")
                .replace("{lui}", "elle" if f else "lui")
                .replace("{e}", "e" if f else ""))


def ucfirst(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


# ------------------------------------------------------------------- lecture
@dataclass
class Reading:
    person: Person
    today: date
    num: numerology.Numerology
    chart: astro.Chart
    place: places.Place
    is_child: bool


def build(person: Person, today: date | None = None) -> Reading:
    today = today or date.today()
    num = numerology.compute(person.full_name, person.naissance, today)
    pl = person.place()
    if person.heure:
        hh, mm = (int(x) for x in person.heure.replace("h", ":").split(":")[:2])
        has_time = True
    else:
        hh, mm, has_time = 12, 0, False
    local = datetime(person.naissance.year, person.naissance.month, person.naissance.day, hh, mm)
    chart = astro.compute(local, pl.utc_offset(local), pl.lat, pl.lon, has_time)
    return Reading(person, today, num, chart, pl, person.age(today) < 16)


# --------------------------------------------------------- numérologie : textes
def numerology_rows(r: Reading) -> list[list[str]]:
    n, p = r.num, r.person
    lp = NT.LIFE_PATH[n.life_path]
    rows = [[f"<b>Chemin de vie {n.life_path}</b>", f"<b>{lp['title']}</b> : {lp['traits']}", lp["vigilance"]]]
    for label, val, table in (("Expression", n.expression, NT.EXPRESSION), ("Âme", n.soul, NT.SOUL),
                              ("Personnalité", n.personality, NT.PERSONALITY)):
        t, traits, vig = table[val]
        rows.append([f"<b>{label} {val}</b>", f"<b>{t}</b> : {traits}", vig])
    bd = n.birthday_reduced
    t1, t2 = NT.BIRTHDAY[bd]
    lbl = f"Jour {n.birthday}" + (f" ({bd})" if n.birthday != bd else "")
    rows.append([f"<b>{lbl}</b>", t1, t2])
    masters = []
    for w, v in n.masters_in_name:
        masters.append(f"<b>{v}</b> dans « {w} » : {NT.MASTER_IN_NAME[v]}")
    for i, rz in enumerate(n.realizations):
        if rz["number"] in numerology.MASTERS:
            span = f"{rz['from']}–{rz['to']} ans" if rz["to"] else f"à partir de {rz['from']} ans"
            masters.append(f"<b>{rz['number']}</b> en réalisation {i + 1} ({span})")
    if n.life_path in numerology.MASTERS:
        masters.append(f"<b>{n.life_path}</b> au chemin de vie lui-même")
    if masters:
        rows.append(["<b>Nombres maîtres</b>", ". ".join(masters) + ".",
                     "Les nombres maîtres s'accompagnent souvent d'une forte exigence ou d'une sensibilité nerveuse."])
    if n.karmic_lessons:
        k = n.karmic_lessons
        lbl = ("Leçons karmiques " if len(k) > 1 else "Leçon karmique ") + ", ".join(map(str, k))
        rows.append([f"<b>{lbl}</b>", " ".join(ucfirst(NT.KARMIC[i]) for i in k),
                     "Ce qui manque dans le nom se travaille par l'expérience, sans fatalité."])
    return [[g(c, p) for c in row] for row in rows]


def numerology_calc_text(r: Reading) -> str:
    n = r.num
    return (f"<b>Chemin de vie</b> : {n.calc_life_path()}. "
            f"<b>Expression</b> (toutes les lettres) : {n.calc_expression()}. "
            f"<b>Âme</b> (voyelles, Y compris) : {n.calc_soul()}. "
            f"<b>Personnalité</b> (consonnes) : {n.calc_personality()}. "
            f"<b>Maturité</b> (Expression + Chemin de vie) : {n.maturity}.")


def numerology_overview(r: Reading) -> str:
    n, p = r.num, r.person
    lp = NT.LIFE_PATH[n.life_path]
    parts = [lp["long"]]
    if numerology.base(n.soul) == numerology.base(n.personality):
        parts.append(f"Le doublé <b>{n.soul}</b> en Âme et en Personnalité est un trait fort : ce que {{p}} ressent et ce "
                     f"qu'{{il}} montre vont dans le même sens. Le besoin intérieur ({NT.SOUL[n.soul][0].lower()}) "
                     f"se voit aussi de l'extérieur.")
    else:
        st = NT.SOUL[n.soul][0]
        art = "une" if st.split()[0] in ("Soif", "Âme") else "un"
        parts.append(f"Au fond {{de lui|d'elle}}, l'<b>Âme {n.soul}</b> dessine {art} {st.lower()} : "
                     f"{NT.SOUL[n.soul][1].rstrip('.')}. Vers l'extérieur, la <b>Personnalité {n.personality}</b> "
                     f"renvoie une {NT.PERSONALITY[n.personality][0].lower()} : "
                     f"{NT.PERSONALITY[n.personality][1].rstrip('.')}. On peut donc mal le{{la}} cerner au premier abord.")
    parts.append(f"Le nombre de maturité <b>{n.maturity}</b> annonce ce vers quoi la personnalité tend avec l'âge : "
                 f"{NT.CYCLE[n.maturity]}.")
    return g(" ".join(parts).replace("le{la}", "{le|la}"), p)


def cycles_rows(r: Reading) -> list[list[str]]:
    n = r.num
    labels = []
    for rz in n.realizations:
        labels.append(f"{rz['from']} – {rz['to']} ans" if rz["to"] else f"{rz['from']} ans et +")
    cyc = [n.cycles[0], n.cycles[1], n.cycles[1], n.cycles[2]]
    rows = [["Période", "Cycle de vie", "Réalisation", "Défi"]]
    for i in range(4):
        c = cyc[i]
        ctext = f"<b>{c['number']}</b> · {NT.CYCLE[c['number']]}" if i != 2 else f"<b>{c['number']}</b> · (suite)"
        rz = n.realizations[i]
        d = n.challenges[i]
        dtext = f"<b>{d}</b> · " + ("défi principal : " if i == 2 else "") + NT.CHALLENGE[d]
        rows.append([labels[i], ctext, f"<b>{rz['number']}</b> · {NT.REALIZATION[rz['number']]}", dtext])
    return rows


def cycles_comment(r: Reading) -> str:
    n, p = r.num, r.person
    age = p.age(r.today)
    cur = 0
    for i, rz in enumerate(n.realizations):
        if rz["to"] is None or age <= rz["to"]:
            cur = i
            break
    rz = n.realizations[cur]
    main = n.challenges[2]
    txt = (f"À {age} an{'s' if age > 1 else ''}, {{p}} est dans sa <b>réalisation {cur + 1}</b>, placée sous le "
           f"<b>{rz['number']}</b> : {NT.REALIZATION[rz['number']]}. Le <b>défi principal</b>, le {main}, porte sur "
           f"un point précis : {NT.CHALLENGE[main]}. C'est là que se jouera une bonne part de l'effort conscient.")
    return g(txt, p)


def _py_label(n: int) -> str:
    return f"{n} (nombre maître, vécue comme un {numerology.base(n)})" if n in numerology.MASTERS else str(n)


def personal_year_text(r: Reading) -> str:
    n, p = r.num, r.person
    a, b = n.personal_years
    fmt = lambda d: f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    txt = (f"En {a['year']}, {{p}} vit une <b>année {_py_label(a['number'])}</b>, "
           f"{NT.PERSONAL_YEAR[numerology.base(a['number'])]} "
           f"Le 1er janvier {b['year']} s'ouvrira une <b>année {_py_label(b['number'])}</b>, "
           f"{NT.PERSONAL_YEAR[numerology.base(b['number'])]}")
    return g(txt, p)


MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
          "septembre", "octobre", "novembre", "décembre"]


# ----------------------------------------------------------- astrologie : textes
def chart_rows(r: Reading) -> list[list[str]]:
    c = r.chart
    rows = [["Point", "Position", "Maison"]]
    for name, pl in c.planets.items():
        if name == "Lune" and not c.moon_sign_certain:
            pos = f"{pl.sign} (position à midi, heure inconnue)"
        else:
            pos = pl.pos + (" (rétrograde)" if pl.retro else "")
        rows.append([name, pos, str(pl.house) if pl.house else "—"])
    if c.asc is not None:
        rows.append(["<b>Ascendant</b>", f"<b>{astro.fmt(c.asc)}</b>", "1"])
        rows.append(["<b>Milieu du Ciel</b>", f"<b>{astro.fmt(c.mc)}</b>", "10"])
    return rows


def chart_note(r: Reading) -> str:
    c, p = r.chart, r.person
    notes = []
    if not c.has_time:
        notes.append("Heure de naissance inconnue : le thème est calculé pour midi, sans ascendant ni maisons.")
    else:
        before, after = c.asc_change_minutes
        margin = min(x for x in (before, after) if x is not None) if (before or after) else None
        if margin is not None and margin <= 20:
            when = "avant" if before == margin else "après"
            notes.append(f"Point de vigilance : l'ascendant change de signe {margin} minutes {when} l'heure indiquée. "
                         "Si l'heure de l'acte a été arrondie, la lecture de l'ascendant peut changer.")
        else:
            notes.append(f"L'ascendant reste en {c.asc_sign} au moins {margin or 60} minutes autour de l'heure indiquée : "
                         "pas besoin de vérifier l'heure de l'acte.")
    notes.append(g(AT.PHASE_NOTE.replace("{phase}", c.moon_phase), p))
    return " ".join(notes)


def chart_sections(r: Reading) -> list[tuple[str, str]]:
    """Liste de (sous-titre, paragraphe) pour la lecture du thème."""
    c, p = r.chart, r.person
    P = c.planets
    out = []
    sun = P["Soleil"]
    title = f"Soleil en {sun.sign}" + (f", maison {sun.house}" if sun.house else "")
    conj = [a.b if a.a == "Soleil" else a.a for a in c.aspects
            if a.kind == "conjonction" and "Soleil" in (a.a, a.b) and a.b not in ("Ascendant", "Milieu du Ciel")]
    if conj:
        title += ", conjoint à " + " et ".join(conj)
    txt = AT.SUN[sun.sign]
    if sun.house:
        txt += f" En {AT.HOUSE[sun.house].replace('la maison', 'maison', 1)}, le Soleil oriente cette énergie : " + AT.HOUSE_SUN[sun.house]
    out.append((title, g(txt, p)))

    moon = P["Lune"]
    title = f"Lune en {moon.sign}" + (f", maison {moon.house}" if moon.house else "")
    txt = AT.MOON[moon.sign]
    if not c.moon_sign_certain:
        txt += " (L'heure étant inconnue, la Lune a pu changer de signe ce jour-là ; cette lecture reste indicative.)"
    if moon.house:
        txt += f" En maison {moon.house}, ses émotions se vivent surtout dans le domaine " + AT.HOUSE[moon.house].split("celle ")[1] + "."
    out.append((title, g(txt, p)))

    if c.asc is not None:
        asc = c.asc_sign
        same = [n for n in ("Soleil", "Lune") if P[n].sign == asc]
        title = f"Ascendant {asc}"
        txt = AT.ASC[asc]
        if same:
            txt += f" Avec {' et '.join('le Soleil' if n == 'Soleil' else 'la Lune' for n in same)} dans le même signe, cet accent {asc} est particulièrement marqué."
        out.append((title, g(txt, p)))

    st = c.stelliums()
    for sign, ps in st:
        txt = (f"{', '.join(ps[:-1])} et {ps[-1]} sont réunis en {sign} : ce signe pèse lourd dans le thème et "
               f"colore toute la personnalité ({AT.STYLE[sign].split(' et ')[0]}).")
        out.append((f"Concentration de planètes en {sign}", g(txt, p)))

    trio = " ".join(AT.DOMAIN[n].format(sign=P[n].sign, style=AT.STYLE[P[n].sign]) for n in ("Mercure", "Vénus", "Mars"))
    out.append(("Mercure, Vénus et Mars", g(trio, p)))

    el = c.elements
    top = max(el.values())
    doms = [e for e, v in el.items() if v == top]
    if len(doms) == 1:
        txt = AT.ELEMENT_DOMINANT[doms[0]]
    else:
        names = {"Feu": "le Feu", "Terre": "la Terre", "Air": "l'Air", "Eau": "l'Eau"}
        lst = [names[e] for e in doms]
        txt = (ucfirst(", ".join(lst[:-1]) + " et " + lst[-1]) + " dominent à égalité, ce qui donne un "
               "tempérament polyvalent, capable de passer d'un registre à l'autre.")
    weak = [e for e, v in el.items() if v == 0]
    if weak:
        txt += " " + " ".join(AT.ELEMENT_MISSING[e] for e in weak)
    out.append(("Équilibre des éléments", g(txt, p)))

    key = [a for a in c.aspects if a.b not in ("Ascendant",)][:3]
    if key:
        lines = []
        for a in key:
            lines.append(AT.ASPECT_TXT[a.kind].format(
                A=_art(a.a), B=_art(a.b, de=False), ka=AT.PLANET_KW[a.a], kb=AT.PLANET_KW[a.b]))
        out.append(("Les aspects les plus serrés", g(" ".join(ucfirst(x) for x in lines), p)))

    if c.mc is not None:
        mcs = c.mc_sign
        out.append((f"Milieu du Ciel en {mcs}",
                    g(f"Le Milieu du Ciel indique une direction de vocation : {AT.MC[mcs]}. "
                      "C'est une piste parmi d'autres, que l'expérience confirmera ou non.", p)))
    return out


def _art(name: str, de: bool = True) -> str:
    if name == "Lune":
        return "la Lune"
    if name == "Vénus":
        return "Vénus"
    if name in ("Ascendant",):
        return "l'Ascendant"
    if name == "Milieu du Ciel":
        return "le Milieu du Ciel"
    if name == "Uranus":
        return "Uranus"
    if name in ("Mercure", "Mars", "Jupiter", "Saturne", "Neptune", "Pluton"):
        return name
    return "le " + name


# --------------------------------------------------------------- synthèse
def synthesis_points(r: Reading) -> dict:
    """Points clés de la synthèse, sous forme de données (pour la capsule vidéo).

    Renvoie {"tags": [étiquettes communes aux deux lectures], "defi": texte du défi principal}.
    """
    n, c = r.num, r.chart
    num_src = [NT.TAGS[n.life_path], NT.TAGS[n.soul], NT.TAGS[n.expression]]
    ast_src = [AT.TAGS[c.planets["Soleil"].sign], AT.TAGS[c.planets["Lune"].sign]]
    if c.asc is not None:
        ast_src.append(AT.TAGS[c.asc_sign])
    st = c.stelliums()
    if st:
        ast_src.insert(0, AT.TAGS[st[0][0]])
    tags, used_src = [], set()
    for nt in num_src:
        for i, at in enumerate(ast_src):
            if i in used_src:
                continue
            common = (nt & at) - set(tags)
            if common:
                tags.append(sorted(common)[0])
                used_src.add(i)
                break
    if not tags:
        tags = [sorted(NT.TAGS[n.life_path])[0], sorted(AT.TAGS[c.planets["Soleil"].sign])[0]]
    return {"tags": tags[:3], "defi": NT.CHALLENGE[n.challenges[2]]}


def synthesis(r: Reading) -> str:
    n, c, p = r.num, r.chart, r.person
    num_src = [(f"le chemin de vie {n.life_path}", NT.TAGS[n.life_path]),
               (f"l'Âme {n.soul}", NT.TAGS[n.soul]), (f"l'Expression {n.expression}", NT.TAGS[n.expression])]
    ast_src = [(f"le Soleil en {c.planets['Soleil'].sign}", AT.TAGS[c.planets["Soleil"].sign]),
               (f"la Lune en {c.planets['Lune'].sign}", AT.TAGS[c.planets["Lune"].sign])]
    if c.asc is not None:
        ast_src.append((f"l'ascendant {c.asc_sign}", AT.TAGS[c.asc_sign]))
    st = c.stelliums()
    if st:
        ast_src.insert(0, (f"la concentration de planètes en {st[0][0]}", AT.TAGS[st[0][0]]))

    found, used, used_src = [], set(), set()
    for nl, nt in num_src:
        for al, at in ast_src:
            if al in used_src:
                continue
            common = (nt & at) - used
            if common:
                tag = sorted(common)[0]
                used.add(tag)
                used_src.add(al)
                found.append(ucfirst(f"{nl} et {al} disent tous deux {AT.TAG_LABEL[tag]}."))
                break
        if len(found) >= 3:
            break
    parts = []
    if found:
        parts.append("Les deux lectures se rejoignent nettement. " + " ".join(found))
    else:
        parts.append("Les deux lectures se complètent plus qu'elles ne se répètent : la numérologie décrit "
                     f"{AT.TAG_LABEL[sorted(NT.TAGS[n.life_path])[0]]}, l'astrologie ajoute "
                     f"{AT.TAG_LABEL[sorted(AT.TAGS[c.planets['Soleil'].sign])[0]]}.")
    hard = [a for a in c.aspects if a.kind in ("carré", "opposition")]
    main = n.challenges[2]
    work = f"Le point de travail, du côté des nombres, est le défi {main} : {NT.CHALLENGE[main]}."
    if hard:
        a = hard[0]
        work += (f" Côté astres, {_art(a.a)} et {_art(a.b, de=False)} sont en {a.kind} : "
                 f"il faudra concilier {AT.PLANET_KW[a.a]} et {AT.PLANET_KW[a.b]}.")
    parts.append(work)
    return g(" ".join(parts), p)


def guidance(r: Reading) -> tuple[str, list[str]]:
    """(titre, paragraphes) des pistes concrètes."""
    n, c, p = r.num, r.chart, r.person
    base = numerology.base(n.life_path)
    dom = c.dominant_element()
    if r.is_child:
        gd = GD.CHILD[base]
        paras = [
            "<b>Activités qui lui conviennent</b> : " + ", ".join(gd["activities"]) + ". " + GD.CHILD_ELEMENT[dom],
            "<b>Sa manière d'apprendre</b> : " + gd["learning"][0].lower() + gd["learning"][1:],
            "<b>Orientations possibles, à long terme</b> : " + gd["orientations"] + ". "
            "À cet âge, ses goûts réels et ce qui le{la} fait vibrer compteront bien davantage.",
        ]
        return "Pistes d'accompagnement", [g(x.replace("le{la}", "{le|la}"), p) for x in paras]
    gd = GD.ADULT[base]
    py = n.personal_years[0]
    paras = [
        "<b>Forces à exploiter</b> : " + gd["strengths"] + ".",
        "<b>Domaines où ces forces s'expriment bien</b> : " + gd["careers"] + "."
        + (f" Le Milieu du Ciel en {c.mc_sign} ajoute une piste : {AT.MC[c.mc_sign]}." if c.mc is not None else ""),
        "<b>Conseil de fond</b> : " + gd["advice"][0].lower() + gd["advice"][1:],
        f"<b>Pour {py['year']}</b> : année {_py_label(py['number'])}, {NT.PERSONAL_YEAR[numerology.base(py['number'])]}",
    ]
    return "Pistes concrètes", [g(x, p) for x in paras]
