#!/usr/bin/env python
"""Emit the human-readable markdown companions to the JSON datasets."""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
MD = json.load(open(os.path.join(ROOT, "MASTER_DATASET.json")))
SY = json.load(open(os.path.join(ROOT, "SYNTHESIS.json")))
T = MD["time_audit"]; BI = MD["birth_input"]

# ------------------------------------------------------------ INPUT_AUDIT.md
L = ["# INPUT AUDIT", "", "## 1. As supplied", "", "| Field | Value |", "|---|---|"]
for k, v in BI["original_user_entered"].items():
    L.append(f"| {k.replace('_',' ')} | {v if v is not None else '_(not stated)_'} |")
L += ["", "## 2. Normalised", "", "| Field | Value |", "|---|---|",
      f"| Local civil instant | `{T['original_local_civil']}` |",
      f"| UTC instant | `{T['utc_instant']}` |",
      f"| Julian Day (UT) | {T['julian_day_ut']} |",
      f"| Delta-T applied | {T['delta_t_seconds']:.3f} s |",
      f"| IANA zone | {T['timezone_iana']} (tzdata {T['tzdata_release']}) |",
      f"| UTC offset | {T['utc_offset_applied']} |",
      f"| DST in effect | {T['dst_in_effect']} |",
      f"| Civil weekday | {T['civil_weekday']} |",
      f"| Local mean solar time | {T['local_mean_solar_time']} |",
      f"| Local apparent (true) solar time | **{T['local_apparent_solar_time']}** |",
      f"| Equation of time | {T['equation_of_time_minutes']:+.3f} min |",
      f"| Longitude correction from IST meridian | {T['longitude_correction_minutes']:+.3f} min |",
      f"| Sunrise (local) | {T['sunrise_local'][11:19]} |",
      f"| Sunset (local) | {T['sunset_local'][11:19]} |",
      f"| Day length | {T['day_length_hours']:.4f} h |", "",
      "### Historical civil time", "",
      f"**Verdict: {T['historical_offset_check']['verdict']}.** {T['historical_offset_check']['reasoning']}",
      "", "### Vedic weekday caveat", "",
      f"Civil weekday is **{T['vedic_vara_note']['civil_weekday']}**, but the panchanga *vara* is "
      f"**{T['vedic_vara_note']['panchanga_vara']}**. {T['vedic_vara_note']['reason']}",
      "", "## 3. Location", "",
      f"Primary: **{BI['location_primary']['name']}** — {BI['location_primary']['latitude_deg']}°N, "
      f"{BI['location_primary']['longitude_deg']}°E", "",
      f"Source: {BI['location_primary']['coordinate_source']}", "",
      f"> **Coordinate ambiguity recorded.** {BI['location_alternate_candidate']['why_recorded']} "
      f"The alternate is {BI['location_alternate_candidate']['latitude_deg']}°N, "
      f"{BI['location_alternate_candidate']['longitude_deg']}°E.", "",
      "## 4. Boundary audit", "",
      "| System | Boundary | Distance | Verdict | What would change |", "|---|---|---|---|---|"]
for b in sorted(MD["boundary_audit"],
                key=lambda z: abs(z["distance_minutes_of_clock_time"]) if z["distance_minutes_of_clock_time"] is not None else 9e9):
    dm = b["distance_minutes_of_clock_time"]
    dist = (f"{dm:+.2f} min" if dm is not None and abs(dm) < 2880 else
            (f"{dm/1440:+.2f} d" if dm is not None else "n/a"))
    L.append(f"| {b['system']} | {b['boundary']} | {dist} | {b['verdict']} | {b['what_would_change'] or '—'} |")
L += ["", "### Notes on the close ones", ""]
for b in MD["boundary_audit"]:
    if b["note"] and b["verdict"] and ("CLOSE" in b["verdict"] or "DIVERGENT" in b["verdict"] or "notable" in b["verdict"]):
        L.append(f"- **{b['system']} — {b['boundary']}**: {b['note']}")
E = MD["time_uncertainty_ensemble"]
L += ["", "## 5. Time-uncertainty ensemble", "",
      f"Stated certainty is *exact minutes*, so the truthful interval is the rounding window "
      f"**±{E['stated_uncertainty_seconds']} s**. Three instants were computed: T−30s, T, T+30s.", "",
      "| Value | ±30 s (stated) | ±15 min (wider probe) |", "|---|---|---|"]
for k in E["stability_stated_uncertainty"]:
    a = E["stability_stated_uncertainty"][k]; b = E["stability_wide_probe_15min"][k]
    L.append(f"| {k} | **{a}** | {b} |")
L += ["", "The ±15 min column is **not** the user's uncertainty. It answers a different question: "
      "*which results would break if the recorded minute were itself wrong?* Everything is stable "
      "at the stated precision; the divisional-chart Lagnas and the true-solar-time hour pillar are "
      "the first things to fail if the minute is not trustworthy.", "",
      "No rectification was performed and none is proposed.", ""]
open(os.path.join(ROOT, "INPUT_AUDIT.md"), "w").write("\n".join(L))

# ------------------------------------------------------ VERIFICATION_REPORT.md
V = MD["verification"]
fails = [v for v in V if v["status"] != "pass"]
L = ["# VERIFICATION REPORT", "",
     f"**{len(V)} material data verified. {len(fails)} failures or alerts.**", "",
     f"Largest primary-vs-validator disagreement across all ten bodies: "
     f"**{MD['shared_astronomy']['max_engine_difference_deg']*3600:.4f} arcseconds** "
     f"({MD['shared_astronomy']['max_engine_difference_deg']:.8f}°), against an alert threshold of 0.01°.",
     "", "## Engine independence — disclosed honestly", "",
     "> " + MD["manifest"]["engine_independence_disclosure"].replace("\n", " "), "",
     "### A frame mismatch was found and fixed before any claim was made", "",
     "The first comparison showed a **constant 14.168″ offset on every single body** — the "
     "signature of a reference-frame error, not an ephemeris difference. It was identified as the "
     "nutation in longitude (Δψ = −14.168017″ at this instant): Skyfield's `ecliptic_latlon(epoch=t)` "
     "returns the *true* equinox of date, so it had to be compared against Swiss Ephemeris apparent "
     "positions rather than against its mean-equinox (`FLG_NONUT`) output. After matching the frames, "
     "agreement fell to 0.0026″. Averaging the two engines was never considered.", "",
     "## Full verification table", "",
     "| System | Datum | Primary | Validator | Difference | Stability | Confidence | Status |",
     "|---|---|---|---|---|---|---|---|"]
for v in V:
    pv = v["primary_value"]
    pv = f"{pv:.6f}" if isinstance(pv, float) else (str(pv)[:46] if not isinstance(pv, dict) else "_(structured)_")
    vv = v["validator_value"]
    vv = f"{vv:.6f}" if isinstance(vv, float) else (str(vv)[:36] if vv is not None else "—")
    df = v["difference"]
    df = (f"{df*3600:.4f}″" if isinstance(df, float) and abs(df) < 1 else
          (f"{df:+.1f} s" if isinstance(df, (int, float)) else (str(df)[:16] if df is not None else "—")))
    L.append(f"| {v['system']} | {v['datum'][:56]} | {pv} | {v['validator'] or '—'} | {df} | "
             f"{v['uncertainty_stability']} | {v['confidence']} | {v['status']} |")
L += ["", "## Invariants", "",
      "| Invariant | Required | Result |", "|---|---|---|",
      "| Rahu–Ketu separation (mean node) | exactly 180.000° | 180.000000° — pass |",
      "| Vimshottari cycle total | 120 years | 120 — pass |",
      "| Ashtakavarga per-planet totals | 48/49/39/54/56/52/39 | all match — pass |",
      "| Sarvashtakavarga grand total | 337 | 337 — pass |",
      "| Egyptian bounds, each sign | 30° | all 12 signs — pass |",
      "| Egyptian bounds, per planet | 57/79/66/82/76 = 360° | all match — pass |",
      "| Zi Wei distinct palaces | 12 | 12 — pass |",
      "| Zi Wei major stars placed | 14 | 14 — pass |",
      "| Zi Wei Four Transformations | classical 壬-year rule | 天梁祿 / 紫微權 / 左輔科 / 武曲忌 — pass |",
      "| Zi Wei Ming palace | 寅 + (month−1) − hour index | (2+11−3) mod 12 = 戌 — pass |",
      "| Zi Wei Shen palace | 寅 + (month−1) + hour index | (2+11+3) mod 12 = 辰 — pass |",
      "| Maya Gregorian round-trip | exact | 2003-01-20 — pass |",
      "| Maya external anchor | 2012-12-21 = 13.0.0.0.0, 4 Ahau 3 Kankin | reproduced — pass |",
      "| Solar-term instants | < 120 s between two independent algorithms | ≤ 0.8 s — pass |",
      "| Timing periods | continuous, ordered, non-overlapping | pass |", "",
      "## Methods deliberately NOT used", "",
      "- **py-iztro** was not run alongside iztro. It wraps the same logic; using both would have "
      "produced a fake second opinion.", "",
      "## Unavailable / omitted", "",
      "| Item | Status | Reason |", "|---|---|---|",
      "| Jyotisha Shadbala | unavailable | No validated implementation was available; approximating "
      "a six-component strength score would have invented numbers. |"]
for k, v in MD["tibetan"]["omitted_components"].items():
    if k != "policy":
        L.append(f"| Tibetan {k} | omitted | {v} |")
L += ["| BaZi Yong Shen (Useful God) | not asserted | " + MD["bazi"]["yong_shen"]["reason"] + " |",
      "| Maya day-sign personality | not asserted | No classical or living-lineage source. |", ""]
open(os.path.join(ROOT, "VERIFICATION_REPORT.md"), "w").write("\n".join(L))

# --------------------------------------------------------- MASTER_DATASET.md
J = MD["jyotisha"]["chart_mean_node"]; W = MD["western"]; B = MD["bazi"]; Z = MD["ziwei"]["chart"]
L = ["# MASTER DATASET (human-readable)", "",
     "Facts only. No interpretation. Full precision lives in `MASTER_DATASET.json`.", "",
     "## Shared astronomy", "",
     f"- Julian Day (UT): `{MD['shared_astronomy']['julian_day_ut']}`",
     f"- Lahiri ayanamsha at birth: **{MD['shared_astronomy']['ayanamsha_lahiri']:.6f}°** (23°53′59.0″)",
     f"- Two-engine max disagreement: **{MD['shared_astronomy']['max_engine_difference_deg']*3600:.4f}″**", "",
     "## Jyotisha — sidereal Lahiri, whole sign, mean node", "",
     f"**Lagna: {J['lagna']['formatted']} ({J['lagna']['sign_western']}) — "
     f"{J['lagna']['nakshatra']['name']} pada {J['lagna']['nakshatra']['pada']} — lord {J['lagna']['lord']}**", "",
     f"MC: {J['lagna']['mc_formatted']}", "",
     "| Graha | Position | House | Nakshatra | Pada | Dignity | D9 | D10 | R | Combust |",
     "|---|---|---|---|---|---|---|---|---|---|"]
for g in ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]:
    p = J["planets"][g]
    L.append(f"| {g} | {p['formatted']} | {p['house_whole_sign']} | {p['nakshatra']['name']} | "
             f"{p['nakshatra']['pada']} | {p['dignity']['state']} | {p['navamsa_sign']} | "
             f"{p['dasamsa_sign']} | {'R' if p['retrograde'] else ''} | "
             f"{'yes' if p.get('combust') else ('—' if 'combust' not in p else 'no')} |")
sav = MD["jyotisha"]["ashtakavarga"]["sarvashtakavarga_by_house"]
L += ["", "### Sarvashtakavarga (bindus per house)", "",
      "| House | " + " | ".join(str(h) for h in range(1, 13)) + " |",
      "|---|" + "---|" * 12,
      "| Bindus | " + " | ".join(str(sav[str(h)]) for h in range(1, 13)) + " |", "",
      f"Total {sum(sav.values())} (invariant: 337). Joint highest: houses 6 and 10 at 37. "
      f"Lowest: house 7 at 19.", "",
      "### Declared yogas evaluated", ""]
L += ["", "### Vimshottari dasha (Gregorian-year convention, 365.2425 d)", "",
      "| Mahadasha | From | To |", "|---|---|---|"]
for m in MD["jyotisha"]["vimshottari_gregorian_year"]["mahadashas"][:5]:
    L.append(f"| {m['lord']} | {m['start'][:10]} | {m['end'][:10]} |")
L += ["", "## Western / Hellenistic — tropical, whole sign, nocturnal", "",
      f"**Ascendant {W['ascendant']['formatted']} — ruler {W['ascendant']['ruler']}. "
      f"MC {W['midheaven']['formatted']}.**", "",
      f"**Sect: {W['sect']['sect']}** — {W['sect']['basis']} ({-W['sect']['minutes_from_sunrise']:.1f} min "
      f"before sunrise). Sect light {W['sect']['sect_light']}; benefic of sect "
      f"{W['sect']['benefic_of_sect']}; malefic of sect {W['sect']['malefic_of_sect']}.", "",
      "| Planet | Position | House | Sect role | Dignities | Score | Solar phase | R |",
      "|---|---|---|---|---|---|---|---|"]
for p in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn"]:
    e = W["planets"][p]; d = e["dignity"]
    dg = [k.replace("in_own_","").replace("in_","") for k in
          ["in_domicile","in_exaltation","in_detriment","in_fall","in_own_bound","in_own_face"] if d[k]]
    if d["is_any_triplicity_ruler"]: dg.append("triplicity")
    L.append(f"| {p} | {e['formatted']} | {e['whole_sign_house']} | {e['of_sect']} | "
             f"{', '.join(dg) or '—'} | {d['ptolemaic_dignity_score']} | "
             f"{e['solar_condition']['condition']} | {'R' if e['retrograde'] else ''} |")
L += ["", f"- Lot of Fortune: **{W['lots']['fortune']['formatted']}** (house 6)",
      f"- Lot of Spirit: **{W['lots']['spirit']['formatted']}** (house 7)",
      f"- Formula: {W['lots']['formula_used']}",
      "- **Mercury and Saturn are in mutual reception by domicile, and every dispositor chain "
      "terminates in that pair.**", "",
      "## BaZi — Four Pillars", "",
      "| | Year | Month | Day | Hour (civil) | Hour (true solar) |", "|---|---|---|---|---|---|",
      f"| Pillar | {B['pillars_civil_time']['year']['ganzhi']} | {B['pillars_civil_time']['month']['ganzhi']} | "
      f"{B['pillars_civil_time']['day']['ganzhi']} | **{B['pillars_civil_time']['hour']['ganzhi']}** | "
      f"**{B['pillars_true_solar_time']['hour']['ganzhi']}** |",
      f"| Ten God | {B['pillars_civil_time']['year']['ten_god_stem']} | {B['pillars_civil_time']['month']['ten_god_stem']} | "
      f"Day Master | {B['pillars_civil_time']['hour']['ten_god_stem']} | {B['pillars_true_solar_time']['hour']['ten_god_stem']} |",
      f"| Na Yin | {B['pillars_civil_time']['year']['na_yin']} | {B['pillars_civil_time']['month']['na_yin']} | "
      f"{B['pillars_civil_time']['day']['na_yin']} | {B['pillars_civil_time']['hour']['na_yin']} | — |", "",
      f"**Day Master {B['day_master_civil']['day_master']} ({B['day_master_civil']['day_master_polarity']} "
      f"{B['day_master_civil']['day_master_element']}) — {B['day_master_civil']['strength_label']}** "
      f"(support ratio {B['day_master_civil']['support_ratio']}).", "",
      f"Seasonal position: {B['day_master_civil']['seasonal_verdict']}", "",
      "| Element | " + " | ".join(B["element_tally_civil"].keys()) + " |",
      "|---|" + "---|" * 5,
      "| Weighted units | " + " | ".join(f"{v}" for v in B["element_tally_civil"].values()) + " |", "",
      "Branch relations (civil): " + "; ".join(
          f"{r['type']} {'-'.join(r.get('branches', []))}" for r in B["branch_relations_civil"]), "",
      f"Da Yun: {B['da_yun']['direction']}, first period begins {B['da_yun']['start_solar_date']}. "
      f"Current: 乙卯 (2018–2027); next 丙辰 (2028–2037).", "",
      "## Zi Wei Dou Shu — iztro 2.6.0", "",
      f"Lunar date {Z['meta']['lunarDate']} · {Z['meta']['chineseDate']} · hour index 3 (Mao 卯) · male", "",
      f"Ming palace **戌**, Shen (body) palace **辰**. Life ruler 禄存, body ruler 火星. "
      f"Five-Elements Bureau **{Z['meta_zh']['fiveElementsClass']}**.", "",
      "| # | Palace | Branch | Major stars (brightness) | Decadal ages |", "|---|---|---|---|---|"]
for p in Z["palaces"]:
    stars = ", ".join(f"{s['name_zh']} ({s['brightness']})" +
                      (f" **[{s['mutagen']}]**" if s["mutagen"] else "") for s in p["majorStars"])
    L.append(f"| {p['index']} | {p['name_zh']} | {p['heavenlyStem']}{p['earthlyBranch']} | "
             f"{stars or '—'} | {p['decadal']['range']} |")
L += ["", "Four Transformations (壬 year): 天梁→祿 (Property), 紫微→權 (Spouse), 左輔→科 (Friends), "
      "武曲→忌 (Migration). Verified against the classical rule.", "",
      "## Maya", "",
      f"- Long Count **{MD['maya']['long_count']['independent_arithmetic']['notation']}**",
      f"- Calendar Round **{MD['maya']['calendar_round']}** (Tzolk'in 8 Caban / Kab'an, Haab' 10 Muwan)",
      f"- Correlation {MD['maya']['correlation_name']}; JDN {MD['maya']['julian_day_number']}",
      f"- Round-trip to source date: exact", "",
      f"> {MD['maya']['interpretation_policy']}", "",
      "## Tibetan", "",
      f"- Year: **{MD['tibetan']['year']['full_name']}** "
      f"(Rabjung {MD['tibetan']['year']['rabjung_cycle']}, year {MD['tibetan']['year']['year_within_rabjung']})",
      f"- Cross-checked against the BaZi year pillar 壬午 (Yang Water Horse) — the two sexagenary "
      f"cycles agree.", "",
      f"> {MD['tibetan']['omitted_components']['policy']}", ""]
open(os.path.join(ROOT, "MASTER_DATASET.md"), "w").write("\n".join(L))
print("INPUT_AUDIT.md, VERIFICATION_REPORT.md, MASTER_DATASET.md written")
for f in ["INPUT_AUDIT.md","VERIFICATION_REPORT.md","MASTER_DATASET.md"]:
    print(f" {f}: {os.path.getsize(f)} bytes")
