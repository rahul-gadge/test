#!/usr/bin/env python
"""Emit PRECISION_REPORT.md -- the convention-sensitivity and completeness layer."""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
MD = json.load(open(os.path.join(ROOT, "MASTER_DATASET.json")))
P = MD["precision_layer"]
L = []
A = L.append

A("# PRECISION REPORT")
A("")
A("What this answers: **which of a practitioner's convention choices actually change a "
  "conclusion in this chart, and which do not.** Nothing here is interpretation.")
A("")
A("## 1. Three independent engines")
A("")
A("| Body | Swiss Ephemeris | JPL DE440s (Skyfield) | Moshier (analytic) | Max spread |")
A("|---|---|---|---|---|")
sky = MD["shared_astronomy"]["validator_positions_de440s"]
for b in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
    sw = MD["shared_astronomy"]["tropical_positions"][b]["longitude"]
    mo = P["third_engine_moshier"][b]["moshier_deg"]
    sk = sky[b]["longitude"]
    spread = (max(sw, mo, sk) - min(sw, mo, sk)) * 3600
    A(f"| {b} | {sw:.7f}° | {sk:.7f}° | {mo:.7f}° | {spread:.4f}″ |")
A("")
A(f"Moshier is an **analytic** ephemeris carrying no data files, so it is mathematically "
  f"independent of the compressed-JPL `.se1` files *and* of DE440s. Largest Swiss-vs-Moshier "
  f"disagreement: **{P['third_engine_moshier']['_max_difference_arcsec']:.4f}″** (the Moon). "
  f"Three separate derivations agree sub-arcsecond.")
A("")
A("## 2. Geocentric vs topocentric")
A("")
A("| Body | Shift | Sign changes? | Nakshatra changes? | Vargas that change |")
A("|---|---|---|---|---|")
for b in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
    v = P["topocentric_vs_geocentric"][b]
    A(f"| {b} | {v['difference_arcmin']:.3f}′ | {'yes' if v['sign_changes'] else 'no'} | "
      f"{'yes' if v['nakshatra_changes'] else 'no'} | {', '.join(v['vargas_that_change']) or '—'} |")
A("")
A("**Declared convention: geocentric**, which is what every tradition here assumes. But the "
  "Moon's parallax is **38.6′**, and that is enough to move six of the finer divisional charts "
  "(D12, D24, D30, D40, D45, D60). Sign, nakshatra and pada are unaffected. Any claim resting on "
  "the Moon in those six vargas is convention-dependent and should say so.")
A("")
A("## 3. Ayanamsha — twelve schools side by side")
A("")
ay = P["ayanamsha_comparison"]
A("| Ayanamsha | Value | Lagna | Nakshatra | Pada | D9 | D10 | Dasha lord |")
A("|---|---|---|---|---|---|---|---|")
for r in ay["rows"]:
    A(f"| {r['ayanamsha']} | {r['value_dms']} | {r['lagna_formatted']} | {r['lagna_nakshatra']} | "
      f"{r['lagna_pada']} | {r['lagna_d9']} | {r['lagna_d10']} | {r['moon_dasha_lord']} |")
A("")
A(f"Spread across schools: **{ay['spread_deg']:.4f}°**. What survives all twelve:")
A("")
A("- **The Lagna sign is Dhanu in every one.**")
A("- **The Vimshottari starting lord is Mercury in every one** — so the entire dasha timeline, "
  "including the current Venus–Jupiter period, is ayanamsha-independent.")
A("")
A("What does not survive:")
A("")
d10s = [r["ayanamsha"] for r in ay["rows"] if r["differs_from_lahiri"]["lagna_d10"]]
nks = [r["ayanamsha"] for r in ay["rows"] if r["differs_from_lahiri"]["lagna_nakshatra_or_pada"]]
A(f"- **The D10 Lagna changes under {len(d10s)} of 12** ({', '.join(d10s)}).")
A(f"- The Lagna nakshatra or pada changes under {len(nks)} ({', '.join(nks)}).")
A("- Saturn changes sign under at least one school — it sits at 29°14′, in the last degree.")
A("")
A("## 4. House system — twelve systems side by side")
A("")
hs = P["house_system_comparison"]
A("| System | Planets that change house vs whole sign |")
A("|---|---|")
for r in hs["rows"]:
    if "error" in r: continue
    ch = r.get("planets_changing_house_vs_whole_sign", [])
    A(f"| {r['system']} | {', '.join(ch) if ch else '— (none)'} |")
A("")
A("The **Ascendant degree is identical in all twelve** — only the divisions differ. The material "
  "finding: **Mars moves from the 12th to the 11th in every quadrant system**, because it sits at "
  "1°48′ Sagittarius, just inside the sign but outside the quadrant cusp. A whole-sign reading and "
  "a Placidus reading will disagree about Mars, and that is a convention choice, not a fact.")
A("")
A("## 5. Sunrise convention — five variants")
A("")
sv = P["sunrise_convention_variants"]
A("| Convention | Sunrise | Birth relative to it |")
A("|---|---|---|")
for k, v in sv.items():
    if k.startswith("_"): continue
    A(f"| {k.replace('_',' ')} | {v['local'][11:19]} | {v['minutes_from_birth']:+.1f} min |")
A("")
A(f"Spread: **{sv['_spread_minutes']:.2f} minutes**. All five agree the birth precedes sunrise, so "
  f"the **nocturnal sect** and the **Sunday panchanga vara** hold under every convention.")
A("")
A("## 6. Panchanga")
A("")
pn = P["panchanga"]
A("| Limb | Value | Distance to next |")
A("|---|---|---|")
A(f"| Tithi | {pn['tithi']['paksha']} {pn['tithi']['name']} (#{pn['tithi']['index']}) | "
  f"{pn['tithi']['degrees_to_next_tithi']:.3f}° |")
A(f"| Vara | {pn['vara']['name']}, lord {pn['vara']['lord']} | — |")
A(f"| Nakshatra | {pn['nakshatra']['of_moon']['name']} pada {pn['nakshatra']['of_moon']['pada']} | — |")
A(f"| Yoga | {pn['yoga']['name']} (#{pn['yoga']['index']}) | {pn['yoga']['degrees_to_next']:.3f}° |")
A(f"| Karana | {pn['karana']['name']} (#{pn['karana']['index']}, {pn['karana']['type']}) | "
  f"{pn['karana']['degrees_to_next']:.3f}° |")
A("")
A("## 7. All sixteen vargas, and which are usable")
A("")
st = P["varga_stability"]
A("| Varga | Name | Lagna sign | Lagna: ±30 s | Lagna: ±15 min | Moon: ±30 s |")
A("|---|---|---|---|---|---|")
for k in ["D1","D2","D3","D4","D7","D9","D10","D12","D16","D20","D24","D27","D30","D40","D45","D60"]:
    v = P["shodasavarga"]["lagna"][k]
    a = st["lagna_at_stated_uncertainty"][k]
    b = st["lagna_at_15min_probe"][k]
    m = st["moon_at_stated_uncertainty"][k]
    mark = " **← unusable**" if a == "sensitive" else ""
    A(f"| {k} | {v['name']} | {v['sign']} | {a}{mark} | {b} | {m} |")
A("")
A("**The practical rule this yields:** at your stated precision, fifteen of the sixteen vargas are "
  "usable and **D60 is not** — it flips within the ±30 s rounding window itself. If the recorded "
  "minute were merely approximate rather than exact, only D1 would survive.")
A("")
vgm = P["shodasavarga"]["lagna_vargottama"]
A(f"Lagna vargottama count: **{vgm['count']} of 16** ({', '.join(vgm['vargas'])}).")
A("")
A("## 8. Shadbala — now computed")
A("")
sb = P["shadbala"]
A("| Planet | Sthana | Dig | Kala | Naisargika | Drik | Cheshta | Total (rupas) | Required | Meets? |")
A("|---|---|---|---|---|---|---|---|---|---|")
for p in sb["rank_strongest_first"]:
    d = sb["planets"][p]
    ch = f"{d['cheshta_bala']:.2f}" if d["cheshta_bala"] is not None else "n/a"
    A(f"| {p} | {d['sthana_bala']['total']:.2f} | {d['dig_bala']:.2f} | {d['kala_bala']['total']:.2f} | "
      f"{d['naisargika_bala']:.2f} | {d['drik_bala']:.2f} | {ch} | "
      f"**{d['total_rupas_with_cheshta']:.3f}** | {d['required_rupas']:.1f} | "
      f"{'yes' if d['meets_requirement_with_cheshta'] else '**no**'} |")
A("")
A(f"Rank: **{' > '.join(sb['rank_strongest_first'])}**")
A("")
A("**Honest limit on this table.** Five of the six components use exact classical formulas. "
  "**Cheshta Bala is an approximation** — BPHS defines it through the cheshta kendra of the "
  "classical epicyclic model, which a modern ephemeris does not reproduce, so speed is mapped onto "
  "0–60 instead. Totals are therefore given both with and without it. The ranking is stable either "
  "way except that **Venus and the Moon swap** when Cheshta is excluded.")
A("")
A("## 9. Yong Shen — computed under three named schools, and unresolved")
A("")
ys = MD["bazi"]["yong_shen_by_school"]
A("| School | Favourable elements | Depends on the hour pillar? | Reasoning |")
A("|---|---|---|---|")
for k, v in ys["schools"].items():
    A(f"| {k} | {', '.join(v['favourable_elements']) or '—'} | "
      f"{'yes' if v['depends_on_hour_pillar'] else 'no'} | {v['reasoning']} |")
A("")
A(f"**Elements all three schools agree on: {ys['elements_all_schools_agree_on'] or 'NONE'}.** "
  f"{ys['verdict']}")
A("")
A("## 10. Combustion")
A("")
cb = MD["precision_layer"]["combustion_school_comparison"]
A(f"No planet is combust under any of the three orb schools tested "
  f"(BPHS, Surya Siddhanta, Western traditional). Planets where the schools disagree: "
  f"**{cb['_planets_where_schools_disagree'] or 'none'}**. This conclusion is convention-free.")
A("")
open(os.path.join(ROOT, "PRECISION_REPORT.md"), "w").write("\n".join(L))
print("PRECISION_REPORT.md written:", os.path.getsize(os.path.join(ROOT, "PRECISION_REPORT.md")), "bytes")
