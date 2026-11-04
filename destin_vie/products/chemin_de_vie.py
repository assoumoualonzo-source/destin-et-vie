"""Produit « Chemin de vie » : étude individuelle complète en PDF."""
from __future__ import annotations

from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, KeepTogether)

from .. import pdf_style as ST
from .. import reading as RD
from ..reading import MONTHS, Person

PRODUCT_LABEL = "CHEMIN DE VIE  ·  NUMÉROLOGIE  ·  THÈME ASTRAL"


def _date_fr(d: date) -> str:
    days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    return f"{days[d.weekday()]} {d.day} {MONTHS[d.month - 1]} {d.year}"


def method_page(S, r: RD.Reading):
    P = lambda t, s="body": Paragraph(t, S[s])
    pl = r.place
    out = [P("Avant de lire", "h1"), P("Méthode et précautions", "h1s"),
           P("Cette étude croise deux approches qu'il faut distinguer. La <b>numérologie</b> ne retient que le nom "
             "complet et la date de naissance. L'<b>astrologie</b>, elle, a besoin de l'heure exacte et du lieu : "
             "c'est ce qui donne l'ascendant et la répartition des planètes dans les douze maisons."),
           P("Les sources", "h2"),
           P(f"Les données viennent de l'acte de naissance : <b>{r.person.full_name}</b>, "
             f"né{'e' if r.person.feminine else ''} le {_date_fr(r.person.naissance)}"
             + (f" à {r.person.heure.replace(':', ' h ')}" if r.person.heure else ", heure non renseignée")
             + f", à {pl.name}."),
           P("Les calculs", "h2"),
           P("<b>Numérologie</b> : système pythagoricien (A = 1, B = 2 … I = 9, puis on recommence à J = 1). "
             "Les nombres 11, 22 et 33 sont conservés comme nombres maîtres. Le Y est compté comme voyelle."),
           P(f"<b>Astrologie</b> : positions planétaires issues d'un calcul astronomique, pour {pl.name} "
             f"({pl.coords_label()}), à l'heure légale du lieu. Maisons en système Placidus, zodiaque tropical.")]
    if r.is_child:
        out += [P("Lire le thème d'un enfant", "h2"),
                P("Un thème d'enfant ne prédit pas ce qu'il deviendra. Il propose une grille d'observation : des "
                  "tempéraments possibles, des besoins à repérer, des terrains où il risque de se sentir à l'étroit. "
                  "L'éducation, l'entourage et ses propres choix compteront bien davantage.")]
    out += [Spacer(1, 8), ST.box([P("Ni la numérologie ni l'astrologie n'ont de fondement scientifique. Leurs "
                                    "descriptions sont assez larges pour que chacun s'y retrouve (l'effet Barnum). "
                                    "Cette étude se lit comme un support de réflexion personnelle, jamais comme un "
                                    "avis médical, financier, juridique ou d'orientation.", "note")])]
    return out


def profile_pages(S, r: RD.Reading):
    P = lambda t, s="body": Paragraph(t, S[s])
    p, n, c = r.person, r.num, r.chart
    header = f"Chemin de vie {n.life_path}  ·  Soleil {c.planets['Soleil'].sign}"
    if c.asc is not None:
        header += f"  ·  Ascendant {c.asc_sign}"
    age = p.age(r.today)
    out = [PageBreak(), P(p.full_name, "h1"), P(header, "h1s"),
           ST.table([["Donnée", "Valeur"],
                     ["Nom complet", p.full_name],
                     ["Naissance", _date_fr(p.naissance).capitalize()
                      + (f", {p.heure.replace(':', ' h ')} (heure locale)" if p.heure else ", heure non renseignée")],
                     ["Lieu", r.place.name],
                     [f"Âge en {MONTHS[r.today.month - 1]} {r.today.year}", f"{age} an{'s' if age > 1 else ''}"]],
                    [45 * mm, 125 * mm], S),
           P("Profil numérologique", "h2"),
           ST.table([["Aspect", "Interprétation", "Points de vigilance"]] + RD.numerology_rows(r),
                    [33 * mm, 72 * mm, 65 * mm], S),
           Spacer(1, 6), P("Détail des calculs", "h3"), P(RD.numerology_calc_text(r), "note"),
           P("Lecture d'ensemble", "h3"), P(RD.numerology_overview(r))]

    grid = n.grid
    out += [KeepTogether([P("Grille d'inclusion", "h3"),
                          P("Nombre de lettres du nom pour chaque valeur. Une case vide signale une leçon karmique ; "
                            "la plus remplie, une énergie dominante.", "small"),
                          ST.table([[str(i) for i in range(1, 10)], [str(grid[i]) for i in range(1, 10)]],
                                   [170 * mm / 9] * 9, S)])]

    out += [PageBreak(), P("Cycles et réalisations", "h2"),
            ST.table(RD.cycles_rows(r), [28 * mm, 42 * mm, 55 * mm, 45 * mm], S),
            Spacer(1, 6), P(RD.cycles_comment(r)),
            P("Année personnelle", "h3"), P(RD.personal_year_text(r)),
            P("Thème natal", "h2"),
            ST.table(RD.chart_rows(r), [50 * mm, 70 * mm, 50 * mm], S),
            Spacer(1, 4), P(RD.chart_note(r), "small")]

    out += [PageBreak(), P("Lecture du thème", "h2")]
    for title, txt in RD.chart_sections(r):
        out += [P(title, "h3"), P(txt)]

    out += [P("Synthèse", "h2"), ST.box([P(RD.synthesis(r), "note")])]
    gt, paras = RD.guidance(r)
    out += [P(gt, "h3")] + [P(x) for x in paras]
    out += [Spacer(1, 12), ST.box([P("Pour conclure : ces lectures n'ont pas de valeur prédictive. Leur intérêt est "
                                     "dans l'attention qu'elles invitent à porter à soi-même ou à ses proches. Si un "
                                     "trait décrit ici ne correspond pas à ce que vous observez, c'est votre "
                                     "observation qui a raison.", "note")])]
    return out


def render(person: Person, out_path: str, today: date | None = None, order_ref: str | None = None) -> RD.Reading:
    r = RD.build(person, today)
    S = ST.styles()
    running = f"Chemin de vie — {person.first}"
    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=22 * mm, bottomMargin=20 * mm,
                          title=f"Chemin de vie — {person.full_name}", author=ST.BRAND)
    fr = Frame(20 * mm, 20 * mm, 170 * mm, A4[1] - 42 * mm, id="f")
    footer = f"Étude établie le {r.today.day} {MONTHS[r.today.month - 1]} {r.today.year}"
    if order_ref:
        footer += f"  ·  Commande {order_ref}"
    doc.addPageTemplates([
        PageTemplate("cover", frames=[fr], onPage=lambda c, d: ST.draw_cover(
            c, "Chemin de vie", person.full_name if len(person.full_name) < 34 else person.first,
            str(r.num.life_path), footer, PRODUCT_LABEL)),
        PageTemplate("body", frames=[fr], onPage=lambda c, d: ST.draw_header(c, d, running)),
    ])
    story = [NextPageTemplate("body"), PageBreak()] + method_page(S, r) + profile_pages(S, r)
    doc.build(story)
    return r
