"""Maya calendar (independently round-tripped) and Tibetan year element-animal."""
from convertdate import mayan, julianday

TZOLKIN_NAMES = ["Imix", "Ik", "Akbal", "Kan", "Chicchan", "Cimi", "Manik", "Lamat",
                 "Muluc", "Oc", "Chuen", "Eb", "Ben", "Ix", "Men", "Cib",
                 "Caban", "Etznab", "Cauac", "Ahau"]
HAAB_MONTHS = ["Pop", "Wo", "Sip", "Sotz", "Sek", "Xul", "Yaxkin", "Mol", "Chen",
               "Yax", "Sak", "Keh", "Mak", "Kankin", "Muwan", "Pax", "Kayab", "Kumku", "Wayeb"]
CORRELATION_GMT = 584283


def _same_name(a, b):
    """Compare day/month names across orthographies (Caban vs Kab'an, Muwan vs Muwan')."""
    norm = lambda x: x.lower().replace("'", "").replace("k", "c").replace("j", "h")
    return norm(a) == norm(b)


def maya(y, m, d, correlation=CORRELATION_GMT):
    # from_gregorian returns the JD at midnight (x.5); the Maya day number is the
    # noon-based integer JDN, hence +0.5 before truncation.
    jdn = int(julianday.from_gregorian(y, m, d) + 0.5)
    days = jdn - correlation

    # --- independent arithmetic (this module), not convertdate ---
    lc = []
    for unit in (144000, 7200, 360, 20, 1):
        lc.append(days // unit); days %= unit
    days = jdn - correlation
    tz_num = (days + 4 - 1) % 13 + 1
    tz_name = TZOLKIN_NAMES[(days + 19) % 20]
    haab_pos = (days + 17 * 20 + 8) % 365
    hb_month = HAAB_MONTHS[haab_pos // 20]
    hb_day = haab_pos % 20

    # --- convertdate as the second implementation ---
    cd_lc = mayan.from_gregorian(y, m, d)
    cd_jd = mayan.to_jd(*cd_lc)
    cd_tz = mayan.to_tzolkin(cd_jd)
    cd_hb = mayan.to_haab(cd_jd)
    roundtrip = mayan.to_gregorian(*cd_lc)

    return {
        "correlation_constant": correlation,
        "correlation_name": "GMT (Goodman-Martinez-Thompson) 584283",
        "julian_day_number": jdn,
        "long_count": {
            "independent_arithmetic": {"baktun": lc[0], "katun": lc[1], "tun": lc[2],
                                       "uinal": lc[3], "kin": lc[4],
                                       "notation": ".".join(str(x) for x in lc)},
            "convertdate": {"baktun": cd_lc[0], "katun": cd_lc[1], "tun": cd_lc[2],
                            "uinal": cd_lc[3], "kin": cd_lc[4],
                            "notation": ".".join(str(x) for x in cd_lc)},
            "agree": tuple(lc) == tuple(cd_lc),
        },
        "tzolkin": {
            "independent_arithmetic": {"number": tz_num, "name": tz_name,
                                       "notation": f"{tz_num} {tz_name}"},
            "convertdate": {"number": cd_tz[0], "name": cd_tz[1],
                            "notation": f"{cd_tz[0]} {cd_tz[1]}"},
            "agree": (tz_num == cd_tz[0] and _same_name(tz_name, cd_tz[1])),
            "orthography_note": ("convertdate uses a modernised Mayan orthography (Kab'an); this "
                                 "module uses the older Thompson spelling (Caban). Same day sign."),
        },
        "haab": {
            "independent_arithmetic": {"day": hb_day, "month": hb_month,
                                       "notation": f"{hb_day} {hb_month}"},
            "convertdate": {"day": cd_hb[0], "month": cd_hb[1],
                            "notation": f"{cd_hb[0]} {cd_hb[1]}"},
            "agree": (hb_day == cd_hb[0] and _same_name(hb_month, cd_hb[1])),
        },
        "calendar_round": f"{tz_num} {tz_name} {hb_day} {hb_month}",
        "roundtrip_gregorian": list(roundtrip),
        "roundtrip_exact": tuple(roundtrip) == (y, m, d),
        "interpretation_policy": (
            "This is a calendrical conversion only. No day-sign personality meaning is asserted. "
            "Modern internet 'Mayan zodiac' personality lists are not classical Maya sources and "
            "are excluded. Maya data contributes no domain vote."
        ),
    }


# --- Tibetan year element-animal (60-year cycle, Rabjung reckoning) ---
TIB_ELEMENTS = ["Wood", "Fire", "Earth", "Iron", "Water"]
TIB_ANIMALS = ["Mouse", "Ox", "Tiger", "Rabbit", "Dragon", "Snake",
               "Horse", "Sheep", "Monkey", "Bird", "Dog", "Pig"]
RABJUNG_EPOCH = 1027   # year 1 of the 1st Rabjung = Fire-Rabbit


def tibetan_year(losar_gregorian_year):
    """Element-animal for the Tibetan year whose Losar fell in the given Gregorian year.

    Anchored on 1027 CE = Fire-Female-Rabbit (me mo yos), year 1 of the 1st Rabjung.
    The Tibetan 60-year cycle runs in lockstep with the Chinese sexagenary cycle, so
    this is cross-checked against the BaZi year pillar in the verification report.
    """
    n = losar_gregorian_year - RABJUNG_EPOCH
    k = (3 + n) % 10          # stem index, 1027 anchored on Ding (index 3)
    el_idx = k // 2
    an_idx = (3 + n) % 12     # 1027 anchored on Rabbit (branch index 3)
    yang = (k % 2 == 0)
    return {
        "element": TIB_ELEMENTS[el_idx],
        "animal": TIB_ANIMALS[an_idx],
        "year_polarity": "male / yang (pho)" if yang else "female / yin (mo)",
        "rabjung_cycle": n // 60 + 1,
        "year_within_rabjung": n % 60 + 1,
        "anchor": "1027 CE = Fire-Female-Rabbit (me mo yos), year 1 of the 1st Rabjung",
        "name": f"{TIB_ELEMENTS[el_idx]} {TIB_ANIMALS[an_idx]}",
        "full_name": ("%s %s %s" % (TIB_ELEMENTS[el_idx], "Male" if yang else "Female",
                                    TIB_ANIMALS[an_idx])),
    }


OMITTED_TIBETAN = {
    "mewa": "omitted - no validated lineage-specific implementation or anchor available",
    "parkha": "omitted - no validated lineage-specific implementation or anchor available",
    "la_force": "omitted - anchor formulas not validated",
    "srog_life_force": "omitted - anchor formulas not validated",
    "lu_body_force": "omitted - anchor formulas not validated",
    "wangthang_power": "omitted - anchor formulas not validated",
    "lungta_windhorse": "omitted - anchor formulas not validated",
    "annual_relations_and_obstacles": "omitted - depends on the omitted personal-force anchors",
    "policy": ("Per protocol 4G, unvalidated Tibetan components are omitted rather than guessed. "
               "Only the element-animal year is retained, as a limited symbolic overlay that "
               "contributes no life-domain vote."),
}
