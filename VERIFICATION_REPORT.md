# VERIFICATION REPORT

**30 material data verified. 0 failures or alerts.**

Largest primary-vs-validator disagreement across all ten bodies: **0.0026 arcseconds** (0.00000071°), against an alert threshold of 0.01°.

## Engine independence — disclosed honestly

> Swiss Ephemeris .se1 files are compressed from a JPL DE integration (DE431 lineage); Skyfield here reads JPL DE440s. The two are therefore NOT fully independent in data lineage, but they are separate code paths and separate DE releases. Agreement is reported as a code-and-release cross-check, not as independent observational confirmation. lunar_python's solar-term algorithm and the Maya modular arithmetic ARE independent of both. py-iztro was deliberately NOT used alongside iztro, since it wraps the same logic and would not constitute a second method.

### A frame mismatch was found and fixed before any claim was made

The first comparison showed a **constant 14.168″ offset on every single body** — the signature of a reference-frame error, not an ephemeris difference. It was identified as the nutation in longitude (Δψ = −14.168017″ at this instant): Skyfield's `ecliptic_latlon(epoch=t)` returns the *true* equinox of date, so it had to be compared against Swiss Ephemeris apparent positions rather than against its mean-equinox (`FLG_NONUT`) output. After matching the frames, agreement fell to 0.0026″. Averaging the two engines was never considered.

## Full verification table

| System | Datum | Primary | Validator | Difference | Stability | Confidence | Status |
|---|---|---|---|---|---|---|---|
| shared_astronomy | Sun tropical apparent longitude | 299.492243 | JPL DE440s via Skyfield 1.55 | 0.0003″ | stable | high | pass |
| shared_astronomy | Moon tropical apparent longitude | 139.141133 | JPL DE440s via Skyfield 1.55 | 0.0026″ | stable | high | pass |
| shared_astronomy | Mercury tropical apparent longitude | 282.967107 | JPL DE440s via Skyfield 1.55 | 0.0002″ | stable | high | pass |
| shared_astronomy | Venus tropical apparent longitude | 252.866689 | JPL DE440s via Skyfield 1.55 | 0.0003″ | stable | high | pass |
| shared_astronomy | Mars tropical apparent longitude | 241.813593 | JPL DE440s via Skyfield 1.55 | 0.0000″ | stable | high | pass |
| shared_astronomy | Jupiter tropical apparent longitude | 134.848351 | JPL DE440s via Skyfield 1.55 | 0.0000″ | stable | high | pass |
| shared_astronomy | Saturn tropical apparent longitude | 83.139033 | JPL DE440s via Skyfield 1.55 | 0.0001″ | stable | high | pass |
| shared_astronomy | Uranus tropical apparent longitude | 327.187156 | JPL DE440s via Skyfield 1.55 | 0.0000″ | stable | high | pass |
| shared_astronomy | Neptune tropical apparent longitude | 310.247897 | JPL DE440s via Skyfield 1.55 | 0.0001″ | stable | high | pass |
| shared_astronomy | Pluto tropical apparent longitude | 258.920612 | JPL DE440s via Skyfield 1.55 | 0.0001″ | stable | high | pass |
| shared_astronomy | Ascendant (tropical) | 275.459414 | — | — | stable | high | pass |
| shared_astronomy | ayanamsha (Lahiri) at birth | 23.899716 | — | — | stable | high | pass |
| shared_astronomy | Rahu-Ketu opposition invariant (mean node) | 180.000000 | — | — | stable | high | pass |
| bazi | solar term Xiaohan 小寒 instant | 2003-01-06T02:27:43.091683 | lunar_python 1.4.8 (independent solar-term algorithm) | 330.0588″ | stable | high | pass |
| bazi | solar term Dahan 大寒 instant | 2003-01-20T19:52:34.195820 | lunar_python 1.4.8 (independent solar-term algorithm) | -2895.0480″ | stable | high | pass |
| bazi | solar term Lichun 立春 instant | 2003-02-04T14:05:19.632746 | lunar_python 1.4.8 (independent solar-term algorithm) | -1322.1144″ | stable | high | pass |
| bazi | Vimshottari cycle total (years) | 120 | — | — | stable | high | pass |
| jyotisha | Ashtakavarga row totals | _(structured)_ | — | — | stable | medium | pass |
| western | Egyptian bounds table | _(structured)_ | — | — | stable | high | pass |
| ziwei | 12 unique palaces | 12 | — | — | stable | high | pass |
| ziwei | 14 major stars placed | 14 | — | — | stable | high | pass |
| ziwei | Four Transformations match the classical 壬 (Ren) year ru | _(structured)_ | classical 壬年四化 rule applied by hand | — | stable | high | pass |
| ziwei | Ming palace branch | xu | hand rule: 寅 + (lunar month - 1) - hour index | — | stable | high | pass |
| ziwei | Shen (body) palace branch | chen | hand rule: 寅 + (lunar month - 1) + hour index | — | stable | high | pass |
| maya | long_count | 12.19.9.16.17 | convertdate 2.4.1 | +0.0 s | stable | high | pass |
| maya | tzolkin | 8 Caban | convertdate 2.4.1 | +0.0 s | stable | high | pass |
| maya | haab | 10 Muwan | convertdate 2.4.1 | +0.0 s | stable | high | pass |
| maya | Gregorian round-trip | [2003, 1, 20] | — | — | stable | high | pass |
| maya | external anchor 2012-12-21 | 13.0.0.0.0 | published reference value | — | stable | high | pass |
| tibetan | year element-animal | Water Male Horse | BaZi year pillar from lunar_python (shared 60-cycle) | — | stable | medium | pass |

## Invariants

| Invariant | Required | Result |
|---|---|---|
| Rahu–Ketu separation (mean node) | exactly 180.000° | 180.000000° — pass |
| Vimshottari cycle total | 120 years | 120 — pass |
| Ashtakavarga per-planet totals | 48/49/39/54/56/52/39 | all match — pass |
| Sarvashtakavarga grand total | 337 | 337 — pass |
| Egyptian bounds, each sign | 30° | all 12 signs — pass |
| Egyptian bounds, per planet | 57/79/66/82/76 = 360° | all match — pass |
| Zi Wei distinct palaces | 12 | 12 — pass |
| Zi Wei major stars placed | 14 | 14 — pass |
| Zi Wei Four Transformations | classical 壬-year rule | 天梁祿 / 紫微權 / 左輔科 / 武曲忌 — pass |
| Zi Wei Ming palace | 寅 + (month−1) − hour index | (2+11−3) mod 12 = 戌 — pass |
| Zi Wei Shen palace | 寅 + (month−1) + hour index | (2+11+3) mod 12 = 辰 — pass |
| Maya Gregorian round-trip | exact | 2003-01-20 — pass |
| Maya external anchor | 2012-12-21 = 13.0.0.0.0, 4 Ahau 3 Kankin | reproduced — pass |
| Solar-term instants | < 120 s between two independent algorithms | ≤ 0.8 s — pass |
| Timing periods | continuous, ordered, non-overlapping | pass |

## Methods deliberately NOT used

- **py-iztro** was not run alongside iztro. It wraps the same logic; using both would have produced a fake second opinion.

## Unavailable / omitted

| Item | Status | Reason |
|---|---|---|
| Jyotisha Shadbala | unavailable | No validated implementation was available; approximating a six-component strength score would have invented numbers. |
| Tibetan mewa | omitted | omitted - no validated lineage-specific implementation or anchor available |
| Tibetan parkha | omitted | omitted - no validated lineage-specific implementation or anchor available |
| Tibetan la_force | omitted | omitted - anchor formulas not validated |
| Tibetan srog_life_force | omitted | omitted - anchor formulas not validated |
| Tibetan lu_body_force | omitted | omitted - anchor formulas not validated |
| Tibetan wangthang_power | omitted | omitted - anchor formulas not validated |
| Tibetan lungta_windhorse | omitted | omitted - anchor formulas not validated |
| Tibetan annual_relations_and_obstacles | omitted | omitted - depends on the omitted personal-force anchors |
| BaZi Yong Shen (Useful God) | not asserted | Useful-God selection is school-dependent and the hour pillar itself diverges by school here. Asserting one favourable element would hide that divergence. |
| Maya day-sign personality | not asserted | No classical or living-lineage source. |
