"""Produit « Famille » : jusqu'à 6 adultes et 10 enfants, avec le lien réel de chacun.

Contenu : la famille en un coup d'œil, sa dynamique (familles de nombres, éléments, nombre de la famille),
les liens entre chaque enfant et les adultes qui l'élèvent, des pistes d'accompagnement par enfant,
puis en annexe le chemin de vie complet de chaque membre.
"""
from __future__ import annotations

from collections import Counter
from datetime import date

from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer

from .. import astro as AS
from .. import numerology as NU
from .. import pdf_style as ST
from .. import reading as RD
from ..reading import Person
from ..texts import compat_texts as CT
from ..texts import famille_texts as FT
from ..texts import numbers as NT
from . import _doc, chemin_de_vie

PRODUCT_LABEL = "ÉTUDE FAMILLE  ·  NUMÉROLOGIE  ·  ASTROLOGIE"
ROLES_ENFANTS = {"Fils", "Fille", "Neveu", "Nièce", "Petit-fils", "Petite-fille", "Petit frère", "Petite sœur",
                 "Enfant"}
MAX_ADULTES, MAX_ENFANTS = 6, 10


class FamilleError(ValueError):
    pass


def _fam(r):
    return CT.FAMILY[NU.base(r.num.life_path)]


def _link(adult, child) -> str:
    A, E = adult.person.first, child.person.first
    if adult.num.life_path == child.num.life_path:
        t = FT.LINK_IDENTICAL
    elif _fam(adult) == _fam(child):
        t = FT.LINK_SAME
    else:
        t = FT.LINK_CROSS[frozenset([_fam(adult), _fam(child)])]
    return RD.g(t.replace("{a}", A).replace("{enf}", E), child.person)


def analyse(people: list[Person], roles: list[str], today: date):
    if len(people) < 2:
        raise FamilleError("Le pack Famille demande au moins deux personnes.")
    reads = [RD.build(p, today) for p in people]
    membres = [dict(r=r, role=(roles[i] if i < len(roles) and roles[i] else ("Adulte" if i == 0 else "Enfant")))
               for i, r in enumerate(reads)]
    adults = [m for m in membres if m["role"] not in ROLES_ENFANTS]
    kids = [m for m in membres if m["role"] in ROLES_ENFANTS]
    if len(adults) > MAX_ADULTES or len(kids) > MAX_ENFANTS:
        raise FamilleError(f"Le pack Famille accepte {MAX_ADULTES} adultes et {MAX_ENFANTS} enfants au plus.")
    if not adults:
        raise FamilleError("Indiquez au moins un adulte qui élève les enfants.")
    fams = Counter(_fam(m["r"]) for m in membres)
    elements = Counter(AS.ELEMENT[m["r"].chart.planets["Soleil"].sign] for m in membres)
    raw = sum(m["r"].num.life_path for m in membres)
    nombre = NU.reduce(raw, True)
    partages = Counter(m["r"].num.life_path for m in membres)
    return dict(membres=membres, adults=adults, kids=kids, fams=fams, elements=elements, raw=raw,
                nombre=nombre, partages={n: c for n, c in partages.items() if c > 1})


def story(S, x) -> list:
    P = lambda t, s="body": Paragraph(t, S[s])
    M, adults, kids = x["membres"], x["adults"], x["kids"]
    out = [P("Avant de lire", "h1"), P("Méthode et précautions", "h1s"),
           P(f"Cette étude réunit <b>{len(M)} membres</b> d'une même famille : {len(adults)} adulte"
             f"{'s' if len(adults) > 1 else ''} et {len(kids)} enfant{'s' if len(kids) > 1 else ''}. "
             "Elle présente d'abord la famille dans son ensemble, puis les liens entre chaque enfant et les adultes "
             "qui l'élèvent, et enfin le chemin de vie complet de chacun."),
           P(FT.RAISED_BY), Spacer(1, 6),
           ST.box([P("La numérologie et l'astrologie n'ont pas de fondement scientifique. Cette étude ne dit pas "
                     "ce qu'un enfant deviendra : elle propose des repères pour mieux le comprendre et l'accompagner.",
                     "note")]),
           PageBreak()]

    rows = [["Lien", "Prénom", "Chemin de vie", "Soleil"]]
    for m in M:
        r = m["r"]
        rows.append([m["role"], r.person.first, f"<b>{r.num.life_path}</b> · {NT.LIFE_PATH[r.num.life_path]['title']}",
                     r.chart.planets["Soleil"].sign])
    out += [P("La famille en un coup d'œil", "h1"), P(f"Nombre de la famille {x['nombre']}", "h1s"),
            ST.table(rows, [34 * mm, 36 * mm, 64 * mm, 36 * mm], S)]

    dom, n_dom = x["fams"].most_common(1)[0]
    titre, txt = FT.DOMINANT[dom]
    out += [P("Ce qui la caractérise", "h2"), P(f"<b>{titre}.</b> {txt}")]
    autres = [f"{FT.FAMILY_NAME[f]} ({c})" for f, c in x["fams"].most_common() if f != dom]
    if autres:
        out.append(P(f"Sur {len(M)} membres, {n_dom} ont un chemin de vie tourné vers {FT.FAMILY_NAME[dom]}. "
                     "Les autres apportent " + " et ".join(autres) + " : c'est cette diversité qui équilibre la maison."))
    el = x["elements"].most_common()
    out.append(P("Côté astres, l'élément le plus présent parmi les Soleils est " + FT.ELEMENT_NOTE[el[0][0]]
                 + (f", suivi de {FT.ELEMENT_NOTE[el[1][0]]}." if len(el) > 1 else ".")))
    out += [P(f"Le nombre de la famille : {x['nombre']}", "h3"),
            P(f"La somme de tous les chemins de vie ({x['raw']}) se réduit à {x['nombre']}. "
              + FT.FAMILY_NUMBER.get(x["nombre"], FT.FAMILY_NUMBER[NU.base(x["nombre"])]))]
    if x["partages"]:
        lignes = []
        for n, c in sorted(x["partages"].items()):
            noms = [m["r"].person.first for m in M if m["r"].num.life_path == n]
            lignes.append(f"chemin de vie {n} pour " + ", ".join(noms[:-1]) + " et " + noms[-1])
        out.append(P("<b>Nombres partagés</b> : " + " ; ".join(lignes) + ". Ces membres se reconnaissent facilement "
                     "les uns dans les autres."))

    if kids:
        out += [PageBreak(), P("Les enfants et ceux qui les élèvent", "h1"),
                P("Un lien après l'autre", "h1s")]
        for k in kids:
            r = k["r"]
            bloc = [P(f"{r.person.first} · {k['role'].lower()}", "h2"),
                    P(f"Chemin de vie {r.num.life_path} ({NT.LIFE_PATH[r.num.life_path]['title']}), "
                      f"Soleil en {r.chart.planets['Soleil'].sign}.", "small")]
            for a in adults:
                bloc.append(P(f"<b>Avec {a['r'].person.first} ({a['role'].lower()})</b> : " + _link(a["r"], r)))
            titre_g, paras = RD.guidance(r)
            bloc += [P(titre_g, "h3")] + [P(t) for t in paras[:2]]
            out += [KeepTogether(bloc[:3]), *bloc[3:], Spacer(1, 4)]

    out += [PageBreak(), P("Conseils pour la famille", "h1"), P("À mettre en pratique", "h1s"),
            ST.box([P(FT.DOMINANT[dom][1], "note")]),
            P("· Prévoyez un moment commun régulier, où chacun peut parler sans être jugé.", "body"),
            P("· Confiez à chaque enfant une responsabilité qui correspond à son chemin de vie.", "body"),
            P("· Répartissez les rôles entre les adultes : celui qui cadre, celui qui écoute, celui qui encourage.",
              "body"),
            Spacer(1, 8),
            P("<b>Annexes</b> : les pages suivantes reprennent le chemin de vie complet de chaque membre.", "small")]
    for m in M:
        out += chemin_de_vie.profile_pages(S, m["r"])
    return out


def render(*args, today: date | None = None, order_ref: str | None = None, roles: list[str] | None = None):
    *people, out_path = args
    today = today or date.today()
    x = analyse(people, roles or [], today)
    S = ST.styles()
    nom = people[0].nom
    _doc.build(out_path, title=f"Étude Famille — {nom}", cover_title="Famille", cover_subtitle=f"Famille {nom}",
               cover_center=str(x["nombre"]), product_label=PRODUCT_LABEL, running=f"Étude Famille — {nom}",
               footer=_doc.footer_line(today, order_ref), story=story(S, x))
    return x
