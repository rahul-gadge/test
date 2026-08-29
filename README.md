# Six-Culture Verified Chart

A reproducible birth-chart computation across six traditions — Jyotisha, BaZi, Western/Hellenistic,
Zi Wei Dou Shu, the Maya calendar, and Tibetan elemental astrology — built for **calculation
accuracy, convention transparency, and honest uncertainty** rather than for prediction.

> This is computed symbolic corroboration among traditional systems. It is **not** a validated
> forecast, carries no causal claim, and makes no medical, lifespan, fertility, financial or legal
> statement.

## Reproducing

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
npm install
./scripts/fetch_ephemeris.sh          # verify checksums against CALCULATION_MANIFEST.json
node scripts/ziwei.js      2003-01-20 3 male            > out/ziwei_raw.json
node scripts/ziwei_horo.js 2003-01-20 3 male 2026-08-29 > out/ziwei_horo.json
.venv/bin/python build.py             # -> MASTER_DATASET.json, CALCULATION_MANIFEST.json, VERIFICATION_REPORT.json
.venv/bin/python synthesize.py        # -> SYNTHESIS.json
.venv/bin/python report.py            # -> INPUT_AUDIT.md, VERIFICATION_REPORT.md, MASTER_DATASET.md
.venv/bin/python precision_report.py  # -> PRECISION_REPORT.md
```

`build.py` is parameterised entirely by `BIRTH_INPUT.json`; no birth data is hardcoded in the
calculation logic. Rebuilds are byte-identical apart from timestamps and checksums.

## Outputs

| File | Contents |
|---|---|
| `BIRTH_INPUT.json` | Original input, normalisation, coordinates and their source |
| `INPUT_AUDIT.md` | Civil-time audit, boundary distances, uncertainty ensemble |
| `CALCULATION_MANIFEST.json` | Versions, ephemeris checksums, every declared convention |
| `MASTER_DATASET.json` / `.md` | All computed facts. No interpretation |
| `VERIFICATION_REPORT.json` / `.md` | 30 verified data, invariants, disclosed engine independence |
| `PRECISION_REPORT.md` | Which convention choices change which conclusions: 12 ayanamshas, 12 house systems, 5 sunrise conventions, 3 combustion tables, geocentric vs topocentric, all 16 vargas with per-varga stability, Shadbala, Yong Shen by school |
| `SYNTHESIS.json` | Projections, cluster counting, domain grades, chronology |
| `FINAL_READING.md` | The reading. Every sentence traceable to the above |

## Engines

| Role | Engine |
|---|---|
| Primary astronomy | Swiss Ephemeris 2.10.03 (`sepl_18`, `semo_18`, `seas_18`) |
| Independent validator | JPL DE440s via Skyfield 1.55 |
| Third, analytic engine | Moshier (`swe FLG_MOSEPH`) — no data files, mathematically independent of both |
| Chinese calendar / solar terms | lunar_python 1.4.8, cross-checked against Swiss Ephemeris solar-longitude crossings |
| Zi Wei Dou Shu | iztro 2.6.0 (canonical JavaScript) |
| Maya calendar | independent modular arithmetic, cross-checked against convertdate 2.4.1 |

Swiss Ephemeris and DE440s share a JPL lineage and are **not** fully independent in data origin;
this is disclosed rather than glossed. The Moshier analytic ephemeris is independent of both, and
agrees to 0.52″ at worst. `py-iztro` was deliberately not used alongside `iztro`,
since it wraps the same logic.

## Coverage

Jyotisha: all sixteen vargas (Shodasavarga) with per-varga stability against the stated time
uncertainty; full panchanga; Shadbala (five components exact, Cheshta approximated and flagged);
Sarvashtakavarga; Vimshottari to three levels under two year-length conventions; a closed yoga
whitelist. Western: essential dignity with Egyptian bounds and Dorothean triplicities, sect from
the true horizon, the seven Hermetic lots, profection, solar returns at birthplace and relocated,
Zodiacal Releasing L1. Sinic: Four Pillars under three time conventions, Ten Gods, branch and stem
relations, Da Yun, annual pillars, Yong Shen under three named schools; Zi Wei via canonical iztro
with hand-verified palace and 四化 rules.

Convention sensitivity is computed rather than assumed: 12 ayanamshas, 12 house systems, 5 sunrise
conventions, 3 combustion tables, and geocentric vs topocentric are each run in full, and
`PRECISION_REPORT.md` records which conclusions move and which do not.

## Counting rules

Three primary clusters vote: **Jyotisha**, **Western/Hellenistic**, and **Sinic** (BaZi and Zi Wei
together contribute at most one vote). Maya and Tibetan results carry **no** domain vote.

An **independence gate** applies: Jyotisha and Hellenistic house placements are mechanically
correlated (6 of 7 traditional planets share a house here, because both use whole-sign houses and
the ayanamsha shifts Ascendant and planets together), so those two clusters earn separate votes
only when at least one rests on a cluster-unique mechanism.
