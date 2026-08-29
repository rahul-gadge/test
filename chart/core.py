"""Core time audit and dual-engine astronomy for the six-culture chart.

Engine A (primary)  : Swiss Ephemeris via pyswisseph, sepl_18/semo_18/seas_18.se1
Engine B (validator): JPL DE440s via jplephem/Skyfield

The two engines share ancestry (Swiss Ephemeris files are compressed from a JPL
DE integration) but are different code paths and different DE releases. That
partial independence is disclosed in the verification report; it is NOT claimed
as fully independent corroboration.
"""
import datetime as dt
import json
import math
import os
from zoneinfo import ZoneInfo

import swisseph as swe

EPHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ephe")
swe.set_ephe_path(EPHE)

TZ = ZoneInfo("Asia/Kolkata")
UTC = dt.timezone.utc

# ---------------------------------------------------------------- time

def local_to_utc(y, m, d, hh, mm, ss=0):
    loc = dt.datetime(y, m, d, hh, mm, ss, tzinfo=TZ)
    return loc, loc.astimezone(UTC)


def jd_ut(u):
    return swe.julday(u.year, u.month, u.day,
                      u.hour + u.minute / 60 + u.second / 3600 + u.microsecond / 3.6e9)


def jd_to_utc(j):
    y, m, d, h = swe.revjul(j)
    day = dt.datetime(y, m, d, tzinfo=UTC)
    return day + dt.timedelta(hours=h)


def jd_to_local(j):
    return jd_to_utc(j).astimezone(TZ)


def iso(x):
    return x.isoformat()


# ------------------------------------------------------- solar time

def solar_times(j, lon):
    """Local mean and local apparent solar time as fractions of a day (UT-based)."""
    e = swe.time_equ(j)                    # LAT - LMT, in days
    eot_days = e[1] if isinstance(e, (tuple, list)) else e
    lmt_jd = j + lon / 360.0
    lat_jd = lmt_jd + eot_days
    return {
        "equation_of_time_minutes": eot_days * 1440.0,
        "lmt_jd": lmt_jd,
        "lat_jd": lat_jd,
        "lmt_clock": _clock(lmt_jd),
        "lat_clock": _clock(lat_jd),
    }


def _clock(j):
    frac = (j + 0.5) % 1.0
    secs = frac * 86400.0
    h = int(secs // 3600); mi = int((secs % 3600) // 60); s = secs % 60
    return f"{h:02d}:{mi:02d}:{s:06.3f}"


# ------------------------------------------------------- Swiss engine

BODIES = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mercury": swe.MERCURY, "Venus": swe.VENUS,
    "Mars": swe.MARS, "Jupiter": swe.JUPITER, "Saturn": swe.SATURN,
    "Uranus": swe.URANUS, "Neptune": swe.NEPTUNE, "Pluto": swe.PLUTO,
    "MeanNode": swe.MEAN_NODE, "TrueNode": swe.TRUE_NODE,
}

FLG_TROP = swe.FLG_SWIEPH | swe.FLG_SPEED
FLG_CMP = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_NONUT   # mean equinox of date, for engine comparison


def swe_positions(j, flags=FLG_TROP, sidereal=False, ayan=swe.SIDM_LAHIRI):
    if sidereal:
        swe.set_sid_mode(ayan)
        flags = flags | swe.FLG_SIDEREAL
    out = {}
    for name, code in BODIES.items():
        xx, rf = swe.calc_ut(j, code, flags)
        out[name] = {
            "longitude": xx[0], "latitude": xx[1], "distance_au": xx[2],
            "speed_long": xx[3], "retrograde": xx[3] < 0, "flags_returned": rf,
        }
    # Ketu = Rahu + 180
    for nn in ("MeanNode", "TrueNode"):
        k = out[nn].copy()
        k["longitude"] = (k["longitude"] + 180.0) % 360.0
        k["latitude"] = -k["latitude"]
        out["Ketu_" + nn] = k
    return out


def ayanamsha(j, ayan=swe.SIDM_LAHIRI):
    swe.set_sid_mode(ayan)
    return swe.get_ayanamsa_ut(j)


def houses(j, lat, lon, system=b"W", sidereal=False, ayan=swe.SIDM_LAHIRI):
    if sidereal:
        swe.set_sid_mode(ayan)
        cusps, ascmc = swe.houses_ex(j, lat, lon, system, swe.FLG_SIDEREAL)
    else:
        cusps, ascmc = swe.houses_ex(j, lat, lon, system)
    return {"cusps": list(cusps), "asc": ascmc[0], "mc": ascmc[1],
            "armc": ascmc[2], "vertex": ascmc[3]}


def sunrise_sunset_for_local_day(j, lat, lon, elev=340.0):
    """Sunrise and sunset of the local civil day containing j."""
    loc = jd_to_local(j)
    midnight = dt.datetime(loc.year, loc.month, loc.day, 0, 0, tzinfo=TZ)
    j0 = jd_ut(midnight.astimezone(UTC))
    _, tr = swe.rise_trans(j0, swe.SUN, swe.CALC_RISE | swe.BIT_DISC_CENTER, (lon, lat, elev))
    _, ts = swe.rise_trans(j0, swe.SUN, swe.CALC_SET | swe.BIT_DISC_CENTER, (lon, lat, elev))
    _, tpr = swe.rise_trans(j0 - 1.0, swe.SUN, swe.CALC_RISE | swe.BIT_DISC_CENTER, (lon, lat, elev))
    _, tps = swe.rise_trans(j0 - 1.0, swe.SUN, swe.CALC_SET | swe.BIT_DISC_CENTER, (lon, lat, elev))
    return {"sunrise_jd": tr[0], "sunset_jd": ts[0],
            "prev_sunrise_jd": tpr[0], "prev_sunset_jd": tps[0]}


# ------------------------------------------------------- solar terms

def solar_longitude_crossing(target_deg, jd_guess, nonut=False):
    """Instant (JD UT) when the Sun's apparent tropical longitude equals target."""
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED | (swe.FLG_NONUT if nonut else 0)
    j = jd_guess
    for _ in range(60):
        xx, _ = swe.calc_ut(j, swe.SUN, flags)
        diff = (xx[0] - target_deg + 180.0) % 360.0 - 180.0
        if abs(diff) < 1e-9:
            break
        j -= diff / xx[3]
    return j


# ------------------------------------------------------- zodiac helpers

SIGNS_TROP = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGNS_SKT = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
             "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"]


def sign_of(lon):
    return int(lon // 30) % 12


def deg_in_sign(lon):
    return lon % 30.0


def dms(x):
    d = int(x); m_ = (x - d) * 60; m = int(m_); s = (m_ - m) * 60
    return f"{d}°{m:02d}'{s:04.1f}\""


def fmt(lon, skt=False):
    s = sign_of(lon)
    nm = SIGNS_SKT[s] if skt else SIGNS_TROP[s]
    return f"{nm} {dms(deg_in_sign(lon))}"


def angsep(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)
