#!/usr/bin/env python3
"""Génère une étude Destin & Vie en PDF (et, en option, sa capsule vidéo).

Exemples :
  python3 generate.py --prenoms "Thimy Akam Matungiatia" --nom "Mbadinga Ella" \
      --sexe M --date 2021-01-24 --heure 15:30 --lieu "Akanda, Gabon" -o thimy.pdf
  python3 generate.py --produit prevision_2027 --json commande.json -o etude.pdf
  python3 generate.py --produit compatibilite --json couple.json -o couple.pdf --video
"""
import argparse
import json
import os
import sys
from datetime import date

from destin_vie.products import MULTI, PRODUCTS
from destin_vie.reading import Person


def person_from(d: dict) -> Person:
    p = Person(prenoms=d.get("prenoms"), nom=d.get("nom"), sexe=d.get("sexe"),
               naissance=date.fromisoformat(d["date"]), heure=d.get("heure"), lieu=d.get("lieu"),
               prenom_usuel=d.get("prenom_usuel"), lat=d.get("lat"), lon=d.get("lon"), tz=d.get("tz"))
    if not all([p.prenoms, p.nom, p.sexe, p.lieu]):
        raise ValueError("prenoms, nom, sexe, date et lieu sont obligatoires")
    return p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--produit", default="chemin_de_vie", choices=sorted(PRODUCTS))
    ap.add_argument("--json", help="Fichier JSON de la commande (voir README)")
    ap.add_argument("--prenoms"); ap.add_argument("--nom"); ap.add_argument("--sexe", choices=["M", "F"])
    ap.add_argument("--date", help="AAAA-MM-JJ"); ap.add_argument("--heure", help="HH:MM (facultatif)")
    ap.add_argument("--lieu"); ap.add_argument("--prenom-usuel")
    ap.add_argument("--lat", type=float); ap.add_argument("--lon", type=float); ap.add_argument("--tz")
    ap.add_argument("--ref", help="Référence de commande imprimée sur la couverture")
    ap.add_argument("--aujourdhui", help="Date de référence AAAA-MM-JJ (tests)")
    ap.add_argument("--video", action="store_true", help="Génère aussi la capsule vidéo (même nom, .mp4)")
    ap.add_argument("-o", "--sortie", required=True)
    a = ap.parse_args(argv)

    d = json.load(open(a.json, encoding="utf-8")) if a.json else {}
    cli = {k: v for k, v in dict(prenoms=a.prenoms, nom=a.nom, sexe=a.sexe, date=a.date, heure=a.heure,
                                 lieu=a.lieu, prenom_usuel=a.prenom_usuel, lat=a.lat, lon=a.lon, tz=a.tz).items()
           if v is not None}
    try:
        if "personnes" in d:
            people = [person_from(x) for x in d["personnes"]]
        else:
            people = [person_from({**cli, **d})]
    except (TypeError, ValueError, KeyError) as e:
        sys.exit(f"Données incomplètes : {e}")
    need = MULTI.get(a.produit, 1)
    lo, hi = need if isinstance(need, tuple) else (need, need)
    if not lo <= len(people) <= hi:
        sys.exit(f"Le produit {a.produit} demande {lo if lo == hi else f'{lo} à {hi}'} personne(s) ; "
                 f"la commande en contient {len(people)}.")
    roles = [x.get("role", "") for x in d.get("personnes", [])]
    for p in people:
        try:
            pl = p.place()
        except LookupError as e:
            sys.exit(str(e))
        print(f"{p.first} : lieu retenu {pl.name} ({pl.coords_label()}, fuseau {pl.tz}). Vérifiez l'acte.")

    today = date.fromisoformat(a.aujourdhui) if a.aujourdhui else None
    ref = a.ref or d.get("ref")
    try:
        extra = {"roles": roles} if a.produit == "famille" else {}
        PRODUCTS[a.produit](*people, a.sortie, today=today, order_ref=ref, **extra)
    except (LookupError, ValueError) as e:
        sys.exit(str(e))
    print(f"Étude générée : {a.sortie}")

    if a.video and a.produit == "famille":
        print("Pas de capsule vidéo pour le pack Famille.")
    elif a.video:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "capsule"))
        import capsule
        import slide
        out = os.path.splitext(a.sortie)[0] + ".mp4"
        if a.produit in slide.CONTENT:      # capsule résumé sur une seule diapositive
            slide.for_order(a.produit, people, out, today=today)
        else:                               # ancien gabarit multi-scènes, en attendant
            capsule.for_order(a.produit, people, out, today=today)


if __name__ == "__main__":
    main()
