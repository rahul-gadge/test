"""Western / Hellenistic track: tropical zodiac, whole-sign houses, 7 traditional planets."""
import datetime as dt
from . import core
import swisseph as swe

TRAD = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
MODERN = ["Uranus", "Neptune", "Pluto"]

DOMICILE = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
            "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
EXALT = {"Sun": (0, 19.0), "Moon": (1, 3.0), "Mercury": (5, 15.0), "Venus": (11, 27.0),
         "Mars": (9, 28.0), "Jupiter": (3, 15.0), "Saturn": (6, 21.0)}
TRIPLICITY = {  # Dorothean: (day, night, participating)
    "fire":  ("Sun", "Jupiter", "Saturn"), "earth": ("Venus", "Moon", "Mars"),
    "air":   ("Saturn", "Mercury", "Jupiter"), "water": ("Venus", "Mars", "Moon"),
}
ELEMENT_OF_SIGN = ["fire", "earth", "air", "water"] * 3
CHALDEAN = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]

EGYPTIAN_BOUNDS = {
 0:[("Jupiter",6),("Venus",12),("Mercury",20),("Mars",25),("Saturn",30)],
 1:[("Venus",8),("Mercury",14),("Jupiter",22),("Saturn",27),("Mars",30)],
 2:[("Mercury",6),("Jupiter",12),("Venus",17),("Mars",24),("Saturn",30)],
 3:[("Mars",7),("Venus",13),("Mercury",19),("Jupiter",26),("Saturn",30)],
 4:[("Jupiter",6),("Venus",11),("Saturn",18),("Mercury",24),("Mars",30)],
 5:[("Mercury",7),("Venus",17),("Jupiter",21),("Mars",28),("Saturn",30)],
 6:[("Saturn",6),("Mercury",14),("Jupiter",21),("Venus",28),("Mars",30)],
 7:[("Mars",7),("Venus",11),("Mercury",19),("Jupiter",24),("Saturn",30)],
 8:[("Jupiter",12),("Venus",17),("Mercury",21),("Saturn",26),("Mars",30)],
 9:[("Mercury",7),("Jupiter",14),("Venus",22),("Saturn",26),("Mars",30)],
10:[("Mercury",7),("Venus",13),("Jupiter",20),("Mars",25),("Saturn",30)],
11:[("Venus",12),("Jupiter",16),("Mercury",19),("Mars",28),("Saturn",30)],
}
BOUND_TOTALS_EXPECTED = {"Saturn": 57, "Jupiter": 79, "Mars": 66, "Venus": 82, "Mercury": 76}

MOIETY = {"Sun": 7.5, "Moon": 6.0, "Mercury": 3.5, "Venus": 3.5,
          "Mars": 4.0, "Jupiter": 4.5, "Saturn": 4.5}
ASPECTS = {0: "conjunction", 60: "sextile", 90: "square", 120: "trine", 180: "opposition"}

ZR_PERIODS = {0:15, 1:8, 2:20, 3:25, 4:19, 5:20, 6:8, 7:15, 8:12, 9:27, 10:30, 11:12}


def validate_bounds():
    tot = {}
    per_sign_ok = True
    for s, rows in EGYPTIAN_BOUNDS.items():
        prev = 0
        for pl, end in rows:
            tot[pl] = tot.get(pl, 0) + (end - prev); prev = end
        if prev != 30: per_sign_ok = False
    return {"per_planet_totals": tot, "expected": BOUND_TOTALS_EXPECTED,
            "planet_totals_pass": tot == BOUND_TOTALS_EXPECTED,
            "each_sign_sums_to_30": per_sign_ok,
            "grand_total": sum(tot.values()), "grand_total_expected": 360}


def bound_ruler(lon):
    s = core.sign_of(lon); d = core.deg_in_sign(lon)
    for pl, end in EGYPTIAN_BOUNDS[s]:
        if d < end: return pl
    return EGYPTIAN_BOUNDS[s][-1][0]


def face_ruler(lon):
    return CHALDEAN[int(lon // 10) % 7]


def dignities(planet, lon, is_day):
    s = core.sign_of(lon); d = core.deg_in_sign(lon)
    out = {"domicile_ruler_of_sign": DOMICILE[s], "in_domicile": DOMICILE[s] == planet,
           "bound_ruler": bound_ruler(lon), "in_own_bound": bound_ruler(lon) == planet,
           "face_ruler": face_ruler(lon), "in_own_face": face_ruler(lon) == planet}
    ex = EXALT.get(planet)
    out["in_exaltation"] = bool(ex and s == ex[0])
    out["in_fall"] = bool(ex and s == (ex[0] + 6) % 12)
    out["exaltation_degree"] = ex[1] if ex else None
    out["in_detriment"] = DOMICILE[(s + 6) % 12] == planet
    el = ELEMENT_OF_SIGN[s]
    trip = TRIPLICITY[el]
    out["triplicity_element"] = el
    out["triplicity_rulers"] = {"day": trip[0], "night": trip[1], "participating": trip[2]}
    out["triplicity_ruler_in_sect"] = trip[0] if is_day else trip[1]
    out["is_triplicity_ruler_in_sect"] = (trip[0] if is_day else trip[1]) == planet
    out["is_any_triplicity_ruler"] = planet in trip
    score = (5 if out["in_domicile"] else 0) + (4 if out["in_exaltation"] else 0) + \
            (3 if out["is_any_triplicity_ruler"] else 0) + (2 if out["in_own_bound"] else 0) + \
            (1 if out["in_own_face"] else 0) - (5 if out["in_detriment"] else 0) - \
            (4 if out["in_fall"] else 0)
    out["ptolemaic_dignity_score"] = score
    out["score_scheme"] = "domicile +5, exaltation +4, triplicity +3, bound +2, face +1, detriment -5, fall -4"
    return out


def sect_of(jd, lat, lon_geo, sun_lon, asc):
    """Day/night from the actual horizon, not from a clock rule."""
    ss = core.sunrise_sunset_for_local_day(jd, lat, lon_geo)
    if ss["sunrise_jd"] <= jd < ss["sunset_jd"]:
        is_day, why = True, "between sunrise and sunset of the local civil day"
    elif jd < ss["sunrise_jd"]:
        is_day, why = False, "before sunrise of the local civil day"
    else:
        is_day, why = False, "after sunset of the local civil day"
    return {
        "is_day_chart": is_day, "sect": "diurnal" if is_day else "nocturnal", "basis": why,
        "sunrise_local": core.jd_to_local(ss["sunrise_jd"]).isoformat(),
        "sunset_local": core.jd_to_local(ss["sunset_jd"]).isoformat(),
        "minutes_from_sunrise": (jd - ss["sunrise_jd"]) * 1440.0,
        "minutes_from_sunset": (jd - ss["prev_sunset_jd"]) * 1440.0,
        "sect_light": "Sun" if is_day else "Moon",
        "benefic_of_sect": "Jupiter" if is_day else "Venus",
        "malefic_of_sect": "Saturn" if is_day else "Mars",
        "malefic_contrary_to_sect": "Mars" if is_day else "Saturn",
        "benefic_contrary_to_sect": "Venus" if is_day else "Jupiter",
    }


def lots(asc, sun, moon, is_day):
    if is_day:
        fortune = (asc + moon - sun) % 360.0
        spirit = (asc + sun - moon) % 360.0
    else:
        fortune = (asc + sun - moon) % 360.0
        spirit = (asc + moon - sun) % 360.0
    return {
        "fortune": {"longitude": fortune, "formatted": core.fmt(fortune),
                    "sign_index": core.sign_of(fortune)},
        "spirit": {"longitude": spirit, "formatted": core.fmt(spirit),
                   "sign_index": core.sign_of(spirit)},
        "formula_used": ("nocturnal: Fortune = Asc + Sun - Moon, Spirit = Asc + Moon - Sun"
                         if not is_day else
                         "diurnal: Fortune = Asc + Moon - Sun, Spirit = Asc + Sun - Moon"),
    }


def aspects_between(pos, orbs_from=MOIETY):
    out = []
    names = TRAD
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            la, lb = pos[a]["longitude"], pos[b]["longitude"]
            sep = core.angsep(la, lb)
            for ang, nm in ASPECTS.items():
                orb_max = orbs_from[a] + orbs_from[b]
                d = abs(sep - ang)
                if d <= orb_max:
                    faster, slower = (a, b) if abs(pos[a]["speed_long"]) >= abs(pos[b]["speed_long"]) else (b, a)
                    delta = (core.angsep(la + pos[a]["speed_long"] * 0.01,
                                         lb + pos[b]["speed_long"] * 0.01) - ang)
                    applying = abs(delta) < abs(sep - ang)
                    out.append({
                        "pair": [a, b], "aspect": nm, "exact_angle": ang,
                        "separation_deg": sep, "orb_deg": d, "max_orb_deg": orb_max,
                        "applying": bool(applying),
                        "phase": "applying" if applying else "separating",
                        "faster_body": faster,
                        "whole_sign_aspect": _ws_aspect(core.sign_of(la), core.sign_of(lb)),
                    })
    return out


def _ws_aspect(sa, sb):
    d = (sb - sa) % 12
    return {0: "same sign (conjunction)", 1: "aversion", 2: "sextile", 3: "square",
            4: "trine", 5: "aversion", 6: "opposition", 7: "aversion", 8: "trine",
            9: "square", 10: "sextile", 11: "aversion"}[d]


def solar_condition(pos):
    sun = pos["Sun"]["longitude"]
    out = {"Sun": {"elongation_deg": 0.0, "condition": "n/a (is the Sun)",
                   "orbs_used": "n/a"}}
    for p in TRAD[1:]:
        sep = core.angsep(pos[p]["longitude"], sun)
        if sep <= 17.0 / 60.0: st = "cazimi (in the heart of the Sun)"
        elif sep <= 8.0: st = "combust"
        elif sep <= 15.0: st = "under the beams"
        else: st = "free of the beams"
        out[p] = {"elongation_deg": sep, "condition": st,
                  "orbs_used": "cazimi <=17', combust <=8deg, under the beams <=15deg"}
    return out


def dispositor_chain(pos, start):
    seen, chain = [], start
    cur = start
    while cur not in seen:
        seen.append(cur)
        nxt = DOMICILE[core.sign_of(pos[cur]["longitude"])]
        if nxt == cur:
            return {"chain": seen, "terminus": cur, "type": "final dispositor (in own domicile)"}
        cur = nxt
    loop_start = seen.index(cur)
    return {"chain": seen, "terminus": None, "type": "loop",
            "loop_members": seen[loop_start:]}


def profection(asc_sign, birth_local, target_local):
    age = target_local.year - birth_local.year - (
        (target_local.month, target_local.day) < (birth_local.month, birth_local.day))
    house = age % 12 + 1
    sign = (asc_sign + age) % 12
    yr_start = birth_local.replace(year=birth_local.year + age)
    yr_end = birth_local.replace(year=birth_local.year + age + 1)
    return {"age_complete_years": age, "profected_house": house,
            "profected_sign_index": sign, "profected_sign": core.SIGNS_TROP[sign],
            "lord_of_the_year": DOMICILE[sign],
            "profection_year_start": yr_start.isoformat(),
            "profection_year_end": yr_end.isoformat(),
            "rule": "age mod 12 houses advanced from the natal Ascendant sign; the domicile "
                    "ruler of that sign is Lord of the Year."}


def solar_return(natal_sun_lon, year, lat, lon_geo, around):
    j = core.solar_longitude_crossing(natal_sun_lon, around)
    h = core.houses(j, lat, lon_geo, b"W")
    pos = core.swe_positions(j)
    return {"exact_jd": j, "exact_utc": core.jd_to_utc(j).isoformat(),
            "exact_local": core.jd_to_local(j).isoformat(),
            "asc": h["asc"], "asc_formatted": core.fmt(h["asc"]),
            "mc": h["mc"], "mc_formatted": core.fmt(h["mc"]),
            "latitude": lat, "longitude": lon_geo,
            "planets": {p: {"longitude": pos[p]["longitude"], "formatted": core.fmt(pos[p]["longitude"])}
                        for p in TRAD}}


def zodiacal_releasing_L1(lot_sign, birth_local, n=12, year_days=365.2425):
    out = []; cur = birth_local; s = lot_sign
    for _ in range(n):
        yrs = ZR_PERIODS[s]
        end = cur + dt.timedelta(days=yrs * year_days)
        out.append({"level": 1, "sign_index": s, "sign": core.SIGNS_TROP[s],
                    "ruler": DOMICILE[s], "years": yrs,
                    "start": cur.isoformat(), "end": end.isoformat()})
        cur = end; s = (s + 1) % 12
    return {"periods": out, "total_of_all_12_periods_years": sum(ZR_PERIODS.values()),
            "year_length_days": year_days,
            "note": ("Level 1 only. Loosing of the Bond does not occur within a human lifespan "
                     "at L1, so no LB rule is applied. Deeper levels are NOT computed and no "
                     "peak-period claim is made. Reported separately; it does NOT add a second "
                     "Western vote.")}


def build(jd, lat, lon_geo, pos, birth_local):
    h = core.houses(jd, lat, lon_geo, b"W")
    asc, mc = h["asc"], h["mc"]
    asc_sign = core.sign_of(asc)
    sect = sect_of(jd, lat, lon_geo, pos["Sun"]["longitude"], asc)
    is_day = sect["is_day_chart"]

    planets = {}
    for p in TRAD + MODERN:
        L = pos[p]["longitude"]; s = core.sign_of(L)
        entry = {
            "longitude_tropical": L, "sign": core.SIGNS_TROP[s], "sign_index": s,
            "degrees_in_sign": core.deg_in_sign(L), "formatted": core.fmt(L),
            "whole_sign_house": (s - asc_sign) % 12 + 1,
            "speed_deg_per_day": pos[p]["speed_long"], "retrograde": pos[p]["retrograde"],
            "latitude": pos[p]["latitude"],
            "angular_whole_sign": ((s - asc_sign) % 12 + 1) in (1, 4, 7, 10),
            "is_traditional": p in TRAD,
        }
        if p in TRAD:
            entry["dignity"] = dignities(p, L, is_day)
            entry["of_sect"] = _of_sect(p, is_day)
        planets[p] = entry

    sc = solar_condition({k: pos[k] for k in TRAD})
    for p, v in sc.items():
        planets[p]["solar_condition"] = v

    houses_info = {}
    for hh in range(1, 13):
        s = (asc_sign + hh - 1) % 12
        houses_info[hh] = {
            "sign_index": s, "sign": core.SIGNS_TROP[s], "ruler": DOMICILE[s],
            "ruler_in_house": (core.sign_of(pos[DOMICILE[s]]["longitude"]) - asc_sign) % 12 + 1,
            "ruler_sign": core.SIGNS_TROP[core.sign_of(pos[DOMICILE[s]]["longitude"])],
            "occupants": [p for p in TRAD if (core.sign_of(pos[p]["longitude"]) - asc_sign) % 12 + 1 == hh],
            "occupants_modern": [p for p in MODERN if (core.sign_of(pos[p]["longitude"]) - asc_sign) % 12 + 1 == hh],
        }

    return {
        "zodiac": "tropical", "house_system": "whole sign",
        "ascendant": {"longitude": asc, "formatted": core.fmt(asc), "sign_index": asc_sign,
                      "sign": core.SIGNS_TROP[asc_sign], "ruler": DOMICILE[asc_sign],
                      "bound_ruler": bound_ruler(asc), "face_ruler": face_ruler(asc)},
        "midheaven": {"longitude": mc, "formatted": core.fmt(mc),
                      "sign": core.SIGNS_TROP[core.sign_of(mc)],
                      "whole_sign_house_containing_mc": (core.sign_of(mc) - asc_sign) % 12 + 1},
        "sect": sect, "planets": planets, "houses": houses_info,
        "lots": lots(asc, pos["Sun"]["longitude"], pos["Moon"]["longitude"], is_day),
        "aspects": aspects_between({k: pos[k] for k in TRAD}),
        "dispositor_chains": {p: dispositor_chain({k: pos[k] for k in TRAD}, p) for p in TRAD},
        "bounds_table_validation": validate_bounds(),
    }


def _of_sect(p, is_day):
    if p == "Sun": return "sect light" if is_day else "contrary to sect (luminary)"
    if p == "Moon": return "contrary to sect (luminary)" if is_day else "sect light"
    if p == "Jupiter": return "benefic of sect" if is_day else "benefic contrary to sect"
    if p == "Venus": return "benefic contrary to sect" if is_day else "benefic of sect"
    if p == "Saturn": return "malefic of sect" if is_day else "malefic contrary to sect"
    if p == "Mars": return "malefic contrary to sect" if is_day else "malefic of sect"
    return "neutral (Mercury takes the sect of its solar phase)"
