"""Thème natal : positions tropicales géocentriques (PyEphem), maisons Placidus.

Précision : de l'ordre de la minute d'arc pour les planètes, suffisante pour un
thème de naissance. Le Nœud Nord est le nœud moyen.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import ephem

SIGNS = ["Bélier", "Taureau", "Gémeaux", "Cancer", "Lion", "Vierge",
         "Balance", "Scorpion", "Sagittaire", "Capricorne", "Verseau", "Poissons"]
ELEMENT = {s: e for s, e in zip(SIGNS, ["Feu", "Terre", "Air", "Eau"] * 3)}
MODE = {s: m for s, m in zip(SIGNS, ["Cardinal", "Fixe", "Mutable"] * 4)}

BODIES = [("Soleil", ephem.Sun), ("Lune", ephem.Moon), ("Mercure", ephem.Mercury),
          ("Vénus", ephem.Venus), ("Mars", ephem.Mars), ("Jupiter", ephem.Jupiter),
          ("Saturne", ephem.Saturn), ("Uranus", ephem.Uranus), ("Neptune", ephem.Neptune),
          ("Pluton", ephem.Pluto)]
PERSONAL = ["Soleil", "Lune", "Mercure", "Vénus", "Mars"]
ASPECTS = [("conjonction", 0, 8), ("sextile", 60, 4), ("carré", 90, 7),
           ("trigone", 120, 7), ("opposition", 180, 8)]


def sign_of(lon: float) -> str:
    return SIGNS[int((lon % 360) // 30)]


def fmt(lon: float) -> str:
    lon %= 360
    tot = round(lon * 60)
    s, r = divmod(tot, 1800)
    return f"{SIGNS[s % 12]} {r // 60}°{r % 60:02d}'"


def _lon(body, d):
    body.compute(d, epoch=d)
    eq = ephem.Equatorial(body.g_ra, body.g_dec, epoch=d)
    return math.degrees(float(ephem.Ecliptic(eq).lon)) % 360


def _obliquity(d) -> float:
    t = (ephem.julian_date(d) - 2451545.0) / 36525
    return 23.4392911 - 0.0130042 * t


def _houses(d, lat, lon):
    obs = ephem.Observer()
    obs.lat, obs.lon, obs.date, obs.pressure = str(lat), str(lon), d, 0
    ramc = math.degrees(float(obs.sidereal_time()))
    e, f = math.radians(_obliquity(d)), math.radians(lat)
    rm = math.radians(ramc)
    mc = math.degrees(math.atan2(math.sin(rm), math.cos(rm) * math.cos(e))) % 360
    asc = math.degrees(math.atan2(math.cos(rm),
                                  -(math.sin(rm) * math.cos(e) + math.tan(f) * math.sin(e)))) % 360

    def ra2lon(ra):
        ra = math.radians(ra)
        return math.degrees(math.atan2(math.sin(ra), math.cos(ra) * math.cos(e))) % 360

    def cusp(k):
        start = {11: ramc + 30, 12: ramc + 60, 2: ramc + 120, 3: ramc + 150}[k]
        l = ra2lon(start)
        for _ in range(60):
            dec = math.asin(math.sin(e) * math.sin(math.radians(l)))
            x = max(-1.0, min(1.0, math.tan(f) * math.tan(dec)))
            ad = math.degrees(math.asin(x))
            ra = {11: ramc + (90 + ad) / 3, 12: ramc + 2 * (90 + ad) / 3,
                  2: ramc + 180 - 2 * (90 - ad) / 3, 3: ramc + 180 - (90 - ad) / 3}[k]
            l = ra2lon(ra)
        return l

    c = [0.0] * 13
    c[1], c[10] = asc, mc
    c[4], c[7] = (mc + 180) % 360, (asc + 180) % 360
    for k in (11, 12, 2, 3):
        c[k] = cusp(k)
        c[(k + 5) % 12 + 1] = (c[k] + 180) % 360
    return c[1:]


def _house_of(lon, cusps):
    for i in range(12):
        a, b = cusps[i], cusps[(i + 1) % 12]
        if (lon - a) % 360 < (b - a) % 360:
            return i + 1
    return 12


@dataclass
class Planet:
    name: str
    lon: float
    sign: str
    house: int | None
    retro: bool

    @property
    def pos(self) -> str:
        return fmt(self.lon)


@dataclass
class Aspect:
    a: str
    b: str
    kind: str
    orb: float


@dataclass
class Chart:
    local: datetime
    utc: datetime
    lat: float
    lon: float
    has_time: bool
    planets: dict[str, Planet]
    asc: float | None
    mc: float | None
    cusps: list[float] | None
    aspects: list[Aspect]
    moon_phase: str
    asc_change_minutes: tuple[int | None, int | None] = (None, None)  # avant, après
    moon_sign_certain: bool = True
    elements: dict[str, float] = field(default_factory=dict)
    modes: dict[str, float] = field(default_factory=dict)

    @property
    def asc_sign(self):
        return sign_of(self.asc) if self.asc is not None else None

    @property
    def mc_sign(self):
        return sign_of(self.mc) if self.mc is not None else None

    def dominant_element(self) -> str:
        return max(self.elements, key=self.elements.get)

    def stelliums(self) -> list[tuple[str, list[str]]]:
        """Signes contenant au moins trois planètes (hors trans-saturniennes)."""
        out = {}
        for p in self.planets.values():
            if p.name in ("Uranus", "Neptune", "Pluton", "Nœud Nord"):
                continue
            out.setdefault(p.sign, []).append(p.name)
        return [(s, ps) for s, ps in out.items() if len(ps) >= 3]


def _phase(elong: float) -> str:
    e = elong % 360
    if e < 45:
        return "nouvelle lune" if e < 12 else "Lune croissante, premier croissant"
    if e < 90:
        return "Lune croissante, premier croissant"
    if e < 135:
        return "premier quartier, Lune croissante"
    if e < 168:
        return "Lune gibbeuse croissante"
    if e < 192:
        return "pleine lune"
    if e < 270:
        return "Lune décroissante, après la pleine lune"
    if e < 315:
        return "dernier quartier, Lune décroissante"
    return "phase balsamique, juste avant la nouvelle lune"


def compute(local: datetime, utc_offset_h: float, lat: float, lon: float,
            has_time: bool = True) -> Chart:
    """`local` est l'heure légale du lieu ; `utc_offset_h` son décalage (Gabon : +1)."""
    if not has_time:
        local = local.replace(hour=12, minute=0)
    utc = (local - timedelta(hours=utc_offset_h)).replace(tzinfo=timezone.utc)
    d = ephem.Date(utc.replace(tzinfo=None))

    cusps = _houses(d, lat, lon) if has_time else None
    planets = {}
    for name, B in BODIES:
        L = _lon(B(), d)
        L2 = _lon(B(), ephem.Date(d + 0.5))
        retro = ((L2 - L + 540) % 360 - 180) < 0 and name not in ("Soleil", "Lune")
        planets[name] = Planet(name, L, sign_of(L), _house_of(L, cusps) if cusps else None, retro)
    t = (ephem.julian_date(d) - 2451545.0) / 36525
    nn = (125.04452 - 1934.136261 * t) % 360
    planets["Nœud Nord"] = Planet("Nœud Nord", nn, sign_of(nn), _house_of(nn, cusps) if cusps else None, False)

    asc = cusps[0] if cusps else None
    mc = cusps[9] if cusps else None

    # Aspects majeurs entre planètes personnelles, sociales et Saturne,
    # plus les conjonctions aux angles.
    names = ["Soleil", "Lune", "Mercure", "Vénus", "Mars", "Jupiter", "Saturne",
             "Uranus", "Neptune", "Pluton"]
    aspects = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a not in PERSONAL and b not in PERSONAL:
                continue
            if not has_time and "Lune" in (a, b):
                continue  # la Lune parcourt ~13° par jour : aspect non fiable sans heure
            sep = abs((planets[a].lon - planets[b].lon + 180) % 360 - 180)
            for kind, angle, orb in ASPECTS:
                o = orb + (1 if "Soleil" in (a, b) or "Lune" in (a, b) else 0)
                if abs(sep - angle) <= o:
                    aspects.append(Aspect(a, b, kind, round(abs(sep - angle), 1)))
    if asc is not None:
        for p in names:
            for ang_name, ang in (("Ascendant", asc), ("Milieu du Ciel", mc)):
                sep = abs((planets[p].lon - ang + 180) % 360 - 180)
                if sep <= 5:
                    aspects.append(Aspect(p, ang_name, "conjonction", round(sep, 1)))
    aspects.sort(key=lambda x: x.orb)

    elong = (planets["Lune"].lon - planets["Soleil"].lon) % 360

    # Sensibilité de l'ascendant : minutes avant/après un changement de signe.
    change = (None, None)
    if has_time:
        s0 = sign_of(asc)
        before = after = None
        for m in range(1, 181):
            if before is None and sign_of(_houses(ephem.Date(d - m / 1440), lat, lon)[0]) != s0:
                before = m
            if after is None and sign_of(_houses(ephem.Date(d + m / 1440), lat, lon)[0]) != s0:
                after = m
            if before and after:
                break
        change = (before, after)

    # Lune : incertitude de signe si l'heure est inconnue.
    moon_certain = True
    if not has_time:
        day0 = ephem.Date(d - 0.5)
        day1 = ephem.Date(d + 0.5)
        moon_certain = sign_of(_lon(ephem.Moon(), day0)) == sign_of(_lon(ephem.Moon(), day1))

    weights = {"Soleil": 2, "Lune": 2, "Mercure": 1, "Vénus": 1, "Mars": 1}
    el = {"Feu": 0.0, "Terre": 0.0, "Air": 0.0, "Eau": 0.0}
    md = {"Cardinal": 0.0, "Fixe": 0.0, "Mutable": 0.0}
    for n, w in weights.items():
        el[ELEMENT[planets[n].sign]] += w
        md[MODE[planets[n].sign]] += w
    if asc is not None:
        el[ELEMENT[sign_of(asc)]] += 2
        md[MODE[sign_of(asc)]] += 2

    return Chart(local=local, utc=utc, lat=lat, lon=lon, has_time=has_time,
                 planets=planets, asc=asc, mc=mc, cusps=cusps, aspects=aspects,
                 moon_phase=_phase(elong), asc_change_minutes=change,
                 moon_sign_certain=moon_certain, elements=el, modes=md)
