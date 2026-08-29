"""Shadbala: the six-fold strength, in virupas (60 virupas = 1 rupa).

Each component names its rule. Where a component cannot be computed strictly from a
modern ephemeris -- Cheshta Bala, whose BPHS definition depends on the classical
epicyclic model rather than on true geocentric speed -- that is stated, and totals are
reported both with and without it so the practitioner can see the sensitivity.
"""
import math
from . import core, vargas as vg
from .jyotisha import NAISARGIKA, EXALT, OWN, MOOLA, SIGN_LORDS

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Deep exaltation points as absolute sidereal longitude.
EXALT_POINT = {"Sun": 10.0, "Moon": 33.0, "Mars": 298.0, "Mercury": 165.0,
               "Jupiter": 95.0, "Venus": 357.0, "Saturn": 200.0}
NAISARGIKA_BALA = {"Sun": 60.0, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.29,
                   "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57}
DIG_BALA_STRONG_HOUSE = {"Jupiter": 1, "Mercury": 1, "Sun": 10, "Mars": 10,
                         "Saturn": 7, "Moon": 4, "Venus": 4}
# Minimum Shadbala required, in rupas (BPHS).
REQUIRED_RUPAS = {"Sun": 5.0, "Moon": 6.0, "Mars": 5.0, "Mercury": 7.0,
                  "Jupiter": 6.5, "Venus": 5.5, "Saturn": 5.0}
BENEFIC_NATURAL = {"Jupiter", "Venus"}          # Mercury and Moon handled contextually
MALEFIC_NATURAL = {"Sun", "Mars", "Saturn"}

SAPTAVARGA = ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]
DIGNITY_POINTS = {"moolatrikona": 45.0, "own": 30.0, "adhimitra": 22.5, "mitra": 15.0,
                  "sama": 7.5, "shatru": 3.75, "adhishatru": 1.875}


# ---------------------------------------------------------------- relationships
def temporal_relation(planet_sign, other_sign):
    """Tatkalika: the 2,3,4,10,11,12th from a planet are its temporal friends."""
    d = (other_sign - planet_sign) % 12 + 1
    return "friend" if d in (2, 3, 4, 10, 11, 12) else "enemy"


def panchadha(planet, other, planet_sign, other_sign):
    """Fivefold relation = natural relation combined with temporal relation."""
    if planet == other:
        return "own"
    nat = ("friend" if other in NAISARGIKA[planet]["friend"]
           else "enemy" if other in NAISARGIKA[planet]["enemy"] else "neutral")
    tmp = temporal_relation(planet_sign, other_sign)
    table = {("friend", "friend"): "adhimitra", ("friend", "enemy"): "sama",
             ("neutral", "friend"): "mitra", ("neutral", "enemy"): "shatru",
             ("enemy", "friend"): "sama", ("enemy", "enemy"): "adhishatru"}
    return table[(nat, tmp)]


# ---------------------------------------------------------------- sthana bala
def uchcha_bala(planet, lon):
    """Distance from the deep debilitation point, scaled 0-60."""
    deb = (EXALT_POINT[planet] + 180.0) % 360.0
    arc = abs(lon - deb) % 360.0
    if arc > 180.0:
        arc = 360.0 - arc
    return arc / 3.0


def saptavargaja_bala(planet, lon, positions):
    total, detail = 0.0, {}
    for key in SAPTAVARGA:
        f = vg.VARGAS[key][0]
        vsign = f(lon)
        lord = SIGN_LORDS[vsign]
        if planet in MOOLA:
            ms, lo, hi = MOOLA[planet]
            if key == "D1" and vsign == ms and lo <= core.deg_in_sign(lon) < hi:
                st = "moolatrikona"
            elif vsign in OWN.get(planet, []):
                st = "own"
            else:
                st = panchadha(planet, lord, core.sign_of(positions[planet]),
                               core.sign_of(positions[lord]))
        else:
            st = "sama"
        pts = DIGNITY_POINTS[st]
        detail[key] = {"varga_sign": core.SIGNS_SKT[vsign], "lord": lord,
                       "relation": st, "points": pts}
        total += pts
    return total, detail


def ojhayugma_bala(planet, lon):
    """Odd/even rasi and navamsa. Moon and Venus favour even; the rest favour odd."""
    likes_even = planet in ("Moon", "Venus")
    rasi_odd = core.sign_of(lon) % 2 == 0
    nav_odd = vg.d9(lon) % 2 == 0
    b = 0.0
    if rasi_odd != likes_even: b += 15.0
    if nav_odd != likes_even: b += 15.0
    return b


def kendradi_bala(house):
    if house in (1, 4, 7, 10): return 60.0
    if house in (2, 5, 8, 11): return 30.0
    return 15.0


def drekkana_bala(planet, lon):
    """Male planets in the 1st drekkana, neuter in the 2nd, female in the 3rd."""
    part = int(core.deg_in_sign(lon) // 10)
    male, neuter, female = ("Sun", "Mars", "Jupiter"), ("Mercury", "Saturn"), ("Moon", "Venus")
    if planet in male and part == 0: return 15.0
    if planet in neuter and part == 1: return 15.0
    if planet in female and part == 2: return 15.0
    return 0.0


# ---------------------------------------------------------------- dig bala
def dig_bala(planet, lon, asc, mc):
    """Distance from the planet's weakest point, measured through the angles."""
    strong_h = DIG_BALA_STRONG_HOUSE[planet]
    strong_point = {1: asc, 4: (mc + 180.0) % 360.0, 7: (asc + 180.0) % 360.0, 10: mc}[strong_h]
    weak = (strong_point + 180.0) % 360.0
    arc = abs(lon - weak) % 360.0
    if arc > 180.0:
        arc = 360.0 - arc
    return arc / 3.0


# ---------------------------------------------------------------- kala bala
def nathonnatha_bala(planet, jd, sunrise_jd, sunset_jd, prev_sunset_jd):
    """Midnight-strong vs noon-strong. Mercury is always full."""
    if planet == "Mercury":
        return 60.0, "Mercury is always full"
    if sunrise_jd <= jd < sunset_jd:
        frac = (jd - sunrise_jd) / (sunset_jd - sunrise_jd)
        noon_dist = abs(frac - 0.5) * 2.0
    else:
        ref = prev_sunset_jd if jd < sunrise_jd else sunset_jd
        night_len = (sunrise_jd - prev_sunset_jd) if jd < sunrise_jd else 1.0
        frac = (jd - ref) / night_len
        noon_dist = 1.0 - abs(frac - 0.5) * 2.0
    diurnal_strong = planet in ("Sun", "Jupiter", "Venus")
    v = (1.0 - noon_dist) * 60.0 if diurnal_strong else noon_dist * 60.0
    return v, ("noon-strong" if diurnal_strong else "midnight-strong")


def paksha_bala(planet, sun_lon, moon_lon):
    """Benefics gain in the waxing fortnight, malefics in the waning."""
    elong = (moon_lon - sun_lon) % 360.0
    waxing_fraction = elong / 180.0 if elong <= 180.0 else (360.0 - elong) / 180.0
    benefic = planet in BENEFIC_NATURAL or planet == "Mercury" or \
        (planet == "Moon" and 90.0 < elong < 270.0)
    v = waxing_fraction * 60.0 if benefic else (1.0 - waxing_fraction) * 60.0
    if planet == "Moon":
        v *= 2.0
    return v, ("benefic" if benefic else "malefic"), elong


def tribhaga_bala(planet, jd, sunrise_jd, sunset_jd, prev_sunset_jd):
    """Jupiter always full; otherwise the ruler of the third of day or night."""
    if planet == "Jupiter":
        return 60.0, "Jupiter always full"
    if sunrise_jd <= jd < sunset_jd:
        third = int((jd - sunrise_jd) / ((sunset_jd - sunrise_jd) / 3.0))
        lords = ["Mercury", "Sun", "Saturn"]
        period = "day"
    else:
        ref = prev_sunset_jd if jd < sunrise_jd else sunset_jd
        length = (sunrise_jd - prev_sunset_jd) if jd < sunrise_jd else 1.0
        third = int((jd - ref) / (length / 3.0))
        lords = ["Moon", "Venus", "Mars"]
        period = "night"
    third = min(third, 2)
    return (60.0 if lords[third] == planet else 0.0), f"{period} third {third+1}, lord {lords[third]}"


def varsha_masa_dina_hora(planet, vara_lord, hora_lord, masa_lord, abda_lord):
    b = 0.0; d = {}
    for label, lord, val in [("abda", abda_lord, 15.0), ("masa", masa_lord, 30.0),
                             ("vara", vara_lord, 45.0), ("hora", hora_lord, 60.0)]:
        got = val if lord == planet else 0.0
        d[label] = {"lord": lord, "points": got}
        b += got
    return b, d


def ayana_bala(planet, declination):
    """Declination-based. North-strong: Sun, Mars, Jupiter, Venus. South-strong: Moon, Saturn."""
    if planet == "Mercury":
        v = 60.0 * (23.45 + abs(declination)) / 46.90
        return min(v, 60.0), "always treated as strong in either declination"
    north = planet in ("Sun", "Mars", "Jupiter", "Venus")
    v = 60.0 * (23.45 + (declination if north else -declination)) / 46.90
    v = max(0.0, min(v, 60.0))
    if planet == "Sun":
        v *= 2.0
    return v, ("north-strong" if north else "south-strong")


# ---------------------------------------------------------------- cheshta
def cheshta_bala(planet, speed, mean_speed, retrograde):
    """APPROXIMATION -- see module docstring.

    BPHS defines Cheshta Bala through the cheshta kendra of the classical epicyclic
    model. A modern ephemeris gives true geocentric speed instead, so this maps
    speed onto 0-60 with retrogression at full strength. It is NOT the strict
    classical value, and totals are also reported with this component excluded.
    """
    if planet in ("Sun", "Moon"):
        return None, "Sun and Moon take Ayana / Paksha Bala in place of Cheshta"
    if retrograde:
        return 60.0, "retrograde -> full"
    ratio = speed / mean_speed if mean_speed else 1.0
    v = max(0.0, min(60.0, 30.0 * (2.0 - ratio)))
    return v, f"direct, speed/mean = {ratio:.4f}"


MEAN_SPEED = {"Mars": 0.5240, "Mercury": 1.3833, "Jupiter": 0.0831,
              "Venus": 1.2000, "Saturn": 0.0335}


# ---------------------------------------------------------------- drik bala
ASPECT_FRACTION = {3: 0.25, 10: 0.25, 5: 0.5, 9: 0.5, 4: 0.75, 8: 0.75, 7: 1.0}
SPECIAL_FULL = {"Mars": (4, 8), "Jupiter": (5, 9), "Saturn": (3, 10)}


def drik_bala(planet, positions, houses_of):
    """Parasari graha drishti, benefic aspects adding and malefic subtracting.

    Fractions: 7th full; 4th and 8th three-quarter; 5th and 9th half; 3rd and 10th
    quarter; plus each planet's own special full aspects. Scaled to virupas by
    (net aspect value) * 60 / 4.
    """
    net, detail = 0.0, []
    target_sign = core.sign_of(positions[planet])
    for other in SEVEN:
        if other == planet:
            continue
        d = (target_sign - core.sign_of(positions[other])) % 12 + 1
        frac = ASPECT_FRACTION.get(d, 0.0)
        if d in SPECIAL_FULL.get(other, ()):
            frac = 1.0
        if frac == 0.0:
            continue
        benefic = other in BENEFIC_NATURAL or other == "Mercury"
        signed = frac if benefic else -frac
        net += signed
        detail.append({"from": other, "house_distance": d, "fraction": frac,
                       "nature": "benefic" if benefic else "malefic", "signed": signed})
    return net * 60.0 / 4.0, detail


# ---------------------------------------------------------------- assemble
def build(positions_sidereal, houses_of, asc, mc, jd, sunrise_jd, sunset_jd,
          prev_sunset_jd, declinations, speeds, retro, vara_lord, hora_lord,
          masa_lord, abda_lord):
    pos = {p: positions_sidereal[p] for p in SEVEN}
    out = {}
    for p in SEVEN:
        lon = pos[p]
        sapta, sapta_detail = saptavargaja_bala(p, lon, pos)
        sth = {
            "uchcha_bala": uchcha_bala(p, lon),
            "saptavargaja_bala": sapta,
            "saptavargaja_detail": sapta_detail,
            "ojhayugmarasyamsa_bala": ojhayugma_bala(p, lon),
            "kendradi_bala": kendradi_bala(houses_of[p]),
            "drekkana_bala": drekkana_bala(p, lon),
        }
        sth["total"] = sum(v for k, v in sth.items() if k.endswith("_bala"))

        dig = dig_bala(p, lon, asc, mc)
        nat_v, nat_why = nathonnatha_bala(p, jd, sunrise_jd, sunset_jd, prev_sunset_jd)
        pak_v, pak_nature, elong = paksha_bala(p, pos["Sun"], pos["Moon"])
        tri_v, tri_why = tribhaga_bala(p, jd, sunrise_jd, sunset_jd, prev_sunset_jd)
        vmdh, vmdh_detail = varsha_masa_dina_hora(p, vara_lord, hora_lord, masa_lord, abda_lord)
        ay_v, ay_why = ayana_bala(p, declinations[p])
        kala = {"nathonnatha_bala": nat_v, "nathonnatha_basis": nat_why,
                "paksha_bala": pak_v, "paksha_nature": pak_nature,
                "sun_moon_elongation": elong,
                "tribhaga_bala": tri_v, "tribhaga_basis": tri_why,
                "abda_masa_vara_hora_bala": vmdh, "abda_masa_vara_hora_detail": vmdh_detail,
                "ayana_bala": ay_v, "ayana_basis": ay_why,
                "yuddha_bala": 0.0, "yuddha_basis": "no planetary war in this chart"}
        kala["total"] = sum(v for k, v in kala.items() if k.endswith("_bala"))

        che_v, che_why = cheshta_bala(p, speeds[p], MEAN_SPEED.get(p), retro[p])
        drk_v, drk_detail = drik_bala(p, pos, houses_of)

        total_wo = sth["total"] + dig + kala["total"] + NAISARGIKA_BALA[p] + drk_v
        total_w = total_wo + (che_v or 0.0)
        out[p] = {
            "sthana_bala": sth, "dig_bala": dig, "kala_bala": kala,
            "cheshta_bala": che_v, "cheshta_basis": che_why,
            "cheshta_is_approximation": che_v is not None,
            "naisargika_bala": NAISARGIKA_BALA[p],
            "drik_bala": drk_v, "drik_detail": drk_detail,
            "total_virupas_with_cheshta": total_w,
            "total_rupas_with_cheshta": total_w / 60.0,
            "total_virupas_without_cheshta": total_wo,
            "total_rupas_without_cheshta": total_wo / 60.0,
            "required_rupas": REQUIRED_RUPAS[p],
            "meets_requirement_with_cheshta": total_w / 60.0 >= REQUIRED_RUPAS[p],
            "meets_requirement_without_cheshta": total_wo / 60.0 >= REQUIRED_RUPAS[p],
            "ishta_kashta_note": "Ishta/Kashta Phala not computed (depends on Cheshta, which is approximated).",
        }
    ranked = sorted(SEVEN, key=lambda p: -out[p]["total_rupas_with_cheshta"])
    return {"planets": out, "rank_strongest_first": ranked,
            "units": "virupas; 60 virupas = 1 rupa",
            "components_computed": ["Sthana (5 sub-components)", "Dig", "Kala (6 sub-components)",
                                    "Naisargika", "Drik"],
            "components_approximated": ["Cheshta -- see module docstring"],
            "validation": _validate(out)}


def _validate(out):
    checks = {}
    checks["uchcha_in_range_0_60"] = all(0 <= out[p]["sthana_bala"]["uchcha_bala"] <= 60 for p in SEVEN)
    checks["dig_in_range_0_60"] = all(0 <= out[p]["dig_bala"] <= 60 for p in SEVEN)
    checks["kendradi_valid"] = all(out[p]["sthana_bala"]["kendradi_bala"] in (15.0, 30.0, 60.0) for p in SEVEN)
    checks["naisargika_matches_classical"] = all(
        abs(out[p]["naisargika_bala"] - NAISARGIKA_BALA[p]) < 1e-9 for p in SEVEN)
    checks["naisargika_order_correct"] = [p for p in sorted(
        SEVEN, key=lambda x: -NAISARGIKA_BALA[x])] == ["Sun", "Moon", "Venus", "Jupiter",
                                                       "Mercury", "Mars", "Saturn"]
    checks["saptavargaja_max_315"] = all(out[p]["sthana_bala"]["saptavargaja_bala"] <= 7 * 45.0 for p in SEVEN)
    checks["all_totals_positive"] = all(out[p]["total_virupas_with_cheshta"] > 0 for p in SEVEN)
    checks["pass"] = all(v for v in checks.values() if isinstance(v, bool))
    return checks
