#!/usr/bin/env python3
"""Relève les nouvelles commandes du site (Netlify Forms), génère l'étude et l'envoie par mail au gérant.

Le paiement Airtel Money n'est PAS vérifié automatiquement : le mail rappelle la référence
« DV + nom » à contrôler dans le compte marchand avant de transmettre l'étude au client.

Variables d'environnement (secrets GitHub) :
  NETLIFY_TOKEN       jeton d'accès personnel Netlify (lecture des formulaires)
  NETLIFY_SITE        domaine du site, par défaut destin-et-vie.online
  GMAIL_USER          adresse Gmail qui envoie
  GMAIL_APP_PASSWORD  mot de passe d'application Gmail
  DEST_EMAIL          adresse qui reçoit les études (par défaut GMAIL_USER)
"""
import json, os, re, smtplib, subprocess, sys, tempfile, unicodedata, urllib.request
from email.message import EmailMessage

ICI = os.path.dirname(os.path.abspath(__file__))
ETAT = os.path.join(ICI, "etat", "traitees.json")
PRODUITS = {"prevision": "prevision_2027", "decouverte": "chemin_de_vie", "essentiel": "essentiel",
            "compatibilite": "compatibilite", "famille": None}


def norm(s):
    return unicodedata.normalize("NFD", s or "").encode("ascii", "ignore").decode().lower()


def produit_de(etude):
    for cle, prod in PRODUITS.items():
        if cle in norm(etude):
            return cle, prod
    return None, None


def soumissions():
    site = os.environ.get("NETLIFY_SITE", "destin-et-vie.online")
    req = urllib.request.Request(f"https://api.netlify.com/api/v1/sites/{site}/submissions?per_page=100",
                                 headers={"Authorization": "Bearer " + os.environ["NETLIFY_TOKEN"],
                                          "User-Agent": "destin-et-vie-commandes"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return [s for s in json.load(r) if s.get("form_name") == "commande"]


def personne(d):
    prenoms, nom = (d.get("prenoms") or "").strip(), (d.get("nom") or "").strip()
    if not (prenoms and nom):                      # ancienne version du formulaire : un seul champ
        mots = (d.get("noms") or "").split()
        prenoms, nom = " ".join(mots[:-1]) or (mots[0] if mots else ""), mots[-1] if mots else ""
    j, m, a = re.match(r"(\d{2})/(\d{2})/(\d{4})", d.get("naissance", "")).groups()
    p = {"prenoms": prenoms, "nom": nom, "sexe": (d.get("sexe") or "F")[:1].upper(),
         "date": f"{a}-{m}-{j}", "lieu": d.get("lieu") or ""}
    if d.get("heure"):
        p["heure"] = d["heure"]
    return p


def generer(prod, pers, ref, dossier):
    cmd = os.path.join(dossier, "commande.json")
    json.dump({**pers, "ref": ref}, open(cmd, "w", encoding="utf-8"), ensure_ascii=False)
    pdf = os.path.join(dossier, f"Destin_et_Vie_{ref}.pdf")
    r = subprocess.run([sys.executable, os.path.join(ICI, "generate.py"), "--produit", prod, "--json", cmd,
                        "--ref", ref, "-o", pdf, "--video"], capture_output=True, text=True, cwd=ICI)
    journal = (r.stdout + r.stderr).strip()
    pieces = [f for f in (pdf, pdf[:-4] + ".mp4") if os.path.exists(f)]
    return r.returncode == 0, pieces, journal


def envoyer(sujet, corps, pieces):
    m = EmailMessage()
    m["From"], m["To"] = os.environ["GMAIL_USER"], os.environ.get("DEST_EMAIL") or os.environ["GMAIL_USER"]
    m["Subject"] = sujet
    m.set_content(corps)
    for f in pieces:
        typ = ("application", "pdf") if f.endswith(".pdf") else ("video", "mp4")
        m.add_attachment(open(f, "rb").read(), maintype=typ[0], subtype=typ[1], filename=os.path.basename(f))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.environ["GMAIL_USER"], os.environ["GMAIL_APP_PASSWORD"])
        s.send_message(m)


def main():
    os.makedirs(os.path.dirname(ETAT), exist_ok=True)
    faites = set(json.load(open(ETAT)) if os.path.exists(ETAT) else [])
    nouvelles = [s for s in soumissions() if s["id"] not in faites]
    print(f"{len(nouvelles)} nouvelle(s) commande(s)")
    for s in sorted(nouvelles, key=lambda x: x.get("created_at", "")):
        d, ref = s.get("data", {}), "DV-" + s["id"][-6:].upper()
        cle, prod = produit_de(d.get("etude", ""))
        entete = (f"Commande {ref} reçue le {s.get('created_at', '')[:16].replace('T', ' ')}\n\n"
                  f"Étude : {d.get('etude')} — {d.get('montant')}\n"
                  f"Référence Airtel annoncée : {d.get('reference') or '—'}\n"
                  f"Contact du client : {d.get('contact') or 'son numéro WhatsApp'}\n\n"
                  "À FAIRE : vérifier ce paiement dans le compte marchand Airtel (code KAMD), "
                  "puis transmettre les pièces jointes au client.\n\n"
                  f"--- Message du client ---\n{d.get('message', '')}\n")
        pieces, statut = [], "à traiter à la main"
        if prod and cle != "compatibilite":
            try:
                with tempfile.TemporaryDirectory() as tmp:
                    ok, pieces, journal = generer(prod, personne(d), ref, tmp)
                    if ok:
                        statut = "étude prête"
                        envoyer(f"[Destin & Vie] {ref} — {d.get('etude')} — {statut}", entete, pieces)
                    else:
                        envoyer(f"[Destin & Vie] {ref} — génération impossible",
                                entete + f"\n--- Erreur ---\n{journal[-1500:]}\n", [])
            except Exception as e:  # noqa: BLE001 — on prévient le gérant plutôt que de bloquer la file
                envoyer(f"[Destin & Vie] {ref} — génération impossible", entete + f"\n--- Erreur ---\n{e}\n", [])
        else:
            envoyer(f"[Destin & Vie] {ref} — {d.get('etude')} — {statut}",
                    entete + "\nCe pack concerne plusieurs personnes : les données des autres personnes "
                             "arrivent par WhatsApp. Transmettez-les à Claude pour générer l'étude.\n", [])
        faites.add(s["id"])
        json.dump(sorted(faites), open(ETAT, "w"))
        print(ref, statut)


if __name__ == "__main__":
    main()
