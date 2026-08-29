"""Side-by-side comparison of the convention choices that actually move results.

The point is not to pick a winner. It is to show a practitioner exactly which of
their school's choices change which conclusions in THIS chart.
"""
from . import core, vargas as vg, jyotisha as jy
import swisseph as swe

AYANAMSHAS = [
    ("Lahiri / Chitrapaksha", swe.SIDM_LAHIRI), ("Raman", swe.SIDM_RAMAN),
    ("Krishnamurti (KP)", swe.SIDM_KRISHNAMURTI), ("Yukteshwar", swe.SIDM_YUKTESHWAR),
    ("True Chitra", swe.SIDM_TRUE_CITRA), ("True Revati", swe.SIDM_TRUE_REVATI),
    ("True Pushya", swe.SIDM_TRUE_PUSHYA), ("Fagan / Bradley", swe.SIDM_FAGAN_BRADLEY),
    ("Sassanian", swe.SIDM_SASSANIAN), ("Aldebaran at 15 Taurus", swe.SIDM_ALDEBARAN_15TAU),
    ("Usha / Shashi", swe.SIDM_USHASHASHI), ("Djwhal Khul", swe.SIDM_DJWHAL_KHUL),
]
HOUSE_SYSTEMS = [
    ("Whole sign", b"W"), ("Placidus", b"P"), ("Koch", b"K"), ("Equal (from Asc)", b"A"),
    ("Porphyry", b"O"), ("Regiomontanus", b"R"), ("Campanus", b"C"), ("Alcabitius", b"B"),
    ("Topocentric", b"T"), ("Morinus", b"M"), ("Krusinski", b"U"), ("Vehlow equal", b"V"),
]
GRAHAS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def ayanamsha_comparison(jd, lat, lon_geo):
    rows = []
    for name, mode in AYANAMSHAS:
        swe.set_sid_mode(mode)
        ay = swe.get_ayanamsa_ut(jd)
        asc = swe.houses_ex(jd, lat, lon_geo, b"W", swe.FLG_SIDEREAL)[1][0]
        pos = {}
        for g in GRAHAS:
            code = core.BODIES[g]
            L = swe.calc_ut(jd, code, swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL)[0][0]
            pos[g] = L
        nk = jy.nakshatra_of(asc)
        mnk = jy.nakshatra_of(pos["Moon"])
        rows.append({
            "ayanamsha": name, "value_deg": ay, "value_dms": core.dms(ay),
            "lagna_deg": asc, "lagna_sign": core.SIGNS_SKT[core.sign_of(asc)],
            "lagna_formatted": core.fmt(asc, skt=True),
            "lagna_nakshatra": nk["name"], "lagna_pada": nk["pada"],
            "lagna_d9": core.SIGNS_SKT[vg.d9(asc)], "lagna_d10": core.SIGNS_SKT[vg.d10(asc)],
            "moon_nakshatra": mnk["name"], "moon_pada": mnk["pada"],
            "moon_dasha_lord": mnk["lord"],
            "planet_signs": {g: core.SIGNS_SKT[core.sign_of(pos[g])] for g in GRAHAS},
            "planet_houses": {g: (core.sign_of(pos[g]) - core.sign_of(asc)) % 12 + 1 for g in GRAHAS},
        })
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    base = rows[0]
    for r in rows:
        r["differs_from_lahiri"] = {
            "lagna_sign": r["lagna_sign"] != base["lagna_sign"],
            "lagna_nakshatra_or_pada": (r["lagna_nakshatra"], r["lagna_pada"]) != (base["lagna_nakshatra"], base["lagna_pada"]),
            "lagna_d9": r["lagna_d9"] != base["lagna_d9"],
            "lagna_d10": r["lagna_d10"] != base["lagna_d10"],
            "moon_dasha_lord": r["moon_dasha_lord"] != base["moon_dasha_lord"],
            "planets_changing_sign": [g for g in GRAHAS if r["planet_signs"][g] != base["planet_signs"][g]],
            "planets_changing_house": [g for g in GRAHAS if r["planet_houses"][g] != base["planet_houses"][g]],
        }
    return {"reference": "Lahiri / Chitrapaksha", "rows": rows,
            "spread_deg": max(r["value_deg"] for r in rows) - min(r["value_deg"] for r in rows),
            "note": ("Ayanamsha is a school choice, not an observable. The Vimshottari dasha "
                     "sequence depends on the Moon's nakshatra, so any ayanamsha that moves the "
                     "Moon across a nakshatra boundary changes the entire dasha timeline.")}


def house_system_comparison(jd, lat, lon_geo, tropical_positions):
    rows = []
    for name, code in HOUSE_SYSTEMS:
        try:
            cusps, ascmc = swe.houses_ex(jd, lat, lon_geo, code)
        except Exception as e:
            rows.append({"system": name, "error": str(e)}); continue
        cl = list(cusps)
        houses = {}
        for g in GRAHAS:
            L = tropical_positions[g]["longitude"]
            if code == b"W":
                h = (core.sign_of(L) - core.sign_of(ascmc[0])) % 12 + 1
            else:
                h = 12
                for i in range(12):
                    a, b = cl[i], cl[(i + 1) % 12]
                    if a <= L < b or (a > b and (L >= a or L < b)):
                        h = i + 1; break
            houses[g] = h
        rows.append({"system": name, "asc": ascmc[0], "asc_formatted": core.fmt(ascmc[0]),
                     "mc": ascmc[1], "mc_formatted": core.fmt(ascmc[1]),
                     "cusps": cl, "planet_houses": houses,
                     "mc_in_house": next((i + 1 for i in range(12)
                                          if cl[i] <= ascmc[1] < cl[(i + 1) % 12] or
                                          (cl[i] > cl[(i + 1) % 12] and
                                           (ascmc[1] >= cl[i] or ascmc[1] < cl[(i + 1) % 12]))), None)})
    base = rows[0]
    for r in rows:
        if "error" in r: continue
        r["planets_changing_house_vs_whole_sign"] = [
            g for g in GRAHAS if r["planet_houses"][g] != base["planet_houses"][g]]
    return {"reference": "Whole sign", "rows": rows,
            "note": ("The Ascendant degree is identical in every system -- only the house "
                     "DIVISIONS differ. Whole sign is the declared primary for both the "
                     "Hellenistic and Parasari tracks.")}


def combustion_schools(sun_lon, positions):
    """Astangata orbs differ by text. Reported rather than silently fixed."""
    SCHOOLS = {
        "BPHS / common Parasari": {"Moon": 12, "Mars": 17, "Mercury": 14, "Jupiter": 11, "Venus": 10, "Saturn": 15},
        "Surya Siddhanta": {"Moon": 12, "Mars": 17, "Mercury": 13, "Jupiter": 11, "Venus": 9, "Saturn": 15},
        "Western traditional": {"Moon": 8, "Mars": 8, "Mercury": 8, "Jupiter": 8, "Venus": 8, "Saturn": 8},
    }
    out = {}
    for school, orbs in SCHOOLS.items():
        out[school] = {}
        for p, orb in orbs.items():
            sep = core.angsep(positions[p]["longitude"], sun_lon)
            out[school][p] = {"elongation_deg": sep, "orb_deg": orb, "combust": sep < orb}
    verdicts = {p: {s: out[s][p]["combust"] for s in SCHOOLS} for p in SCHOOLS["BPHS / common Parasari"]}
    out["_planets_where_schools_disagree"] = [p for p, v in verdicts.items() if len(set(v.values())) > 1]
    return out
