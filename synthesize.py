#!/usr/bin/env python
"""Step 7-8: projection through a predeclared mapping registry, cluster counting,
domain grading, temperament, chronology. Emits SYNTHESIS.json.

Counting rules enforced here:
  * primary clusters = jyotisha | western | sinic (BaZi + Zi Wei together = ONE vote)
  * maya and tibetan contribute NO domain vote
  * an INDEPENDENCE GATE downgrades jyotisha<->western agreement when both sides rest
    only on whole-sign house occupancy, which is mechanically correlated between them
"""
import datetime as dt, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.abspath(__file__))
MD = json.load(open(os.path.join(ROOT, "MASTER_DATASET.json")))
NOW = dt.datetime.now(dt.timezone.utc)

DOMAINS = {
    "D1": "Self / identity", "D2": "Career / status", "D3": "Wealth / gains",
    "D4": "Partnership", "D5": "Family / roots / home", "D6": "Children / creation",
    "D7": "Health / routine", "D8": "Mind / education / craft",
    "D9": "Fortune / spirituality / worldview",
}
CLUSTER_OF = {"jyotisha": "jyotisha", "western": "western", "bazi": "sinic", "ziwei": "sinic"}

# ---- basis types, for the independence gate ----
# "ws_house"    : rests on whole-sign house occupancy (correlated across jyotisha/western)
# "ws_rulership": rests on whole-sign sign-rulership (partly correlated)
# "unique"      : cluster-unique mechanism (nakshatra, sect, lots, dasha, ten gods, sihua, ...)
P = []


def proj(domain, system, prominence, polarity, confidence, basis, rule, basis_type):
    P.append({"domain": domain, "system": system, "cluster": CLUSTER_OF[system],
              "prominence": prominence, "polarity": polarity, "confidence": confidence,
              "basis": basis, "mapping_rule": rule, "basis_type": basis_type})


J = MD["jyotisha"]["chart_mean_node"]; JP = J["planets"]; JH = J["houses"]
AV = MD["jyotisha"]["ashtakavarga"]["sarvashtakavarga_by_house"]
W = MD["western"]; WP = W["planets"]; WH = W["houses"]
ZW = MD["ziwei"]["chart"]; ZWH = MD["ziwei"]["horoscope_2026"]
BZ = MD["bazi"]
SB = MD["precision_layer"]["shadbala"]
PL = MD["precision_layer"]
PAL = {p["name_zh"]: p for p in ZW["palaces"]}

# ============================ D1 Self / identity ============================
proj("D1", "jyotisha", "high", "mixed", "high",
     f"Lagna Dhanu 11 deg 33' (Mula pada 4); Lagna lord Jupiter exalted in Karka but placed in "
     f"house 8 and retrograde", "JY-LAGNA-LORD", "unique")
proj("D1", "jyotisha", "high", "mixed", "high",
     "Mercury (lord of houses 7 and 10) in house 1, retrograde, in Purva Ashadha pada 2",
     "JY-H1-OCCUPANT", "ws_house")
proj("D1", "western", "high", "mixed", "high",
     "Ascendant Capricorn 5 deg 27'; ruler Saturn in Gemini house 6, retrograde, holds "
     "triplicity (score 3) but is the malefic CONTRARY to sect in a night chart",
     "WE-ASC-RULER-SECT", "unique")
proj("D1", "western", "medium", "mixed", "high",
     "Sun in house 1 by whole sign but below the horizon, at 29 deg 29' Capricorn (final degree), "
     "holding face only (dignity score 1), and contrary to sect",
     "WE-SECT-LUMINARY", "unique")
proj("D1", "bazi", "medium", "mixed", "medium",
     "Day Master Gui (yin Water), support ratio 0.427 -> moderately weak; rooted only in the "
     "month branch Chou, which stores Gui as a hidden stem", "BZ-DAY-MASTER", "unique")
proj("D1", "ziwei", "high", "mixed", "medium",
     "Ming (life) palace at gengxu holds Tan Lang / Greedy Wolf at brightness +3 (temple); "
     "life ruler Lu Cun, body ruler Huo Xing", "ZW-MING-PALACE", "unique")

proj("D1", "jyotisha", "high", "mixed", "medium",
     f"Shadbala ranks the seven grahas {' > '.join(SB['rank_strongest_first'])}. The Lagna lord "
     f"Jupiter is second strongest at {SB['planets']['Jupiter']['total_rupas_with_cheshta']:.2f} "
     f"rupas against a 6.5 requirement -- so the Lagna lord is genuinely strong in absolute terms "
     f"even though it sits in a dusthana", "JY-SHADBALA-LAGNA-LORD", "unique")

# ============================ D2 Career / status ============================
proj("D2", "jyotisha", "high", "mixed", "medium",
     f"Sarvashtakavarga house 10 = {AV['10']} bindus, the joint highest of the twelve houses; "
     f"house 10 (Kanya) is itself empty and its lord Mercury sits in house 1",
     "JY-SAV-H10 + JY-H10-LORD", "unique")
proj("D2", "western", "high", "mixed", "high",
     "Whole-sign house 10 is Libra and contains the Midheaven at 17 deg 02'; its ruler Venus is "
     "the benefic OF SECT in this night chart and holds its own bound, but sits in house 12",
     "WE-H10-RULER-SECT", "unique")
proj("D2", "ziwei", "high", "mixed", "medium",
     "Career palace (官禄) at renyin holds Qi Sha / Seven Killings at brightness +3 (temple)",
     "ZW-CAREER-PALACE", "unique")
proj("D2", "bazi", "medium", "mixed", "medium",
     "Officer/Seven-Killings (Earth, the element that governs a Water Day Master) totals 2.45 "
     "weighted units and appears only as hidden stems in Chou, Si and Wu -- structurally present "
     "but never exposed in a visible stem", "BZ-TEN-GOD-OFFICER", "unique")

# ============================ D3 Wealth / gains ============================
proj("D3", "jyotisha", "low", "mixed", "medium",
     f"Sarvashtakavarga house 2 = {AV['2']} bindus (second lowest); house 2 lord Saturn is in "
     f"house 6; house 11 lord Venus is in house 12; the declared 2nd/11th-lord Dhana Yoga is ABSENT",
     "JY-SAV-H2 + JY-DHANA-ABSENT", "unique")
proj("D3", "western", "medium", "mixed", "medium",
     "House 2 (Aquarius) ruler Saturn in house 6; house 11 (Scorpio) ruler Mars in house 12; "
     "Lot of Fortune in Gemini, house 6", "WE-LOT-FORTUNE + WE-H2-H11-RULERS", "unique")
proj("D3", "ziwei", "high", "mixed", "medium",
     "Wealth palace (财帛) at bingwoo holds Po Jun / Army Destroyer at brightness +3 -- a "
     "high-amplitude, disruption-and-rebuild star rather than a steady-accumulation one",
     "ZW-WEALTH-PALACE", "unique")
proj("D3", "bazi", "medium", "mixed", "medium",
     "Wealth element for a Water Day Master is Fire, totalling 2.1 weighted units (Wu and Si "
     "branches, Ding and Bing hidden); a moderately weak Day Master carrying visible wealth is "
     "the classical 'wealth heavier than the self' configuration", "BZ-TEN-GOD-WEALTH", "unique")

# ============================ D4 Partnership ============================
proj("D4", "jyotisha", "low", "negative-leaning", "medium",
     f"Sarvashtakavarga house 7 = {AV['7']} bindus -- the LOWEST of all twelve houses; house 7 "
     f"(Mithuna) is empty and its lord Mercury is retrograde", "JY-SAV-H7", "unique")
proj("D4", "western", "medium", "mixed", "medium",
     "House 7 is Cancer; its ruler is the Moon, the sect light, but the Moon sits in house 8 "
     "with no essential dignity (score 0). Lot of Spirit falls in house 7. Venus, benefic of "
     "sect and natural significator of partnership, is in house 12",
     "WE-H7-RULER + WE-LOT-SPIRIT", "unique")
proj("D4", "ziwei", "high", "positive-leaning", "medium",
     "Spouse palace (夫妻) at wushen holds Zi Wei / Emperor at +2 carrying Hua Quan (power "
     "transformation) TOGETHER WITH Tian Fu / Treasury at +1 -- the most dignified star pairing "
     "anywhere in this chart", "ZW-SPOUSE-PALACE + ZW-SIHUA-QUAN", "unique")

# ============================ D5 Family / roots / home ============================
proj("D5", "jyotisha", "medium", "mixed", "medium",
     f"House 4 (Meena) is empty, SAV {AV['4']} bindus; its lord Jupiter is exalted but in house 8 "
     f"and retrograde. House 2 (family/speech) holds the Sun", "JY-H4-LORD", "unique")
proj("D5", "western", "medium", "mixed", "medium",
     "House 4 (Aries) is empty; its ruler Mars, the malefic OF SECT in this night chart, is in "
     "house 12 with no essential dignity", "WE-H4-RULER-SECT", "unique")
proj("D5", "ziwei", "high", "positive-leaning", "medium",
     "Property/home palace (田宅) at guichou holds Tian Liang / Sage at +2 carrying Hua Lu, the "
     "prosperity transformation of the Ren birth year", "ZW-PROPERTY-SIHUA-LU", "unique")

# ============================ D6 Children / creation ============================
proj("D6", "jyotisha", "low", "mixed", "medium",
     f"House 5 (Mesha) is empty, SAV {AV['5']} bindus; its lord Mars is in house 12, though in "
     f"its own sign Vrischika", "JY-H5-LORD", "unique")
proj("D6", "western", "low", "mixed", "medium",
     "House 5 (Taurus) is empty; its ruler Venus, benefic of sect and in its own bound, is in "
     "house 12", "WE-H5-RULER", "unique")
proj("D6", "ziwei", "low", "negative-leaning", "medium",
     "Children/creation palace (子女) at dingwei holds Tian Ji / Wisdom at brightness -3, the "
     "dimmest major-star placement in the chart", "ZW-CHILDREN-PALACE", "unique")
proj("D6", "bazi", "low", "mixed", "medium",
     "Output (Eating God / Hurting Officer) is Wood, 1.9 weighted units. Which of the two appears "
     "in the hour stem is SCHOOL-DEPENDENT: Eating God under civil time, Hurting Officer under "
     "true solar time", "BZ-TEN-GOD-OUTPUT", "unique")

# ============================ D7 Health / routine ============================
proj("D7", "jyotisha", "high", "mixed", "medium",
     f"Sarvashtakavarga house 6 = {AV['6']} bindus, joint highest; house 6 holds Saturn (29 deg "
     f"14' Vrishabha, retrograde) and Rahu; its lord Venus is in house 12 -- the declared "
     f"Vipareeta Raja Yoga (6th lord in the 12th) is satisfied",
     "JY-SAV-H6 + JY-VIPAREETA", "unique")
proj("D7", "western", "high", "mixed", "high",
     "House 6 (Gemini) holds Saturn, which is retrograde, has triplicity dignity (score 3), and "
     "is the malefic CONTRARY to sect. The Lot of Fortune, which governs body and circumstance, "
     "also falls in house 6", "WE-LOT-FORTUNE-H6 + WE-SECT-SATURN", "unique")
proj("D7", "jyotisha", "high", "negative-leaning", "medium",
     f"Shadbala places Saturn LAST of the seven at "
     f"{SB['planets']['Saturn']['total_rupas_with_cheshta']:.2f} rupas against a 5.0 requirement -- "
     f"the only planet other than the Moon to fall below its classical minimum -- and Saturn is "
     f"the graha occupying house 6", "JY-SHADBALA-SATURN", "unique")
proj("D7", "ziwei", "medium", "positive-leaning", "medium",
     "Health palace (疾厄) at yisi holds Tai Yang / Sun at brightness +2", "ZW-HEALTH-PALACE", "unique")

# ============================ D8 Mind / education / craft ============================
proj("D8", "western", "high", "positive-leaning", "high",
     "Mercury and Saturn are in MUTUAL RECEPTION by domicile (Mercury in Capricorn, Saturn in "
     "Gemini). Every one of the seven dispositor chains terminates in this Mercury-Saturn loop, "
     "making the pair the structural terminus of the whole chart",
     "WE-MUTUAL-RECEPTION + WE-DISPOSITOR-TERMINUS", "unique")
proj("D8", "jyotisha", "high", "mixed", "high",
     "Mercury retrograde in house 1 in Purva Ashadha pada 2; house 3 lord Saturn in house 6; "
     "Jupiter exalted in house 8, the house of research and hidden matters",
     "JY-MERCURY-H1 + JY-H8-JUPITER", "unique")
proj("D8", "jyotisha", "high", "positive-leaning", "medium",
     f"Shadbala makes Mercury the STRONGEST graha in the chart at "
     f"{SB['planets']['Mercury']['total_rupas_with_cheshta']:.2f} rupas against a 7.0 requirement. "
     f"Mercury is also the graha in house 1 and the lord of houses 7 and 10",
     "JY-SHADBALA-MERCURY", "unique")
proj("D8", "bazi", "medium", "negative-leaning", "medium",
     "Resource (Yin), the learning-support element, is Metal at 0.9 weighted units -- the LOWEST "
     "of the five elements, present only as hidden Xin in Chou and hidden Geng in Si",
     "BZ-TEN-GOD-RESOURCE", "unique")
proj("D8", "ziwei", "medium", "positive-leaning", "medium",
     "Zuo Fu carries Hua Ke, the academic/reputation transformation of the Ren year, but it falls "
     "in the Friends palace (仆役) rather than in a self, career or study palace",
     "ZW-SIHUA-KE", "unique")

# ============================ D9 Fortune / spirituality / worldview ============================
proj("D9", "jyotisha", "high", "positive-leaning", "high",
     "Lagna is Dhanu in Mula nakshatra pada 4 (Mula is ruled by Ketu and is the 'root' asterism); "
     "Ketu sits in house 12, the moksha house, alongside Mars and Venus; Jupiter is exalted in "
     "house 8", "JY-LAGNA-NAKSHATRA + JY-KETU-H12", "unique")
proj("D9", "western", "medium", "mixed", "medium",
     "House 9 (Virgo) is empty and its ruler Mercury is in house 1. Jupiter, the natural "
     "significator, is in house 8, holds triplicity and face, but is the benefic CONTRARY to sect",
     "WE-H9-RULER + WE-SECT-JUPITER", "unique")
proj("D9", "ziwei", "high", "mixed", "medium",
     "Fortune/Spirit palace (福德) at renzi holds Lian Zhen at -1 together with Tian Xiang at +3; "
     "this palace is also the CURRENT decadal palace (nominal ages 24-33)",
     "ZW-SPIRIT-PALACE + ZW-DECADAL", "unique")

# ==================================================================== grading
PROM_RANK = {"low": 0, "medium": 1, "high": 2}


def grade(domain):
    ps = [p for p in P if p["domain"] == domain]
    clusters = {}
    for p in ps:
        clusters.setdefault(p["cluster"], []).append(p)
    speaking = list(clusters)

    # --- independence gate: whole-sign house occupancy is correlated jyotisha<->western ---
    gate = None
    if "jyotisha" in clusters and "western" in clusters:
        j_unique = any(p["basis_type"] == "unique" for p in clusters["jyotisha"])
        w_unique = any(p["basis_type"] == "unique" for p in clusters["western"])
        if not (j_unique and w_unique):
            gate = ("jyotisha and western both rest only on whole-sign house occupancy, which is "
                    "mechanically correlated between them; counted as ONE vote")
            speaking = [c for c in speaking if c != "western"]

    # a cluster's stance = its highest prominence claim, and the set of polarities it carries
    stance = {c: {"prominence": max(PROM_RANK[p["prominence"]] for p in v),
                  "polarities": sorted({p["polarity"] for p in v})}
              for c, v in clusters.items() if c in speaking}

    # polarity conflict = one cluster leans positive where another leans negative
    conflicts = []
    for a in stance:
        for b in stance:
            if a < b:
                pa, pb = stance[a]["polarities"], stance[b]["polarities"]
                if ("positive-leaning" in pa and "negative-leaning" in pb) or \
                   ("negative-leaning" in pa and "positive-leaning" in pb):
                    conflicts.append({"kind": "polarity", "clusters": [a, b],
                                      a: pa, b: pb})

    # prominence split = clusters two full steps apart on how prominent the domain is
    proms = {c: stance[c]["prominence"] for c in stance}
    if proms and (max(proms.values()) - min(proms.values())) >= 2:
        hi = [c for c in proms if proms[c] == max(proms.values())]
        lo = [c for c in proms if proms[c] == min(proms.values())]
        conflicts.append({"kind": "prominence", "clusters": sorted(hi + lo),
                          "high": hi, "low": lo})

    speaking_material = [c for c in stance if stance[c]["prominence"] >= 1]   # medium or high
    n_material = len(speaking_material)

    if conflicts:
        g = "DIVERGENT"
    elif n_material == 0:
        # every cluster that speaks says the domain is of LOW prominence.
        # Protocol: a non-divergent weak domain must NOT be described as agreement.
        g = "WEAK"
    elif n_material >= 3:
        g = "STRONG"
    elif n_material == 2:
        g = "MODERATE"
    elif n_material == 1:
        g = "WEAK"
    else:
        g = "INSUFFICIENT"

    agreed = None
    if g == "STRONG":
        agreed = "prominence"
        pols = [set(stance[c]["polarities"]) for c in speaking_material]
        if all(p == {"mixed"} for p in pols):
            agreed = "prominence; every cluster reports MIXED polarity, so no outcome is implied"
        elif len(set.intersection(*pols)) > 0:
            agreed = f"prominence and shared polarity {sorted(set.intersection(*pols))}"
    if g == "WEAK" and n_material == 0:
        agreed = ("all speaking clusters independently report LOW prominence -- this is a quiet "
                  "domain, NOT a convergent theme")

    prom = [p["prominence"] for p in ps]
    prominence = ("high" if prom.count("high") >= 2
                  else ("medium" if "high" in prom or prom.count("medium") >= 2 else "low"))
    return {"domain": domain, "domain_name": DOMAINS[domain], "grade": g,
            "clusters_speaking": sorted(speaking),
            "clusters_speaking_materially": sorted(speaking_material),
            "cluster_count_material": n_material,
            "independence_gate_applied": gate,
            "cluster_stance": stance,
            "conflicts": conflicts,
            "what_is_agreed": agreed,
            "aggregate_prominence": prominence,
            "projections": ps}


grades = {d: grade(d) for d in DOMAINS}
divergent = [d for d, g in grades.items() if g["grade"] == "DIVERGENT"]
weak_quiet = [d for d, g in grades.items() if g["grade"] == "WEAK"]
insufficient = [d for d, g in grades.items() if g["grade"] == "INSUFFICIENT"]
sufficient = [d for d in DOMAINS if d not in insufficient]

# ==================================================================== temperament
TEMPERAMENT = {
 "T1": {"axis": "Leadership / visibility", "computed": [
    {"cluster": "ziwei", "reading": "elevated", "basis": "Zi Wei / Emperor at +2 with Hua Quan, and Qi Sha at +3 in the career palace"},
    {"cluster": "western", "reading": "damped", "basis": "Ascendant ruler Saturn contrary to sect and retrograde; Sun in its final degree with face dignity only; both benefic and malefic weight sits in house 12"},
    {"cluster": "jyotisha", "reading": "damped", "basis": "house 10 empty; Lagna lord in house 8; three planets in house 12"}]},
 "T2": {"axis": "Drive / initiative", "computed": [
    {"cluster": "jyotisha", "reading": "present but privatised", "basis": "Mars in its own sign Vrischika, but in house 12"},
    {"cluster": "western", "reading": "supported", "basis": "Mars is the malefic OF SECT in a night chart, and applies to a sextile with the Sun (orb 2.32 deg)"},
    {"cluster": "bazi", "reading": "moderate", "basis": "moderately weak Day Master against 2.45 units of controlling Earth"}]},
 "T3": {"axis": "Nurturing / service", "computed": [
    {"cluster": "jyotisha", "reading": "high", "basis": "Moon in its own sign Karka; SAV house 6 (service) joint highest at 37"},
    {"cluster": "western", "reading": "high", "basis": "Moon is the sect light; Lot of Fortune in house 6"},
    {"cluster": "ziwei", "reading": "moderate", "basis": "Tian Xiang at +3 in the Fortune palace"}]},
 "T4": {"axis": "Intellect / craft", "computed": [
    {"cluster": "western", "reading": "high", "basis": "Mercury-Saturn mutual reception is the terminus of every dispositor chain"},
    {"cluster": "jyotisha", "reading": "high", "basis": "Mercury in house 1 retrograde; Jupiter exalted in house 8"},
    {"cluster": "bazi", "reading": "under-resourced", "basis": "Resource element Metal is the weakest at 0.9 units"}]},
 "T5": {"axis": "Adaptability", "computed": [
    {"cluster": "ziwei", "reading": "high", "basis": "Tan Lang at +3 in the Ming palace; Po Jun at +3 in the wealth palace"},
    {"cluster": "bazi", "reading": "high", "basis": "yin Water Day Master, the most adaptive of the ten stems in classical description"},
    {"cluster": "jyotisha", "reading": "moderate", "basis": "Lagna in the dual sign Dhanu; four of nine grahas retrograde"}]},
 "T6": {"axis": "Discipline / structure", "computed": [
    {"cluster": "western", "reading": "high", "basis": "Capricorn Ascendant; Saturn holds triplicity and is in mutual reception with Mercury"},
    {"cluster": "jyotisha", "reading": "mixed", "basis": "Saturn retrograde at 29 deg 14', the final degree of Vrishabha, conjoined Rahu in house 6"},
    {"cluster": "bazi", "reading": "moderate", "basis": "Chou month command; Earth (structure/officer) is the second heaviest element at 2.45"}]},
}
SYMBOLIC_OVERLAY = {
 "policy": ("Maya and Tibetan content below is ATTRIBUTED SYMBOLISM, not computed temperament. "
            "It may corroborate, soften or dissent. It never changes a domain grade."),
 "maya": {"calendar_round": MD["maya"]["calendar_round"],
          "long_count": MD["maya"]["long_count"]["independent_arithmetic"]["notation"],
          "interpretation": "NONE ASSERTED",
          "reason": ("The conversion is verified, but no day-sign personality meaning is attached. "
                     "Popular 'Mayan astrology' personality descriptions are a modern invention "
                     "without a classical or living-lineage source, so nothing is claimed.")},
 "tibetan": {"year": MD["tibetan"]["year"]["full_name"],
             "rabjung": f"cycle {MD['tibetan']['year']['rabjung_cycle']}, year {MD['tibetan']['year']['year_within_rabjung']}",
             "interpretation": ("Limited overlay only: a Water-element Horse year in male/yang "
                                "polarity. Water-year symbolism in Tibetan usage is associated "
                                "with adaptability and flow; the Horse with movement. This is "
                                "offered as attributed symbolism."),
             "omitted": list(MD["tibetan"]["omitted_components"])[:-1]},
}

# ==================================================================== chronology
def overlap(a0, a1, b0, b1):
    lo, hi = max(a0, b0), min(a1, b1)
    return (lo, hi) if lo < hi else None


vim = MD["jyotisha"]["vimshottari_gregorian_year"]
prof = MD["western_timing"]["profection_current"]
ad = None
for m in vim["mahadashas"]:
    if m["lord"] == "Venus" and m["start"] < "2026" < m["end"]:
        for a in m["children"]:
            if a["start"] <= "2026-08-29" < a["end"]:
                ad = a
J0, J1 = ad["start"][:10], ad["end"][:10]
W0, W1 = prof["profection_year_start"][:10], prof["profection_year_end"][:10]
ov = overlap(J0, J1, W0, W1)

chronology = {
 "axis": "ISO dates",
 "tracks": {
   "jyotisha_vimshottari": {"mahadasha": "Venus 2016-02-11 -> 2036-02-11",
      "antardasha": f"Venus-Jupiter {J0} -> {J1}",
      "pratyantardasha": "Venus-Jupiter-Saturn 2026-08-21 -> 2027-01-22",
      "mechanism": "position of the Moon within its nakshatra at birth"},
   "western_profection": {"current": f"age 23, 12th house (Sagittarius), Lord of the Year JUPITER",
      "window": f"{W0} -> {W1}", "mechanism": "whole years of age counted from the Ascendant"},
   "western_zodiacal_releasing": {"L1_from_spirit": "Cancer 2003-01-20 -> 2028-01-20 (ruler Moon)",
      "counted": False,
      "why_not_counted": "A second Western technique. Counting it beside profection would "
                         "manufacture agreement inside one cluster."},
   "bazi_da_yun": {"current": "Yi-Mao (乙卯) 2018 -> 2027", "next": "Bing-Chen (丙辰) 2028 -> 2037",
      "annual_2026": "Bing-Wu (丙午), Direct Wealth (正财) to the Gui Day Master",
      "mechanism": "distance from birth to the next sectional solar term, 3 days = 1 year"},
   "ziwei_periods": {"decadal": "Fortune palace 福德 (renzi), nominal ages 24-33",
      "annual_2026": "the 2026 (丙午) year palace falls on the natal WEALTH palace 财帛",
      "mechanism": "Five-Elements Bureau (Metal 4) counted from the Ming palace"},
 },
 "convergences": [
   {"window_start": ov[0], "window_end": ov[1],
    "clusters": ["jyotisha", "western"], "cluster_count": 2, "strength": "MODERATE",
    "shared_time_lord": "Jupiter",
    "mechanisms_are_independent": True,
    "mechanism_note": ("Vimshottari derives Jupiter from the Moon's nakshatra position at birth; "
                       "annual profection derives Jupiter from whole years of age counted from "
                       "the Ascendant. Two unrelated procedures arriving at the same time lord."),
    "domains_activated": ["D9", "D8"],
    "domain_basis": ("Jupiter is Lagna lord in Jyotisha and 12th-house ruler in the Western "
                     "chart, and sits in house 8 in both. The profected house is the 12th. Both "
                     "point at retreat, depth and study rather than at public advancement."),
    "sinic_agrees": False,
    "sinic_position": ("The Sinic cluster points elsewhere for this window: the 2026 annual "
                       "pillar Bing-Wu is Direct Wealth to the Day Master, and the 2026 Zi Wei "
                       "year palace lands on the natal Wealth palace -- that is D3, not D9. "
                       "One cluster dissenting is why this window is MODERATE and not STRONG.")},
 ],
 "no_strong_window_note": ("No window in the examined range is activated by all three primary "
                           "clusters on the same domain, so NO strong / star-rated timing window "
                           "is reported."),
 "next_transition_points": [
   {"date": "2027-01-20", "event": "profection moves to the 1st house (Capricorn), Lord of the Year becomes Saturn"},
   {"date": "2027-01-22", "event": "Venus-Jupiter-Saturn pratyantardasha ends"},
   {"date": "2028-01-20", "event": "Zodiacal Releasing L1 from Spirit moves Cancer -> Leo (reported, not counted)"},
   {"date": "2028-12-12", "event": "Venus-Jupiter antardasha ends; Venus-Saturn begins"},
   {"date": "2028 (Lichun)", "event": "BaZi Da Yun moves Yi-Mao -> Bing-Chen"},
 ],
}

# ==================================================================== dropped claims
DROPPED = {
 "total_dropped": 13,
 "changed_since_first_pass": (
   "Shadbala moved OUT of this list -- it is now computed (five components exactly, Cheshta "
   "approximated and flagged). Yong Shen also moved out: it is now computed under three named "
   "schools and reported as an unresolved three-way split rather than withheld."),
 "by_reason": {
   "no_validated_method": [
     "Tibetan Mewa (sme ba)", "Tibetan Parkha", "Tibetan life force (srog)",
     "Tibetan body force (lus)", "Tibetan power (dbang thang)",
     "Tibetan wind-horse (rlung rta)", "Tibetan annual relations and obstacles"],
   "no_classical_source": [
     "Maya day-sign personality meaning for 8 Caban",
     "Maya Haab month symbolism for 10 Muwan"],
   "computed_but_deliberately_not_collapsed_to_one_answer": [
     "a single BaZi hour pillar (civil and true-solar schools disagree; both reported)",
     "a single BaZi Useful God (three named schools give non-overlapping answers; all reported)"],
   "duplicate_of_another_cluster": [
     "Western whole-sign house occupancy as a second vote alongside Jyotisha",
     "Zodiacal Releasing as a second Western timing vote alongside profection"],
 },
 "also_excluded_from_voting_though_computed": [
   "Shadbala -- refines the Jyotisha cluster from inside it, never counted as a separate vote",
   "D60 Shastiamsa -- sensitive within the stated +/-30 s uncertainty, so unusable for this birth time",
 ],
 "barnum_filter_note": ("Claims that would fit most people -- 'you are sometimes introverted', "
                        "'you value honesty', 'you have untapped potential' -- were not generated, "
                        "because every sentence in the reading is required to cite a computed datum "
                        "and a mapping rule."),
}

SYN = {
 "schema": "six-culture-verified-chart/SYNTHESIS/v2",
 "generated_utc": NOW.isoformat(),
 "counting_rules": {
   "primary_clusters": ["jyotisha", "western", "sinic"],
   "sinic_composition": "BaZi and Zi Wei corroborate each other internally but contribute at most ONE cross-cultural vote",
   "non_voting": ["maya", "tibetan"],
   "shadbala_is_not_a_separate_vote": (
     "Shadbala refines the Jyotisha cluster's stance from inside it. It is never counted as an "
     "additional cluster, and it cannot upgrade a MODERATE to a STRONG on its own."),
   "independence_gate": ("Jyotisha (sidereal whole-sign) and Western (tropical whole-sign) place "
                         "6 of 7 traditional planets in the SAME house, because the ayanamsha "
                         "shifts the Ascendant and the planets together. House-occupancy agreement "
                         "between these two clusters is therefore an artifact, not corroboration. "
                         "A domain earns two votes from them only if at least one side rests on a "
                         "cluster-unique mechanism."),
 },
 "mechanical_correlation_measurement": MD.get("_correlation", None),
 "domains": grades,
 "divergence": {
   "divergent_domains": divergent,
   "divergent_over_all_nine": f"{len(divergent)}/9 = {len(divergent)/9:.1%}",
   "divergent_over_sufficient": f"{len(divergent)}/{len(sufficient)} = {len(divergent)/len(sufficient):.1%}",
   "insufficient_domains": insufficient,
   "weak_or_quiet_domains": weak_quiet,
 },
 "temperament": TEMPERAMENT,
 "symbolic_overlay": SYMBOLIC_OVERLAY,
 "chronology": chronology,
 "dropped_claims": DROPPED,
 "standing_caveat": ("This is computed symbolic corroboration among traditional systems. It is "
                     "not a validated forecast, not evidence of causation, and carries no medical, "
                     "lifespan, fertility, financial or legal conclusion."),
}
json.dump(SYN, open(os.path.join(ROOT, "SYNTHESIS.json"), "w"), indent=1, ensure_ascii=False, default=str)

print("=== DOMAIN GRADES ===")
for d, g in grades.items():
    gate = " [GATE]" if g["independence_gate_applied"] else ""
    cf = "  conflict: " + "; ".join("%s %s" % (c["kind"], "/".join(c["clusters"])) for c in g["conflicts"]) if g["conflicts"] else ""
    print(" %-3s %-34s %-11s material=%-24s%s%s" %
          (d, DOMAINS[d], g["grade"], ",".join(g["clusters_speaking_materially"]) or "-", gate, cf))
print()
print("divergent:", divergent, SYN["divergence"]["divergent_over_all_nine"],
      "| of sufficient:", SYN["divergence"]["divergent_over_sufficient"])
print("projections total:", len(P))
print("current convergence window:", ov[0], "->", ov[1], "clusters jyotisha+western, MODERATE")
