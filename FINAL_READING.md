# Six-Culture Verified Chart & Reading

**Birth data:** 20 January 2003, 05:24 IST, Warud (Amravati district), Maharashtra, India · male · time certainty: exact minutes

Every statement below traces to a computed value in `MASTER_DATASET.json` and a mapping rule in `SYNTHESIS.json`. Nothing is asserted that was not calculated.

---

## 1. Input and sensitivity

| | |
|---|---|
| Local civil instant | `2003-01-20T05:24:00+05:30` |
| UTC instant | `2003-01-19T23:54:00Z` |
| Julian Day (UT) | 2452659.4958333 |
| Coordinates | 21.4737672 °N, 78.2569898 °E (Warud town, OSM relation 14221227) |
| Civil weekday | **Monday** |
| Panchanga *vara* | **Sunday** — the Vedic day begins at sunrise, and you were born 94 minutes before it |
| Local mean solar time | 05:07:02 |
| Local apparent (true) solar time | **04:56:15** |
| Sunrise / sunset | 06:58:26 / 17:57:25 |

**Historical civil time is reliable.** India held IST = UTC+05:30 with no daylight saving throughout 2003 (Indian DST existed only in 1942–45 and briefly in 1965 and 1971). The date is post-1970, so the IANA database governs. There is no offset ambiguity to preserve.

**Everything material is stable at your stated precision.** "Exact minutes" means a ±30-second rounding window. All three ensemble instants (T−30 s, T, T+30 s) give identical results for every categorical output: Lagna sign, nakshatra and pada, Navamsa and Dasamsa Lagna, tropical Ascendant sign, Moon's nakshatra and pada, and all four BaZi pillars under both time schools. No rectification was performed and none is proposed.

**Three boundaries you should know about:**

- **The Dasamsa (D10) Lagna is 1.86 minutes of clock time from a boundary.** It is stable at ±30 s, so it is reported — but if the recorded minute is off by even two minutes, the D10 Lagna moves from Meena to Mesha. Treat every D10-derived career statement as contingent on the minute being exactly right.
- **Your true solar time falls 3 minutes 45 seconds on the far side of a BaZi hour boundary.** This is the single most consequential convention split in your chart, and section 5 deals with it directly.
- **Your Sun sits at 29°29′ Capricorn — the final degree.** The sign is stable for your birth time, but the Sun crosses into Aquarius roughly 12 hours later.

**A coordinate ambiguity was found and tested, not assumed away.** Two settlements named Warud exist in Amravati district, about 68 km apart. You named the district but not the tehsil. Both were computed. The Ascendant differs by 3.7 arcminutes and *every* categorical output is identical — same sign, nakshatra, pada, D9, D10, sect, and BaZi hour under both schools. The ambiguity is immaterial here.

---

## 2. Verification

**30 material data were independently verified. Zero failures. Zero alerts.**

- **Swiss Ephemeris vs JPL DE440s (Skyfield):** largest disagreement across ten bodies was **0.0026 arcseconds** — about 4,000 times inside the 0.01° alert threshold.
- **A frame error was caught before any claim rested on it.** The first comparison showed a *constant* 14.168″ offset on every body — the signature of a reference-frame mismatch, not an ephemeris difference. It was identified as the nutation in longitude (Δψ = −14.168017″ at this instant) and the frames were matched. Agreement then fell to 0.0026″. The two engines were never averaged.
- **Solar terms cross-checked by two genuinely independent algorithms:** Swiss Ephemeris solar-longitude crossings vs lunar_python's own routine agreed to **under one second** on Xiaohan, Dahan and Lichun.
- **The Maya conversion was validated against an external anchor:** the same code reproduces 2012-12-21 = 13.0.0.0.0, 4 Ahau 3 Kankin.
- **The Zi Wei chart was checked against classical rules by hand,** not just trusted: the Ming palace (寅 + month − hour index = 戌), the Shen palace (= 辰), and all four 壬-year transformations (天梁→祿, 紫微→權, 左輔→科, 武曲→忌) match.
- Invariants passed: Rahu–Ketu exactly 180°, Vimshottari totalling 120 years, Ashtakavarga per-planet totals (48/49/39/54/56/52/39) summing to 337, Egyptian bounds summing to 360°, 12 distinct Zi Wei palaces, 14 major stars, Maya round-trip exact, all timing periods continuous and non-overlapping.

**Engine independence, stated honestly.** Swiss Ephemeris files descend from a JPL integration (DE431 lineage) and Skyfield here reads DE440s. These are *not* fully independent in data lineage — they are separate code paths and separate DE releases, and that is what their agreement demonstrates. The solar-term and Maya cross-checks *are* genuinely independent. **py-iztro was deliberately not run alongside iztro**, because it wraps the same logic and would have produced a fake second opinion.

**Not computed, and therefore not used:** Jyotisha Shadbala (no validated implementation); Tibetan Mewa, Parkha, and all personal-force calculations (no validated lineage anchors); the BaZi Useful God (school-dependent, and the hour pillar itself is unresolved); any Maya day-sign personality meaning (no classical or living-lineage source). **14 candidate claims were dropped** — 8 for having no validated method, 2 for having no classical source, 2 as unresolvable school disputes, and 2 as duplicates of another cluster's vote.

---

## 3. Divergence rate — before any positive theme

**3 of 9 domains diverge (33.3 %).** One further domain is quiet. Only 5 of 9 carry a convergent theme, and in every one of those five the convergence is about *prominence*, not about outcome.

Before the agreements are worth anything, one structural finding has to be stated, because it would otherwise inflate everything that follows:

> **Jyotisha and Hellenistic house placements are mechanically correlated, not independent.** Both use whole-sign houses. The Lahiri ayanamsha (23°53′59″) shifts your Ascendant *and* every planet by the same amount, so the house number survives the translation. **6 of your 7 traditional planets land in the same house in both systems** — only the Sun differs, because the ayanamsha carried the Ascendant back from Capricorn into Sagittarius while the Sun stayed in Capricorn.
>
> So when a Jyotisha reading and a Western reading "agree" that Jupiter is in your 8th house, that is one observation stated twice. An independence gate in the synthesis enforces this: these two clusters earn two votes only when at least one side rests on a mechanism the other does not have — dignity, sect, lots, nakshatra, or a timing technique.

Where they *genuinely* differ is **dignity**, because dignity depends on the sign, and the sign does change:

| Planet | Jyotisha (sidereal) | Western (tropical) |
|---|---|---|
| Moon | Cancer — **own sign** | Leo — no essential dignity |
| Mars | Scorpio — **own sign** | Sagittarius — no essential dignity |
| Jupiter | Cancer — **exalted** | Leo — triplicity + face only |

That is a real, material disagreement between two of your three primary clusters about how well-placed your three most-discussed planets actually are. It is not smoothed over anywhere below.

---

## 4. Strongest cross-cultural themes

**All five of these are STRONG on prominence with mixed polarity.** That distinction is the whole point: three traditions independently marking an area as *significant* is not the same as three traditions predicting it will go *well*. None of the five carries a directional claim.

### D1 · Self / identity — STRONG (prominence), polarity mixed in all three clusters

Three unrelated mechanisms each place the anchor of your identity somewhere effortful rather than somewhere easy:

- **Jyotisha:** Lagna is Dhanu 11°33′ in Mula pada 4. Its lord Jupiter is *exalted* — but sits in the 8th house and is retrograde.
- **Western:** Ascendant Capricorn 5°27′; its ruler Saturn is in the 6th house, retrograde, holds triplicity dignity (score 3) — and is the malefic **contrary to sect** in a night chart, its least comfortable condition.
- **Sinic:** Day Master 癸 Gui (yin Water) computes as *moderately weak* (support ratio 0.427), rooted only in the month branch 丑, which stores 癸 as a hidden stem rather than exposing it. Zi Wei places 貪狼 (Greedy Wolf) at brightness +3 in the Ming palace.

The convergent theme is that the significator of "you" is dignified or capable in principle but positioned where it has to work indirectly. Note the two clusters disagree on *which* planet that even is — Jupiter in Jyotisha, Saturn in the Western chart — which is why the theme is about placement, not about a planet.

### D2 · Career / status — STRONG (prominence), polarity mixed

- **Jyotisha:** Sarvashtakavarga gives house 10 **37 bindus — the joint highest of your twelve houses**. Yet house 10 (Kanya) is empty, and its lord Mercury sits in house 1.
- **Western:** whole-sign house 10 is Libra and holds the Midheaven at 17°02′. Its ruler Venus is the **benefic of sect** in your night chart and occupies its own bound — but sits in house 12.
- **Sinic:** the career palace 官禄 holds 七殺 (Seven Killings) at brightness +3, a decisive and demanding star. In BaZi, the Officer/Seven-Killings element (Earth, 2.45 units) is structurally present but appears *only* as hidden stems — never in a visible stem.

Three systems, three mechanisms, one shape: career registers as a high-prominence area whose significators are strong but positioned out of direct view — the 12th house, an empty 10th worked through its lord, hidden stems.

### D5 · Family / roots / home — STRONG (prominence)

Jyotisha's 4th lord Jupiter is exalted but in the 8th; the Western 4th ruler Mars — malefic *of* sect, so not the harder one — is in the 12th; Zi Wei's property palace 田宅 carries 天梁 at +2 with **化祿, the prosperity transformation of your 壬 birth year**. The Zi Wei signal leans positive where the other two read as displaced; no cluster contradicts another outright, so this is agreement on prominence only.

### D7 · Health and daily routine — STRONG (prominence)

- **Jyotisha:** Sarvashtakavarga house 6 = **37 bindus, joint highest**; the house holds Saturn (29°14′ Vrishabha, retrograde) and Rahu; its lord Venus is in the 12th, satisfying a declared **Vipareeta Raja Yoga**.
- **Western:** house 6 holds Saturn — retrograde, with triplicity dignity, and **contrary to sect**. The **Lot of Fortune**, which governs body and circumstance, also falls in house 6.
- **Sinic:** the health palace 疾厄 holds 太陽 at +2.

Read this as *routine, regimen and work-discipline being a structurally loaded area of the chart*. **No medical inference is drawn, and none should be.** This protocol makes no diagnostic, prognostic or health-outcome claim, and a symbolic system is not evidence about your body.

### D9 · Fortune / spirituality / worldview — STRONG (prominence)

- **Jyotisha:** Lagna in **Mula** pada 4 — the "root" asterism, ruled by Ketu; Ketu itself in the 12th (the moksha house) with Mars and Venus; Jupiter exalted in the 8th.
- **Western:** house 9 is empty and worked through Mercury in house 1; Jupiter holds triplicity and face but is the benefic **contrary to sect**.
- **Sinic:** the Fortune palace 福德 holds 廉貞 (−1) with 天相 (+3) — and it is your **current decadal palace** (nominal ages 24–33).

Three independent routes to the same emphasis: an orientation toward depth, roots and what is hidden rather than toward what is displayed. The Jyotisha side is the only one leaning positive; the other two read mixed.

---

## 5. Disagreements — not smoothed over

### The BaZi hour pillar is unresolved, and I will not pick one

This is the sharpest split in your chart.

| Convention | Time used | Hour pillar | Hour Ten God |
|---|---|---|---|
| Civil clock | 05:24:00 | 乙卯 (Yi-Mao) | 食神 Eating God |
| Local mean solar time | 05:07:02 | 乙卯 (Yi-Mao) | 食神 Eating God |
| **True solar time** | **04:56:15** | **甲寅 (Jia-Yin)** | **傷官 Hurting Officer** |

Your longitude is 4.24° west of the IST meridian (−16.97 min) and the equation of time on 20 January is −10.78 min. Together they pull true solar time to 04:56:15 — **3 minutes 45 seconds** before the 卯 boundary, into the 寅 hour.

Two of the three conventions give 乙卯, and that is worth knowing, but it is not a majority verdict — schools are not votes. The branch relations change too: under 寅 you additionally get a 寅-巳 harm *and* a partial 寅-巳-申 punishment that simply do not exist under 卯. What *both* schools agree on: the year (壬午), month (癸丑) and day (癸巳) pillars, the 癸 yin-Water Day Master, and its "moderately weak" strength label (0.427 civil vs 0.405 true-solar). **Anything resting on the hour pillar alone is low confidence. Anything resting on the other three is not.**

### D3 · Wealth — DIVERGENT (prominence conflict: Jyotisha vs Sinic)

- **Jyotisha says quiet:** Sarvashtakavarga house 2 = **21 bindus, the second lowest**; the 2nd lord Saturn is in the 6th; the 11th lord Venus is in the 12th; and the declared 2nd/11th-lord **Dhana Yoga is absent** — the two lords are not conjunct.
- **Zi Wei says loud:** the wealth palace 财帛 holds **破軍 (Army Destroyer) at brightness +3** — a high-amplitude, disruption-and-rebuild star. In BaZi, Fire (wealth for a Water Day Master) totals 2.1 units against a moderately weak Day Master — the classical "wealth heavier than the self" configuration.

One cluster reads this as a low-emphasis area; another reads it as a high-amplitude one. They are not describing the same thing and cannot be reconciled by averaging. Both are reported.

### D4 · Partnership — DIVERGENT (both polarity and prominence)

- **Jyotisha says weak:** Sarvashtakavarga house 7 = **19 bindus — the lowest of all twelve houses**; the house is empty; its lord Mercury is retrograde.
- **Zi Wei says the opposite:** the spouse palace 夫妻 holds **紫微 (Emperor) at +2 carrying 化權, the power transformation, together with 天府 (Treasury) at +1** — the most dignified star pairing anywhere in your chart.
- **Western sits between:** the 7th ruler is the Moon, your sect light, but with no essential dignity and placed in the 8th; the **Lot of Spirit falls in the 7th**; Venus, benefic of sect and natural significator of partnership, is in the 12th.

This is the starkest contradiction in the whole chart: your weakest house by Jyotisha's own arithmetic is your strongest palace by Zi Wei's. Anyone who tells you these "really agree" is choosing one and hiding the other.

### D8 · Mind / education / craft — DIVERGENT (polarity: Western vs Sinic)

- **Western says strong:** Mercury and Saturn are in **mutual reception by domicile** (Mercury in Capricorn, Saturn in Gemini), and **all seven dispositor chains terminate in that pair** — it is the structural terminus of your entire chart. Disciplined, technical, structure-building intelligence.
- **BaZi says under-resourced:** the Resource element (印), which governs learning support, is **Metal at 0.9 units — the weakest of your five elements**, present only as hidden 辛 in 丑 and hidden 庚 in 巳.
- Jyotisha is mixed: Mercury retrograde in house 1 in Purva Ashadha; Jupiter exalted in the 8th (research, hidden matters). Zi Wei places 左輔 with **化科** — the academic transformation — but in the Friends palace 仆役 rather than in a self, career or study palace.

The Western chart says the craft structure is the best-built thing you have; the BaZi says the fuel supply for it is the thinnest. Both are computed, and they point opposite ways.

---

## 6. Weak and quiet — where not to over-read

### D6 · Children / creation — WEAK

Every cluster that speaks reports **low** prominence: house 5 empty with 26 bindus and its lord Mars in the 12th; the Western 5th ruler Venus also in the 12th; Zi Wei's 子女 palace holding 天機 at **−3, the dimmest major-star placement in your chart**; BaZi output (Wood) at 1.9 units, and *which* output star it is — Eating God or Hurting Officer — is one of the casualties of the unresolved hour pillar.

**Unanimous quiet is not a convergent theme, and it is certainly not a prediction.** Four systems agreeing there is little signal means there is little signal — nothing more. No fertility, pregnancy or family-planning inference is drawn from this or from anything else in this chart.

Also genuinely absent, and worth stating because their absence is often glossed over: the **Dhana Yoga** (2nd/11th lords conjunct) does **not** form. Three **Vipareeta Raja Yogas** do form (6th lord in the 12th, 8th lord in the 8th, 12th lord in the 12th), and **Gajakesari** forms (Jupiter conjunct the Moon in Karka). **Kemadruma is cancelled** — Jupiter sits with the Moon. No Pancha Mahapurusha Yoga forms: Mars is in its own sign but in the 12th, and Jupiter is exalted but in the 8th, so neither reaches a kendra.

---

## 7. Temperament overlay

Computed axes (Jyotisha, Western and Sinic only):

| Axis | Reading | Basis |
|---|---|---|
| **T1 Leadership / visibility** | **contested** | Zi Wei elevated (紫微 +2 with 化權; 七殺 +3 in career); Western and Jyotisha both damped (Ascendant ruler contrary to sect and retrograde, empty 10th, three planets in the 12th) |
| **T2 Drive / initiative** | present, privatised | Mars in its own sign but in the 12th (Jyotisha); Mars is the malefic *of sect* and applies to a sextile with the Sun at 2.32° — though by whole sign the two are in **aversion**, so the degree-based aspect is the weaker testimony (Western) |
| **T3 Nurturing / service** | **high, all three clusters** | Moon in own sign Karka; Moon is the sect light; Lot of Fortune in the 6th; SAV house 6 joint-highest at 37 |
| **T4 Intellect / craft** | high but under-fuelled | Mercury–Saturn mutual reception as chart terminus; Mercury in house 1; Resource element weakest at 0.9 |
| **T5 Adaptability** | **high, all three clusters** | 貪狼 +3 and 破軍 +3; yin-Water Day Master; dual-sign Lagna with three of the seven true grahas retrograde (Mercury, Jupiter, Saturn — the nodes are retrograde by definition) |
| **T6 Discipline / structure** | high with friction | Capricorn Ascendant and Saturn in triplicity and mutual reception; but Saturn retrograde at 29°14′, the final degree, sharing house 6 with Rahu 17° away |

**Attributed symbolism — no domain weight, no grade changes:**

- **Maya:** Long Count **12.19.9.16.17**, Calendar Round **8 Caban 10 Muwan**. The conversion is verified three ways. **No personality meaning is asserted.** Popular "Mayan astrology" day-sign character lists are a modern invention with no classical or living-lineage source, so nothing is claimed from them.
- **Tibetan:** **Water Male Horse**, 17th Rabjung, year 16 — cross-checked against the BaZi year pillar 壬午, since the two sexagenary cycles run in lockstep. Water-year symbolism is associated with adaptability and flow, the Horse with movement. That is offered as attributed symbolism and nothing more. Mewa, Parkha and all personal-force calculations were **omitted** rather than guessed.

---

## 8. Timing

**Current window: 13 April 2026 → 20 January 2027. MODERATE (two of three clusters).**

Two primary clusters independently arrive at **Jupiter** as time lord by wholly unrelated procedures:

- **Jyotisha:** Venus Mahadasha (2016-02-11 → 2036-02-11) / **Jupiter Antardasha (2026-04-13 → 2028-12-12)** / Saturn Pratyantardasha (2026-08-21 → 2027-01-22). Derived from the Moon's position within Ashlesha at birth.
- **Western:** annual profection, age 23 → **12th house (Sagittarius), Lord of the Year Jupiter**, 2026-01-20 → 2027-01-20. Derived from whole years of age counted from the Ascendant.

The exact overlap of the two windows is **2026-04-13 → 2027-01-20**. Both point at the same register: Jupiter rules the 1st in Jyotisha and the 12th in the Western chart, and sits in the 8th house in both; the profected house is the 12th. Retreat, depth, study and behind-the-scenes work rather than public advancement — domains **D9** and **D8**.

**The Sinic cluster dissents, and that is why this is not a strong window.** BaZi's 2026 annual pillar 丙午 is **Direct Wealth (正财)** to your Day Master, and the Zi Wei 2026 year palace lands on your natal **wealth palace 财帛**. Both point at D3, not D9. Two clusters agree; one points elsewhere.

**There is no strong window.** No period in the examined range is activated by all three primary clusters on the same domain. Zodiacal Releasing was computed (L1 from Spirit: Cancer 2003-01-20 → 2028-01-20) but is **reported separately and not counted** — it is a second Western technique, and stacking it beside profection would manufacture agreement inside a single cluster.

**Next transitions:** 2027-01-20, profection moves to the 1st house and the Lord of the Year becomes **Saturn** · 2027-01-22, the Saturn pratyantardasha ends · Lichun 2028, BaZi Da Yun turns 乙卯 → 丙辰 · 2028-12-12, Venus–Jupiter gives way to Venus–Saturn.

---

## 9. Closing frame

What you have here is a reproducible calculation and an honest tally of where six traditional symbolic systems corroborate one another and where they contradict one another. The arithmetic is verified: two ephemeris engines agree to 0.0026 arcseconds, two independent algorithms agree on the solar terms to under a second, and every structural invariant passes.

**None of that makes any of it a validated method of prediction.** Verified inputs and correct arithmetic produce a verified chart, not a verified forecast. The agreements above are agreements between interpretive traditions — several of which, as section 3 shows, are not even as independent of each other as they appear.

Three things this document deliberately does not do: it names no favourable outcome, it makes no claim about health, lifespan, fertility, finances or legal matters, and it does not choose between schools where the schools genuinely disagree. Where your chart is ambiguous — the hour pillar, partnership, wealth, the fuel behind your craft — it is left ambiguous, because that is what the calculation actually says.

Read the strong themes as *areas your chart marks as loaded*, not as areas that will go well or badly. Nothing here is fate, and nothing here should displace your own judgement about your life.
