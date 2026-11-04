"""Assemblage commun d'un document : couverture + pages à en-tête."""
from __future__ import annotations

from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, NextPageTemplate, PageBreak, PageTemplate

from .. import pdf_style as ST
from ..reading import MONTHS


def footer_line(today: date, order_ref: str | None) -> str:
    s = f"Étude établie le {today.day} {MONTHS[today.month - 1]} {today.year}"
    return s + (f"  ·  Commande {order_ref}" if order_ref else "")


def build(out_path: str, *, title: str, cover_title: str, cover_subtitle: str, cover_center: str,
          product_label: str, running: str, footer: str, story: list):
    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=22 * mm, bottomMargin=20 * mm, title=title, author=ST.BRAND)
    fr = Frame(20 * mm, 20 * mm, 170 * mm, A4[1] - 42 * mm, id="f")
    doc.addPageTemplates([
        PageTemplate("cover", frames=[fr], onPage=lambda c, d: ST.draw_cover(
            c, cover_title, cover_subtitle, cover_center, footer, product_label)),
        PageTemplate("body", frames=[fr], onPage=lambda c, d: ST.draw_header(c, d, running)),
    ])
    doc.build([NextPageTemplate("body"), PageBreak()] + story)
