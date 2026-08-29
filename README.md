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
| `SYNTHESIS.json` | Projections, cluster counting, domain grades, chronology |
| `FINAL_READING.md` | The reading. Every sentence traceable to the above |

## Engines

| Role | Engine |
|---|---|
| Primary astronomy | Swiss Ephemeris 2.10.03 (`sepl_18`, `semo_18`, `seas_18`) |
| Independent validator | JPL DE440s via Skyfield 1.55 |
| Chinese calendar / solar terms | lunar_python 1.4.8, cross-checked against Swiss Ephemeris solar-longitude crossings |
| Zi Wei Dou Shu | iztro 2.6.0 (canonical JavaScript) |
| Maya calendar | independent modular arithmetic, cross-checked against convertdate 2.4.1 |

Swiss Ephemeris and DE440s share a JPL lineage and are **not** fully independent in data origin;
this is disclosed rather than glossed. `py-iztro` was deliberately not used alongside `iztro`,
since it wraps the same logic.

## Counting rules

Three primary clusters vote: **Jyotisha**, **Western/Hellenistic**, and **Sinic** (BaZi and Zi Wei
together contribute at most one vote). Maya and Tibetan results carry **no** domain vote.

An **independence gate** applies: Jyotisha and Hellenistic house placements are mechanically
correlated (6 of 7 traditional planets share a house here, because both use whole-sign houses and
the ayanamsha shifts Ascendant and planets together), so those two clusters earn separate votes
only when at least one rests on a cluster-unique mechanism.
