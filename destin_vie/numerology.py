"""Numérologie pythagoricienne (A=1 … I=9, J=1 …).

Toutes les fonctions sont pures : elles prennent un nom et une date, et renvoient
des nombres et le détail des calculs, pour que le rapport puisse les montrer.
"""
from __future__ import annotations

import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from datetime import date

MASTERS = (11, 22, 33)
VOWELS = set("AEIOUY")  # le Y est compté comme voyelle (convention retenue)


def clean(text: str) -> str:
    """Majuscules sans accents, en ne gardant que les lettres et les espaces."""
    nfd = unicodedata.normalize("NFD", text)
    no_acc = "".join(c for c in nfd if unicodedata.category(c) != "Mn").upper()
    return "".join(c if "A" <= c <= "Z" else " " for c in no_acc)


def letter_value(c: str) -> int:
    return (ord(c) - 65) % 9 + 1


def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))


def reduce(n: int, keep_masters: bool = True) -> int:
    while n > 9 and not (keep_masters and n in MASTERS):
        n = digit_sum(n)
    return n


def reduction_chain(n: int, keep_masters: bool = True) -> list[int]:
    """[127, 10, 1] : toutes les étapes, pour l'affichage."""
    chain = [n]
    while n > 9 and not (keep_masters and n in MASTERS):
        n = digit_sum(n)
        chain.append(n)
    return chain


def fmt_chain(chain: list[int]) -> str:
    return ", puis ".join(str(x) for x in chain)


@dataclass
class Word:
    text: str
    total: int
    vowels: int
    consonants: int


@dataclass
class Numerology:
    full_name: str
    birth: date
    words: list[Word]
    life_path: int
    life_path_sum: int
    life_path_digits: str
    expression: int
    expression_sum: int
    soul: int
    soul_sum: int
    personality: int
    personality_sum: int
    maturity: int
    birthday: int            # jour brut (1-31)
    birthday_reduced: int
    grid: dict[int, int]     # grille d'inclusion : chiffre -> nombre de lettres
    karmic_lessons: list[int]
    dominant_digits: list[int]
    masters_in_name: list[tuple[str, int]]
    cycles: list[dict]
    realizations: list[dict]
    challenges: list[int]    # [défi 1, défi 2, défi principal, défi 4]
    personal_years: list[dict] = field(default_factory=list)

    # --- textes de calcul prêts à afficher -------------------------------
    def calc_life_path(self) -> str:
        digits = "+".join(self.life_path_digits)
        return f"{digits} = {fmt_chain(reduction_chain(self.life_path_sum))}"

    def calc_expression(self) -> str:
        parts = " + ".join(f"{w.text.capitalize()} {w.total}" for w in self.words)
        return f"{parts} = {fmt_chain(reduction_chain(self.expression_sum))}"

    def calc_soul(self) -> str:
        return fmt_chain(reduction_chain(self.soul_sum))

    def calc_personality(self) -> str:
        return fmt_chain(reduction_chain(self.personality_sum))


def personal_year(birth: date, year: int) -> int:
    """Année personnelle de l'année civile `year` (du 1er janvier au 31 décembre).

    Jour réduit + mois réduit + année réduite. Un total de 11 ou 22 est conservé
    comme nombre maître (vécu comme 2 ou 4) ; utiliser base() pour le chiffre simple.
    """
    rd = reduce(birth.day, False)
    rm = reduce(birth.month, False)
    ry = reduce(digit_sum(year), False)
    return reduce(rd + rm + ry, True)


def personal_year_periods(birth: date, today: date) -> list[dict]:
    """Année civile en cours puis la suivante."""
    return [{"year": y, "start": date(y, 1, 1), "number": personal_year(birth, y)}
            for y in (today.year, today.year + 1)]


def compute(full_name: str, birth: date, today: date | None = None) -> Numerology:
    today = today or date.today()
    words = []
    for raw in clean(full_name).split():
        tot = sum(letter_value(c) for c in raw)
        vow = sum(letter_value(c) for c in raw if c in VOWELS)
        words.append(Word(raw, tot, vow, tot - vow))
    if not words:
        raise ValueError("Le nom est vide après nettoyage.")

    letters = "".join(w.text for w in words)
    e_sum = sum(w.total for w in words)
    s_sum = sum(w.vowels for w in words)
    p_sum = e_sum - s_sum

    digits = f"{birth.day:02d}{birth.month:02d}{birth.year}"
    lp_sum = sum(int(d) for d in digits)
    lp = reduce(lp_sum)
    expr = reduce(e_sum)
    soul = reduce(s_sum)
    pers = reduce(p_sum)

    grid_c = Counter(letter_value(c) for c in letters)
    grid = {i: grid_c.get(i, 0) for i in range(1, 10)}
    lessons = [i for i in range(1, 10) if grid[i] == 0]
    top = max(grid.values())
    dominant = [i for i in range(1, 10) if grid[i] == top]

    masters = [(w.text.capitalize(), w.total) for w in words if w.total in MASTERS]

    rd = reduce(birth.day, False)
    rm = reduce(birth.month, False)
    ry = reduce(digit_sum(birth.year), False)
    lp_single = reduce(lp_sum, False)
    end1 = 36 - lp_single
    ages = [(0, end1), (end1 + 1, end1 + 9), (end1 + 10, end1 + 18), (end1 + 19, None)]

    r1 = reduce(rd + rm)
    r2 = reduce(rd + ry)
    r3 = reduce(reduce(r1, False) + reduce(r2, False))
    r4 = reduce(rm + ry)
    realizations = [{"number": n, "from": a, "to": b} for n, (a, b) in zip((r1, r2, r3, r4), ages)]

    d1 = abs(rd - rm)
    d2 = abs(rd - ry)
    challenges = [d1, d2, abs(d1 - d2), abs(rm - ry)]

    cycles = [
        {"number": reduce(birth.month), "from": 0, "to": end1, "name": "formatif"},
        {"number": reduce(birth.day), "from": end1 + 1, "to": end1 + 18, "name": "productif"},
        {"number": reduce(digit_sum(birth.year)), "from": end1 + 19, "to": None, "name": "de moisson"},
    ]

    return Numerology(
        full_name=full_name, birth=birth, words=words,
        life_path=lp, life_path_sum=lp_sum, life_path_digits=digits,
        expression=expr, expression_sum=e_sum, soul=soul, soul_sum=s_sum,
        personality=pers, personality_sum=p_sum,
        maturity=reduce(reduce(e_sum, False) + lp_single),
        birthday=birth.day, birthday_reduced=reduce(birth.day),
        grid=grid, karmic_lessons=lessons, dominant_digits=dominant,
        masters_in_name=masters, cycles=cycles, realizations=realizations,
        challenges=challenges,
        personal_years=personal_year_periods(birth, today),
    )


def base(n: int) -> int:
    """Nombre maître ramené à son chiffre de base (11 -> 2)."""
    return reduce(n, False)
