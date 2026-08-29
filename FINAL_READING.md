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

**43 material data were independently verified across three engines. Zero failures. Zero alerts.**

- **Three independent engines, not two.** Swiss Ephemeris vs JPL DE440s (Skyfield) agree to **0.0026″**. A third path — the **Moshier analytic ephemeris**, which carries no data files and is mathematically independent of both the compressed-JPL `.se1` files *and* of DE440s — agrees to **0.52″** at worst (the Moon). Three separate derivations, sub-arcsecond.
- **A frame error was caught before any claim rested on it.** The first comparison showed a *constant* 14.168″ offset on every body — the signature of a reference-frame mismatch, not an ephemeris difference. It was identified as the nutation in longitude (Δψ = −14.168017″ at this instant) and the frames were matched. Agreement then fell to 0.0026″. The two engines were never averaged.
- **Solar terms cross-checked by two genuinely independent algorithms:** Swiss Ephemeris solar-longitude crossings vs lunar_python's own routine agreed to **under one second** on Xiaohan, Dahan and Lichun.
- **The Maya conversion was validated against an external anchor:** the same code reproduces 2012-12-21 = 13.0.0.0.0, 4 Ahau 3 Kankin.
- **The Zi Wei chart was checked against classical rules by hand,** not just trusted: the Ming palace (寅 + month − hour index = 戌), the Shen palace (= 辰), and all four 壬-year transformations (天梁→祿, 紫微→權, 左輔→科, 武曲→忌) match.
- Invariants passed: Rahu–Ketu exactly 180°, Vimshottari totalling 120 years, Ashtakavarga per-planet totals (48/49/39/54/56/52/39) summing to 337, Egyptian bounds summing to 360°, 12 distinct Zi Wei palaces, 14 major stars, Maya round-trip exact, all timing periods continuous and non-overlapping.

**Engine independence, stated honestly.** Swiss Ephemeris files descend from a JPL integration (DE431 lineage) and Skyfield here reads DE440s. These are *not* fully independent in data lineage — they are separate code paths and separate DE releases, and that is what their agreement demonstrates. The solar-term and Maya cross-checks *are* genuinely independent. **py-iztro was deliberately not run alongside iztro**, because it wraps the same logic and would have produced a fake second opinion.

**Since the first pass, two of the four gaps have been closed.** Shadbala is now computed — five of its six components from exact classical formulas, with Cheshta Bala flagged as an approximation and totals given both with and without it. The BaZi Useful God is now computed **under three named schools**, which turns out to be more informative than the single answer I withheld (see section 5). A validation gate on the sixteen divisional charts caught a genuine bug in my own code: `int(lon // (30/9))` mis-floors on exact boundaries because 30/9 is not representable in binary, so 30.000° returned the 9th navamsa instead of the 10th. Fixed by multiplying first.

**Still not computed, and still not used:** Tibetan Mewa, Parkha and all personal-force calculations (no validated lineage anchors); any Maya day-sign personality meaning (no classical or living-lineage source). **13 claims remain withheld** — 7 Tibetan components with no validated lineage anchor, 2 Maya meanings with no classical source, 2 deliberately left as school splits rather than collapsed to one answer (the hour pillar and the Useful God), and 2 duplicates of another cluster's vote. Two further items are computed but excluded from voting: Shadbala, which refines the Jyotisha cluster from inside it, and D60, which is unusable at this time precision.

---


### What survives a change of school

The point of hardening the data was not more decimal places — the astronomy was already 0.0026″, far past astrological relevance. It was to find out **which of a practitioner's convention choices actually move a conclusion in this chart.** Twelve ayanamshas, twelve house systems, five sunrise conventions, three combustion tables and geocentric-vs-topocentric were each computed in full.

**Survives everything — state these firmly:**

- **The Lagna is Dhanu under all twelve ayanamshas**, across an 8.37° spread from Djwhal Khul to Sassanian.
- **The Vimshottari starting lord is Mercury under all twelve** — so the entire dasha timeline, including the current Venus–Jupiter period, is ayanamsha-independent. That is a much stronger result than I could claim in the first pass.
- **Nocturnal sect holds under all five sunrise conventions** (they span only 3.96 minutes).
- **No planet is combust** under BPHS, Surya Siddhanta or Western orbs — unanimous.
- **Fifteen of the sixteen vargas are stable** at your stated ±30 s.

**Does not survive — hedge these, or name your school:**

- **The D10 Lagna changes under seven of the twelve ayanamshas.** Combined with its 1.86-minute boundary distance, the D10 is the single most fragile thing in your chart. Any career claim drawn from it is doubly contingent.
- **D60 is unusable.** It flips *within* the ±30 s rounding window itself. Fifteen vargas survive your time precision; the Shastiamsa does not, and no honest reading should use it here.
- **Mars moves from the 12th house to the 11th in every quadrant system** (Placidus, Koch, Campanus, Regiomontanus, Alcabitius, Porphyry, Topocentric, Krusinski). It sits at 1°48′ Sagittarius — inside the sign but outside the cusp. A whole-sign reader and a Placidus reader will disagree about Mars, and that is a convention, not a fact.
- **The Moon's topocentric position differs from its geocentric position by 38.6′**, enough to move six of the finer vargas (D12, D24, D30, D40, D45, D60). Geocentric is declared as primary here, since that is what these traditions assume — but a claim about the Moon in those six vargas is convention-dependent.
- **Saturn changes sign under at least one ayanamsha.** It sits at 29°14′, the last degree of Vrishabha.

The full tables are in `PRECISION_REPORT.md`.

### Panchanga

Tithi **Krishna Dvitiya** (waning, #17) · Vara **Ravivara / Sunday** (lord Sun — the Vedic day begins at sunrise, so the civil Monday does not apply) · Nakshatra **Ashlesha pada 3** · Yoga **Ayushman** · Karana **Gara**.

## 3. Divergence rate — before any positive theme

**4 of 9 domains diverge (44.4 %).** One further domain is quiet. Only 4 of 9 carry a convergent theme, and in every one the convergence is about *prominence*, not about outcome.

> **The divergence rate went UP when the data got better.** In the first pass it was 3 of 9. Computing Shadbala moved **D7 (Health/routine) from STRONG to DIVERGENT**: Jyotisha's own strength arithmetic puts Saturn — the graha sitting in house 6 — **last of the seven and below its classical minimum**, which contradicts Zi Wei's bright Sun in the health palace. More rigour found more disagreement, not less. That is the expected direction when you stop letting vague agreement stand in for real agreement.

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

**All four of these are STRONG on prominence with mixed polarity.** That distinction is the whole point: three traditions independently marking an area as *significant* is not the same as three traditions predicting it will go *well*. None of the four carries a directional claim.

### D1 · Self / identity — STRONG (prominence), polarity mixed in all three clusters

Three unrelated mechanisms each place the anchor of your identity somewhere effortful rather than somewhere easy:

- **Jyotisha:** Lagna is Dhanu 11°33′ in Mula pada 4. Its lord Jupiter is *exalted* — but sits in the 8th house and is retrograde.
- **Western:** Ascendant Capricorn 5°27′; its ruler Saturn is in the 6th house, retrograde, holds triplicity dignity (score 3) — and is the malefic **contrary to sect** in a night chart, its least comfortable condition.
- **Sinic:** Day Master 癸 Gui (yin Water) computes as *moderately weak* (support ratio 0.427), rooted only in the month branch 丑, which stores 癸 as a hidden stem rather than exposing it. Zi Wei places 貪狼 (Greedy Wolf) at brightness +3 in the Ming palace.

Shadbala sharpens this rather than softening it: the Lagna lord Jupiter ranks **second strongest of the seven at 8.19 rupas against a 6.5 requirement**, so it is genuinely strong in absolute terms — and still sits in a dusthana.

The convergent theme is that the significator of "you" is dignified or capable in principle but positioned where it has to work indirectly. Note the two clusters disagree on *which* planet that even is — Jupiter in Jyotisha, Saturn in the Western chart — which is why the theme is about placement, not about a planet.

### D2 · Career / status — STRONG (prominence), polarity mixed

- **Jyotisha:** Sarvashtakavarga gives house 10 **37 bindus — the joint highest of your twelve houses**. Yet house 10 (Kanya) is empty, and its lord Mercury sits in house 1.
- **Western:** whole-sign house 10 is Libra and holds the Midheaven at 17°02′. Its ruler Venus is the **benefic of sect** in your night chart and occupies its own bound — but sits in house 12.
- **Sinic:** the career palace 官禄 holds 七殺 (Seven Killings) at brightness +3, a decisive and demanding star. In BaZi, the Officer/Seven-Killings element (Earth, 2.45 units) is structurally present but appears *only* as hidden stems — never in a visible stem.

Three systems, three mechanisms, one shape: career registers as a high-prominence area whose significators are strong but positioned out of direct view — the 12th house, an empty 10th worked through its lord, hidden stems.

### D5 · Family / roots / home — STRONG (prominence)

Jyotisha's 4th lord Jupiter is exalted but in the 8th; the Western 4th ruler Mars — malefic *of* sect, so not the harder one — is in the 12th; Zi Wei's property palace 田宅 carries 天梁 at +2 with **化祿, the prosperity transformation of your 壬 birth year**. The Zi Wei signal leans positive where the other two read as displaced; no cluster contradicts another outright, so this is agreement on prominence only.

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


### The BaZi favourable element splits three ways

In the first pass I declined to name a Useful God (用神). Computing it under three named schools shows why that was the right call — and is more useful than the refusal:

| School | Favourable elements | Hour-dependent? |
|---|---|---|
| 扶抑 Fu Yi (support / suppress) | **Water, Metal** | yes |
| 調候 Tiao Hou (climate regulation) | **Fire** | no |
| 通關 Tong Guan (bridging) | **Wood** | yes |

**Three schools, three answers, zero overlap.** Fu Yi supports a moderately weak Day Master with its own element and its resource. Tiao Hou reads 癸 born in the 丑 month as frozen water needing 丙 to warm it. Tong Guan bridges the heavy Water–Fire control clash with Wood. Two of the three additionally depend on the hour pillar, which is itself unresolved.

Any practitioner who hands you a single favourable element for this chart has silently picked a school. Ask which one.

### D3 · Wealth — DIVERGENT (prominence conflict: Jyotisha vs Sinic)

- **Jyotisha says quiet:** Sarvashtakavarga house 2 = **21 bindus, the second lowest**; the 2nd lord Saturn is in the 6th; the 11th lord Venus is in the 12th; and the declared 2nd/11th-lord **Dhana Yoga is absent** — the two lords are not conjunct.
- **Zi Wei says loud:** the wealth palace 财帛 holds **破軍 (Army Destroyer) at brightness +3** — a high-amplitude, disruption-and-rebuild star. In BaZi, Fire (wealth for a Water Day Master) totals 2.1 units against a moderately weak Day Master — the classical "wealth heavier than the self" configuration.

One cluster reads this as a low-emphasis area; another reads it as a high-amplitude one. They are not describing the same thing and cannot be reconciled by averaging. Both are reported.

### D4 · Partnership — DIVERGENT (both polarity and prominence)

- **Jyotisha says weak:** Sarvashtakavarga house 7 = **19 bindus — the lowest of all twelve houses**; the house is empty; its lord Mercury is retrograde.
- **Zi Wei says the opposite:** the spouse palace 夫妻 holds **紫微 (Emperor) at +2 carrying 化權, the power transformation, together with 天府 (Treasury) at +1** — the most dignified star pairing anywhere in your chart.
- **Western sits between:** the 7th ruler is the Moon, your sect light, but with no essential dignity and placed in the 8th; the **Lot of Spirit falls in the 7th**; Venus, benefic of sect and natural significator of partnership, is in the 12th.

This is the starkest contradiction in the whole chart: your weakest house by Jyotisha's own arithmetic is your strongest palace by Zi Wei's. Anyone who tells you these "really agree" is choosing one and hiding the other.

### D7 · Health and daily routine — DIVERGENT (polarity: Jyotisha vs Sinic)

This one changed when Shadbala was computed, and the change is instructive.

- **Jyotisha marks it prominent but weak.** Sarvashtakavarga gives house 6 **37 bindus, joint highest** of the twelve. But the graha sitting there is Saturn, and Shadbala puts **Saturn last of the seven at 3.77 rupas against a 5.0 requirement** — one of only two planets that fail their classical minimum. Its lord Venus is in the 12th, satisfying a **Vipareeta Raja Yoga**.
- **Western agrees on the loading:** house 6 holds Saturn, retrograde, with triplicity dignity but **contrary to sect**; the **Lot of Fortune**, which governs body and circumstance, also falls in house 6. Two of the seven Hermetic lots land there — Fortune and Courage.
- **Zi Wei says the opposite:** the health palace 疾厄 holds **太陽 at +2**, a bright benefic placement.

A high-bindu house occupied by the chart's weakest planet, against a bright star in the corresponding palace. These do not reconcile, and averaging them would be dishonest.

Read the whole domain as *routine, regimen and work-discipline being a structurally loaded area*. **No medical inference is drawn, and none should be.** This protocol makes no diagnostic, prognostic or health-outcome claim, and a symbolic system is not evidence about your body.

### D8 · Mind / education / craft — DIVERGENT (Jyotisha and Western vs Sinic)

- **Western says strong:** Mercury and Saturn are in **mutual reception by domicile** (Mercury in Capricorn, Saturn in Gemini), and **all seven dispositor chains terminate in that pair** — it is the structural terminus of your entire chart. Disciplined, technical, structure-building intelligence.
- **BaZi says under-resourced:** the Resource element (印), which governs learning support, is **Metal at 0.9 units — the weakest of your five elements**, present only as hidden 辛 in 丑 and hidden 庚 in 巳.
- **Jyotisha now sides with the Western chart, by its own arithmetic:** Shadbala makes **Mercury the strongest graha in the chart at 8.61 rupas against a 7.0 requirement**. So the Mercury–Saturn pair that the Hellenistic chart calls its structural terminus is, in Jyotisha's own strength reckoning, a pairing of the chart's **strongest and weakest planets**. That sharpens the divergence rather than settling it. Mercury is retrograde in house 1 in Purva Ashadha; Jupiter is exalted in the 8th. Zi Wei places 左輔 with **化科** — the academic transformation — but in the Friends palace 仆役 rather than in a self, career or study palace.

Two clusters now say the craft structure is the best-built thing you have; the BaZi says the fuel supply for it is the thinnest. Both are computed, and they point opposite ways. Note that Jyotisha and Western reaching the same conclusion here is **not** double-counting — one is a Shadbala total, the other a reception-and-dispositor argument, and neither derives from the shared whole-sign house frame.

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
| **T4 Intellect / craft** | high but under-fuelled | Mercury–Saturn mutual reception as chart terminus; **Mercury is the strongest graha by Shadbala (8.61 rupas)**; but the BaZi Resource element is weakest at 0.9 |
| **T5 Adaptability** | **high, all three clusters** | 貪狼 +3 and 破軍 +3; yin-Water Day Master; dual-sign Lagna with three of the seven true grahas retrograde (Mercury, Jupiter, Saturn — the nodes are retrograde by definition) |
| **T6 Discipline / structure** | high with friction | Capricorn Ascendant, Saturn in triplicity and in mutual reception; but Saturn is **last of the seven by Shadbala (3.77 rupas, below its 5.0 minimum)**, retrograde at 29°14′, sharing house 6 with Rahu |

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

What you have here is a reproducible calculation and an honest tally of where six traditional symbolic systems corroborate one another and where they contradict one another. The arithmetic is verified: three ephemeris engines agree sub-arcsecond, two independent algorithms agree on the solar terms to under a second, every structural invariant passes, and the conclusions have been tested against twelve ayanamshas, twelve house systems and five sunrise conventions.

**None of that makes any of it a validated method of prediction.** Verified inputs and correct arithmetic produce a verified chart, not a verified forecast. The agreements above are agreements between interpretive traditions — several of which, as section 3 shows, are not even as independent of each other as they appear.

And note which direction the extra rigour pushed things: measured divergence rose from 33 % to 44 % once Shadbala was computed. Better data found *more* disagreement between these traditions, not less.

Three things this document deliberately does not do: it names no favourable outcome, it makes no claim about health, lifespan, fertility, finances or legal matters, and it does not choose between schools where the schools genuinely disagree. Where your chart is ambiguous — the hour pillar, partnership, wealth, the fuel behind your craft — it is left ambiguous, because that is what the calculation actually says.

Read the strong themes as *areas your chart marks as loaded*, not as areas that will go well or badly. Nothing here is fate, and nothing here should displace your own judgement about your life.
