#!/usr/bin/env python3
"""Capsule « résumé » Destin & Vie : une seule diapositive animée (9:16, 1080x1920).

Principe :
- une seule composition, qui se construit au rythme de la voix off puis reste à l'écran ;
- peu de texte : le titre de l'étude, le prénom et le nom (écrits, jamais prononcés),
  le nombre, et les deux ou trois points de la conclusion avec une icône chacun ;
- couleurs pastel accordées au thème nuit étoilée du site.

Ressources libres :
- fond : illustration « Sparkling night sky with a purple moon and pink clouds »,
  Severina Seidl, Unsplash (licence Unsplash, usage commercial libre)
- icônes : Phosphor Icons, licence MIT (capsule/icones/LICENSE-Phosphor.txt)
- musique : « Kalimba Relaxation Music », Kevin MacLeod, FreePD, CC0
- voix : Piper, voix française fr_FR-siwis-medium
"""
from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys
import tempfile
from datetime import date

import cairosvg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import capsule as CAP                                  # noqa: E402  (voix, musique, polices)
from destin_vie import reading as RD                   # noqa: E402
from destin_vie.reading import Person, g               # noqa: E402
from destin_vie.texts import astro_texts as AT         # noqa: E402
from destin_vie.texts import numbers as NT             # noqa: E402

W, H, FPS = 1080, 1920, 30
FOND = os.path.join(HERE, "assets", "fond_pastel.jpg")
ICONS = os.path.join(HERE, "icones")

CREAM = (251, 246, 238)
GOLD = (236, 206, 150)
INK = (45, 51, 84)
MUTED = (110, 112, 140)
ACCENTS = [(150, 136, 214), (226, 146, 172), (118, 176, 156), (232, 160, 116)]

TAG_SHORT = {
    "affirmation": "Affirmation de soi", "indépendance": "Indépendance", "action": "Goût de l'action",
    "relation": "Le lien aux autres", "sensibilité": "Sensibilité", "harmonie": "Besoin d'harmonie",
    "expression": "Expression", "créativité": "Créativité", "structure": "Sens de la structure",
    "concret": "Sens du concret", "travail": "Goût de l'effort", "liberté": "Liberté",
    "mouvement": "Mouvement", "curiosité": "Curiosité", "soin": "Attention aux autres",
    "famille": "Attachement à la famille", "réflexion": "Réflexion", "intériorité": "Vie intérieure",
    "ambition": "Ambition", "idéal": "Idéal", "ouverture": "Ouverture au monde",
}
TAG_ICON = {
    "affirmation": "crown-simple", "indépendance": "compass", "action": "lightning", "relation": "handshake",
    "sensibilité": "drop", "harmonie": "yin-yang", "expression": "chat-circle", "créativité": "palette",
    "structure": "cube", "concret": "hammer", "travail": "hammer", "liberté": "bird", "mouvement": "wind",
    "curiosité": "magnifying-glass", "soin": "hand-heart", "famille": "house-line", "réflexion": "lightbulb",
    "intériorité": "moon-stars", "ambition": "trophy", "idéal": "star-four", "ouverture": "globe-hemisphere-west",
}


# ---------------------------------------------------------------- contenu
def content_chemin_de_vie(person: Person, today: date | None = None) -> dict:
    r = RD.build(person, today)
    pts = RD.synthesis_points(r)
    lp = r.num.life_path
    title = NT.LIFE_PATH[lp]["title"].replace(" (nombre maître)", "")
    child = r.is_child
    labels = [AT.TAG_LABEL[t] for t in pts["tags"]]
    if len(labels) == 1:
        resume = labels[0]
    else:
        resume = ", ".join(labels[:-1]) + ", et " + labels[-1]
    voix = [
        "Chemin de vie.",
        f"{'Son' if child else 'Votre'} nombre : le {CAP.mots(lp)}. {title}.",
        f"Ce qui {'le{la}' if child else 'vous'} résume : {resume}.".replace("le{la}", "{le|la}"),
        f"À cultiver : {pts['defi']}.",
    ]
    return {
        "titre": "Chemin de vie",
        "prenom": person.first, "nom": person.nom.upper(),
        "chiffre": str(lp), "legende": title,
        "points": [(TAG_ICON[t], TAG_SHORT[t]) for t in pts["tags"]],
        "defi": ("plant", "À cultiver", pts["defi"][0].upper() + pts["defi"][1:]),
        "voix": [voix[0]],          # seul le titre est dit ; le reste défile sans paroles
    }


# ---------------------------------------------------------------- dessin
def font(path, size):
    return ImageFont.truetype(path, size)


def icon(name: str, color, size: int) -> Image.Image:
    svg = open(os.path.join(ICONS, name + ".svg"), encoding="utf-8").read()
    svg = svg.replace("currentColor", "#%02x%02x%02x" % color)
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def background() -> Image.Image:
    img = Image.open(FOND).convert("RGB")
    cw = int(img.height * 9 / 16)
    x0 = min(img.width - cw, max(0, int(img.width * 0.62) - cw // 2))
    img = img.crop((x0, 0, x0 + cw, img.height)).resize((int(W * 1.08), int(H * 1.08)), Image.LANCZOS)
    # voile pastel : adoucit l'image et éclaircit le bas pour la carte
    veil = Image.new("RGB", img.size, (236, 228, 246))
    mask = np.zeros((img.height, img.width), np.float32)
    ys = np.linspace(0, 1, img.height)[:, None]
    mask += 0.10 + 0.35 * np.clip((ys - 0.55) / 0.45, 0, 1)
    m = Image.fromarray((mask * 255).astype(np.uint8))
    return Image.composite(veil, img, m)


def spaced(s: str) -> str:
    return " ".join(s)


def layers(c: dict) -> list[Image.Image]:
    """Une couche par étape d'apparition (synchronisée avec les phrases de la voix)."""
    out = []

    # 0. marque, titre, prénom et nom
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    d.text((W / 2, 150), "DESTIN & VIE", font=font(CAP.FONT_DISPLAY, 44), fill=GOLD + (255,), anchor="mm")
    d.line([(W / 2 - 50, 190), (W / 2 + 50, 190)], fill=GOLD + (200,), width=2)
    d.text((W / 2, 290), c["titre"], font=font(CAP.FONT_DISPLAY, 96), fill=CREAM + (255,), anchor="mm")
    big = c["prenom"]
    fs = 120 if len(big) <= 10 else 96
    d.text((W / 2, 445), big, font=font(CAP.FONT_DISPLAY, fs), fill=CREAM + (255,), anchor="mm")
    fn = font(CAP.FONT_TEXT_REG, 40)
    nm = spaced(c["nom"]) if d.textlength(spaced(c["nom"]), font=fn) < W - 160 else c["nom"]
    d.text((W / 2, 540), nm, font=fn, fill=GOLD + (255,), anchor="mm")
    out.append(_shadow(L))

    # 1. le nombre, posé sur la lune, et sa légende
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx, cy, r = W / 2, 790, 150
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30], fill=(255, 250, 240, 90))
    L = Image.alpha_composite(L, glow.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(L)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 252, 247, 70), outline=CREAM + (230,), width=3)
    d.text((cx, cy + 6), c["chiffre"], font=font(CAP.FONT_DISPLAY, 190), fill=CREAM + (255,), anchor="mm")
    d.text((cx, cy + r + 62), c["legende"], font=font(CAP.FONT_DISPLAY, 64), fill=CREAM + (255,), anchor="mm")
    out.append(_shadow(L))

    # 2+. carte pastel : une ligne par point de la conclusion, puis le point à cultiver
    rows = [(ic, txt, None) for ic, txt in c["points"]] + [c["defi"]]
    card_top, row_h = 1150, 150
    card_h = row_h * len(rows) + 60
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([70, card_top, W - 70, card_top + card_h], radius=44, fill=(255, 255, 255, 190))
    for i, row in enumerate(rows):
        L = card.copy() if i == 0 else Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(L)
        y = card_top + 30 + i * row_h + row_h / 2
        col = ACCENTS[i % len(ACCENTS)] if i < len(rows) - 1 else ACCENTS[2]
        d.ellipse([130, y - 52, 234, y + 52], fill=col + (60,))
        dark = tuple(int(v * 0.62) for v in col)
        L.alpha_composite(icon(row[0], dark, 76), (144, int(y - 38)))
        if i < len(rows) - 1:
            d.text((270, y), row[1], font=font(CAP.FONT_TEXT, 56), fill=INK + (255,), anchor="lm")
        else:
            d.text((270, y - 26), row[1].upper(), font=font(CAP.FONT_TEXT_REG, 32), fill=MUTED + (255,),
                   anchor="lm")
            d.text((270, y + 22), row[2], font=font(CAP.FONT_TEXT, 54), fill=INK + (255,), anchor="lm")
        if 0 < i:
            d.line([(130, y - row_h / 2), (W - 130, y - row_h / 2)], fill=(200, 196, 220, 160), width=2)
        out.append(L)
    return out


def _shadow(L: Image.Image) -> Image.Image:
    a = np.asarray(L)[..., 3]
    sh = np.zeros((H, W, 4), np.uint8)
    sh[..., :3] = (60, 50, 100)
    sh[..., 3] = (a * 0.45).astype(np.uint8)
    s = Image.fromarray(sh, "RGBA").filter(ImageFilter.GaussianBlur(8))
    return Image.alpha_composite(s, L)


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- montage
def render(c: dict, out: str):
    model = CAP.ensure_voice()
    tmp = tempfile.mkdtemp(prefix="slide_")
    # La voix ne dit que le titre de l'étude ; ensuite le visuel défile seul, en musique.
    wavs = [os.path.join(tmp, "v0.wav")]
    title_dur = CAP.tts(c["voix"][0], wavs[0], model, 1.08)
    starts_v = [0.8]
    lay = layers(c)
    # Étapes : titre + nom, puis le nombre, puis chaque ligne de la carte, à intervalle régulier.
    first = 0.8 + title_dur + 0.6
    step = 2.2
    appear = [0.3] + [first + i * step for i in range(len(lay) - 1)]
    total = min(30.0, appear[-1] + 4.0)

    bg = background()
    lay_np = [np.asarray(L).astype(np.float32) for L in lay]
    silent = os.path.join(tmp, "video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "24", "-maxrate", "3500k", "-bufsize", "7000k", "-pix_fmt", "yuv420p", silent],
                           stdin=subprocess.PIPE)
    nf = int(round(total * FPS))
    for f in range(nf):
        tt = f / FPS
        p = tt / total
        z = 1.0 + 0.06 * p
        cw, ch = bg.width / 1.08 / z, bg.height / 1.08 / z
        cx, cy = bg.width / 2, bg.height / 2 - 20 * p
        frame = np.asarray(bg.resize((W, H), Image.BILINEAR,
                                     box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))).astype(np.float32)
        for L, a0 in zip(lay_np, appear):
            a = ease((tt - a0) / 0.7)
            if a <= 0:
                continue
            dy = int((1 - a) * 22)
            src = L
            if dy:
                src = np.zeros_like(L)
                src[:-dy] = L[dy:]
            al = src[..., 3:4] / 255 * a
            frame = frame * (1 - al) + src[..., :3] * al
        fade = min(1.0, tt / 0.5, (total - tt) / 0.8)
        enc.stdin.write(np.clip(frame * max(fade, 0), 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(CAP.MUSIC_START), "-t", f"{total:.2f}", "-i", CAP.MUSIC]
    for w in wavs:
        cmd += ["-i", w]
    fc, labels = [], []
    for i, st in enumerate(starts_v):
        ms = int(st * 1000)
        fc.append(f"[{i + 1}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms},volume=1.5[v{i}]")
        labels.append(f"[v{i}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(wavs)}:normalize=0,apad=whole_dur={total:.2f},asplit=2[vo][sc]")
    fc.append(f"[0:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.6,"
              f"afade=t=in:d=1.2,afade=t=out:st={total - 2.0:.2f}:d=2[mu]")
    fc.append("[mu][sc]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[duck]")
    fc.append("[duck][vo]amix=inputs=2:normalize=0,alimiter=limit=0.95[a]")
    audio = os.path.join(tmp, "audio.m4a")
    cmd += ["-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "aac", "-b:a", "160k", audio]
    subprocess.run(cmd, check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", audio, "-c:v", "copy", "-c:a", "copy",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    print(f"Capsule générée : {out} ({total:.1f} s)")
    return out


CONTENT = {"chemin_de_vie": content_chemin_de_vie}


def for_order(produit: str, people: list[Person], out: str, today: date | None = None):
    if produit not in CONTENT:
        raise KeyError(f"La capsule résumé n'existe pas encore pour « {produit} ».")
    return render(CONTENT[produit](people[0], today), out)


if __name__ == "__main__":
    from generate import person_from
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--produit", default="chemin_de_vie")
    ap.add_argument("--json", required=True)
    ap.add_argument("--aujourdhui")
    ap.add_argument("-o", "--sortie", required=True)
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))
    people = [person_from(x) for x in d["personnes"]] if "personnes" in d else [person_from(d)]
    for_order(a.produit, people, a.sortie, date.fromisoformat(a.aujourdhui) if a.aujourdhui else None)
