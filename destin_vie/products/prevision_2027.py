"""Produit « Prévision 2027 » : année personnelle 2027 et mois personnels.

Convention retenue : l'année personnelle 2027 couvre l'année civile, du 1er janvier
au 31 décembre 2027, et chaque mois personnel = année personnelle + mois civil.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer

from .. import numerology as NU
from .. import pdf_style as ST
from .. import reading as RD
from ..reading import MONTHS, Person, g, ucfirst
from ..texts import numbers as NT
from ..texts import year_texts as YT
from . import _doc

YEAR = 2027
PRODUCT_LABEL = "PRÉVISION 2027  ·  ANNÉE PERSONNELLE  ·  MOIS PAR MOIS"


@dataclass
class Forecast:
    person: Person
    today: date
    is_child: bool
    rd: int
    rm: int
    ry: int
    raw: int
    year_number: int      # 11 ou 22 si nombre maître, sinon 1 à 9
    base: int             # chiffre de base (1 à 9)
    months: list[dict]
    life_path: int


def compute(person: Person, today: date | None = None) -> Forecast:
    today = today or date.today()
    b = person.naissance
    rd = NU.reduce(b.day, False)
    rm = NU.reduce(b.month, False)
    ry = NU.reduce(NU.digit_sum(YEAR), False)
    raw = rd + rm + ry
    yn = NU.reduce(raw, True)
    base = NU.reduce(raw, False)
    months = []
    for m in range(1, 13):
        mr = NU.reduce(m, False)
        months.append({"month": m, "number": NU.reduce(base + mr, False), "calc": f"{base} + {mr}"})
    lp = NU.compute(person.full_name, b, today).life_path
    return Forecast(person, today, person.age(today) < 16, rd, rm, ry, raw, yn, base, months, lp)


def _calc_text(f: Forecast) -> str:
    b = f.person.naissance
    day = f"{b.day}" + (f" → {f.rd}" if b.day != f.rd else "")
    mon = f"{b.month}" + (f" → {f.rm}" if b.month != f.rm else "")
    chain = NU.reduction_chain(f.raw, True)
    total = " → ".join(str(x) for x in chain)
    out = (f"Jour de naissance {day} ; mois de naissance {mon} ; année {YEAR} : 2 + 0 + 2 + 7 = 11 → {f.ry}. "
           f"Total : {f.rd} + {f.rm} + {f.ry} = {total}.")
    return out


HIGH_ADULT = {1: "le meilleur moment pour lancer ou décider.", 8: "le moment de négocier et de concrétiser."}
HIGH_CHILD = {1: "un bon moment pour commencer une activité nouvelle.",
              8: "un mois où {il} aime relever des défis et montrer ce qu'{il} sait faire."}
CARE_ADULT = {4: "charge de travail plus lourde, prévoir de vrais temps de repos.",
              7: "énergie plus basse, éviter les décisions hâtives.",
              9: "période de fin et de tri, ne pas forcer les nouveaux départs."}
CARE_CHILD = {4: "rythme plus chargé, veiller au sommeil et aux routines.",
              7: "besoin de calme et de moments à soi.",
              9: "période de transition, l'accompagner dans ce qui change."}


def _highlights(f: Forecast) -> tuple[list[str], list[str]]:
    lp_base = NU.base(f.life_path)
    strong, careful = [], []
    for m in f.months:
        name = MONTHS[m["month"] - 1].capitalize()
        n = m["number"]
        if n == lp_base:
            strong.append(f"<b>{name}</b> (mois {n}) : en résonance avec son chemin de vie, un mois où {{p}} "
                          "se sent pleinement à sa place.")
        elif n in (1, 8):
            strong.append(f"<b>{name}</b> (mois {n}) : " + (HIGH_CHILD if f.is_child else HIGH_ADULT)[n])
        if n in YT.CARE and n != lp_base:
            careful.append(f"<b>{name}</b> (mois {n}) : " + (CARE_CHILD if f.is_child else CARE_ADULT)[n])
    return strong, careful


def _cross(f: Forecast) -> str:
    lp, py = NU.base(f.life_path), f.base
    if lp == py:
        match = YT.CROSS_MATCH
    elif YT.FAMILY[lp] == YT.FAMILY[py]:
        match = YT.CROSS_EASY
    else:
        match = YT.CROSS_HARD
    txt = YT.CROSS.format(lp=f.life_path, lp_title=NT.LIFE_PATH[f.life_path]["title"].lower(), p="{p}",
                          lp_style=YT.LP_STYLE[lp], py=f.year_number, py_ask=YT.PY_ASK[py], match=match)
    return g(txt, f.person)


def story(S, f: Forecast, *, bonus: bool = False, with_intro: bool = True) -> list:
    P = lambda t, s="body": Paragraph(t, S[s])
    p = f.person
    Y = YT.YEAR[f.base]
    out = []
    if with_intro:
        out += [P("Avant de lire", "h1"), P("Comment se lit une année personnelle", "h1s"),
                P("En numérologie, chaque année de votre vie porte un nombre, de 1 à 9, qui revient tous les neuf "
                  "ans. On l'obtient en ajoutant votre jour et votre mois de naissance à l'année en cours. Ce nombre "
                  "donne la couleur générale de l'année ; chaque mois a ensuite sa propre nuance."),
                P(f"Cette étude couvre l'année civile {YEAR}, du 1er janvier au 31 décembre. Elle repose uniquement "
                  f"sur la date de naissance de <b>{p.full_name}</b>, né{'e' if p.feminine else ''} le "
                  f"{p.naissance.day} {MONTHS[p.naissance.month - 1]} {p.naissance.year}."),
                Spacer(1, 6),
                ST.box([P("La numérologie n'a pas de fondement scientifique. Cette prévision décrit des tendances "
                          "symboliques, à lire comme un support de réflexion pour organiser son année, jamais comme "
                          "une certitude ni comme un avis médical, financier ou juridique.", "note")]),
                PageBreak()]

    out += [P(f"Votre année {YEAR}", "h1"),
            P(f"Année personnelle {f.year_number}  ·  {Y['title']}  ·  {p.full_name}", "h1s"),
            ST.table([["Donnée", "Valeur"],
                      ["Nom complet", p.full_name],
                      ["Date de naissance", f"{p.naissance.day} {MONTHS[p.naissance.month - 1]} {p.naissance.year}"],
                      [f"Année personnelle {YEAR}", f"<b>{f.year_number}</b> · {Y['keywords']}"]],
                     [55 * mm, 115 * mm], S),
            P("Le calcul", "h3"), P(_calc_text(f), "note"),
            P(Y["title"], "h2"), P(g(Y["theme"], p))]
    if f.year_number in YT.MASTER_YEAR:
        out.append(P(YT.MASTER_YEAR[f.year_number]))
    out.append(P(YT.UNIVERSAL_2027, "small"))
    if f.is_child:
        out.append(P(g("Chez un enfant de cet âge, ces tendances se lisent à son échelle : son rythme, son humeur, "
                       "ses envies et la vie de la famille autour de {lui}.", p)))
    else:
        out += [P("Ce que l'année favorise", "h3"), P(g(ucfirst(Y["favorable"]) + ".", p)),
                P("Ce qui demande de l'attention", "h3"), P(g(ucfirst(Y["vigilance"]) + ".", p))]

    rows = [["Mois", "Nombre", "Tendance"]]
    for m in f.months:
        t, txt = YT.MONTH[m["number"]]
        rows.append([MONTHS[m["month"] - 1].capitalize(), f"<b>{m['number']}</b>", f"<b>{t}</b> · {g(txt, p)}"])
    out += [PageBreak(), P(f"{YEAR} mois par mois", "h2"),
            P(f"Chaque mois personnel s'obtient en ajoutant le numéro du mois à l'année personnelle "
              f"({f.base}). Exemple : mars = {f.base} + 3 = {f.months[2]['number']}.", "small"),
            Spacer(1, 4), ST.table(rows, [30 * mm, 20 * mm, 120 * mm], S)]

    strong, careful = _highlights(f)
    out.append(P("Les temps forts", "h2"))
    out += [P(g(x, p)) for x in strong] if strong else [P("Aucun mois ne se détache nettement : l'année avance de façon "
                                                     "régulière, sans pic marqué.")]
    out.append(P("Les périodes à vivre plus doucement", "h2"))
    out += [P(g(x, p)) for x in careful] if careful else [P("Aucune période ne demande de prudence particulière.")]

    if bonus:
        out += [KeepTogether([P(f"Bonus : votre chemin de vie et votre année {YEAR}", "h2"),
                              ST.box([P(_cross(f), "note")])])]

    adv = Y["child"] if f.is_child else Y["adult"]
    first = next((MONTHS[m["month"] - 1] for m in f.months if m["number"] in (1, 8)), None)
    synth = (f"En résumé, {YEAR} est pour {{p}} {Y['title'][0].lower() + Y['title'][1:]}. "
             f"Le fil conducteur tient en trois mots : {Y['keywords']}.")
    if first:
        synth += (f" Le mois le plus dynamique de l'année sera {first}." if f.is_child
                  else f" S'il ne fallait retenir qu'un moment pour agir, ce serait {first}.")
    out += [P("Synthèse et conseils", "h2"), P(g(synth, p)),
            P("Pour les parents" if f.is_child else "Conseil pour l'année", "h3"), P(g(adv, p)),
            P("Une année personnelle donne une tendance, pas un programme : de quoi choisir le bon moment, "
              "jamais une raison de renoncer à ce qui compte.", "small")]
    return out


def render(person: Person, out_path: str, today: date | None = None, order_ref: str | None = None,
           bonus: bool = False):
    f = compute(person, today)
    S = ST.styles()
    _doc.build(out_path, title=f"Prévision {YEAR} — {person.full_name}", cover_title=f"Mon année {YEAR}",
               cover_subtitle=person.full_name if len(person.full_name) < 34 else person.first,
               cover_center=str(f.year_number), product_label=PRODUCT_LABEL,
               running=f"Prévision {YEAR} — {person.first}", footer=_doc.footer_line(f.today, order_ref),
               story=story(S, f, bonus=bonus))
    return f
