"""Produit « Compatibilité amoureuse » : deux personnes, lecture du couple + deux chemins de vie."""
from __future__ import annotations

from datetime import date

from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, Spacer

from .. import astro as AS
from .. import numerology as NU
from .. import pdf_style as ST
from .. import reading as RD
from ..reading import Person
from ..texts import compat_texts as CT
from ..texts import numbers as NT
from . import _doc, chemin_de_vie

PRODUCT_LABEL = "COMPATIBILITÉ AMOUREUSE  ·  NUMÉROLOGIE  ·  SYNASTRIE"
ORBS = {"conjonction": (0, 8), "sextile": (60, 5), "carré": (90, 7), "trigone": (120, 7), "opposition": (180, 8)}
PAIRS = [("Soleil", "Lune"), ("Lune", "Soleil"), ("Vénus", "Mars"), ("Mars", "Vénus"), ("Lune", "Lune"),
         ("Vénus", "Vénus"), ("Soleil", "Soleil"), ("Mercure", "Mercure"), ("Soleil", "Vénus"),
         ("Vénus", "Soleil"), ("Lune", "Vénus"), ("Vénus", "Lune"), ("Mars", "Mars")]
SOFT = {"trigone", "sextile"}


class CompatError(ValueError):
    pass


def _contacts(ra: RD.Reading, rb: RD.Reading):
    out = []
    seen = set()
    for pa, pb in PAIRS:
        if "Lune" in (pa, pb) and not (ra.chart.has_time and rb.chart.has_time):
            continue
        key = frozenset([(pa, "a"), (pb, "b")])
        if key in seen:
            continue
        seen.add(key)
        la, lb = ra.chart.planets[pa].lon, rb.chart.planets[pb].lon
        sep = abs((la - lb + 180) % 360 - 180)
        for kind, (ang, orb) in ORBS.items():
            if abs(sep - ang) <= orb:
                topic = CT.PAIR_TOPIC.get((pa, pb)) or CT.PAIR_TOPIC.get((pb, pa))
                out.append(dict(a=pa, b=pb, kind=kind, orb=round(abs(sep - ang), 1), topic=topic))
    out.sort(key=lambda x: x["orb"])
    return out


def _art(name: str) -> str:
    return {"Lune": "la Lune", "Vénus": "Vénus", "Soleil": "le Soleil", "Mars": "Mars", "Mercure": "Mercure"}[name]


def analyse(pa: Person, pb: Person, today: date):
    ra, rb = RD.build(pa, today), RD.build(pb, today)
    for p in (pa, pb):
        if p.age(today) < 18:
            raise CompatError(f"La compatibilité amoureuse est réservée aux adultes ({p.first} a moins de 18 ans).")
    na, nb = ra.num, rb.num
    A, B = pa.first, pb.first
    fa, fb = CT.FAMILY[NU.base(na.life_path)], CT.FAMILY[NU.base(nb.life_path)]

    if na.life_path == nb.life_path:
        lp_txt = CT.SAME_NUMBER
    elif fa == fb:
        lp_txt = CT.SAME_FAMILY.replace("{fam}", CT.FAMILY_LABEL[fa])
    else:
        lp_txt = CT.CROSS_FAMILY[frozenset([fa, fb])]
    sa, sb = NU.base(na.soul), NU.base(nb.soul)
    if na.soul == nb.soul:
        soul_txt = CT.SOUL_SAME
    elif CT.FAMILY[sa] == CT.FAMILY[sb]:
        soul_txt = CT.SOUL_FAMILY
    else:
        soul_txt = CT.SOUL_DIFF.replace("{sa}", NT.SOUL[na.soul][0].lower()).replace("{sb}", NT.SOUL[nb.soul][0].lower())

    couple_raw = na.life_path + nb.life_path
    couple = NU.reduce(couple_raw, False)
    ea = AS.ELEMENT[ra.chart.planets["Soleil"].sign]
    eb = AS.ELEMENT[rb.chart.planets["Soleil"].sign]
    el_txt = CT.ELEMENT_PAIR["same"].replace("{e}", ea) if ea == eb else CT.ELEMENT_PAIR[frozenset([ea, eb])]

    contacts = _contacts(ra, rb)
    forces, frictions = [], []
    if na.life_path == nb.life_path or fa == fb:
        forces.append("des chemins de vie de la même famille, qui facilitent la compréhension mutuelle")
    else:
        frictions.append("des chemins de vie de familles différentes, qui demandent d'expliquer ses besoins")
    if na.soul == nb.soul or CT.FAMILY[sa] == CT.FAMILY[sb]:
        forces.append("des besoins profonds (Âmes) proches")
    if ea == eb:
        forces.append(f"des Soleils du même élément ({ea})")
    elif frozenset([ea, eb]) in (frozenset(["Feu", "Air"]), frozenset(["Terre", "Eau"])):
        forces.append(f"des Soleils d'éléments complémentaires ({ea} et {eb})")
    else:
        frictions.append(f"des tempéraments solaires différents ({ea} et {eb})")
    for c in contacts[:6]:
        label = f"{_art(c['a'])} de {A} et {_art(c['b'])} de {B} en {c['kind']}"
        (forces if c["kind"] in SOFT or (c["kind"] == "conjonction" and c["a"] != "Mars") else frictions).append(label)

    return dict(ra=ra, rb=rb, A=A, B=B, lp_txt=lp_txt, soul_txt=soul_txt, couple=couple, couple_raw=couple_raw,
                el_txt=el_txt, contacts=contacts, forces=forces, frictions=frictions, fa=fa, fb=fb)


def _sub(t: str, A: str, B: str) -> str:
    return t.replace("{a}", A).replace("{b}", B)


def story(S, x) -> list:
    P = lambda t, s="body": Paragraph(t, S[s])
    ra, rb, A, B = x["ra"], x["rb"], x["A"], x["B"]
    na, nb, ca, cb = ra.num, rb.num, ra.chart, rb.chart

    def asc(c):
        return c.asc_sign if c.asc is not None else "heure inconnue"

    def moon(c):
        return c.planets["Lune"].sign + ("" if c.moon_sign_certain else " (indicatif)")

    out = [P("Avant de lire", "h1"), P("Méthode et précautions", "h1s"),
           P(f"Cette étude compare les profils de <b>{ra.person.full_name}</b> et de <b>{rb.person.full_name}</b>. "
             "Elle croise deux lectures : la numérologie (noms et dates de naissance) et la synastrie, c'est-à-dire "
             "la comparaison des deux thèmes astraux, planète par planète."),
           P("Elle se termine par le chemin de vie complet de chacun, pour que chaque partenaire dispose aussi de "
             "sa propre étude."),
           Spacer(1, 6),
           ST.box([P("Ni la numérologie ni l'astrologie n'ont de fondement scientifique. Aucune de ces lectures ne "
                     "dit si un couple va durer : cela dépend de ce que les deux personnes construisent. Lisez-la "
                     "comme une base de conversation à deux.", "note")]),
           PageBreak(),
           P(f"{A} & {B}", "h1"), P(f"Nombre du couple {x['couple']}  ·  {CT.COUPLE[x['couple']][0]}", "h1s"),
           ST.table([["", A, B],
                     ["Chemin de vie", f"<b>{na.life_path}</b> · {NT.LIFE_PATH[na.life_path]['title']}",
                      f"<b>{nb.life_path}</b> · {NT.LIFE_PATH[nb.life_path]['title']}"],
                     ["Expression", str(na.expression), str(nb.expression)],
                     ["Âme", f"{na.soul} · {NT.SOUL[na.soul][0]}", f"{nb.soul} · {NT.SOUL[nb.soul][0]}"],
                     ["Personnalité", str(na.personality), str(nb.personality)],
                     ["Soleil", ca.planets["Soleil"].sign, cb.planets["Soleil"].sign],
                     ["Lune", moon(ca), moon(cb)],
                     ["Ascendant", asc(ca), asc(cb)],
                     ["Vénus", ca.planets["Vénus"].sign, cb.planets["Vénus"].sign],
                     ["Mars", ca.planets["Mars"].sign, cb.planets["Mars"].sign]],
                    [38 * mm, 66 * mm, 66 * mm], S),
           P("Ce que disent les nombres", "h2"),
           P("Les chemins de vie", "h3"), P(_sub(x["lp_txt"], A, B)),
           P("Les besoins profonds", "h3"), P(_sub(x["soul_txt"], A, B)),
           P(f"Le nombre du couple : {x['couple']}", "h3"),
           P(f"En additionnant les deux chemins de vie ({na.life_path} + {nb.life_path} = {x['couple_raw']}"
             + (f", réduit à {x['couple']}" if x["couple_raw"] != x["couple"] else "") + "), on obtient le nombre "
             "de ce que le couple construit ensemble. " + _sub(CT.COUPLE[x["couple"]][1], A, B))]

    out += [PageBreak(), P("Ce que disent les astres", "h2"), P(x["el_txt"])]
    if x["contacts"]:
        rows = [["Contact", "Aspect", "Ce que cela touche"]]
        for c in x["contacts"][:7]:
            rows.append([f"{c['a']} ({A}) – {c['b']} ({B})", c["kind"], c["topic"]])
        out += [ST.table(rows, [62 * mm, 28 * mm, 80 * mm], S), Spacer(1, 6)]
        for c in x["contacts"][:4]:
            out.append(P(f"<b>{RD.ucfirst(_art(c['a']))} de {A} et {_art(c['b'])} de {B}</b> "
                         f"{CT.ASPECT_FEEL[c['kind']]}. Ce contact touche {c['topic']}."))
    else:
        out.append(P("Aucun contact majeur et serré entre les planètes personnelles des deux thèmes : le lien se "
                     "construit davantage sur les choix communs que sur une attirance évidente."))
    if not (ca.has_time and cb.has_time):
        out.append(P("Une heure de naissance manque : les contacts impliquant la Lune et l'ascendant ne sont pas "
                     "pris en compte.", "small"))

    out += [P("Forces du couple", "h2")]
    out += [P("· " + RD.ucfirst(f) + ".") for f in x["forces"]] or [P("Aucune force évidente ne ressort des calculs.")]
    out += [P("Points de friction", "h2")]
    out += [P("· " + RD.ucfirst(f) + ".") for f in x["frictions"]] or [P("Aucune friction marquée.")]
    adv = CT.ADVICE[x["fa"]] if x["fa"] == x["fb"] else (CT.ADVICE[x["fa"]] + " " + CT.ADVICE[x["fb"]])
    if any(c["kind"] in ("carré", "opposition") for c in x["contacts"]):
        adv += " " + CT.ADVICE_TENSION
    out += [P("Conseils pour le couple", "h2"), ST.box([P(adv, "note")])]

    out += [Spacer(1, 8), P(f"<b>Annexes</b> : les pages suivantes reprennent le chemin de vie complet de {A}, "
                            f"puis celui de {B}.", "small")]
    out += chemin_de_vie.profile_pages(S, ra) + chemin_de_vie.profile_pages(S, rb)
    return out


def render(pa: Person, pb: Person, out_path: str, today: date | None = None, order_ref: str | None = None):
    today = today or date.today()
    x = analyse(pa, pb, today)
    S = ST.styles()
    _doc.build(out_path, title=f"Compatibilité amoureuse — {pa.first} & {pb.first}",
               cover_title="Compatibilité", cover_subtitle=f"{pa.first} & {pb.first}",
               cover_center=str(x["couple"]), product_label=PRODUCT_LABEL,
               running=f"Compatibilité — {pa.first} & {pb.first}", footer=_doc.footer_line(today, order_ref),
               story=story(S, x))
    return x
