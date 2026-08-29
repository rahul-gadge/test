"""Panchanga: the five limbs -- tithi, vara, nakshatra, yoga, karana."""
from . import core
import swisseph as swe

TITHI_NAMES = ["Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashthi","Saptami",
               "Ashtami","Navami","Dashami","Ekadashi","Dvadashi","Trayodashi","Chaturdashi"]
YOGA_NAMES = ["Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma",
              "Dhriti","Shula","Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra",
              "Siddhi","Vyatipata","Variyana","Parigha","Shiva","Siddha","Sadhya","Shubha",
              "Shukla","Brahma","Indra","Vaidhriti"]
KARANA_MOVABLE = ["Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti"]
KARANA_FIXED = ["Shakuni","Chatushpada","Naga","Kimstughna"]
VARA_NAMES = ["Ravivara (Sunday)","Somavara (Monday)","Mangalavara (Tuesday)","Budhavara (Wednesday)",
              "Guruvara (Thursday)","Shukravara (Friday)","Shanivara (Saturday)"]
VARA_LORDS = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]


def karana_of(index_1_to_60):
    """60 half-tithis per lunar month. 1 is Kimstughna; 58-60 are the three fixed karanas."""
    n = index_1_to_60
    if n == 1:
        return {"index": n, "name": "Kimstughna", "type": "fixed"}
    if n >= 58:
        return {"index": n, "name": KARANA_FIXED[n - 58], "type": "fixed"}
    return {"index": n, "name": KARANA_MOVABLE[(n - 2) % 7], "type": "movable"}


def build(jd, lat, lon_geo, sun_sid, moon_sid, sunrise_jd, birth_local):
    diff = (moon_sid - sun_sid) % 360.0
    tithi_f = diff / 12.0
    tithi_i = int(tithi_f) + 1
    paksha = "Shukla (waxing)" if tithi_i <= 15 else "Krishna (waning)"
    tname = ("Purnima" if tithi_i == 15 else
             ("Amavasya" if tithi_i == 30 else TITHI_NAMES[(tithi_i - 1) % 15]))

    yoga_f = ((sun_sid + moon_sid) % 360.0) / (360.0 / 27)
    yoga_i = int(yoga_f) + 1

    karana_i = int(diff / 6.0) + 1

    # Vara begins at sunrise, not midnight.
    vara_idx = int((sunrise_jd + 1.5) % 7)
    if jd < sunrise_jd:
        vara_idx = (vara_idx - 1) % 7

    return {
        "tithi": {"index": tithi_i, "name": tname, "paksha": paksha,
                  "elapsed_fraction": tithi_f - int(tithi_f),
                  "sun_moon_elongation_deg": diff,
                  "degrees_to_next_tithi": 12.0 - (diff % 12.0),
                  "rule": "tithi = floor((Moon - Sun) / 12 deg) + 1, sidereal longitudes"},
        "vara": {"index": vara_idx, "name": VARA_NAMES[vara_idx], "lord": VARA_LORDS[vara_idx],
                 "civil_weekday": birth_local.strftime("%A"),
                 "differs_from_civil": VARA_NAMES[vara_idx].split()[1].strip("()") != birth_local.strftime("%A"),
                 "rule": "the Vedic day runs sunrise to sunrise; a pre-sunrise birth belongs to "
                         "the previous vara"},
        "nakshatra": {"of_moon": None},   # filled by caller from the Moon's nakshatra
        "yoga": {"index": yoga_i, "name": YOGA_NAMES[(yoga_i - 1) % 27],
                 "degrees_to_next": (360.0 / 27) - (((sun_sid + moon_sid) % 360.0) % (360.0 / 27)),
                 "rule": "yoga = floor((Sun + Moon) / 13 deg 20') + 1"},
        "karana": {**karana_of(karana_i),
                   "degrees_to_next": 6.0 - (diff % 6.0),
                   "rule": "karana = floor((Moon - Sun) / 6 deg) + 1, half-tithis"},
    }


def sunrise_variants(jd, lat, lon_geo, elev):
    """Sunrise under the conventions that different traditions actually use.

    The choice moves the sect boundary and the Vedic day boundary, so it is reported
    rather than silently fixed.
    """
    out = {}
    for name, flags in [
        ("disc_centre_with_refraction", swe.BIT_DISC_CENTER),
        ("upper_limb_with_refraction", 0),
        ("disc_centre_no_refraction", swe.BIT_DISC_CENTER | swe.BIT_NO_REFRACTION),
        ("upper_limb_no_refraction", swe.BIT_NO_REFRACTION),
        ("hindu_sunrise_upper_limb", swe.BIT_HINDU_RISING),
    ]:
        import datetime as dt
        loc = core.jd_to_local(jd)
        midnight = dt.datetime(loc.year, loc.month, loc.day, 0, 0, tzinfo=core.TZ)
        j0 = core.jd_ut(midnight.astimezone(dt.timezone.utc))
        _, tr = swe.rise_trans(j0, swe.SUN, swe.CALC_RISE | flags, (lon_geo, lat, elev))
        out[name] = {"jd": tr[0], "local": core.jd_to_local(tr[0]).isoformat(),
                     "minutes_from_birth": (jd - tr[0]) * 1440.0,
                     "birth_is_before_sunrise": jd < tr[0]}
    spread = max(v["jd"] for v in out.values()) - min(v["jd"] for v in out.values())
    out["_spread_minutes"] = spread * 1440.0
    out["_all_agree_birth_before_sunrise"] = len({v["birth_is_before_sunrise"]
                                                  for k, v in out.items() if not k.startswith("_")}) == 1
    return out
