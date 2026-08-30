# RECONCILIATION — external Master Pack vs. this repository's verified chart

**External pack:** `Rahul_Gadge_All_Astrology_Data_Master_Pack_20260830`, dated 30 Aug 2026.
**Adjudicated against:** this repo's independently computed chart — Swiss Ephemeris primary,
JPL DE440s and the Moshier analytic ephemeris as validators, agreeing to 0.0026″.

The pack's own rule is *"when values conflict, do not synthesize an average chart."*
That rule is followed here. Nothing is averaged; each conflict is decided on evidence.

---

## 1. The two-dataset conflict — RESOLVED

The pack flags "two materially different D1 longitude datasets" and asks for a two-layer
analysis. That caution is no longer necessary: one of them is arithmetically wrong.

| Body | **Verified** | Dataset A | error | Dataset B (Vedaansh) | error |
|---|---|---|---:|---|---:|
| Ascendant | 11°33.8′ | 25°36′ | **+842.2′** | 11°35′ | +1.2′ |
| Sun | 5°35.8′ | 5°23′ | −12.8′ | 5°35′ | −0.8′ |
| Moon | 25°14.7′ | 22°04′ | **−190.7′** | 25°14′ | −0.7′ |
| Mars | 7°55.1′ | 7°47′ | −8.1′ | 7°55′ | −0.1′ |
| Mercury | 19°04.3′ | 19°11′ | +6.7′ | 19°04′ | −0.3′ |
| Jupiter | 20°57.2′ | 20°59′ | +1.8′ | 20°57′ | −0.2′ |
| Venus | 18°58.3′ | 18°44′ | −14.3′ | 18°58′ | −0.3′ |
| Saturn | 29°14.6′ | 29°16′ | +1.4′ | 29°14′ | −0.6′ |
| Rahu | 12°07.7′ mean · 13°30.4′ true | 12°09′ | +1.3′ vs **mean** | 13°30′ | −0.4′ vs **true** |

### Verdict

- **Dataset B (Vedaansh) is CORRECT.** Maximum error 1.2 arcminutes across every body —
  consistent with rounding to the arcminute. Its nodes match the **true** node to 0.4′,
  confirming the pack's statement that Vedaansh uses true nodes.
- **Dataset A is SUPERSEDED and should be retired, not preserved as a variant.**

### Why Dataset A is wrong — root cause identified

Back-solving the birth time each Dataset A value would require gives a **4.9-hour spread**.
A single real birth moment yields one time for every body, so Dataset A is not a chart for a
different time — it is not a valid chart for *any* time.

Testing the obvious hypothesis: recompute for **2003-01-19 23:54 treated as local time** —
i.e. the correct UTC instant fed back in without converting to IST, a classic
double-conversion error.

| Body | Dataset A | timezone-error hypothesis | diff |
|---|---|---|---:|
| Sun | 5°23′ | 5°21.8′ | 1.2′ |
| Moon | 22°04′ | 22°03.7′ | 0.3′ |
| Mars | 7°47′ | 7°46.2′ | 0.8′ |
| Mercury | 19°11′ | 19°10.7′ | 0.3′ |
| Jupiter | 20°59′ | 20°58.9′ | 0.1′ |
| Venus | 18°44′ | 18°43.6′ | 0.4′ |
| Saturn | 29°16′ | 29°15.4′ | 0.6′ |
| Rahu | 12°09′ | 12°08.4′ | 0.6′ |

**Mean absolute error: 0.5′** against the timezone-error hypothesis, versus 119.9′ against
the true birth time. Dataset A's planets were computed with the timezone applied in the
wrong direction.

**But its Ascendant fits neither time.** At the erroneous instant the Lagna would be
**Virgo 27°24′**, not Sagittarius 25°36′. So Dataset A is a **composite of at least two
incompatible calculations** — mis-timed planets bolted to an Ascendant from a third source.

That also explains the 25°36′ figure that has been circulating in the older records.
It has no valid derivation.

---

## 2. Jaimini Chara Karakas — CONFIRMED, all eight

Computed from the same longitudes, 8-body scheme with Rahu counted in reverse:

| | Karaka | Degree | Pack's earlier set |
|---|---|---:|---|
| AK | Saturn | 29.243° | ✅ match |
| AmK | Moon | 25.245° | ✅ match |
| BK | Jupiter | 20.953° | ✅ match |
| MK | Mercury | 19.071° | ✅ match |
| PiK | Venus | 18.971° | ✅ match |
| PK | Rahu | 17.872° | ✅ match |
| GK | Mars | 7.918° | ✅ match |
| DK | Sun | 5.596° | ✅ match |

**All eight match exactly.** The Vedaansh page that left Putrikaraka blank is simply
incomplete, not in conflict — Rahu at 17.872° occupies that slot unambiguously.

Note that **Saturn is the Atmakaraka and is also the weakest planet in the chart**
(Shadbala 3.77 rupas against a 5.0 minimum, last of seven). Both facts are computed here.

---

## 3. Arudha padas — the A7 / A10 conflict RESOLVED in favour of the earlier set

The classical rule: if a pada falls in the same sign as its own house, or the 7th from it,
take the 10th from that result instead.

| Pada | **Computed** | Earlier set | Vedaansh | Exception needed? | Verdict |
|---|---|---|---|---|---|
| A1 | Aquarius | Aquarius | Aquarius | no | all agree |
| A2 | Virgo | Virgo | Virgo | no | all agree |
| A5 | Gemini | Gemini | Gemini | no | all agree |
| **A7** | **Pisces** | Pisces | Gemini | **yes** | **earlier set correct** |
| **A10** | **Sagittarius** | Sagittarius | Pisces | **yes** | **earlier set correct** |

All twelve computed padas match the earlier full set. The diagnostic is clean:

> Of the five padas Vedaansh displays, the **three that need no exception all agree**, and
> the **two that require the exception rule both differ**. Vedaansh is not applying the
> 1st/7th exception. This is a systematic omission, not a school difference.

Six of the twelve padas require the exception, so this affects more than the two disputed
values — treat the whole Vedaansh Arudha table as unreliable and use the computed set.

---

## 4. Sarvashtakavarga — agreement within table variance

| House | This repo | Vedaansh | diff |
|---|---:|---:|---:|
| 1 | 31 | 31 | 0 |
| 2 | 21 | 21 | 0 |
| 3 | 31 | 31 | 0 |
| 4 | 26 | 27 | +1 |
| 5 | 26 | 26 | 0 |
| 6 | 37 | 37 | 0 |
| 7 | 19 | 18 | −1 |
| 8 | 24 | 23 | −1 |
| 9 | 29 | 30 | +1 |
| 10 | 37 | 37 | 0 |
| 11 | 31 | 31 | 0 |
| 12 | 25 | 25 | 0 |
| **Total** | **337** | **337** | 0 |

Eight of twelve identical; four differ by exactly one bindu, netting to zero. Both satisfy
the 337 invariant. This is ordinary variance between BAV table transcriptions, not an error
in either.

**Every rank-order conclusion survives:** house 7 lowest in both, houses 6 and 10 joint
highest in both, house 2 second-lowest in both. No claim in the dashboard depends on the
four disputed bindus.

---

## 5. Net effect on this repository

| Item | Change |
|---|---|
| Ascendant, all planets | **No change.** Vedaansh independently corroborates to ≤1.2′ |
| Chara Karakas | **No change.** All eight independently confirmed |
| Arudha Lagna (Aquarius) | **No change.** Confirmed by both sources and computation |
| Arudha A7 / A10 | Conflict resolved; computed values stand |
| Sarvashtakavarga | **No change.** Within table variance; conclusions unaffected |
| Dataset A / the 25°36′ Ascendant | **Retired.** Root cause identified as a timezone error plus a foreign Ascendant |

The external pack did not change a single conclusion in this repository. It did something
more useful: it **independently corroborated the chart from a different toolchain**, and
supplied two conflicts that could be settled by computation rather than authority.

---

## 6. Node convention — a standing caution

The pack is right to insist this be stated every time. In this chart it matters more than
usual, because **Rahu sits at 12°07.7′ (mean) or 13°30.4′ (true) — a 1.4° difference**,
and that gap has real consequences. Both fall in **Rohini**, so the nakshatra is stable — but
the **pada changes from 1 to 2** (Rohini pada 1 under mean nodes, pada 2 under true), and
Rahu's **D9 shifts from Aries to Taurus**. Its D10 is Taurus either way. So pada-level and
D9 claims about Rahu depend on which convention you picked; D10 claims do not.

- This repository uses **mean nodes** as primary, with true nodes computed and retained.
- Vedaansh uses **true nodes**.
- Neither is wrong. Never mix them in a single reading.
