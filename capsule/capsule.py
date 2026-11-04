#!/usr/bin/env python3
"""Gabarit de capsule vidéo Destin & Vie (9:16, 1080x1920, MP4, 30 s maximum).

Chaque commande produit une capsule personnalisée, sans intervention :
- fond : le ciel étoilé du site (assets/fond_site.jpg), en lent travelling
- charte : encre et laiton, polices Marcellus (titres) et Liberation Sans (sous-titres)
- emplacements : grand titre, PRÉNOM, NOM, grand chiffre, sous-titre de la voix off
- voix off française : Piper, modèle fr_FR-siwis-medium (local, gratuit)
- musique : « Kalimba Relaxation Music », Kevin MacLeod, FreePD, CC0 (domaine public)
  baissée automatiquement sous la voix
- modèles de script par produit : modeles.json (variables remplies depuis le moteur)

Usage direct :
  python3 capsule.py --produit chemin_de_vie --json ../exemples/commande_exemple.json -o capsule.mp4
Depuis generate.py : ajouter --video.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
import textwrap
import urllib.request
import wave
from datetime import date

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from destin_vie import numerology as NU                     # noqa: E402
from destin_vie import reading as RD                        # noqa: E402
from destin_vie.reading import MONTHS, Person, g            # noqa: E402
from destin_vie.texts import numbers as NT                  # noqa: E402
from destin_vie.texts import year_texts as YT               # noqa: E402

W, H, FPS = 1080, 1920, 30
MAX_DUR = 30.0
FADE = 0.45
INK = (27, 36, 64)
BRASS = (215, 180, 110)
WHITE = (246, 243, 236)

FOND = os.path.join(HERE, "assets", "fond_site.jpg")
FONT_DISPLAY = os.path.join(HERE, "assets", "Marcellus-Regular.ttf")
FONT_TEXT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_TEXT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
MUSIC = os.path.join(HERE, "musique", "Kalimba Relaxation Music.mp3")
MUSIC_START = 8.0
MODELES = os.path.join(HERE, "modeles.json")
VOICE_DIR = os.path.join(HERE, "voix")
VOICE = "fr_FR-siwis-medium"
VOICE_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/siwis/medium/"

# ---------------------------------------------------------------- textes courts
PHRASE = {
    1: "Vous êtes {fait|faite} pour ouvrir la voie.", 2: "Votre force, c'est l'écoute et le lien.",
    3: "Vous avancez par la parole et la création.", 4: "Vous construisez du solide, pas à pas.",
    5: "Vous êtes {fait|faite} pour la liberté et la découverte.", 6: "Vous prenez soin de ceux que vous aimez.",
    7: "Vous cherchez le sens profond des choses.", 8: "Vous visez haut, et vous savez réaliser.",
    9: "Votre cœur est ouvert sur le monde.", 11: "Votre intuition éclaire les autres.",
    22: "Vous êtes {fait|faite} pour bâtir grand.", 33: "Vous êtes {né|née} pour guider et transmettre.",
}
PHRASE_ENFANT = {
    1: "{Il} aime décider et ouvrir la voie.", 2: "{Il} est tout en douceur et en écoute.",
    3: "{Il} avance par la parole, le jeu et la création.", 4: "{Il} aime les choses bien faites.",
    5: "{Il} a besoin de bouger et de découvrir.", 6: "{Il} prend soin de ceux qu'{il} aime.",
    7: "{Il} veut tout comprendre.", 8: "{Il} aime relever des défis.",
    9: "{Il} a un grand cœur, ouvert sur le monde.", 11: "{Il} a une intuition très vive.",
    22: "{Il} a l'âme d'un bâtisseur.", 33: "{Il} a le sens du partage et de l'entraide.",
}
COUPLE_PHRASE = {
    1: "Ensemble, vous osez davantage.", 2: "Votre couple vit de tendresse et de dialogue.",
    3: "Votre couple aime rire, sortir et partager.", 4: "Ensemble, vous construisez du durable.",
    5: "Votre couple a besoin d'aventure et de liberté.", 6: "Votre couple est tourné vers le foyer.",
    7: "Votre couple partage une complicité profonde.", 8: "Ensemble, vous réussissez vos projets.",
    9: "Votre couple est généreux et ouvert sur le monde.",
}

UNITS = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze",
         "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]


def mots(n: int) -> str:
    if n < 20:
        return UNITS[n]
    if n < 40:
        d, u = divmod(n, 10)
        base = {2: "vingt", 3: "trente"}[d]
        return base + ("" if u == 0 else (" et un" if u == 1 else "-" + UNITS[u]))
    return str(n)


# ---------------------------------------------------------------- variables
def variables(produit: str, people: list[Person], today: date | None = None) -> tuple[str, dict]:
    """Choisit le modèle et calcule les variables à injecter, depuis le moteur."""
    today = today or date.today()
    p = people[0]
    child = p.age(today) < 16
    v = {"prenom": p.first, "nom": p.nom.upper(), "prenoms": p.prenoms}

    if produit in ("chemin_de_vie", "essentiel", "compatibilite"):
        n = NU.compute(p.full_name, p.naissance, today)
        lp = n.life_path
        title = NT.LIFE_PATH[lp]["title"].replace(" (nombre maître)", "")
        traits = NT.LIFE_PATH[lp]["traits"].rstrip(".").split(", ")
        main = n.challenges[2]
        st = NT.SOUL[n.soul][0]
        v.update(chemin=lp, chemin_mots=mots(lp), chemin_titre=title,
                 chemin_titre_min=title[0].lower() + title[1:],
                 ame=("une " if st.split()[0] in ("Soif", "Âme") else "un ") + st.lower(),
                 phrase=g((PHRASE_ENFANT if child else PHRASE)[lp], p),
                 forces=", ".join(traits[:3]),
                 defi=NT.CHALLENGE[main])

    if produit in ("prevision_2027", "essentiel", "chemin_de_vie"):
        from destin_vie.products import prevision_2027 as PV
        f = PV.compute(p, today)
        y = YT.YEAR[f.base]
        strong = [m for m in f.months if m["number"] in (1, 8) or m["number"] == NU.base(f.life_path)]
        soft = [m for m in f.months if m["number"] in YT.CARE and m["number"] != NU.base(f.life_path)]
        v.update(annee=f.year_number, annee_mots=mots(f.year_number), annee_titre=y["title"],
                 annee_titre_min=y["title"][0].lower() + y["title"][1:],
                 annee_cles=y["keywords"], favorise=g(y["favorable"], p),
                 mois_fort=MONTHS[(strong or f.months)[0]["month"] - 1],
                 mois_doux=MONTHS[(soft or f.months)[0]["month"] - 1])

    if produit == "compatibilite":
        from destin_vie.products import compatibilite as CP
        q = people[1]
        x = CP.analyse(p, q, today)
        v.update(prenom2=q.first, nom2=q.nom.upper(), couple=x["couple"], couple_mots=mots(x["couple"]),
                 couple_titre=CP.CT.COUPLE[x["couple"]][0],
                 couple_titre_min="un" + CP.CT.COUPLE[x["couple"]][0][2:], couple_phrase=COUPLE_PHRASE[x["couple"]],
                 force=_force(x), friction=_friction(x),
                 conseil=CP.CT.ADVICE[x["fa"]].split(",")[0].rstrip(".") .lower())
    key = produit + ("_enfant" if child and produit in ("chemin_de_vie", "prevision_2027") else "")
    return key, v


def _friction(x) -> str:
    hard = [c for c in x["contacts"] if c["kind"] in ("carré", "opposition")]
    if hard:
        t = hard[0]["topic"].replace("leurs ", "vos ").replace("leur ", "votre ")
        t = ("de " + t).replace("de le ", "du ").replace("de les ", "des ")
        t = t.replace(" et l'", " et de l'")
        return "parler ouvertement " + t
    if x["fa"] != x["fb"]:
        return "des rythmes différents à accorder"
    return "le risque de partager les mêmes angles morts"


def _force(x) -> str:
    if x["fa"] == x["fb"]:
        return "vous vous comprenez sans tout expliquer"
    na, nb = x["ra"].num, x["rb"].num
    from destin_vie.texts import compat_texts as CT
    if CT.FAMILY[NU.base(na.soul)] == CT.FAMILY[NU.base(nb.soul)]:
        return "vos besoins profonds se rejoignent"
    soft = [c for c in x["contacts"] if c["kind"] in ("trigone", "sextile", "conjonction")]
    if soft:
        return "une belle entente sur " + soft[0]["topic"]
    return "vous vous complétez"


# ---------------------------------------------------------------- voix
def ensure_voice() -> str:
    os.makedirs(VOICE_DIR, exist_ok=True)
    for f in (VOICE + ".onnx", VOICE + ".onnx.json"):
        path = os.path.join(VOICE_DIR, f)
        if not os.path.exists(path):
            print(f"Téléchargement de la voix {f}…")
            urllib.request.urlretrieve(VOICE_URL + f, path)
    return os.path.join(VOICE_DIR, VOICE + ".onnx")


def tts(text: str, out: str, model: str, speed: float) -> float:
    subprocess.run([sys.executable, "-m", "piper", "-m", model, "--length-scale", f"{speed:.2f}", "-f", out],
                   input=text.encode(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(out) as w:
        return w.getnframes() / w.getframerate()


# ---------------------------------------------------------------- dessin
def font(path, size):
    return ImageFont.truetype(path, size)


def background() -> Image.Image:
    """Fond du site recadré en 9:16, avec une marge horizontale pour le travelling."""
    img = Image.open(FOND).convert("RGB")
    h = img.height
    w = int(h * 9 / 16 * 1.35)
    x = (img.width - w) // 2
    img = img.crop((x, 0, x + w, h))
    return img.resize((int(W * 1.35 * 1.06), int(H * 1.06)), Image.LANCZOS)


def static_layer() -> Image.Image:
    """Voile sombre, marque et filets, communs à toute la capsule."""
    a = np.zeros((H, W), np.float32)
    ys = np.arange(H, dtype=np.float32)[:, None]
    a += 95
    a = np.maximum(a, np.clip((ys - H * 0.55) / (H * 0.45), 0, 1) * 200)
    a = np.maximum(a, np.clip((H * 0.14 - ys) / (H * 0.14), 0, 1) * 170)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = INK
    rgba[..., 3] = a.astype(np.uint8)
    layer = Image.fromarray(rgba, "RGBA")
    d = ImageDraw.Draw(layer)
    d.text((W / 2, 175), "DESTIN & VIE", font=font(FONT_DISPLAY, 50), fill=BRASS + (255,), anchor="mm")
    d.line([(W / 2 - 60, 222), (W / 2 + 60, 222)], fill=BRASS + (200,), width=2)
    return layer


def _wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def emblem(d, cx, cy, r):
    for rr in (r, r - 22):
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=BRASS + (255,), width=3)
    for k in range(12):
        a = math.radians(k * 30)
        d.line([(cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a)),
                (cx + r * math.cos(a), cy + r * math.sin(a))], fill=BRASS + (255,), width=3)


def scene_layer(sc: dict, v: dict) -> Image.Image:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if sc.get("fin"):
        emblem(d, W / 2, H * 0.36, 150)
        d.ellipse([W / 2 - 9, H * 0.36 - 9, W / 2 + 9, H * 0.36 + 9], fill=BRASS + (255,))
        d.text((W / 2, H * 0.53), "Destin & Vie", font=font(FONT_DISPLAY, 130), fill=BRASS + (255,), anchor="mm")
        d.line([(W / 2 - 90, H * 0.585), (W / 2 + 90, H * 0.585)], fill=BRASS + (255,), width=3)
    else:
        if sc.get("titre"):
            ft = font(FONT_DISPLAY, 92)
            lines = _wrap(d, sc["titre"].format(**v), ft, W - 160)
            y = 470 - (len(lines) - 1) * 52
            for i, ln in enumerate(lines):
                d.text((W / 2, y + i * 104), ln, font=ft, fill=BRASS + (255,), anchor="mm")
        if sc.get("nom"):
            if "prenom2" in v:
                big = f"{v['prenom']} & {v['prenom2']}"
                small = f"{v['nom']}  ·  {v['nom2']}"
            else:
                big, small = v["prenom"], v["nom"]
            fs = 150 if len(big) <= 10 else (118 if len(big) <= 16 else 92)
            d.text((W / 2, 860), big, font=font(FONT_DISPLAY, fs), fill=WHITE + (255,), anchor="mm")
            fn = font(FONT_TEXT_REG, 46)
            spaced = " ".join(small)
            if d.textlength(spaced, font=fn) > W - 120:
                spaced = small
            d.text((W / 2, 990), spaced, font=fn, fill=BRASS + (255,), anchor="mm")
        if sc.get("chiffre"):
            emblem(d, W / 2, 900, 210)
            d.text((W / 2, 905), str(sc["chiffre"]).format(**v), font=font(FONT_DISPLAY, 230),
                   fill=WHITE + (255,), anchor="mm")
    # sous-titre
    text = sc.get("ecran", "").format(**v)
    if not text:
        return layer
    text = text[0].upper() + text[1:]
    centre = not (sc.get("fin") or sc.get("nom") or sc.get("chiffre"))
    ft = font(FONT_TEXT, 72 if centre else 60)
    lines = _wrap(d, text, ft, W - 150)
    lh = 92 if centre else 76
    y0 = (930 if centre else 1460) - (len(lines) * lh) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i, ln in enumerate(lines):
        sd.text((W / 2, y0 + i * lh + 4 + int(lh * 0.72)), ln, font=ft, fill=(0, 0, 0, 190), anchor="ms")
    layer = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)), layer)
    d = ImageDraw.Draw(layer)
    for i, ln in enumerate(lines):
        d.text((W / 2, y0 + i * lh + int(lh * 0.72)), ln, font=ft, fill=WHITE + (255,), anchor="ms")
    return layer


# ---------------------------------------------------------------- montage
def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def render(scenes: list[dict], v: dict, out: str):
    model = ensure_voice()
    tmp = tempfile.mkdtemp(prefix="capsule_")
    texts = [sc.get("voix", "").format(**v) for sc in scenes]

    # Durées : voix + respiration ; on accélère légèrement si on dépasse 30 s.
    for speed in (1.08, 1.0, 0.92, 0.86):
        wavs, durs = [], []
        for i, t in enumerate(texts):
            if not t:
                wavs.append(None)
                durs.append(0.0)
                continue
            w = os.path.join(tmp, f"v{i}.wav")
            durs.append(tts(t, w, model, speed))
            wavs.append(w)
        pads = [d + 1.3 if d else 2.4 for d in durs]
        if sum(pads) <= MAX_DUR:
            break
    scale = min(1.0, MAX_DUR / sum(pads))
    pads = [p * scale for p in pads]
    starts = np.cumsum([0] + pads[:-1]).tolist()
    total = sum(pads)

    bg = background()
    static = np.asarray(static_layer()).astype(np.float32)
    layers = [np.asarray(scene_layer(sc, v)).astype(np.float32) for sc in scenes]

    silent = os.path.join(tmp, "video.mp4")
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
                            "-crf", "26", "-maxrate", "3500k", "-bufsize", "7000k", "-pix_fmt", "yuv420p", silent], stdin=subprocess.PIPE)
    n = int(round(total * FPS))
    span_x = bg.width - W
    for f in range(n):
        t = f / FPS
        p = t / total
        z = 1.0 + 0.05 * p
        cw, ch = W / z * 1.0, H / z * 1.0
        cx = W / 2 + span_x * (0.15 + 0.7 * p)
        cy = bg.height / 2
        frame = np.asarray(bg.resize((W, H), Image.BILINEAR,
                                     box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))).astype(np.float32)
        al = static[..., 3:4] / 255
        frame = frame * (1 - al) + static[..., :3] * al
        for i, L in enumerate(layers):
            lt = t - starts[i]
            if lt < -FADE or lt > pads[i] + FADE:
                continue
            a = ease((lt + 0.0) / FADE) if i > 0 else ease(lt / 0.6)
            if i < len(layers) - 1:
                a *= 1 - ease((lt - pads[i] + FADE) / FADE)
            if a <= 0:
                continue
            dy = int((1 - ease(lt / 0.7)) * 24) if lt < 0.7 else 0
            src = L
            if dy > 0:
                src = np.zeros_like(L)
                src[:-dy] = L[dy:]
            la = src[..., 3:4] / 255 * a
            frame = frame * (1 - la) + src[..., :3] * la
        if t > total - 0.6:
            frame *= max(0.0, (total - t) / 0.6)
        if t < 0.4:
            frame *= t / 0.4
        enc.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()

    # Audio : voix posées sur la timeline, musique baissée sous la voix (sidechain).
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(MUSIC_START), "-t", f"{total:.2f}", "-i", MUSIC]
    voiced = [(w, st) for w, st in zip(wavs, starts) if w]
    for w, _ in voiced:
        cmd += ["-i", w]
    fc, labels = [], []
    for i, (_, st) in enumerate(voiced):
        ms = int((st + 0.35) * 1000)
        fc.append(f"[{i + 1}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms},volume=1.5[v{i}]")
        labels.append(f"[v{i}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(voiced)}:normalize=0[voice]")
    fc.append(f"[voice]apad=whole_dur={total:.2f},asplit=2[vo][sc]")
    fc.append(f"[0:a]aresample=44100,aformat=channel_layouts=stereo,volume=0.55,"
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


def for_order(produit: str, people: list[Person], out: str, today: date | None = None):
    key, v = variables(produit, people, today)
    modeles = json.load(open(MODELES, encoding="utf-8"))
    if key not in modeles:
        raise KeyError(f"Pas de modèle de capsule pour « {key} » dans modeles.json")
    return render(modeles[key], v, out)


if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    from generate import person_from
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--produit", required=True)
    ap.add_argument("--json", required=True)
    ap.add_argument("--aujourdhui")
    ap.add_argument("-o", "--sortie", required=True)
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))
    people = [person_from(x) for x in d["personnes"]] if "personnes" in d else [person_from(d)]
    for_order(a.produit, people, a.sortie, date.fromisoformat(a.aujourdhui) if a.aujourdhui else None)
