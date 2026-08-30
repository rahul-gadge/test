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

## Period forecaster

`forecast.py` reports which life domains the traditions **flag as salient** in a window,
with exact dates and the computed basis. It does **not** predict events, outcomes, or
whether anything will go well — the registry maps to domain salience only, and there is
no verb vocabulary in it, so outcome, health, lifespan, fertility, financial and legal
claims are structurally impossible to emit.

```bash
./forecast.py --on 2026-08-29                    # what is active on one date
./forecast.py --from 2026-01-01 --to 2031-01-01  # activation windows in a range
./forecast.py --years 5 --log                    # seal a forecast for later scoring
./forecast.py --score forecast_log/outcomes_template_*.json
```

Two rules keep it from manufacturing agreement:

- **Each cluster votes with its finest active period,** and that vote counts only if the
  period is within 4x the window length. A ten-year Zi Wei decadal palace is constant
  background across a nine-month window — it cannot discriminate that window from any
  other inside the decade, so it is reported separately and not counted. Without this
  rule the engine reported the current window as STRONG 3/3; with it, it reproduces the
  synthesis's MODERATE 2/3.
- **BaZi and Zi Wei together contribute one vote,** as everywhere else in the project.

`--log` seals a forecast with a content hash and writes an outcomes template. Fill in
which domains actually turned out notable, then `--score` compares hits against an exact
hypergeometric baseline — the chance of overlap if the same number of domains had been
flagged at random. Scoring is grouped by time window, not by (window, domain) pair, and
refuses to run if the sealed file was edited after the fact. It reports its own sample-size
limits and the biases it cannot control.

## Counting rules

Three primary clusters vote: **Jyotisha**, **Western/Hellenistic**, and **Sinic** (BaZi and Zi Wei
together contribute at most one vote). Maya and Tibetan results carry **no** domain vote.

An **independence gate** applies: Jyotisha and Hellenistic house placements are mechanically
correlated (6 of 7 traditional planets share a house here, because both use whole-sign houses and
the ayanamsha shifts Ascendant and planets together), so those two clusters earn separate votes
only when at least one rests on a cluster-unique mechanism.
