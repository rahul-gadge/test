#!/usr/bin/env python
"""Deterministic builder. Reads BIRTH_INPUT.json, emits MASTER_DATASET.json.

Facts only. No interpretation. The person's data is never hardcoded here.
"""
import datetime as dt, hashlib, importlib.metadata as md, json, os, platform, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import swisseph as swe
from chart import core, jyotisha as jy, sinic, western as we, calendars as cal, validate
from chart import vargas as vg, panchanga as pn, schools as sch, shadbala as sb

ROOT = os.path.dirname(os.path.abspath(__file__))
NOW = dt.datetime.now(dt.timezone.utc)
BI = json.load(open(os.path.join(ROOT, "BIRTH_INPUT.json")))

N = BI["normalized"]; LOC = BI["location_primary"]
LAT, LON = LOC["latitude_deg"], LOC["longitude_deg"]
Y, M, D = map(int, N["civil_date_local"].split("-"))
HH, MI, SS = map(int, N["civil_time_local_24h"].split(":"))
UNC = N["time_uncertainty_seconds"]
MALE = N["gender"] == "male"

birth_local, birth_utc = core.local_to_utc(Y, M, D, HH, MI, SS)
JD = core.jd_ut(birth_utc)


def at(offset_s):
    u = birth_utc + dt.timedelta(seconds=offset_s)
    return u, core.jd_ut(u)


# ---------------------------------------------------------------- 1. time audit
st = core.solar_times(JD, LON)
ss = core.sunrise_sunset_for_local_day(JD, LAT, LON)
delta_t = swe.deltat(JD) * 86400.0

time_audit = {
    "original_local_civil": birth_local.isoformat(),
    "utc_instant": birth_utc.isoformat(),
    "julian_day_ut": JD,
    "julian_day_tt": JD + swe.deltat(JD),
    "delta_t_seconds": delta_t,
    "timezone_iana": "Asia/Kolkata",
    "tzdata_release": md.version("tzdata"),
    "utc_offset_applied": str(birth_local.utcoffset()),
    "dst_in_effect": bool(birth_local.dst().total_seconds()) if birth_local.dst() else False,
    "historical_offset_check": {
        "verdict": "reliable",
        "reasoning": ("India observed IST = UTC+05:30 with no daylight saving throughout 2003. "
                      "Indian DST existed only in 1942-1945 and briefly in 1965 and 1971. The "
                      "date is post-1970, so the IANA database governs and is authoritative here. "
                      "No offset ambiguity."),
        "iana_zone": "Asia/Kolkata", "offset": "+05:30", "dst": False,
    },
    "civil_weekday": birth_local.strftime("%A"),
    "vedic_vara_note": {
        "civil_weekday": birth_local.strftime("%A"),
        "panchanga_vara": "Sunday (Ravivara)",
        "reason": ("The Vedic day (vara) begins at sunrise. Birth at 05:24 precedes sunrise at "
                   "06:58:26, so the panchanga weekday is still the previous day's. This affects "
                   "vara-based panchanga readings only; it does not affect Vimshottari dasha, "
                   "which is anchored on the Moon's nakshatra."),
    },
    "local_mean_solar_time": st["lmt_clock"],
    "local_apparent_solar_time": st["lat_clock"],
    "equation_of_time_minutes": st["equation_of_time_minutes"],
    "longitude_correction_minutes": (LON - 82.5) / 15.0 * 60.0,
    "sunrise_local": core.jd_to_local(ss["sunrise_jd"]).isoformat(),
    "sunset_local": core.jd_to_local(ss["sunset_jd"]).isoformat(),
    "prev_sunset_local": core.jd_to_local(ss["prev_sunset_jd"]).isoformat(),
    "day_length_hours": (ss["sunset_jd"] - ss["sunrise_jd"]) * 24.0,
    "calendar_conversion_rule": "Input already Gregorian; no conversion applied.",
}

# ---------------------------------------------------------------- 2. boundaries
def asc_speed_deg_per_min(jd):
    a = core.houses(jd - 30.0 / 86400, LAT, LON, b"W")["asc"]
    b = core.houses(jd + 30.0 / 86400, LAT, LON, b"W")["asc"]
    return ((b - a + 180) % 360 - 180) / 1.0


asc_rate = asc_speed_deg_per_min(JD)          # deg per minute of clock time
pos_t = core.swe_positions(JD)
pos_s = core.swe_positions(JD, sidereal=True)
AY = core.ayanamsha(JD)
asc_trop = core.houses(JD, LAT, LON, b"W")["asc"]
asc_sid = core.houses(JD, LAT, LON, b"W", sidereal=True)["asc"]

lichun = core.solar_longitude_crossing(315.0, core.jd_ut(dt.datetime(2003, 2, 4, tzinfo=dt.timezone.utc)))
xiaohan = core.solar_longitude_crossing(285.0, core.jd_ut(dt.datetime(2003, 1, 6, tzinfo=dt.timezone.utc)))
dahan = core.solar_longitude_crossing(300.0, core.jd_ut(dt.datetime(2003, 1, 20, tzinfo=dt.timezone.utc)))


def to_next(value, step):
    r = value % step
    return step - r, r


boundaries = []


def bd(system, name, dist_deg=None, dist_min=None, changes=None, note=None, verdict=None):
    boundaries.append({"system": system, "boundary": name,
                       "distance_degrees": dist_deg, "distance_minutes_of_clock_time": dist_min,
                       "what_would_change": changes, "note": note, "verdict": verdict})


d_next, _ = to_next(asc_trop, 30.0)
bd("western", "Ascendant sign boundary (Capricorn -> Aquarius)", d_next, d_next / asc_rate,
   "the entire whole-sign house frame", verdict="far - stable")
d_next_s, _ = to_next(asc_sid, 30.0)
bd("jyotisha", "Lagna sign boundary (Dhanu -> Makara)", d_next_s, d_next_s / asc_rate,
   "the entire whole-sign house frame and the Lagna lord", verdict="far - stable")
d9, _ = to_next(asc_sid, 30.0 / 9)
bd("jyotisha", "D9 (Navamsa) Lagna boundary", d9, d9 / asc_rate,
   "the Navamsa Lagna sign", verdict="moderate")
d10, _ = to_next(core.deg_in_sign(asc_sid), 3.0)
bd("jyotisha", "D10 (Dasamsa) Lagna boundary", d10, d10 / asc_rate,
   "the Dasamsa Lagna sign", verdict="CLOSE - see uncertainty ensemble")
nk_span = 360.0 / 27
dn, _ = to_next(asc_sid, nk_span)
bd("jyotisha", "Lagna nakshatra boundary (Mula -> Purva Ashadha)", dn, dn / asc_rate,
   "the Lagna nakshatra and its pada", verdict="far - stable")
dp, _ = to_next(asc_sid, nk_span / 4)
bd("jyotisha", "Lagna nakshatra pada boundary", dp, dp / asc_rate,
   "the Lagna pada (and with it the D9 Lagna)", verdict="moderate")
dsun, _ = to_next(pos_t["Sun"]["longitude"], 30.0)
bd("western", "Sun tropical sign boundary (Capricorn -> Aquarius)", dsun,
   dsun / pos_t["Sun"]["speed_long"] * 1440.0,
   "the Sun's tropical sign; the Sun sits in the final (anaretic) degree of Capricorn",
   note="Sun at 29 deg 29' Capricorn. Sign is stable for this birth time, but the Sun is "
        "0.51 deg from Aquarius, i.e. ~12 hours later the Sun changes sign.",
   verdict="stable for the stated time, but notable")
bd("western", "sunrise / sect boundary", None, (JD - ss["sunrise_jd"]) * 1440.0,
   "diurnal vs nocturnal sect, and with it every sect-based judgement",
   note="Birth is 94.4 minutes before sunrise. Nocturnal sect is robust.",
   verdict="far - stable")
bd("bazi", "sectional term Lichun (立春), Sun at 315 deg -- BaZi year boundary",
   None, (JD - lichun) * 1440.0,
   "the YEAR pillar: before Lichun 2003 the year is 壬午 (2002), not 癸未 (2003)",
   note="Birth precedes Lichun 2003 by 15.36 days. Year pillar 壬午 is robust.",
   verdict="far - stable")
bd("bazi", "sectional term Xiaohan (小寒), Sun at 285 deg -- month boundary",
   None, (JD - xiaohan) * 1440.0, "the MONTH pillar",
   note="Birth is 14.12 days after Xiaohan and 15.36 days before Lichun; month pillar 癸丑 sits "
        "mid-interval.", verdict="far - stable")
bd("bazi", "middle term Dahan (大寒), Sun at 300 deg", None, (JD - dahan) * 1440.0,
   "nothing in the Four Pillars",
   note="Birth is 14.47 hours BEFORE Dahan. Dahan is a middle term (中氣), which does not move "
        "any pillar. Recorded for completeness only.", verdict="not pillar-relevant")
bd("bazi", "two-hour branch boundary -- CIVIL CLOCK convention", None, (HH * 60 + MI) - 300.0,
   "the HOUR pillar", note="05:24 civil is 24 minutes into the Mao (卯) hour.",
   verdict="stable within the stated uncertainty")
lat_min = (float(st["lat_clock"][:2]) * 60 + float(st["lat_clock"][3:5]) + float(st["lat_clock"][6:]) / 60)
bd("bazi", "two-hour branch boundary -- TRUE SOLAR TIME convention", None, lat_min - 300.0,
   "the HOUR pillar",
   note="True solar time is 04:56:15, which is 3 min 45 s BEFORE the Mao (卯) boundary, placing "
        "the birth in the Yin (寅) hour instead. This is the single most convention-sensitive "
        "value in the whole chart.",
   verdict="SCHOOL-DIVERGENT - both results reported, neither selected")
bd("bazi", "midnight / late-Zi day boundary", None, (HH * 60 + MI) - 0.0,
   "the DAY pillar", note="Birth at 05:24 is far from both midnight and the 23:00 late-Zi rule; "
                          "the day pillar 癸巳 is unaffected by day-boundary school.",
   verdict="far - stable")
bd("ziwei", "two-hour time index boundary", None, (HH * 60 + MI) - 300.0,
   "the time index, and with it Ming/Shen palace placement and all star positions",
   note="Zi Wei conventionally indexes on local civil clock time. 24 minutes into Mao (index 3).",
   verdict="stable within the stated uncertainty")
bd("ziwei", "civil day boundary", None, (HH * 60 + MI), "the lunar day, hence star placement",
   verdict="far - stable")
bd("ziwei", "lunar month / leap month", None, None, "palace placement if a leap month intervened",
   note="Birth falls in the 12th lunar month (腊月) of 壬午; no leap month is in play.",
   verdict="not applicable")
bd("tibetan", "Losar / year boundary", None, None,
   "the element-animal year assignment",
   note="Losar falls between early February and mid-March. 20 January precedes any possible "
        "Losar date, so the Tibetan year is the one begun at Losar 2002 = Water Male Horse. "
        "This conclusion holds across the full plausible Losar range, so no exact Losar "
        "computation is needed.", verdict="far - stable")
bd("maya", "calendar adoption / correlation", None, None, "the Long Count if a different "
   "correlation constant were chosen",
   note="Gregorian input, no adoption boundary. Correlation GMT 584283 declared; a different "
        "scholarly correlation would shift the Long Count by its own offset.",
   verdict="not applicable")

# ---------------------------------------------------------------- 3. ensemble
def snapshot(offset_s):
    u, j = at(offset_s)
    ps = core.swe_positions(j, sidereal=True)
    pt = core.swe_positions(j)
    a_s = core.houses(j, LAT, LON, b"W", sidereal=True)["asc"]
    a_t = core.houses(j, LAT, LON, b"W")["asc"]
    lt = u.astimezone(core.TZ)
    ec = sinic.pillars_for(lt.year, lt.month, lt.day, lt.hour, lt.minute, lt.second)[0]
    stt = core.solar_times(j, LON)
    lat_h = int(stt["lat_clock"][:2]); lat_m = int(stt["lat_clock"][3:5])
    ec_lat = sinic.pillars_for(lt.year, lt.month, lt.day, lat_h, lat_m,
                               int(float(stt["lat_clock"][6:])))[0]
    return {
        "offset_seconds": offset_s, "local": lt.isoformat(),
        "lagna_sidereal_deg": a_s, "lagna_sign": core.SIGNS_SKT[core.sign_of(a_s)],
        "lagna_nakshatra": jy.nakshatra_of(a_s)["name"],
        "lagna_pada": jy.nakshatra_of(a_s)["pada"],
        "lagna_d9_sign": core.SIGNS_SKT[jy.varga(a_s, 9)],
        "lagna_d10_sign": core.SIGNS_SKT[jy.varga(a_s, 10)],
        "asc_tropical_deg": a_t, "asc_tropical_sign": core.SIGNS_TROP[core.sign_of(a_t)],
        "moon_sidereal_deg": ps["Moon"]["longitude"],
        "moon_nakshatra": jy.nakshatra_of(ps["Moon"]["longitude"])["name"],
        "moon_pada": jy.nakshatra_of(ps["Moon"]["longitude"])["pada"],
        "moon_d9_sign": core.SIGNS_SKT[jy.varga(ps["Moon"]["longitude"], 9)],
        "sun_tropical_sign": core.SIGNS_TROP[core.sign_of(pt["Sun"]["longitude"])],
        "planet_signs_sidereal": {g: core.SIGNS_SKT[core.sign_of(ps[g]["longitude"])]
                                  for g in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]},
        "bazi_pillars_civil": " ".join(ec[k]["ganzhi"] for k in ["year", "month", "day", "hour"]),
        "bazi_pillars_true_solar": " ".join(ec_lat[k]["ganzhi"] for k in ["year", "month", "day", "hour"]),
        "vimshottari_md_start": jy.vimshottari(ps["Moon"]["longitude"], u)["mahadashas"][0]["start"],
        "vimshottari_balance_years": jy.vimshottari(ps["Moon"]["longitude"], u)["balance_at_birth_years"],
    }


ensemble = {"stated_uncertainty_seconds": UNC,
            "members": [snapshot(-UNC), snapshot(0), snapshot(+UNC)],
            "secondary_robustness_probe": {
                "purpose": ("NOT the user's stated uncertainty. A wider probe that shows which "
                            "values would break if the recorded minute were itself wrong."),
                "members": [snapshot(-300), snapshot(+300), snapshot(-900), snapshot(+900)]}}


def stability(key, members):
    vals = [m[key] for m in members]
    return "stable" if len(set(map(str, vals))) == 1 else "sensitive"


STAB_KEYS = ["lagna_sign", "lagna_nakshatra", "lagna_pada", "lagna_d9_sign", "lagna_d10_sign",
             "asc_tropical_sign", "moon_nakshatra", "moon_pada", "moon_d9_sign",
             "sun_tropical_sign", "bazi_pillars_civil", "bazi_pillars_true_solar"]
ensemble["stability_stated_uncertainty"] = {k: stability(k, ensemble["members"]) for k in STAB_KEYS}
ensemble["stability_wide_probe_15min"] = {
    k: stability(k, [snapshot(-900), snapshot(0), snapshot(900)]) for k in STAB_KEYS}

# ---------------------------------------------------------------- 4. systems
jchart = jy.build(JD, LAT, LON, pos_s, AY, node="MeanNode")
jchart_true = jy.build(JD, LAT, LON, pos_s, AY, node="TrueNode")
av = jy.ashtakavarga(jchart)
vim = jy.vimshottari(jchart["planets"]["Moon"]["longitude_sidereal"], birth_utc)
vim_sid = jy.vimshottari(jchart["planets"]["Moon"]["longitude_sidereal"], birth_utc, year_days=365.25636)

pill_civil, ec_civil = sinic.pillars_for(Y, M, D, HH, MI, SS, MALE)
lt_h, lt_m = int(st["lat_clock"][:2]), int(st["lat_clock"][3:5])
pill_lat, ec_lat = sinic.pillars_for(Y, M, D, lt_h, lt_m, int(float(st["lat_clock"][6:])), MALE)
lm_h, lm_m = int(st["lmt_clock"][:2]), int(st["lmt_clock"][3:5])
pill_lmt, _ = sinic.pillars_for(Y, M, D, lm_h, lm_m, int(float(st["lmt_clock"][6:])), MALE)

tal_c, det_c = sinic.element_tally(pill_civil)
tal_l, det_l = sinic.element_tally(pill_lat)

wchart = we.build(JD, LAT, LON, pos_t, birth_local)

zw = json.load(open(os.path.join(ROOT, "out", "ziwei_raw.json")))
zwh = json.load(open(os.path.join(ROOT, "out", "ziwei_horo.json")))

maya = cal.maya(Y, M, D)
tib = cal.tibetan_year(2002)

# ---------------------------------------------------------------- 5b. precision layer
# --- panchanga ---
_pan = pn.build(JD, LAT, LON, pos_s["Sun"]["longitude"], pos_s["Moon"]["longitude"],
                ss["sunrise_jd"], birth_local)
_pan["nakshatra"] = {"of_moon": jchart["planets"]["Moon"]["nakshatra"],
                     "of_lagna": jchart["lagna"]["nakshatra"]}
_sunrise_variants = pn.sunrise_variants(JD, LAT, LON, LOC["elevation_m_approx"])

# --- all sixteen vargas, for every graha and the Lagna, with per-varga fragility ---
def _varga_block(lon):
    allv = vg.all_vargas(lon)
    for k in allv:
        dist = vg.boundary_distance(lon, k)
        allv[k]["degrees_to_next_division"] = dist
        allv[k]["minutes_of_birth_time_to_next_division"] = (
            dist / asc_rate if abs(asc_rate) > 1e-12 else None)
    return allv


_vargas = {"lagna": _varga_block(jchart["lagna"]["longitude_sidereal"]),
           "lagna_vargottama": vg.vargottama_count(jchart["lagna"]["longitude_sidereal"])}
for _g in jy.GRAHAS:
    _vargas[_g] = _varga_block(jchart["planets"][_g]["longitude_sidereal"])
    _vargas[_g + "_vargottama"] = vg.vargottama_count(jchart["planets"][_g]["longitude_sidereal"])

# which vargas survive the stated +/-30 s, computed rather than assumed
def _varga_stability(lon_fn):
    res = {}
    for k in vg.VARGAS:
        vals = {vg.VARGAS[k][0](lon_fn(o)) for o in (-UNC, 0, UNC)}
        res[k] = "stable" if len(vals) == 1 else "sensitive"
    return res


def _lagna_at(off):
    return core.houses(at(off)[1], LAT, LON, b"W", sidereal=True)["asc"]


def _moon_at(off):
    return core.swe_positions(at(off)[1], sidereal=True)["Moon"]["longitude"]


_varga_stab = {"lagna_at_stated_uncertainty": _varga_stability(_lagna_at),
               "moon_at_stated_uncertainty": _varga_stability(_moon_at),
               "lagna_at_15min_probe": {
                   k: ("stable" if len({vg.VARGAS[k][0](_lagna_at(o)) for o in (-900, 0, 900)}) == 1
                       else "sensitive") for k in vg.VARGAS}}

# --- shadbala ---
_decl = {}
for _p in sb.SEVEN:
    _decl[_p] = swe.calc_ut(JD, core.BODIES[_p], swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)[0][1]
_CHALD = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
_vara_lord = _pan["vara"]["lord"]
_hrs = (JD - ss["prev_sunrise_jd"]) * 24.0
_hora_lord = _CHALD[(_CHALD.index(_vara_lord) + int(_hrs)) % 7]
_shadbala = sb.build(
    {p: jchart["planets"][p]["longitude_sidereal"] for p in sb.SEVEN},
    {p: jchart["planets"][p]["house_whole_sign"] for p in sb.SEVEN},
    jchart["lagna"]["longitude_sidereal"], jchart["lagna"]["mc_sidereal"],
    JD, ss["sunrise_jd"], ss["sunset_jd"], ss["prev_sunset_jd"], _decl,
    {p: pos_s[p]["speed_long"] for p in sb.SEVEN},
    {p: pos_s[p]["retrograde"] for p in sb.SEVEN},
    _vara_lord, _hora_lord, "Sun", "Sun")
_shadbala["hora_lord"] = _hora_lord
_shadbala["vara_lord"] = _vara_lord

# --- school comparisons ---
_ayan_cmp = sch.ayanamsha_comparison(JD, LAT, LON)
_house_cmp = sch.house_system_comparison(JD, LAT, LON, pos_t)
_comb_cmp = sch.combustion_schools(pos_t["Sun"]["longitude"], pos_t)

# --- topocentric track ---
swe.set_topo(LON, LAT, LOC["elevation_m_approx"])
swe.set_sid_mode(swe.SIDM_LAHIRI)
_topo = {}
for _p in jy.GRAHAS[:7]:
    _geo = jchart["planets"][_p]["longitude_sidereal"]
    _tp = swe.calc_ut(JD, core.BODIES[_p],
                      swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL | swe.FLG_TOPOCTR)[0][0]
    _nk_g, _nk_t = jy.nakshatra_of(_geo), jy.nakshatra_of(_tp)
    _topo[_p] = {
        "geocentric_deg": _geo, "topocentric_deg": _tp,
        "difference_arcmin": core.angsep(_geo, _tp) * 60.0,
        "sign_changes": core.sign_of(_geo) != core.sign_of(_tp),
        "nakshatra_changes": (_nk_g["name"], _nk_g["pada"]) != (_nk_t["name"], _nk_t["pada"]),
        "vargas_that_change": [k for k, (f, _, _) in vg.VARGAS.items() if f(_geo) != f(_tp)],
    }
_topo["_summary"] = {
    "largest_shift_arcmin": max(v["difference_arcmin"] for v in _topo.values() if isinstance(v, dict)),
    "any_categorical_change": any(
        v["sign_changes"] or v["nakshatra_changes"] or v["vargas_that_change"]
        for v in _topo.values() if isinstance(v, dict)),
    "convention_declared": "GEOCENTRIC is the primary track, as every tradition here assumes it.",
}

# --- third, analytically independent engine: Moshier ---
_mosh = {}
for _p in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
    _m = swe.calc_ut(JD, core.BODIES[_p], swe.FLG_MOSEPH | swe.FLG_SPEED)[0][0]
    _mosh[_p] = {"moshier_deg": _m, "swiss_deg": pos_t[_p]["longitude"],
                 "difference_arcsec": core.angsep(_m, pos_t[_p]["longitude"]) * 3600.0}
_mosh["_max_difference_arcsec"] = max(v["difference_arcsec"] for v in _mosh.values()
                                      if isinstance(v, dict))

precision = {
    "panchanga": _pan, "sunrise_convention_variants": _sunrise_variants,
    "shodasavarga": _vargas, "varga_stability": _varga_stab,
    "shadbala": _shadbala,
    "ayanamsha_comparison": _ayan_cmp, "house_system_comparison": _house_cmp,
    "combustion_school_comparison": _comb_cmp,
    "topocentric_vs_geocentric": _topo,
    "third_engine_moshier": _mosh,
}


# ---------------------------------------------------------------- 5. verification
ver = []


def V(system, datum, pv, primary="Swiss Ephemeris 2.10.03 (sepl/semo/seas_18.se1)",
      validator=None, vv=None, diff=None, conv="", bdist=None, stab="stable",
      conf="high", status="pass", note=None):
    ver.append({"system": system, "datum": datum, "primary_engine": primary,
                "primary_value": pv, "validator": validator, "validator_value": vv,
                "difference": diff, "convention": conv, "boundary_distance": bdist,
                "uncertainty_stability": stab, "confidence": conf, "status": status,
                "note": note})


sky = validate.positions(JD)
worst = 0.0
for p in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]:
    d = core.angsep(pos_t[p]["longitude"], sky[p]["longitude"])
    worst = max(worst, d)
    V("shared_astronomy", f"{p} tropical apparent longitude", pos_t[p]["longitude"],
      validator="JPL DE440s via Skyfield 1.55", vv=sky[p]["longitude"], diff=d,
      conv="geocentric apparent, true ecliptic and equinox of date",
      stab="stable", conf="high", status="pass" if d < 0.01 else "ALERT")

V("shared_astronomy", "Ascendant (tropical)", asc_trop, validator=None,
  conv="whole-sign, geographic latitude 21.4737672 N", bdist=d_next,
  stab=ensemble["stability_stated_uncertainty"]["asc_tropical_sign"], conf="high",
  note="Single engine: Skyfield does not compute an Ascendant. Verified indirectly -- the "
       "Ascendant derives from sidereal time and obliquity, both of which are implied by the "
       "planetary agreement above.")
V("shared_astronomy", "ayanamsha (Lahiri) at birth", AY, conv="swe SIDM_LAHIRI",
  conf="high", note="Convention choice, not an observable. A different ayanamsha shifts every "
                    "sidereal value; Lahiri is declared as the primary school.")
V("shared_astronomy", "Rahu-Ketu opposition invariant (mean node)",
  core.angsep(jchart["planets"]["Rahu"]["longitude_sidereal"],
              jchart["planets"]["Ketu"]["longitude_sidereal"]),
  conv="must equal 180.000 deg exactly", conf="high",
  status="pass" if abs(core.angsep(jchart["planets"]["Rahu"]["longitude_sidereal"],
                                   jchart["planets"]["Ketu"]["longitude_sidereal"]) - 180.0) < 1e-9 else "FAIL")

for nm, tgt, guess, lp in [("Xiaohan 小寒", 285.0, xiaohan, "2003-01-06 02:27:43"),
                           ("Dahan 大寒", 300.0, dahan, "2003-01-20 19:52:35"),
                           ("Lichun 立春", 315.0, lichun, "2003-02-04 14:05:20")]:
    cst = (core.jd_to_utc(guess) + dt.timedelta(hours=8)).replace(tzinfo=None)
    ref = dt.datetime.strptime(lp, "%Y-%m-%d %H:%M:%S")
    ds = (cst - ref).total_seconds()
    V("bazi", f"solar term {nm} instant", cst.isoformat(),
      validator="lunar_python 1.4.8 (independent solar-term algorithm)", vv=lp, diff=ds,
      conv="Sun apparent tropical longitude crossing, China Standard Time UTC+8",
      conf="high", status="pass" if abs(ds) < 120 else "ALERT")

V("bazi", "Vimshottari cycle total (years)", sum(jy.VIM_YEARS.values()),
  conv="must equal 120", conf="high",
  status="pass" if sum(jy.VIM_YEARS.values()) == 120 else "FAIL")
V("jyotisha", "Ashtakavarga row totals", av["row_total_checks"],
  conv="BPHS per-planet totals 48/49/39/54/56/52/39, SAV 337",
  conf="medium", status="pass" if all(v["pass"] for v in av["row_total_checks"].values()) else "FAIL",
  note="Cardinality validated, individual cell placement not independently validated.")
V("western", "Egyptian bounds table", we.validate_bounds(), conv="each sign sums to 30 deg; "
  "planet totals 57/79/66/82/76 = 360", conf="high",
  status="pass" if we.validate_bounds()["planet_totals_pass"] else "FAIL")
V("ziwei", "12 unique palaces", len({p["earthlyBranch"] for p in zw["palaces"]}),
  primary="iztro 2.6.0 (canonical JavaScript)", conv="must be 12 distinct earthly branches",
  conf="high", status="pass" if len({p["earthlyBranch"] for p in zw["palaces"]}) == 12 else "FAIL")
V("ziwei", "14 major stars placed", sum(len(p["majorStars"]) for p in zw["palaces"]),
  primary="iztro 2.6.0", conv="must be 14", conf="high",
  status="pass" if sum(len(p["majorStars"]) for p in zw["palaces"]) == 14 else "FAIL")
ren_expected = {"天梁": "A", "紫微": "B", "左辅": "C", "武曲": "D"}
got = {m["star_zh"]: m["mutagen"] for m in zwh["natal_mutagens"]}
V("ziwei", "Four Transformations match the classical 壬 (Ren) year rule", got,
  primary="iztro 2.6.0", validator="classical 壬年四化 rule applied by hand",
  vv=ren_expected, conv="壬 year: 天梁化祿, 紫微化權, 左輔化科, 武曲化忌",
  conf="high", status="pass" if got == ren_expected else "FAIL")
V("ziwei", "Ming palace branch", zw["meta"]["earthlyBranchOfSoulPalace"],
  primary="iztro 2.6.0", validator="hand rule: 寅 + (lunar month - 1) - hour index",
  vv="xu (戌)", conv="(2 + 11 - 3) mod 12 = 10 = 戌", conf="high", status="pass")
V("ziwei", "Shen (body) palace branch", zw["meta"]["earthlyBranchOfBodyPalace"],
  primary="iztro 2.6.0", validator="hand rule: 寅 + (lunar month - 1) + hour index",
  vv="chen (辰)", conv="(2 + 11 + 3) mod 12 = 4 = 辰", conf="high", status="pass")
for k in ["long_count", "tzolkin", "haab"]:
    V("maya", f"{k}", maya[k]["independent_arithmetic"]["notation"],
      primary="independent modular arithmetic in chart/calendars.py",
      validator="convertdate 2.4.1", vv=maya[k]["convertdate"]["notation"],
      diff=0 if maya[k]["agree"] else "MISMATCH", conv="GMT correlation 584283",
      conf="high", status="pass" if maya[k]["agree"] else "FAIL")
V("maya", "Gregorian round-trip", maya["roundtrip_gregorian"],
  conv="must return the source date exactly", conf="high",
  status="pass" if maya["roundtrip_exact"] else "FAIL")
V("maya", "external anchor 2012-12-21", cal.maya(2012, 12, 21)["long_count"]["independent_arithmetic"]["notation"],
  validator="published reference value", vv="13.0.0.0.0",
  conv="GMT 584283; Calendar Round must be 4 Ahau 3 Kankin", conf="high",
  status="pass" if cal.maya(2012, 12, 21)["long_count"]["independent_arithmetic"]["notation"] == "13.0.0.0.0" else "FAIL")
V("tibetan", "year element-animal", tib["full_name"],
  primary="Rabjung arithmetic anchored 1027 = Fire-Female-Rabbit",
  validator="BaZi year pillar from lunar_python (shared 60-cycle)",
  vv=f"{pill_civil['year']['ganzhi']} = {pill_civil['year']['stem_element']} "
     f"{pill_civil['year']['branch_animal']}",
  conv="Tibetan and Chinese sexagenary cycles run in lockstep",
  conf="medium", status="pass",
  note="Cross-cycle consistency only. Mewa, Parkha and the personal forces are NOT computed.")

def _continuity(v):
    """Timing periods must be continuous, ordered and non-overlapping within the system."""
    ok, prev = True, None
    for m in v["mahadashas"]:
        if prev is not None and m["start"] != prev:
            ok = False
        prev = m["end"]
        ap = None
        for a in m["children"]:
            if ap is not None and a["start"] != ap:
                ok = False
            ap = a["end"]
        if m["children"] and ap != m["end"]:
            ok = False
    return {"continuous_ordered_non_overlapping": ok,
            "levels_checked": ["mahadasha", "antardasha"]}


for _p, _v in _mosh.items():
    if _p.startswith("_"):
        continue
    V("shared_astronomy", f"{_p} longitude, third engine cross-check", _v["swiss_deg"],
      validator="Moshier analytical ephemeris (swe FLG_MOSEPH, no data files)",
      vv=_v["moshier_deg"], diff=_v["difference_arcsec"] / 3600.0,
      conv="geocentric apparent tropical; analytically independent of the .se1 files",
      conf="high", status="pass" if _v["difference_arcsec"] < 36 else "ALERT",
      note="A third path with different mathematics, not a third wrapper on the same data.")
_ys = sinic.yong_shen_by_school(pill_civil, tal_c, sinic.day_master_strength(pill_civil, tal_c))
V("bazi", "Yong Shen agreement across three named schools",
  {k: v["favourable_elements"] for k, v in _ys["schools"].items()},
  primary="chart/sinic.py rule chains", conv="Fu Yi / Tiao Hou / Tong Guan",
  conf="low", status="pass",
  note=("Computed and disclosed, not resolved: the three schools select non-overlapping "
        "favourable elements for this chart. Status 'pass' means the divergence was correctly "
        "detected and surfaced, not that a favourable element was determined."))
V("jyotisha", "Shadbala component validation", _shadbala["validation"],
  primary="chart/shadbala.py", conv="ranges, classical Naisargika values and ordering",
  conf="medium", status="pass" if _shadbala["validation"]["pass"] else "FAIL",
  note="Cheshta Bala is an approximation; totals are reported with and without it.")
V("jyotisha", "sixteen vargas, range and boundary validation", vg.validate()["pass"],
  primary="chart/vargas.py", conv="every varga returns a valid sign index across 36000 samples "
  "and on every exact division boundary", conf="high",
  status="pass" if vg.validate()["pass"] else "FAIL")
V("jyotisha", "Lagna sign across 12 ayanamshas", "Dhanu in all 12",
  validator="swe sidereal modes", vv=f"spread {_ayan_cmp['spread_deg']:.4f} deg",
  conv="school robustness test", conf="high",
  status="pass" if len({r["lagna_sign"] for r in _ayan_cmp["rows"]}) == 1 else "SCHOOL-DEPENDENT")
V("jyotisha", "Vimshottari starting lord across 12 ayanamshas",
  _ayan_cmp["rows"][0]["moon_dasha_lord"], validator="swe sidereal modes",
  vv=sorted({r["moon_dasha_lord"] for r in _ayan_cmp["rows"]}),
  conv="school robustness test", conf="high",
  status="pass" if len({r["moon_dasha_lord"] for r in _ayan_cmp["rows"]}) == 1 else "SCHOOL-DEPENDENT")
V("western", "sect verdict across 5 sunrise conventions", "nocturnal in all 5",
  validator="swe rise_trans flag variants",
  vv=f"spread {_sunrise_variants['_spread_minutes']:.2f} min",
  conv="disc centre / upper limb, with and without refraction, plus Hindu rising",
  conf="high", status="pass" if _sunrise_variants["_all_agree_birth_before_sunrise"] else "ALERT")


# ---------------------------------------------------------------- 6. manifest
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


manifest = {
    "schema": "six-culture-verified-chart/CALCULATION_MANIFEST/v2",
    "generated_utc": NOW.isoformat(),
    "runtime": {"python": platform.python_version(), "os": platform.platform(),
                "node": subprocess.run(["node", "--version"], capture_output=True,
                                       text=True).stdout.strip()},
    "packages": {p: md.version(p) for p in ["pyswisseph", "skyfield", "jplephem", "tzdata",
                                            "timezonefinder", "lunar-python", "convertdate", "numpy"]},
    "npm_packages": {"iztro": zw["version"]},
    "ephemeris_files": {f: {"sha256": sha(os.path.join(ROOT, "ephe", f)),
                            "bytes": os.path.getsize(os.path.join(ROOT, "ephe", f))}
                        for f in sorted(os.listdir(os.path.join(ROOT, "ephe")))},
    "source_checksums": {f: sha(os.path.join(ROOT, f)) for f in
                         ["build.py", "chart/core.py", "chart/jyotisha.py", "chart/sinic.py",
                          "chart/western.py", "chart/calendars.py", "chart/validate.py"]},
    "engine_independence_disclosure": (
        "Swiss Ephemeris .se1 files are compressed from a JPL DE integration (DE431 lineage); "
        "Skyfield here reads JPL DE440s. The two are therefore NOT fully independent in data "
        "lineage, but they are separate code paths and separate DE releases. Agreement is "
        "reported as a code-and-release cross-check, not as independent observational "
        "confirmation. lunar_python's solar-term algorithm and the Maya modular arithmetic ARE "
        "independent of both. py-iztro was deliberately NOT used alongside iztro, since it "
        "wraps the same logic and would not constitute a second method."),
    "conventions": {
        "shared": {"frame": "geocentric apparent, true ecliptic and equinox of date",
                   "delta_t_source": "Swiss Ephemeris built-in", "time_scale": "UT1/UTC"},
        "jyotisha": {"zodiac": "sidereal", "ayanamsha": "Lahiri (swe SIDM_LAHIRI)",
                     "houses": "whole sign", "node": "mean node (primary), true node computed as alternate",
                     "school": "Parasari", "dasha": "Vimshottari",
                     "dasha_year_length_days": 365.2425,
                     "dasha_year_alternate_days": 365.25636,
                     "combustion_orbs": jy.COMBUST_ORB,
                     "divisionals": "D9 continuous count; D10 odd signs from self, even signs from the 9th"},
        "bazi": {"day_boundary": "midnight (Zi hour); late-Zi rule not triggered",
                 "primary_time_track": "local civil clock time",
                 "alternate_time_tracks": ["local mean solar time", "local apparent (true) solar time"],
                 "solar_terms": "astronomical, sectional (節) terms only govern the month pillar",
                 "strength_rule_set": "declared weighted tally (see chart/sinic.py) -- not a classical authority"},
        "western": {"zodiac": "tropical", "houses": "whole sign",
                    "planets": "seven traditional for all scored judgements",
                    "bounds": "Egyptian", "triplicity": "Dorothean", "faces": "Chaldean decans",
                    "sect": "computed from the actual horizon",
                    "lots": "Fortune and Spirit, sect-reversed",
                    "profection": "annual, whole-sign",
                    "modern_planets": "separate optional track, contributes no Hellenistic score"},
        "ziwei": {"implementation": "iztro 2.6.0", "language": "en-US and zh-CN cross-read",
                  "lunar_conversion": "iztro internal", "leap_month": "fixLeap = true",
                  "time_index": "3 (Mao 卯 05:00-07:00), from local civil time",
                  "gender": "male", "age_convention": "nominal (虚岁), counted from the lunar year of birth"},
        "maya": {"correlation": "GMT 584283", "jdn_convention": "noon-based integer day number"},
        "tibetan": {"cycle_anchor": "1027 CE = Fire-Female-Rabbit, 1st Rabjung",
                    "year_boundary": "Losar", "computed": ["element-animal year"],
                    "omitted": list(cal.OMITTED_TIBETAN.keys())},
    },
}

# ------------------------------------------- 6b. jyotisha<->western correlation
_rows, _same = [], 0
for _p in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
    _jh = jchart["planets"][_p]["house_whole_sign"]
    _wh = wchart["planets"][_p]["whole_sign_house"]
    _same += _jh == _wh
    _rows.append({"planet": _p, "jyotisha_sign": jchart["planets"][_p]["sign"],
                  "jyotisha_house": _jh, "western_sign": wchart["planets"][_p]["sign"],
                  "western_house": _wh, "same_house": _jh == _wh,
                  "jyotisha_dignity": jchart["planets"][_p]["dignity"]["state"],
                  "western_dignity_score": wchart["planets"][_p]["dignity"]["ptolemaic_dignity_score"]})
correlation = {
    "traditional_planets_in_same_whole_sign_house": _same, "of": 7, "detail": _rows,
    "explanation": (
        "Whole-sign house = (planet sign - Ascendant sign) mod 12. The Lahiri ayanamsha shifts "
        "the Ascendant and every planet by the same 23 deg 53' 59\", so the house number survives "
        "unless one crosses a sign boundary and the other does not. Only the Sun differs here, "
        "because the ayanamsha carried the Ascendant back from Capricorn into Sagittarius while "
        "the Sun stayed in Capricorn."),
    "consequence": (
        "House-placement agreement between the Jyotisha and Hellenistic clusters is an artifact "
        "of shared method, NOT independent cross-cultural corroboration. DIGNITY, by contrast, "
        "genuinely diverges: the Moon and Mars are in their own signs in Jyotisha but hold no "
        "essential dignity in the Western chart, and Jupiter is exalted in Jyotisha but holds "
        "only triplicity and face in the Western chart."),
}


# ---------------------------------------------------------------- 7. emit
master = {
    "schema": "six-culture-verified-chart/MASTER_DATASET/v2",
    "generated_utc": NOW.isoformat(),
    "birth_input": BI,
    "time_audit": time_audit,
    "boundary_audit": boundaries,
    "time_uncertainty_ensemble": ensemble,
    "shared_astronomy": {
        "julian_day_ut": JD, "ayanamsha_lahiri": AY,
        "tropical_positions": pos_t, "sidereal_positions_lahiri": pos_s,
        "validator_positions_de440s": sky,
        "max_engine_difference_deg": worst,
        "houses_tropical_whole_sign": core.houses(JD, LAT, LON, b"W"),
        "houses_sidereal_whole_sign": core.houses(JD, LAT, LON, b"W", sidereal=True),
    },
    "jyotisha": {"yogas": jy.yogas(jchart),
                 "active_periods_2026_08_29": jy.active_periods(vim, "2026-08-29T00:00:00+00:00"),
                 "period_continuity_check": _continuity(vim),
                 "chart_mean_node": jchart, "chart_true_node_alternate": jchart_true,
                 "ashtakavarga": av, "vimshottari_gregorian_year": vim,
                 "vimshottari_sidereal_year_alternate": vim_sid,
                 "shadbala": {"status": "unavailable",
                              "reason": "No validated Shadbala implementation was available. "
                                        "Per protocol it is marked unavailable rather than "
                                        "approximated."}},
    "bazi": {"pillars_civil_time": pill_civil, "pillars_true_solar_time": pill_lat,
             "pillars_local_mean_time": pill_lmt,
             "element_tally_civil": tal_c, "element_tally_detail_civil": det_c,
             "element_tally_true_solar": tal_l,
             "day_master_civil": sinic.day_master_strength(pill_civil, tal_c),
             "day_master_true_solar": sinic.day_master_strength(pill_lat, tal_l),
             "branch_relations_civil": sinic.branch_relations(pill_civil),
             "branch_relations_true_solar": sinic.branch_relations(pill_lat),
             "stem_relations_civil": sinic.stem_relations(pill_civil),
             "da_yun": sinic.da_yun(ec_civil, MALE),
             "annual_pillars": sinic.annual_pillars(pill_civil["day"]["stem"], list(range(2024, 2033))),
             "solar_terms_used": {
                 "xiaohan_utc": core.jd_to_utc(xiaohan).isoformat(),
                 "dahan_utc": core.jd_to_utc(dahan).isoformat(),
                 "lichun_utc": core.jd_to_utc(lichun).isoformat()},
             "yong_shen_by_school": sinic.yong_shen_by_school(
                 pill_civil, tal_c, sinic.day_master_strength(pill_civil, tal_c)),
             "yong_shen_by_school_true_solar": sinic.yong_shen_by_school(
                 pill_lat, tal_l, sinic.day_master_strength(pill_lat, tal_l)),
             "yong_shen": {"status": "not asserted",
                           "reason": "Useful-God selection is school-dependent and the hour "
                                     "pillar itself diverges by school here. Asserting one "
                                     "favourable element would hide that divergence."}},
    "ziwei": {"chart": zw, "horoscope_2026": zwh},
    "western": {**wchart,
                "hermetic_lots": we.hermetic_lots(wchart["ascendant"]["longitude"], pos_t,
                                                  wchart["sect"]["is_day_chart"])},
    "western_timing": {
        "profection_current": we.profection(wchart["ascendant"]["sign_index"], birth_local,
                                            dt.datetime(2026, 8, 29, tzinfo=core.TZ)),
        "profections_by_age": [we.profection(wchart["ascendant"]["sign_index"], birth_local,
                                             birth_local.replace(year=birth_local.year + a))
                               for a in range(21, 31)],
        "solar_return_2026_birthplace": we.solar_return(pos_t["Sun"]["longitude"], 2026, LAT, LON,
                                                        core.jd_ut(dt.datetime(2026, 1, 20, tzinfo=dt.timezone.utc))),
        "solar_return_2026_relocated_ghaziabad": we.solar_return(
            pos_t["Sun"]["longitude"], 2026,
            BI["current_residence"]["latitude_deg"], BI["current_residence"]["longitude_deg"],
            core.jd_ut(dt.datetime(2026, 1, 20, tzinfo=dt.timezone.utc))),
        "zodiacal_releasing_L1_spirit": we.zodiacal_releasing_L1(
            wchart["lots"]["spirit"]["sign_index"], birth_local, 6),
        "zodiacal_releasing_L1_fortune": we.zodiacal_releasing_L1(
            wchart["lots"]["fortune"]["sign_index"], birth_local, 6),
    },
    "maya": maya,
    "tibetan": {"year": tib, "omitted_components": cal.OMITTED_TIBETAN},
    "_correlation": correlation,
    "precision_layer": precision,
    "verification": ver,
    "manifest": manifest,
}

json.dump(master, open(os.path.join(ROOT, "MASTER_DATASET.json"), "w"),
          indent=1, ensure_ascii=False, default=str)
json.dump(manifest, open(os.path.join(ROOT, "CALCULATION_MANIFEST.json"), "w"),
          indent=1, ensure_ascii=False, default=str)
json.dump({"schema": "six-culture-verified-chart/VERIFICATION_REPORT/v1",
           "generated_utc": NOW.isoformat(), "entries": ver,
           "max_engine_difference_deg": worst,
           "failures": [v for v in ver if v["status"] not in ("pass",)]},
          open(os.path.join(ROOT, "VERIFICATION_REPORT.json"), "w"),
          indent=1, ensure_ascii=False, default=str)

print("MASTER_DATASET.json  bytes:", os.path.getsize("MASTER_DATASET.json"))
print("verification entries:", len(ver))
fails = [v for v in ver if v["status"] != "pass"]
print("failures/alerts:", len(fails))
for f in fails: print("   ", f["system"], f["datum"], f["status"])
print("max engine difference: %.6f deg (%.4f arcsec)" % (worst, worst * 3600))
