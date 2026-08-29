# INPUT AUDIT

## 1. As supplied

| Field | Value |
|---|---|
| date of birth | 20 January 2003 |
| time of birth | 5:24 AM (05:24), IST |
| time certainty | Exact minutes |
| birthplace | Warud, Maharashtra, India (Amravati district) |
| gender | Male |
| current residence | Ghaziabad, Uttar Pradesh, India |
| calendar note supplied by user | _(not stated)_ |
| dst or tz uncertainty note supplied by user | _(not stated)_ |

## 2. Normalised

| Field | Value |
|---|---|
| Local civil instant | `2003-01-20T05:24:00+05:30` |
| UTC instant | `2003-01-19T23:54:00+00:00` |
| Julian Day (UT) | 2452659.495833333 |
| Delta-T applied | 64.480 s |
| IANA zone | Asia/Kolkata (tzdata 2026.3) |
| UTC offset | 5:30:00 |
| DST in effect | False |
| Civil weekday | Monday |
| Local mean solar time | 05:07:01.678 |
| Local apparent (true) solar time | **04:56:14.763** |
| Equation of time | -10.782 min |
| Longitude correction from IST meridian | -16.972 min |
| Sunrise (local) | 06:58:26 |
| Sunset (local) | 17:57:25 |
| Day length | 10.9829 h |

### Historical civil time

**Verdict: reliable.** India observed IST = UTC+05:30 with no daylight saving throughout 2003. Indian DST existed only in 1942-1945 and briefly in 1965 and 1971. The date is post-1970, so the IANA database governs and is authoritative here. No offset ambiguity.

### Vedic weekday caveat

Civil weekday is **Monday**, but the panchanga *vara* is **Sunday (Ravivara)**. The Vedic day (vara) begins at sunrise. Birth at 05:24 precedes sunrise at 06:58:26, so the panchanga weekday is still the previous day's. This affects vara-based panchanga readings only; it does not affect Vimshottari dasha, which is anchored on the Moon's nakshatra.

## 3. Location

Primary: **Warud (town), Warud tehsil, Amravati district, Maharashtra, India** — 21.4737672°N, 78.2569898°E

Source: OpenStreetMap Nominatim, relation 14221227, 'Warud (rural), Warud, Amravati, Maharashtra, 444906, India', queried 2026-08-29

> **Coordinate ambiguity recorded.** A second settlement named Warud exists in the same district, ~68 km SSW. The user named the district but not the tehsil. Treated as a coordinate-sensitivity case, not as the primary. The alternate is 20.8995723°N, 77.9013313°E.

## 4. Boundary audit

| System | Boundary | Distance | Verdict | What would change |
|---|---|---|---|---|
| jyotisha | D10 (Dasamsa) Lagna boundary | +1.86 min | CLOSE - see uncertainty ensemble | the Dasamsa Lagna sign |
| bazi | two-hour branch boundary -- TRUE SOLAR TIME convention | -3.75 min | SCHOOL-DIVERGENT - both results reported, neither selected | the HOUR pillar |
| jyotisha | D9 (Navamsa) Lagna boundary | +7.54 min | moderate | the Navamsa Lagna sign |
| jyotisha | Lagna nakshatra boundary (Mula -> Purva Ashadha) | +7.54 min | far - stable | the Lagna nakshatra and its pada |
| jyotisha | Lagna nakshatra pada boundary | +7.54 min | moderate | the Lagna pada (and with it the D9 Lagna) |
| bazi | two-hour branch boundary -- CIVIL CLOCK convention | +24.00 min | stable within the stated uncertainty | the HOUR pillar |
| ziwei | two-hour time index boundary | +24.00 min | stable within the stated uncertainty | the time index, and with it Ming/Shen palace placement and all star positions |
| jyotisha | Lagna sign boundary (Dhanu -> Makara) | +78.59 min | far - stable | the entire whole-sign house frame and the Lagna lord |
| western | sunrise / sect boundary | -94.44 min | far - stable | diurnal vs nocturnal sect, and with it every sect-based judgement |
| western | Ascendant sign boundary (Capricorn -> Aquarius) | +104.61 min | far - stable | the entire whole-sign house frame |
| bazi | midnight / late-Zi day boundary | +324.00 min | far - stable | the DAY pillar |
| ziwei | civil day boundary | +324.00 min | far - stable | the lunar day, hence star placement |
| western | Sun tropical sign boundary (Capricorn -> Aquarius) | +718.54 min | stable for the stated time, but notable | the Sun's tropical sign; the Sun sits in the final (anaretic) degree of Capricorn |
| bazi | middle term Dahan (大寒), Sun at 300 deg | -718.57 min | not pillar-relevant | nothing in the Four Pillars |
| bazi | sectional term Xiaohan (小寒), Sun at 285 deg -- month boundary | +14.23 d | far - stable | the MONTH pillar |
| bazi | sectional term Lichun (立春), Sun at 315 deg -- BaZi year boundary | -15.26 d | far - stable | the YEAR pillar: before Lichun 2003 the year is 壬午 (2002), not 癸未 (2003) |
| ziwei | lunar month / leap month | n/a | not applicable | palace placement if a leap month intervened |
| tibetan | Losar / year boundary | n/a | far - stable | the element-animal year assignment |
| maya | calendar adoption / correlation | n/a | not applicable | the Long Count if a different correlation constant were chosen |

### Notes on the close ones

- **western — Sun tropical sign boundary (Capricorn -> Aquarius)**: Sun at 29 deg 29' Capricorn. Sign is stable for this birth time, but the Sun is 0.51 deg from Aquarius, i.e. ~12 hours later the Sun changes sign.
- **bazi — two-hour branch boundary -- TRUE SOLAR TIME convention**: True solar time is 04:56:15, which is 3 min 45 s BEFORE the Mao (卯) boundary, placing the birth in the Yin (寅) hour instead. This is the single most convention-sensitive value in the whole chart.

## 5. Time-uncertainty ensemble

Stated certainty is *exact minutes*, so the truthful interval is the rounding window **±30 s**. Three instants were computed: T−30s, T, T+30s.

| Value | ±30 s (stated) | ±15 min (wider probe) |
|---|---|---|
| lagna_sign | **stable** | stable |
| lagna_nakshatra | **stable** | sensitive |
| lagna_pada | **stable** | sensitive |
| lagna_d9_sign | **stable** | sensitive |
| lagna_d10_sign | **stable** | sensitive |
| asc_tropical_sign | **stable** | stable |
| moon_nakshatra | **stable** | stable |
| moon_pada | **stable** | stable |
| moon_d9_sign | **stable** | stable |
| sun_tropical_sign | **stable** | stable |
| bazi_pillars_civil | **stable** | stable |
| bazi_pillars_true_solar | **stable** | sensitive |

The ±15 min column is **not** the user's uncertainty. It answers a different question: *which results would break if the recorded minute were itself wrong?* Everything is stable at the stated precision; the divisional-chart Lagnas and the true-solar-time hour pillar are the first things to fail if the minute is not trustworthy.

No rectification was performed and none is proposed.
