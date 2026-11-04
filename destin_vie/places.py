"""Lieux de naissance : coordonnées et fuseau horaire.

La table couvre les villes du Gabon et les villes de naissance fréquentes de la
diaspora et des pays voisins. Pour un lieu absent, passer latitude, longitude et
fuseau IANA explicitement (voir README).
"""
from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class Place:
    name: str
    lat: float
    lon: float
    tz: str

    def utc_offset(self, local: datetime) -> float:
        off = ZoneInfo(self.tz).utcoffset(local)
        return off.total_seconds() / 3600

    def coords_label(self) -> str:
        ns = "N" if self.lat >= 0 else "S"
        ew = "E" if self.lon >= 0 else "O"
        def dm(x):
            x = abs(x)
            return f"{int(x)}°{int(round((x % 1) * 60)):02d}'"
        return f"{dm(self.lat)} {ns}, {dm(self.lon)} {ew}"


G = "Africa/Libreville"
CITIES = {
    # Gabon (UTC+1 toute l'année)
    "Libreville": (0.392, 9.454, G), "Akanda": (0.567, 9.483, G), "Owendo": (0.291, 9.504, G),
    "Ntoum": (0.390, 9.761, G), "Kango": (0.171, 10.125, G), "Cocobeach": (1.000, 9.583, G),
    "Port-Gentil": (-0.719, 8.781, G), "Omboué": (-1.574, 9.262, G), "Lambaréné": (-0.700, 10.240, G),
    "Fougamou": (-1.216, 10.583, G), "Ndjolé": (-0.183, 10.765, G), "Franceville": (-1.633, 13.583, G),
    "Moanda": (-1.567, 13.200, G), "Mounana": (-1.408, 13.161, G), "Okondja": (-0.656, 13.675, G),
    "Léconi": (-1.588, 14.247, G), "Bongoville": (-1.320, 13.633, G), "Oyem": (1.599, 11.579, G),
    "Bitam": (2.077, 11.500, G), "Mitzic": (0.782, 11.548, G), "Minvoul": (2.150, 12.133, G),
    "Médouneu": (0.950, 10.783, G), "Makokou": (0.571, 12.864, G), "Mékambo": (1.017, 13.933, G),
    "Booué": (-0.100, 11.941, G), "Koulamoutou": (-1.135, 12.474, G), "Lastoursville": (-0.818, 12.708, G),
    "Mouila": (-1.868, 11.056, G), "Ndendé": (-2.401, 11.358, G), "Mbigou": (-1.900, 11.933, G),
    "Lébamba": (-2.200, 11.483, G), "Tchibanga": (-2.850, 11.033, G), "Mayumba": (-3.432, 10.655, G),
    "Gamba": (-2.650, 10.000, G),
    # Afrique centrale et de l'Ouest
    "Yaoundé": (3.867, 11.517, "Africa/Douala"), "Douala": (4.050, 9.700, "Africa/Douala"),
    "Ebolowa": (2.900, 11.150, "Africa/Douala"), "Brazzaville": (-4.267, 15.283, "Africa/Brazzaville"),
    "Pointe-Noire": (-4.778, 11.863, "Africa/Brazzaville"), "Kinshasa": (-4.322, 15.312, "Africa/Kinshasa"),
    "Malabo": (3.750, 8.783, "Africa/Malabo"), "Bata": (1.863, 9.765, "Africa/Malabo"),
    "Bangui": (4.367, 18.583, "Africa/Bangui"), "São Tomé": (0.336, 6.727, "Africa/Sao_Tome"),
    "Dakar": (14.693, -17.447, "Africa/Dakar"), "Abidjan": (5.360, -4.008, "Africa/Abidjan"),
    "Lomé": (6.131, 1.223, "Africa/Lome"), "Cotonou": (6.366, 2.418, "Africa/Porto-Novo"),
    "Lagos": (6.455, 3.384, "Africa/Lagos"), "Bamako": (12.639, -8.003, "Africa/Bamako"),
    "Ouagadougou": (12.371, -1.520, "Africa/Ouagadougou"), "Casablanca": (33.573, -7.589, "Africa/Casablanca"),
    # Europe et Amérique du Nord
    "Paris": (48.857, 2.352, "Europe/Paris"), "Lyon": (45.764, 4.836, "Europe/Paris"),
    "Marseille": (43.296, 5.370, "Europe/Paris"), "Bordeaux": (44.838, -0.579, "Europe/Paris"),
    "Toulouse": (43.605, 1.444, "Europe/Paris"), "Lille": (50.629, 3.057, "Europe/Paris"),
    "Montpellier": (43.611, 3.877, "Europe/Paris"), "Nantes": (47.218, -1.554, "Europe/Paris"),
    "Bruxelles": (50.850, 4.352, "Europe/Brussels"), "Genève": (46.204, 6.143, "Europe/Zurich"),
    "Montréal": (45.502, -73.567, "America/Toronto"), "Québec": (46.813, -71.208, "America/Toronto"),
}


def _key(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return "".join(c for c in s if c.isalnum())


_INDEX = {_key(k): k for k in CITIES}


def resolve(text: str) -> Place:
    """Trouve la ville dans un texte libre (« Akanda, Gabon », « né à Port Gentil »)."""
    parts = [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]
    for candidate in parts + [text]:
        k = _key(candidate)
        if k in _INDEX:
            name = _INDEX[k]
            lat, lon, tz = CITIES[name]
            return Place(name, lat, lon, tz)
    k_all = _key(text)
    for k, name in sorted(_INDEX.items(), key=lambda kv: -len(kv[0])):
        if k and k in k_all:
            lat, lon, tz = CITIES[name]
            return Place(name, lat, lon, tz)
    raise LookupError(
        f"Lieu inconnu : « {text} ». Ajoutez-le dans places.CITIES ou fournissez "
        "latitude, longitude et fuseau.")
