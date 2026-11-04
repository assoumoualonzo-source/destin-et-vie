"""Charte graphique Destin & Vie (encre et laiton, polices Liberation)."""
from __future__ import annotations

import math
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle

BRAND = "Destin & Vie"

FONT_DIRS = ["/usr/share/fonts/truetype/liberation/", "/usr/share/fonts/liberation/",
             os.path.join(os.path.dirname(__file__), "fonts")]


def _font_path(name):
    for d in FONT_DIRS:
        p = os.path.join(d, name + ".ttf")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"Police {name} introuvable : installez fonts-liberation ou copiez-la dans destin_vie/fonts/")


_registered = False


def register_fonts():
    global _registered
    if _registered:
        return
    for n, f in [("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
                 ("Serif-I", "LiberationSerif-Italic"), ("Serif-BI", "LiberationSerif-BoldItalic"),
                 ("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold")]:
        pdfmetrics.registerFont(TTFont(n, _font_path(f)))
    registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
    _registered = True


INK = colors.HexColor("#1F2A44")
GOLD = colors.HexColor("#B8862B")
SOFT = colors.HexColor("#F4EFE4")
LINE = colors.HexColor("#D9CFBB")
GREY = colors.HexColor("#5A5F6B")
WIDTH = 170 * mm


def styles():
    register_fonts()
    return {
        "body": ParagraphStyle("body", fontName="Serif", fontSize=10.5, leading=15, alignment=TA_JUSTIFY,
                               textColor=INK, spaceAfter=6),
        "h1": ParagraphStyle("h1", fontName="Serif-B", fontSize=24, leading=28, textColor=INK, spaceAfter=2),
        "h1s": ParagraphStyle("h1s", fontName="Sans", fontSize=10.5, leading=14, textColor=GOLD, spaceAfter=14),
        "h2": ParagraphStyle("h2", fontName="Sans-B", fontSize=12.5, leading=16, textColor=INK, spaceBefore=12,
                             spaceAfter=6),
        "h3": ParagraphStyle("h3", fontName="Serif-BI", fontSize=11, leading=14, textColor=GOLD, spaceBefore=6,
                             spaceAfter=2),
        "cell": ParagraphStyle("cell", fontName="Serif", fontSize=9.3, leading=12, textColor=INK),
        "th": ParagraphStyle("th", fontName="Sans-B", fontSize=8.8, leading=11, textColor=colors.white),
        "small": ParagraphStyle("small", fontName="Serif-I", fontSize=9, leading=12, textColor=GREY,
                                alignment=TA_JUSTIFY),
        "note": ParagraphStyle("note", fontName="Serif", fontSize=9.6, leading=13.5, textColor=INK,
                               alignment=TA_JUSTIFY),
    }


def table(rows, widths, S, header=True):
    data = []
    for i, r in enumerate(rows):
        st = S["th"] if (header and i == 0) else S["cell"]
        data.append([Paragraph(c, st) if isinstance(c, str) else c for c in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
             ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5)]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), INK))
    for i in range(1 if header else 0, len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), SOFT))
    t.setStyle(TableStyle(style))
    return t


def box(paras):
    t = Table([[paras]], colWidths=[WIDTH])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SOFT), ("BOX", (0, 0), (-1, -1), 0.6, GOLD),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def draw_cover(c, title, subtitle, center_text, footer, product_label):
    w, h = A4
    c.saveState()
    c.setFillColor(INK)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    cx, cy = w / 2, h * 0.62
    c.circle(cx, cy, 70, stroke=1, fill=0)
    c.circle(cx, cy, 58, stroke=1, fill=0)
    for k in range(12):
        a = math.radians(k * 30)
        c.line(cx + 58 * math.cos(a), cy + 58 * math.sin(a), cx + 70 * math.cos(a), cy + 70 * math.sin(a))
    c.setFillColor(GOLD)
    c.setFont("Serif-B", 34 if len(center_text) <= 2 else 26)
    c.drawCentredString(cx, cy - 11, center_text)
    c.setFont("Sans-B", 11)
    c.drawCentredString(cx, h - 70, BRAND.upper())
    c.setFillColor(colors.white)
    c.setFont("Serif-B", 34)
    c.drawCentredString(w / 2, h * 0.40, title)
    c.setFont("Serif-I", 20)
    c.drawCentredString(w / 2, h * 0.40 - 32, subtitle)
    c.setFillColor(GOLD)
    c.setFont("Sans", 10.5)
    c.drawCentredString(w / 2, h * 0.40 - 62, product_label)
    c.setFillColor(colors.HexColor("#C9CEDA"))
    c.setFont("Serif", 10)
    c.drawCentredString(w / 2, 60, footer)
    c.restoreState()


def draw_header(c, doc, running_title):
    w, h = A4
    c.saveState()
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(20 * mm, h - 15 * mm, w - 20 * mm, h - 15 * mm)
    c.setFont("Sans", 8)
    c.setFillColor(GREY)
    c.drawString(20 * mm, h - 12.5 * mm, running_title)
    c.drawRightString(w - 20 * mm, h - 12.5 * mm, BRAND)
    c.drawRightString(w - 20 * mm, 12 * mm, str(doc.page))
    c.restoreState()
