"""Shodasavarga: the sixteen Parasari divisional charts, with per-varga stability.

Each function maps an absolute sidereal longitude to a divisional sign index 0-11.
Rules are stated in the docstrings so a practitioner can check them against their
own school before trusting any varga-derived claim.
"""
from . import core

MOVABLE = (0, 3, 6, 9)      # Aries, Cancer, Libra, Capricorn
FIXED = (1, 4, 7, 10)
DUAL = (2, 5, 8, 11)
FIRE, EARTH, AIR, WATER = (0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)


def _s(lon):
    return core.sign_of(lon)


def _d(lon):
    return core.deg_in_sign(lon)


def _part(deg_in_sign, n):
    """Index 0..n-1 of the division a degree falls in.

    Multiply-first: int(d * n / 30) rather than int(d // (30/n)). Forming the step 30/n
    first is inexact for n in {7, 9, 27, 45}, which mis-floors exactly on a boundary
    (30.0 with n=9 yielded 8 instead of 9). The clamp guards the d == 30.0 edge.
    """
    return min(int(deg_in_sign * n / 30.0), n - 1)


def _cont(lon, n):
    """Continuous division count from 0 deg Aries, multiply-first."""
    return int(lon * n / 30.0)


def d1(lon):
    """Rasi. The sign itself."""
    return _s(lon)


def d2(lon):
    """Hora. Odd sign: first half Leo (Sun), second half Cancer (Moon). Even sign: reversed."""
    s, d = _s(lon), _d(lon)
    first = d < 15.0
    odd = s % 2 == 0
    return 4 if (odd == first) else 3


def d3(lon):
    """Drekkana. 10 deg each: 1st the sign itself, 2nd the 5th from it, 3rd the 9th."""
    s, d = _s(lon), _d(lon)
    return (s + _part(d, 3) * 4) % 12


def d4(lon):
    """Chaturthamsa. 7.5 deg each: the sign, then the 4th, 7th and 10th from it."""
    s, d = _s(lon), _d(lon)
    return (s + _part(d, 4) * 3) % 12


def d7(lon):
    """Saptamsa. 4 deg 17'8.57" each: odd signs count from the sign, even signs from the 7th."""
    s, d = _s(lon), _d(lon)
    part = _part(d, 7)
    base = s if s % 2 == 0 else (s + 6) % 12
    return (base + part) % 12


def d9(lon):
    """Navamsa. 3 deg 20' each, continuous count from Aries -- equivalent to the classical
    movable-from-self / fixed-from-9th / dual-from-5th rule."""
    return _cont(lon, 9) % 12


def d10(lon):
    """Dasamsa. 3 deg each: odd signs from the sign itself, even signs from the 9th."""
    s, d = _s(lon), _d(lon)
    base = s if s % 2 == 0 else (s + 8) % 12
    return (base + _part(d, 10)) % 12


def d12(lon):
    """Dwadasamsa. 2 deg 30' each, counted from the sign itself."""
    s, d = _s(lon), _d(lon)
    return (s + _part(d, 12)) % 12


def d16(lon):
    """Shodasamsa. 1 deg 52'30" each: movable from Aries, fixed from Leo, dual from Sagittarius."""
    s, d = _s(lon), _d(lon)
    base = 0 if s in MOVABLE else (4 if s in FIXED else 8)
    return (base + _part(d, 16)) % 12


def d20(lon):
    """Vimsamsa. 1 deg 30' each: movable from Aries, fixed from Sagittarius, dual from Leo."""
    s, d = _s(lon), _d(lon)
    base = 0 if s in MOVABLE else (8 if s in FIXED else 4)
    return (base + _part(d, 20)) % 12


def d24(lon):
    """Chaturvimsamsa. 1 deg 15' each: odd signs from Leo, even signs from Cancer."""
    s, d = _s(lon), _d(lon)
    base = 4 if s % 2 == 0 else 3
    return (base + _part(d, 24)) % 12


def d27(lon):
    """Bhamsa / Nakshatramsa. 1 deg 6'40" each: fire from Aries, earth from Cancer,
    air from Libra, water from Capricorn."""
    s, d = _s(lon), _d(lon)
    base = 0 if s in FIRE else (3 if s in EARTH else (6 if s in AIR else 9))
    return (base + _part(d, 27)) % 12


TRIMSAMSA_ODD = [(5.0, 0), (10.0, 10), (18.0, 8), (25.0, 2), (30.0, 6)]     # Mars,Sat,Jup,Merc,Ven
TRIMSAMSA_EVEN = [(5.0, 1), (12.0, 5), (20.0, 11), (25.0, 9), (30.0, 7)]    # Ven,Merc,Jup,Sat,Mars


def d30(lon):
    """Trimsamsa. Unequal, and assigned to a planet's sign rather than by continuous count.
    Odd: Mars 0-5, Saturn 5-10, Jupiter 10-18, Mercury 18-25, Venus 25-30.
    Even: the mirror -- Venus 0-5, Mercury 5-12, Jupiter 12-20, Saturn 20-25, Mars 25-30."""
    s, d = _s(lon), _d(lon)
    table = TRIMSAMSA_ODD if s % 2 == 0 else TRIMSAMSA_EVEN
    for end, sign in table:
        if d < end:
            return sign
    return table[-1][1]


def d40(lon):
    """Khavedamsa. 45' each: odd signs from Aries, even signs from Libra."""
    s, d = _s(lon), _d(lon)
    base = 0 if s % 2 == 0 else 6
    return (base + _part(d, 40)) % 12


def d45(lon):
    """Akshavedamsa. 40' each: movable from Aries, fixed from Leo, dual from Sagittarius."""
    s, d = _s(lon), _d(lon)
    base = 0 if s in MOVABLE else (4 if s in FIXED else 8)
    return (base + _part(d, 45)) % 12


def d60(lon):
    """Shastiamsa. 30' each, counted from the sign itself."""
    s, d = _s(lon), _d(lon)
    return (s + _part(d, 60)) % 12


VARGAS = {"D1": (d1, "Rasi", "body / overall"), "D2": (d2, "Hora", "wealth"),
          "D3": (d3, "Drekkana", "siblings, courage"), "D4": (d4, "Chaturthamsa", "home, fortune"),
          "D7": (d7, "Saptamsa", "children, progeny"), "D9": (d9, "Navamsa", "spouse, dharma, general strength"),
          "D10": (d10, "Dasamsa", "career, action"), "D12": (d12, "Dwadasamsa", "parents"),
          "D16": (d16, "Shodasamsa", "vehicles, comforts"), "D20": (d20, "Vimsamsa", "spiritual practice"),
          "D24": (d24, "Chaturvimsamsa", "education, learning"),
          "D27": (d27, "Bhamsa", "strengths and weaknesses"),
          "D30": (d30, "Trimsamsa", "misfortune, character"), "D40": (d40, "Khavedamsa", "maternal legacy"),
          "D45": (d45, "Akshavedamsa", "paternal legacy"), "D60": (d60, "Shastiamsa", "totality, past karma")}

# Divisional span in degrees, used to compute distance to the next boundary.
SPANS = {"D1": 30.0, "D2": 15.0, "D3": 10.0, "D4": 7.5, "D7": 30.0 / 7, "D9": 30.0 / 9,
         "D10": 3.0, "D12": 2.5, "D16": 30.0 / 16, "D20": 1.5, "D24": 1.25, "D27": 30.0 / 27,
         "D30": None, "D40": 0.75, "D45": 30.0 / 45, "D60": 0.5}


def all_vargas(lon):
    return {k: {"sign_index": f(lon), "sign": core.SIGNS_SKT[f(lon)],
                "sign_western": core.SIGNS_TROP[f(lon)], "name": nm, "signifies": sig}
            for k, (f, nm, sig) in VARGAS.items()}


def boundary_distance(lon, key):
    """Degrees until this longitude crosses into the next division of that varga."""
    span = SPANS[key]
    if span is None:                       # D30 has unequal divisions
        s, d = _s(lon), _d(lon)
        table = TRIMSAMSA_ODD if s % 2 == 0 else TRIMSAMSA_EVEN
        for end, _ in table:
            if d < end:
                return end - d
        return 30.0 - d
    return span - (lon % span)


def vargottama_count(lon):
    """How many of the sixteen divisions repeat the D1 sign (a classical strength marker)."""
    base = d1(lon)
    hits = [k for k, (f, _, _) in VARGAS.items() if f(lon) == base]
    return {"count": len(hits), "vargas": sorted(hits)}


def validate():
    """Every varga must return a valid sign index across the whole zodiac."""
    bad = []
    x = 0.0
    while x < 360.0:
        for k, (f, _, _) in VARGAS.items():
            v = f(x)
            if not isinstance(v, int) or not 0 <= v <= 11:
                bad.append((k, x, v))
        x += 0.01
    return {"samples_per_varga": 36000, "vargas_checked": len(VARGAS),
            "invalid_results": bad, "pass": not bad}
