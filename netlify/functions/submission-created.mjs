// Déclenchée par Netlify à chaque commande validée sur le site (formulaire « commande »).
// Elle réveille aussitôt la tâche GitHub qui génère l'étude et l'envoie par mail.
// Variable d'environnement Netlify requise : GH_TOKEN (jeton GitHub limité à « Actions : lecture et écriture »).
const DEPOT = "assoumoualonzo-source/destin-et-vie";

export default async (req) => {
  let formulaire = "";
  try { formulaire = (await req.json())?.payload?.form_name || ""; } catch {}
  if (formulaire && formulaire !== "commande") return new Response("ignoré");
  const r = await fetch(`https://api.github.com/repos/${DEPOT}/actions/workflows/commandes.yml/dispatches`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.GH_TOKEN}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "destin-et-vie-netlify",
    },
    body: JSON.stringify({ ref: "main" }),
  });
  console.log("Déclenchement GitHub :", r.status);
  return new Response(r.ok ? "ok" : `erreur ${r.status}`, { status: r.ok ? 200 : 502 });
};
