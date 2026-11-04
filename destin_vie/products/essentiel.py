"""Pack « Essentiel » : chemin de vie complet + prévision 2027 + bonus (lecture croisée)."""
from __future__ import annotations

from datetime import date

from reportlab.platypus import PageBreak

from .. import pdf_style as ST
from .. import reading as RD
from ..reading import Person
from . import _doc, chemin_de_vie, prevision_2027

PRODUCT_LABEL = "CHEMIN DE VIE  ·  PRÉVISION 2027  ·  BONUS"


def render(person: Person, out_path: str, today: date | None = None, order_ref: str | None = None):
    r = RD.build(person, today)
    f = prevision_2027.compute(person, today)
    S = ST.styles()
    story = (chemin_de_vie.method_page(S, r) + chemin_de_vie.profile_pages(S, r) + [PageBreak()]
             + prevision_2027.story(S, f, bonus=True, with_intro=False))
    _doc.build(out_path, title=f"Pack Essentiel — {person.full_name}", cover_title="Destin & Vie",
               cover_subtitle=person.full_name if len(person.full_name) < 34 else person.first,
               cover_center=str(r.num.life_path), product_label=PRODUCT_LABEL,
               running=f"Pack Essentiel — {person.first}", footer=_doc.footer_line(r.today, order_ref),
               story=story)
    return r
