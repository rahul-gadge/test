"""Jyotisha (Parasari track): sidereal Lahiri, whole-sign houses, mean node."""
import math
from . import core

GRAHAS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
              "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
              "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
              "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
              "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"]

VIM_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
VIM_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
             "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}

SIGN_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
              "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

EXALT = {"Sun": (0, 10.0), "Moon": (1, 3.0), "Mars": (9, 28.0), "Mercury": (5, 15.0),
         "Jupiter": (3, 5.0), "Venus": (11, 27.0), "Saturn": (6, 20.0)}
OWN = {"Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
       "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10]}
MOOLA = {"Sun": (4, 0, 20), "Moon": (1, 4, 30), "Mars": (0, 0, 12), "Mercury": (5, 16, 20),
         "Jupiter": (8, 0, 10), "Venus": (6, 0, 15), "Saturn": (10, 0, 20)}

NAISARGIKA = {
    "Sun":     {"friend": ["Moon", "Mars", "Jupiter"], "neutral": ["Mercury"], "enemy": ["Venus", "Saturn"]},
    "Moon":    {"friend": ["Sun", "Mercury"], "neutral": ["Mars", "Jupiter", "Venus", "Saturn"], "enemy": []},
    "Mars":    {"friend": ["Sun", "Moon", "Jupiter"], "neutral": ["Venus", "Saturn"], "enemy": ["Mercury"]},
    "Mercury": {"friend": ["Sun", "Venus"], "neutral": ["Mars", "Jupiter", "Saturn"], "enemy": ["Moon"]},
    "Jupiter": {"friend": ["Sun", "Moon", "Mars"], "neutral": ["Saturn"], "enemy": ["Mercury", "Venus"]},
    "Venus":   {"friend": ["Mercury", "Saturn"], "neutral": ["Mars", "Jupiter"], "enemy": ["Sun", "Moon"]},
    "Saturn":  {"friend": ["Mercury", "Venus"], "neutral": ["Jupiter"], "enemy": ["Sun", "Moon", "Mars"]},
}

# Astangata (combustion) orbs in degrees of longitude from the Sun.
COMBUST_ORB = {"Moon": 12.0, "Mars": 17.0, "Mercury": 14.0, "Jupiter": 11.0,
               "Venus": 10.0, "Saturn": 15.0}
COMBUST_ORB_RETRO = {"Mercury": 12.0, "Venus": 8.0}

# Graha drishti: special full aspects (houses counted from the graha, 7 is universal).
SPECIAL_ASPECTS = {"Mars": [4, 7, 8], "Jupiter": [5, 7, 9], "Saturn": [3, 7, 10],
                   "Rahu": [5, 7, 9], "Ketu": [5, 7, 9]}
DEFAULT_ASPECTS = [7]

# --- Bhinnashtakavarga benefic-point tables (BPHS). Row totals validated. ---
BAV = {
 "Sun": {"Sun":[1,2,4,7,8,9,10,11],"Moon":[3,6,10,11],"Mars":[1,2,4,7,8,9,10,11],
         "Mercury":[3,5,6,9,10,11,12],"Jupiter":[5,6,9,11],"Venus":[6,7,12],
         "Saturn":[1,2,4,7,8,9,10,11],"Lagna":[3,4,6,10,11,12]},
 "Moon":{"Sun":[3,6,7,8,10,11],"Moon":[1,3,6,7,10,11],"Mars":[2,3,5,6,9,10,11],
         "Mercury":[1,3,4,5,7,8,10,11],"Jupiter":[1,4,7,8,10,11,12],"Venus":[3,4,5,7,9,10,11],
         "Saturn":[3,5,6,11],"Lagna":[3,6,10,11]},
 "Mars":{"Sun":[3,5,6,10,11],"Moon":[3,6,11],"Mars":[1,2,4,7,8,10,11],
         "Mercury":[3,5,6,11],"Jupiter":[6,10,11,12],"Venus":[6,8,11,12],
         "Saturn":[1,4,7,8,9,10,11],"Lagna":[1,3,6,10,11]},
 "Mercury":{"Sun":[5,6,9,11,12],"Moon":[2,4,6,8,10,11],"Mars":[1,2,4,7,8,9,10,11],
         "Mercury":[1,3,5,6,9,10,11,12],"Jupiter":[6,8,11,12],"Venus":[1,2,3,4,5,8,9,11],
         "Saturn":[1,2,4,7,8,9,10,11],"Lagna":[1,2,4,6,8,10,11]},
 "Jupiter":{"Sun":[1,2,3,4,7,8,9,10,11],"Moon":[2,5,7,9,11],"Mars":[1,2,4,7,8,10,11],
         "Mercury":[1,2,4,5,6,9,10,11],"Jupiter":[1,2,3,4,7,8,10,11],"Venus":[2,5,6,9,10,11],
         "Saturn":[3,5,6,12],"Lagna":[1,2,4,5,6,7,9,10,11]},
 "Venus":{"Sun":[8,11,12],"Moon":[1,2,3,4,5,8,9,11,12],"Mars":[3,4,6,9,11,12],
         "Mercury":[3,5,6,9,11],"Jupiter":[5,8,9,10,11],"Venus":[1,2,3,4,5,8,9,10,11],
         "Saturn":[3,4,5,8,9,10,11],"Lagna":[1,2,3,4,5,8,9,11]},
 "Saturn":{"Sun":[1,2,4,7,8,10,11],"Moon":[3,6,11],"Mars":[3,5,6,10,11,12],
         "Mercury":[6,8,9,10,11,12],"Jupiter":[5,6,11,12],"Venus":[6,11,12],
         "Saturn":[3,5,6,11],"Lagna":[1,3,4,6,10,11]},
}
BAV_EXPECTED_TOTALS = {"Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54,
                       "Jupiter": 56, "Venus": 52, "Saturn": 39}


def nakshatra_of(lon):
    span = 360.0 / 27.0
    idx = int(lon // span) % 27
    within = lon % span
    pada = int(within // (span / 4)) + 1
    return {"index": idx + 1, "name": NAKSHATRAS[idx], "pada": pada,
            "lord": VIM_ORDER[idx % 9], "degrees_into": within,
            "fraction_elapsed": within / span}


def dignity(planet, lon):
    s = core.sign_of(lon); d = core.deg_in_sign(lon)
    if planet in ("Rahu", "Ketu"):
        return {"state": "not_assigned",
                "note": "No cross-school consensus on nodal exaltation; omitted rather than guessed."}
    out = {"state": "neutral_or_friendly", "detail": []}
    ex = EXALT.get(planet)
    if ex and s == ex[0]:
        out["state"] = "exalted"; out["detail"].append(f"exaltation sign; deep point {ex[1]}deg")
    elif ex and s == (ex[0] + 6) % 12:
        out["state"] = "debilitated"; out["detail"].append(f"debilitation sign; deep point {ex[1]}deg")
    mt = MOOLA.get(planet)
    if mt and s == mt[0] and mt[1] <= d < mt[2]:
        out["state"] = "moolatrikona"; out["detail"].append("moolatrikona arc")
    elif s in OWN.get(planet, []) and out["state"] not in ("exalted", "debilitated"):
        out["state"] = "own_sign"; out["detail"].append("own sign")
    lord = SIGN_LORDS[s]
    if lord != planet and planet in NAISARGIKA:
        rel = ("friend" if lord in NAISARGIKA[planet]["friend"]
               else "enemy" if lord in NAISARGIKA[planet]["enemy"] else "neutral")
        out["dispositor"] = lord
        out["naisargika_relation_to_dispositor"] = rel
    return out


def varga(lon, division):
    """Continuous-count divisional sign index."""
    if division == 9:
        return int(lon // (30.0 / 9)) % 12
    if division == 10:
        s = core.sign_of(lon); part = int(core.deg_in_sign(lon) // 3.0)
        base = s if s % 2 == 0 else (s + 8) % 12   # odd signs from self, even signs from 9th
        return (base + part) % 12
    if division == 3:
        s = core.sign_of(lon); part = int(core.deg_in_sign(lon) // 10.0)
        return (s + part * 4) % 12
    if division == 12:
        s = core.sign_of(lon); part = int(core.deg_in_sign(lon) // 2.5)
        return (s + part) % 12
    raise ValueError(division)


def build(jd, lat, lon_geo, sidereal_pos, ayan, node="MeanNode"):
    h = core.houses(jd, lat, lon_geo, b"W", sidereal=True)
    lagna = h["asc"]
    lagna_sign = core.sign_of(lagna)

    pos = {}
    for g in GRAHAS:
        if g == "Rahu":
            src = sidereal_pos[node]
        elif g == "Ketu":
            src = sidereal_pos["Ketu_" + node]
        else:
            src = sidereal_pos[g]
        pos[g] = src

    sun_lon = pos["Sun"]["longitude"]
    planets = {}
    for g in GRAHAS:
        L = pos[g]["longitude"]
        s = core.sign_of(L)
        house = (s - lagna_sign) % 12 + 1
        retro = pos[g]["retrograde"] if g not in ("Rahu", "Ketu") else True
        entry = {
            "longitude_sidereal": L,
            "sign_index": s, "sign": core.SIGNS_SKT[s], "sign_western": core.SIGNS_TROP[s],
            "degrees_in_sign": core.deg_in_sign(L),
            "formatted": core.fmt(L, skt=True),
            "house_whole_sign": house,
            "latitude": pos[g]["latitude"],
            "speed_deg_per_day": pos[g]["speed_long"],
            "retrograde": bool(retro),
            "nakshatra": nakshatra_of(L),
            "dignity": dignity(g, L),
            "navamsa_sign": core.SIGNS_SKT[varga(L, 9)],
            "navamsa_sign_index": varga(L, 9),
            "dasamsa_sign": core.SIGNS_SKT[varga(L, 10)],
            "dasamsa_sign_index": varga(L, 10),
            "vargottama_d9": varga(L, 9) == s,
        }
        if g not in ("Sun", "Rahu", "Ketu"):
            sep = core.angsep(L, sun_lon)
            orb = COMBUST_ORB.get(g)
            if retro and g in COMBUST_ORB_RETRO:
                orb = COMBUST_ORB_RETRO[g]
            entry["distance_from_sun_deg"] = sep
            entry["combust"] = bool(orb and sep < orb)
            entry["combustion_orb_used_deg"] = orb
        planets[g] = entry

    # planetary war: two true planets within 1 degree
    wars = []
    tp = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    for i in range(len(tp)):
        for j in range(i + 1, len(tp)):
            d = core.angsep(planets[tp[i]]["longitude_sidereal"], planets[tp[j]]["longitude_sidereal"])
            if d < 1.0:
                wars.append({"pair": [tp[i], tp[j]], "separation_deg": d})

    # house lords and occupancy
    house_info = {}
    for hh in range(1, 13):
        sidx = (lagna_sign + hh - 1) % 12
        occ = [g for g in GRAHAS if planets[g]["house_whole_sign"] == hh]
        house_info[hh] = {
            "sign_index": sidx, "sign": core.SIGNS_SKT[sidx],
            "lord": SIGN_LORDS[sidx],
            "lord_in_house": None, "occupants": occ,
        }
    for hh in range(1, 13):
        lrd = house_info[hh]["lord"]
        house_info[hh]["lord_in_house"] = planets[lrd]["house_whole_sign"]

    # graha drishti (aspects), house-based
    aspects = {}
    for g in GRAHAS:
        src_h = planets[g]["house_whole_sign"]
        arcs = SPECIAL_ASPECTS.get(g, DEFAULT_ASPECTS)
        aspects[g] = {"aspect_arcs_houses": arcs,
                      "aspected_houses": sorted({(src_h + a - 2) % 12 + 1 for a in arcs})}

    lagna_entry = {
        "longitude_sidereal": lagna, "sign_index": lagna_sign,
        "sign": core.SIGNS_SKT[lagna_sign], "sign_western": core.SIGNS_TROP[lagna_sign],
        "degrees_in_sign": core.deg_in_sign(lagna), "formatted": core.fmt(lagna, skt=True),
        "nakshatra": nakshatra_of(lagna), "lord": SIGN_LORDS[lagna_sign],
        "navamsa_sign": core.SIGNS_SKT[varga(lagna, 9)],
        "navamsa_sign_index": varga(lagna, 9),
        "dasamsa_sign": core.SIGNS_SKT[varga(lagna, 10)],
        "dasamsa_sign_index": varga(lagna, 10),
        "vargottama_d9": varga(lagna, 9) == lagna_sign,
        "mc_sidereal": h["mc"], "mc_formatted": core.fmt(h["mc"], skt=True),
    }
    return {"ayanamsha_deg": ayan, "node_convention": node,
            "lagna": lagna_entry, "planets": planets, "houses": house_info,
            "aspects": aspects, "planetary_war": wars}


def ashtakavarga(jd_chart):
    """Bhinna + Sarva ashtakavarga from whole-sign positions."""
    p = jd_chart["planets"]; lagna_sign = jd_chart["lagna"]["sign_index"]
    contributor_sign = {g: p[g]["sign_index"] for g in
                        ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    contributor_sign["Lagna"] = lagna_sign

    bav = {}
    for subject, rows in BAV.items():
        counts = [0] * 12
        for contrib, houses_list in rows.items():
            cs = contributor_sign[contrib]
            for hnum in houses_list:
                counts[(cs + hnum - 1) % 12] += 1
        bav[subject] = counts
    sav = [sum(bav[s][i] for s in bav) for i in range(12)]

    checks = {}
    for s, c in bav.items():
        checks[s] = {"total": sum(c), "expected": BAV_EXPECTED_TOTALS[s],
                     "pass": sum(c) == BAV_EXPECTED_TOTALS[s]}
    checks["SAV_total"] = {"total": sum(sav), "expected": 337, "pass": sum(sav) == 337}

    return {"bhinnashtakavarga_by_sign_index": bav,
            "sarvashtakavarga_by_sign_index": sav,
            "sarvashtakavarga_by_house": {h: sav[(lagna_sign + h - 1) % 12] for h in range(1, 13)},
            "row_total_checks": checks,
            "validation_note": ("Row totals match the classical per-planet totals "
                                "(48/49/39/54/56/52/39, sum 337). This validates the table "
                                "cardinalities, not each individual cell. Single implementation, "
                                "no independent second engine -> confidence capped at medium.")}


DAY = 86400.0

def vimshottari(moon_lon, birth_utc, year_days=365.2425, levels=3):
    import datetime as dt
    nk = nakshatra_of(moon_lon)
    start_lord = nk["lord"]
    i0 = VIM_ORDER.index(start_lord)
    balance_years = VIM_YEARS[start_lord] * (1.0 - nk["fraction_elapsed"])
    # epoch at which the running mahadasha began
    md_start = birth_utc - dt.timedelta(days=(VIM_YEARS[start_lord] - balance_years) * year_days)

    periods = []
    cursor = md_start
    for k in range(9 + 3):
        lord = VIM_ORDER[(i0 + k) % 9]
        yrs = VIM_YEARS[lord]
        end = cursor + dt.timedelta(days=yrs * year_days)
        md = {"level": 1, "lord": lord, "start": cursor.isoformat(), "end": end.isoformat(),
              "years": yrs, "children": []}
        if levels >= 2:
            ac = cursor
            j0 = VIM_ORDER.index(lord)
            for m in range(9):
                al = VIM_ORDER[(j0 + m) % 9]
                adays = yrs * VIM_YEARS[al] / 120.0 * year_days
                aend = ac + dt.timedelta(days=adays)
                ad = {"level": 2, "lord": al, "start": ac.isoformat(), "end": aend.isoformat(),
                      "days": adays, "children": []}
                if levels >= 3:
                    pc = ac
                    k0 = VIM_ORDER.index(al)
                    for q in range(9):
                        pl = VIM_ORDER[(k0 + q) % 9]
                        pdays = adays * VIM_YEARS[pl] / 120.0
                        pend = pc + dt.timedelta(days=pdays)
                        ad["children"].append({"level": 3, "lord": pl,
                                               "start": pc.isoformat(), "end": pend.isoformat(),
                                               "days": pdays})
                        pc = pend
                md["children"].append(ad)
                ac = aend
        periods.append(md)
        cursor = end
    return {"moon_nakshatra": nk, "starting_lord": start_lord,
            "balance_at_birth_years": balance_years,
            "year_length_days": year_days,
            "cycle_total_years": sum(VIM_YEARS.values()),
            "mahadashas": periods}


# ---------------- declared yoga whitelist (exact rules, no pattern mining) ----------------
KENDRA = (1, 4, 7, 10)
MAHAPURUSHA = {"Mars": "Ruchaka", "Mercury": "Bhadra", "Jupiter": "Hamsa",
               "Venus": "Malavya", "Saturn": "Sasa"}


def yogas(ch):
    P = ch["planets"]; found = []

    def house_from(a, b):
        return (P[b]["sign_index"] - P[a]["sign_index"]) % 12 + 1

    if house_from("Moon", "Jupiter") in KENDRA:
        found.append({"name": "Gajakesari Yoga",
                      "rule": "Jupiter occupies a kendra (1/4/7/10) counted from the Moon.",
                      "satisfied_by": {"Moon": P["Moon"]["formatted"], "Jupiter": P["Jupiter"]["formatted"],
                                       "house_of_Jupiter_from_Moon": house_from("Moon", "Jupiter")}})
    if P["Sun"]["sign_index"] == P["Mercury"]["sign_index"]:
        found.append({"name": "Budha-Aditya Yoga",
                      "rule": "Sun and Mercury occupy the same sign.",
                      "satisfied_by": {"Sun": P["Sun"]["formatted"], "Mercury": P["Mercury"]["formatted"]},
                      "caveat": "Combustion is reported separately and is not excluded by this rule."})
    if P["Moon"]["sign_index"] == P["Mars"]["sign_index"] or house_from("Moon", "Mars") == 7:
        found.append({"name": "Chandra-Mangala Yoga",
                      "rule": "Moon and Mars conjunct in one sign, or exactly 7th from each other.",
                      "satisfied_by": {"Moon": P["Moon"]["formatted"], "Mars": P["Mars"]["formatted"]}})
    ms = P["Moon"]["sign_index"]
    neighbours = [(ms + 1) % 12, (ms - 1) % 12]
    occupied = [g for g in ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
                if P[g]["sign_index"] in neighbours or P[g]["sign_index"] == ms]
    if not occupied:
        found.append({"name": "Kemadruma Yoga",
                      "rule": "No planet other than the Sun and the nodes occupies the 2nd or 12th "
                              "from the Moon, nor the Moon's own sign.",
                      "satisfied_by": {"Moon": P["Moon"]["formatted"]}})
    else:
        found.append({"name": "Kemadruma Yoga -- ABSENT (cancelled)",
                      "rule": "Kemadruma requires the 2nd/12th from the Moon and the Moon's sign to "
                              "be empty of the five star planets.",
                      "not_satisfied_because": {"planets_adjacent_to_or_with_Moon": occupied},
                      "polarity": "positive by absence"})
    for pl, nm in MAHAPURUSHA.items():
        d = P[pl]["dignity"]["state"]
        if d in ("own_sign", "moolatrikona", "exalted") and P[pl]["house_whole_sign"] in KENDRA:
            found.append({"name": f"{nm} Yoga (Pancha Mahapurusha)",
                          "rule": f"{pl} in own sign / moolatrikona / exaltation AND in a kendra "
                                  f"from the Lagna.",
                          "satisfied_by": {pl: P[pl]["formatted"], "dignity": d,
                                           "house": P[pl]["house_whole_sign"]}})
    dusthana = [6, 8, 12]
    for h in dusthana:
        lord = ch["houses"][h]["lord"]
        lh = P[lord]["house_whole_sign"]
        if lh in dusthana:
            found.append({"name": f"Vipareeta Raja Yoga ({h}th lord in the {lh}th)",
                          "rule": "The lord of a dusthana (6/8/12) is placed in another dusthana.",
                          "satisfied_by": {"house": h, "lord": lord,
                                           "lord_placed_in_house": lh,
                                           "lord_position": P[lord]["formatted"]}})
    l2, l11 = ch["houses"][2]["lord"], ch["houses"][11]["lord"]
    if P[l2]["sign_index"] == P[l11]["sign_index"]:
        found.append({"name": "Dhana Yoga (2nd and 11th lords conjunct)",
                      "rule": "The 2nd lord and the 11th lord occupy the same sign.",
                      "satisfied_by": {"2nd_lord": l2, "11th_lord": l11,
                                       "sign": P[l2]["sign"]}})
    else:
        found.append({"name": "Dhana Yoga (2nd/11th lord conjunction) -- ABSENT",
                      "rule": "Requires the 2nd lord and 11th lord in the same sign.",
                      "not_satisfied_because": {"2nd_lord": l2, "in": P[l2]["sign"],
                                                "11th_lord": l11, "in": P[l11]["sign"]},
                      "polarity": "neutral"})
    return {"whitelist_only": True,
            "declared_rules_evaluated": ["Gajakesari", "Budha-Aditya", "Chandra-Mangala",
                                         "Kemadruma", "Pancha Mahapurusha (5)",
                                         "Vipareeta Raja", "Dhana (2nd/11th)"],
            "note": "Closed whitelist. No unrestricted pattern mining was performed, and absences "
                    "are reported alongside presences.",
            "results": found}


def active_periods(vim, when_iso):
    """Return the (MD, AD, PD) active at an ISO instant."""
    out = {}
    for md in vim["mahadashas"]:
        if md["start"] <= when_iso < md["end"]:
            out["mahadasha"] = {k: md[k] for k in ("lord", "start", "end")}
            for ad in md["children"]:
                if ad["start"] <= when_iso < ad["end"]:
                    out["antardasha"] = {k: ad[k] for k in ("lord", "start", "end")}
                    for pd in ad["children"]:
                        if pd["start"] <= when_iso < pd["end"]:
                            out["pratyantardasha"] = {k: pd[k] for k in ("lord", "start", "end")}
    return out
