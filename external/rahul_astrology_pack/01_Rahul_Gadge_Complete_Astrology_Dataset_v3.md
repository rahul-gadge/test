# Rahul Gadge --- AI-Ready Master Astrology Dataset

**Version:** 3.0 --- August 2026 consolidated verification\
**Format:** Markdown\
**Purpose:** Portable source-of-truth package for analysis by ChatGPT,
Claude, Gemini, Grok, DeepSeek, or other LLMs.\
**Scope:** Traditional Vedic astrology / Jyotish data supplied by the
native across multiple reports and conversations.

> **Important:** This file intentionally preserves conflicting source
> calculations instead of silently merging them.\
> Astrology is a traditional belief system, not a scientifically
> validated predictive method.\
> An AI using this file should distinguish **raw source data**,
> **derived values**, **transcriptions**, and **interpretations**.

------------------------------------------------------------------------

# 0. Instructions for Any AI Model

When analysing this dataset:

1.  Do **not** use generic astrology when specific data is available.
2.  Keep source datasets separate when their longitudes, ascendant,
    ayanamsha, coordinates, house calculations, or dasha dates differ.
3.  Never silently "fix" contradictory values.
4.  For each major conclusion use this order where possible:
    -   D1 promise
    -   house and lord
    -   karaka
    -   dignity / avastha
    -   relevant divisional chart
    -   strength systems
    -   yoga
    -   Jaimini / Arudha / KP confirmation
    -   dasha activation
    -   transit activation if current ephemeris data is separately
        supplied
5.  Label conclusions as:
    -   Very strong
    -   Strong
    -   Moderate
    -   Weak
    -   Speculative
6.  Separate:
    -   **Raw fact**
    -   **Traditional interpretation**
    -   **Inference**
    -   **Speculation**
7.  When sources conflict, state the conflict before analysis.
8.  Do not invent missing Varga placements.
9.  D60 is birth-time-sensitive; treat it cautiously unless birth-time
    rectification is performed.
10. Never give deterministic medical, financial, legal, death-date,
    lottery, exact salary, or exact exam-score predictions from
    astrology.

------------------------------------------------------------------------

# 1. Source Registry

The master dataset has been assembled from the following source classes:

## S1 --- User-established master chart data

Data repeatedly supplied/confirmed in conversation before the Vedaansh
dossier.

## S2 --- Vedaansh Kundali Master Dossier

Premium Vedic Jyotish report computed 31 July 2026.\
Settings shown in the report include Lahiri ayanamsha, whole-sign
houses, and true nodes.

## S3 --- AstroSage Kundli

AstroSage report generated June 2026, including Panchanga, Shodashvarga
charts, Shadbala/Bhavabala, Jaimini, Varshaphala and Lal Kitab sections.

## S4 --- KP Kundali

OnlineJyotish / KP-oriented report including cuspal sub-lords,
Panchanga, D1/D9 and interpretive sections.

## S5 --- Traditional handwritten Jyotish workbook

Photographs of Sanskrit/Hindi workbook pages with handwritten planetary
positions. These are **transcriptions**, not independently recalculated
values.

## S6 --- Earlier screenshots / extracted calculation pages

Includes Vimsopaka Bala, Baladi Avastha, Ashtakavarga, Bhava Bala,
Arudha, Upapada and dasha screenshots shared in conversation.

------------------------------------------------------------------------

# 2. Native Identity and Birth Data

-   **Name:** Rahul Nathuji Gadge
-   **Gender:** Male
-   **Date of birth:** 20 January 2003
-   **Birth time:** 05:24 AM IST
-   **Birth place:** Warud, Maharashtra, India
-   **Timezone:** Asia/Kolkata (UTC+05:30)

## Coordinates --- source variants

### Vedaansh

-   Latitude: 21.4714° N
-   Longitude: 78.2829° E

### User-provided Vedaansh URL

-   Latitude: 21.4714062 N
-   Longitude: 78.2828795 E

### AstroSage report

The AstroSage PDF shows a different coordinate entry for Varud/Warud.\
Do not merge that coordinate set with the Vedaansh calculation without
checking the original report settings.

------------------------------------------------------------------------

# 3. Calculation Settings

## Vedaansh

-   Zodiac: Sidereal
-   Ayanamsha: Lahiri
-   Ayanamsha value shown: approximately 23.8997°
-   House system: Whole Sign
-   Node mode: True
-   Computed: 31 July 2026

## AstroSage

-   Ayanamsha: Lahiri
-   Ayanamsha shown: 23°53′57″ in the June 2026 report

------------------------------------------------------------------------

# 4. Critical Data Conflict Audit

There are **two materially different D1 longitude datasets** in the
material supplied.

## Dataset A --- Earlier user-established master D1

-   Ascendant: Sagittarius 25°36′
-   Sun: Capricorn 5°23′
-   Moon: Cancer 22°04′
-   Mars: Scorpio 7°47′
-   Mercury Rx: Sagittarius 19°11′
-   Jupiter Rx: Cancer 20°59′
-   Venus: Scorpio 18°44′
-   Saturn Rx: Taurus 29°16′
-   Rahu: Taurus 12°09′
-   Ketu: Scorpio 12°09′

## Dataset B --- Vedaansh 31 July 2026 D1

-   Ascendant: Sagittarius 11°35′
-   Sun: Capricorn 5°35′
-   Moon: Cancer 25°14′
-   Mars: Scorpio 7°55′
-   Mercury Rx: Sagittarius 19°04′
-   Jupiter Rx: Cancer 20°57′
-   Venus: Scorpio 18°58′
-   Saturn Rx: Taurus 29°14′
-   Rahu Rx: Taurus 13°30′
-   Ketu Rx: Scorpio 13°30′

### Consequence

The signs/houses are broadly the same in both datasets, but: - Ascendant
degree differs substantially. - Moon degree differs materially. -
Rahu/Ketu differ by over 1°. - Nakshatra padas and some sensitive
divisional-chart placements can therefore differ.

**AI instruction:** run two-layer analysis: 1. Sign/house-level
conclusions that are common to both datasets. 2. Degree-sensitive
conclusions only from the specifically named source dataset.

------------------------------------------------------------------------

# 5. D1 --- Core Sign and House Structure

Using Sagittarius rising and whole-sign houses:

  House   Sign          Lord
  ------- ------------- ---------
  1       Sagittarius   Jupiter
  2       Capricorn     Saturn
  3       Aquarius      Saturn
  4       Pisces        Jupiter
  5       Aries         Mars
  6       Taurus        Venus
  7       Gemini        Mercury
  8       Cancer        Moon
  9       Leo           Sun
  10      Virgo         Mercury
  11      Libra         Venus
  12      Scorpio       Mars

## D1 planetary house occupancy common to the supplied datasets

-   1H Sagittarius: Mercury
-   2H Capricorn: Sun
-   6H Taurus: Saturn + Rahu
-   8H Cancer: Moon + Jupiter
-   12H Scorpio: Mars + Venus + Ketu

This 1/2/6/8/12 concentration is one of the strongest structural
features of the chart.

------------------------------------------------------------------------

# 6. Planetary Dignities --- Vedaansh Dataset

  ----------------------------------------------------------------------------------
  Planet    Sign                 House Dignity   Nakshatra            Pada State
                                       in report                           
  --------- ------------- ------------ --------- ------------ ------------ ---------
  Sun       Capricorn                2 Neutral   Uttara                  3 Mrita /
                                                 Ashadha                   Swapna

  Moon      Cancer                   8 Own       Ashlesha                3 Bala /
                                                                           Jagrat

  Mars      Scorpio                 12 Own       Anuradha                2 Vriddha /
                                                                           Jagrat

  Mercury   Sagittarius              1 Neutral   Purva                   2 Vriddha /
  Rx                                             Ashadha                   Swapna

  Jupiter   Cancer                   8 Exalted   Ashlesha                2 Kumara /
  Rx                                                                       Jagrat

  Venus     Scorpio                 12 Neutral   Jyeshtha                1 Kumara /
                                                                           Swapna

  Saturn Rx Taurus                   6 Neutral   Mrigashira              2 Bala /
                                                                           Swapna

  Rahu Rx   Taurus                   6 Exalted   Rohini                  2 Yuva /
                                       in report                           Jagrat

  Ketu Rx   Scorpio                 12 Exalted   Anuradha                4 Yuva /
                                       in report                           Jagrat
  ----------------------------------------------------------------------------------

> Note: Rahu/Ketu exaltation signs differ among Jyotish traditions.
> Preserve the report's classification but do not present it as
> universally accepted.

------------------------------------------------------------------------

# 7. Panchanga

## Vedaansh / KP-consistent core data

-   Tithi: Krishna Dwitiya
-   Nakshatra: Ashlesha
-   Yoga: Ayushman
-   Karana: Garija / Gar
-   Vedic weekday: Sunday
-   Civil weekday for 20 Jan 2003: Monday
-   Moon sign: Cancer
-   Nakshatra lord: Mercury
-   Rashi lord: Moon
-   Lagna: Sagittarius
-   Lagna lord: Jupiter

## Vedaansh Nakshatra attributes

-   Nakshatra: Ashlesha
-   Pada in Vedaansh: 3
-   Deity: Sarpas / Nagas
-   Symbol: Coiled serpent
-   Nature: Tikshna
-   Yoni: Cat
-   Gana: Rakshasa
-   Nadi: Kapha / Antya
-   Shakti: Vishleshana Shakti
-   Paya: Tamra (Copper)
-   Name sound: De

## AstroSage favourable/ghatak metadata

-   Lucky number: 7
-   Good numbers: 1, 2, 3, 9
-   Lucky days: Sunday, Tuesday
-   Lucky metal: Silver
-   Lucky stone listed by report: Pearl
-   Ghatak weekday: Wednesday
-   Ghatak nakshatra: Anuradha
-   Ghatak rashi: Leo
-   Ghatak tithis: 2, 7, 12

These are **report metadata**, not empirically verified recommendations.

------------------------------------------------------------------------

# 8. Special Lagnas and Sensitive Points --- Vedaansh

  Point               Placement
  ------------------- --------------------
  Arudha Lagna (AL)   Aquarius
  Bhrigu Bindu        Gemini 19.38°
  Yogi                Venus
  Sahayogi            Sun
  Avayogi             Mars
  Bhava Lagna         Sagittarius 11.33°
  Hora Lagna          Scorpio 18.01°
  Ghati Lagna         Virgo 8.06°
  Vighati Lagna       Scorpio 18.01°
  Varnada Lagna       Cancer 11.59°
  Shri Lagna          Leo 3.21°
  Pranapada           Virgo 18.30°
  Indu Lagna          Libra 25.25°
  Bija Sphuta         Sagittarius 15.52°
  Kshetra Sphuta      Gemini 24.12°

A near-identical Vedaansh table gives minute-level variants: - Bhava
Lagna 11°19′ Sagittarius - Hora Lagna 18°00′ Scorpio - Ghati Lagna 8°03′
Virgo - Varnada 11°35′ Cancer - Shri Lagna 3°12′ Leo - Pranapada 18°17′
Virgo - Indu Lagna 25°14′ Libra

Keep both as rounding/source-output variants.

------------------------------------------------------------------------

# 9. Jaimini Chara Karakas

## Earlier user-established eight-karaka set

-   Atmakaraka (AK): Saturn
-   Amatyakaraka (AmK): Moon
-   Bhratrukaraka (BK): Jupiter
-   Matrukaraka (MK): Mercury
-   Pitrukaraka (PiK): Venus
-   Putrakaraka (PK): Rahu
-   Gnatikaraka (GK): Mars
-   Darakaraka (DK): Sun

## Vedaansh display

-   AK: Saturn
-   AmK: Moon
-   BK: Jupiter
-   MK: Mercury
-   PiK: Venus
-   GnK: Mars
-   DK: Sun
-   Putrikaraka field shown blank in one Vedaansh page

**Instruction:** preserve the earlier eight-karaka scheme if using Rahu
as PK, but note the Vedaansh display difference.

------------------------------------------------------------------------

# 10. Arudha Padas

## Earlier full Arudha set

-   AL: Aquarius
-   A2: Virgo
-   A3: Taurus
-   A4: Scorpio
-   A5: Gemini
-   A6: Aquarius
-   A7: Pisces
-   A8: Aries
-   A9: Gemini
-   A10: Sagittarius
-   A11: Sagittarius
-   A12: Leo

## Vedaansh selected Arudha table

-   AL: Aquarius
-   A2 / Dhanapada: Virgo
-   A5 / Mantrapada: Gemini
-   A7 / Darapada: Gemini
-   A10 / Rajyapada: Pisces

### Conflict note

Earlier extracted A7 and A10 differ from the later Vedaansh selected
table. Do not silently merge them.

## Upapada Lagna

Earlier supplied: - UL: Virgo - UL lord: Mercury - 12th lord relation
previously noted: Mars in Scorpio

------------------------------------------------------------------------

# 11. Divisional Charts --- Availability

The user has supplied chart material for:

-   D1 Rashi
-   D2 Hora
-   D3 Drekkana
-   D4 Chaturthamsha
-   D5 Panchamsha
-   D6 Shashtamsha
-   D7 Saptamsha
-   D9 Navamsha
-   D10 Dashamsha
-   D12 Dwadashamsha
-   D16 Shodashamsha
-   D20 Vimshamsha
-   D24 Chaturvimshamsha / Siddhamsha
-   D27 Bhamsa / Saptavimshamsha
-   D30 Trimshamsha
-   D40 Khavedamsha
-   D45 Akshavedamsha
-   D60 Shashtiamsha

## Vedaansh nine-chart Shodashavarga page

The Vedaansh dossier visually contains: D1, D2, D3, D4, D7, D9, D12,
D10, D16.

Because the parsed chart text is layout-sensitive, do not convert every
number on that page into sign placements unless the original chart image
is consulted.

## AstroSage Shodashvarga pages

AstroSage additionally supplies: - D20 - D24 - D27 - D30 - D40 - D45 -
D60

The original AstroSage PDF should be consulted for exact sign placement
if a degree-sensitive cross-Varga analysis is required.

------------------------------------------------------------------------

# 12. D9 Navamsha --- Vedaansh Visual Transcription

The Vedaansh D9 chart shows Cancer Lagna in the North-Indian style
chart.

Visible planetary labels include: - Mars \~11° - Mercury Rx \~21° -
Saturn Rx \~23° - Rahu Rx \~1° - Ketu Rx \~1° - Venus \~20° - Jupiter Rx
\~8° - Sun \~20° - Moon \~17°

**Do not infer exact signs from this text-only transcription without the
source chart layout.**

------------------------------------------------------------------------

# 13. Bhava Bala

## Earlier supplied Bhava Bala dataset

-   Average: 438.9 virupas
-   Strongest house: H4
-   Weakest house: H3
-   Strongest planet/power source noted: Jupiter

Earlier house values: - H1 570 - H2 416 - H3 176 - H4 630 - H5 413 - H6
422 - H7 576 - H8 267 - H9 385 - H10 576 - H11 422 - H12 413

## AstroSage Bhavabala table

  --------------------------------------------------------------------------------
       House   Bhavadhipati   Bhav Dig       Bhav      Total      Rupas   Relative
                       Bala       Bala    Drishti Bhava Bala                  Rank
                                             Bala                       
  ---------- -------------- ---------- ---------- ---------- ---------- ----------
           1         510.13         60      31.03     601.15      10.02          2

           2         247.64         20      42.53     310.17       5.17         12

           3         247.64         40      63.40     351.04       5.85         11

           4         510.13         60      65.46     635.58      10.59          1

           5         377.26         10      68.94     456.20       7.60          6

           6         371.17         20       3.25     394.41       6.57          9

           7         500.43          0      37.06     537.49       8.96          4

           8         351.72         20      33.41     405.13       6.75          8

           9         333.31         50       3.15     386.45       6.44         10

          10         500.43         30      18.02     548.45       9.14          3

          11         371.17         40      45.91     457.07       7.62          5

          12         377.26         10      35.63     422.88       7.05          7
  --------------------------------------------------------------------------------

This dataset also ranks H4 strongest and H2 weakest, unlike the earlier
screenshot where H3 was weakest.

------------------------------------------------------------------------

# 14. Shadbala

## Vedaansh Shadbala in Rupas

  --------------------------------------------------------------------------------------
  Planet      Sthana      Dig     Kala   Cheshta   Naisargika     Drik    Total Status
  --------- -------- -------- -------- --------- ------------ -------- -------- --------
  Sun           2.57     0.43     0.68      0.16         1.00     0.01     4.84 Weak

  Moon          2.73     0.32     2.71      1.78         0.86    -0.07     8.34 Strong

  Mars          2.62     0.75     2.28      0.32         0.29     0.24     6.50 Strong

  Mercury       3.17     0.96     2.80      0.80         0.43    -0.07     8.08 Strong

  Jupiter       3.19     0.22     4.16      0.92         0.57    -0.06     9.00 Strong

  Venus         1.91     0.31     1.41      0.73         0.71     0.10     5.18 Weak

  Saturn        1.44     0.93     1.49      0.80         0.14     0.08     4.88 Weak
  --------------------------------------------------------------------------------------

### Vedaansh rank by total

1.  Jupiter 9.00
2.  Moon 8.34
3.  Mercury 8.08
4.  Mars 6.50
5.  Venus 5.18
6.  Saturn 4.88
7.  Sun 4.84

## AstroSage Shadbala

AstroSage reports: - Sun: 5.56 rupas, ratio 1.11, rank 5 - Moon: 5.86
rupas, ratio 0.98, rank 6 - Mars: 6.29 rupas, ratio 1.26, rank 2 -
Mercury: 8.34 rupas, ratio 1.19, rank 3 - Jupiter: 8.50 rupas, ratio
1.31, rank 1 - Venus: 6.19 rupas, ratio 1.12, rank 4 - Saturn: 4.13
rupas, ratio 0.83, rank 7

### AstroSage detailed component totals (virupas)

  Planet      Sthana     Dig     Kala   Cheshta   Naisargika    Drik      Total
  --------- -------- ------- -------- --------- ------------ ------- ----------
  Sun         154.16   24.99    83.64      9.84        60.00    0.68     333.31
  Moon        178.84   18.44    53.51     53.45        51.42   -3.94     351.72
  Mars        172.07   44.20   106.48     22.92        17.16   14.41     377.26
  Mercury     201.14   56.93   172.52     48.50        25.74   -4.39     500.43
  Jupiter     191.56   13.70   218.26     55.75        34.26   -3.40     510.13
  Venus       114.83   19.47   153.86     34.02        42.84    6.14     371.17
  Saturn       86.20   56.45    43.16     48.40         8.58    4.85   \~247.64

------------------------------------------------------------------------

# 15. Vimsopaka Bala

Earlier supplied overall data: - Average: 5.76 / 20 - Strongest: Moon
8.07 / 20 - Weakest: Ketu 3.60 / 20

A Shad-Varga ranking supplied earlier: 1. Moon 9.40 2. Mars 7.30 3.
Jupiter 6.55 4. Rahu 6.05 5. Venus 5.85 6. Mercury 5.70 7. Saturn 5.50
8. Sun 3.55 9. Ketu 2.50

A separate page showed: - Sun 4.85 / 20

**Do not mix Shad-Varga and Shodasha-Varga scoring scales.**

------------------------------------------------------------------------

# 16. Baladi / Jagratadi / Deeptadi Avasthas

## Earlier supplied Baladi

-   Rahu: Yuva --- 100%
-   Ketu: Yuva --- 100%
-   Jupiter: Kumara --- 50%
-   Venus: Kumara --- 50%
-   Moon: Bala --- 25%
-   Saturn: Bala --- 25%
-   Mars: Vriddha --- 10%
-   Mercury: Vriddha --- 10%
-   Sun: Mrita --- 0%

## AstroSage Avastha table

-   Sun: Sushupta / Mrta / Mudita
-   Moon: Jagrat / Bala / Khala
-   Mars: Sushupta / Vriddha / Mudita
-   Mercury: Swapna / Vriddha / Deena
-   Jupiter: Jagrat / Kumara / Mudita
-   Venus: Swapna / Kumara / Swastha
-   Saturn: Jagrat / Bala / Mudita

Rahu/Ketu are not represented in the same classical table.

------------------------------------------------------------------------

# 17. Ashtakavarga --- Vedaansh

## Full BAV/SAV matrix

  ------------------------------------------------------------------------------------------
  Sign              Sun    Moon    Mars   Mercury   Jupiter   Venus   Saturn     SAV   Rekha
  ------------- ------- ------- ------- --------- --------- ------- -------- ------- -------
  Aries               4       4       3         2         6       4        3      26      30

  Taurus              7       4       7         7         5       3        4      37      19

  Gemini              2       2       4         5         2       2        1      18      38

  Cancer              2       6       0         3         4       5        3      23      33

  Leo                 4       4       2         4         7       6        3      30      26

  Virgo               5       6       4         5         7       4        6      37      19

  Libra               4       5       4         3         5       4        6      31      25

  Scorpio             6       1       3         5         3       4        3      25      31

  Sagittarius         4       3       5         8         4       4        3      31      25

  Capricorn           2       4       1         3         5       4        2      21      35

  Aquarius            5       4       4         6         3       7        2      31      25

  Pisces              3       6       2         3         5       5        3      27      29
  ------------------------------------------------------------------------------------------

-   SAV total: 337
-   Sodhita SAV: 99
-   Strongest signs: Taurus 37, Virgo 37
-   Next: Libra / Sagittarius / Aquarius 31
-   Weakest: Gemini 18, Capricorn 21, Cancer 23

## Sodhya Pindas --- Vedaansh

  Planet      Rasi Pinda   Graha Pinda   Total
  --------- ------------ ------------- -------
  Sun                145            85     230
  Moon               152            75     227
  Mars               129            90     219
  Mercury            163            80     243
  Jupiter            116            15     131
  Venus               72            20      92
  Saturn              69            10      79

## Earlier screenshot-based SAV values

A previous transcription gave: Aries 26, Taurus 37, Gemini 19, Cancer
24, Leo 29, Virgo 37, Libra 31, Scorpio 25, Sagittarius 31, Capricorn
21, Aquarius 30, Pisces 27.

The Vedaansh matrix above is internally summated and should be kept as
the newer report dataset rather than silently "correcting" the old
transcription.

------------------------------------------------------------------------

# 18. Yogas --- Source Detection vs Manual Audit

## Vedaansh detected yogas

1.  Raja Yoga --- Jupiter/Sun parivartana --- Moderate
2.  Raja Yoga --- Mercury/Jupiter parivartana --- Moderate
3.  Raja Yoga --- Mercury (H7 lord) conjunct Sun (H9 lord) in H1 ---
    Strong
4.  Gajakesari Yoga --- Jupiter conjunct Moon in H8 --- Strong
5.  Budhaditya Yoga --- Sun + Mercury --- Weak
6.  Vosi Yoga --- Venus 12th from Sun --- Strong
7.  Harsha Yoga --- H6 lord Venus in H12 --- Moderate
8.  Dainya Parivartana H11↔H12 --- Strong
9.  Pasha Yoga --- main planets occupy five houses --- Moderate

## Earlier manual verification performed in conversation

The following audit was made against the supplied D1 sign placements:

### Accepted / meaningful

-   Gajakesari Yoga: accepted
-   Budhaditya: accepted but weak/moderate
-   Vasi/Vosi: accepted
-   Sun--Mercury career/dharma connection: meaningful, although the
    software's house wording must be checked against the actual D1
    layout
-   Harsha/Viparita-type indication: accepted as debatable/moderate
-   Pasha: accepted as secondary

### Disputed / likely software over-detection

-   Sun--Jupiter Parivartana
-   Mercury--Jupiter Parivartana
-   Dainya Parivartana

Reason: based on the supplied sign placements, these do not appear to
satisfy a straightforward classical mutual sign exchange.

**AI instruction:** treat the report yoga list as software detections
and the manual audit as a separate interpretive layer.

## KP report yogas

KP/OnlineJyotish material also mentions: - Vasi Yoga - Viparita Raja
Yoga - Moon--Jupiter two-planet yoga - Mars--Venus two-planet yoga

------------------------------------------------------------------------

# 19. Vimshottari Dasha --- Vedaansh

## Mahadasha

  Mahadasha   Start         End
  ----------- ------------- -------------
  Mercury     19 Jan 2003   11 Feb 2009
  Ketu        11 Feb 2009   11 Feb 2016
  Venus       11 Feb 2016   11 Feb 2036
  Sun         11 Feb 2036   11 Feb 2042
  Moon        11 Feb 2042   11 Feb 2052
  Mars        11 Feb 2052   11 Feb 2059
  Rahu        11 Feb 2059   11 Feb 2077
  Jupiter     11 Feb 2077   11 Feb 2093
  Saturn      11 Feb 2093   12 Feb 2112

## Venus Mahadasha Antardashas

  Antardasha   Start         End
  ------------ ------------- -------------
  Venus        11 Feb 2016   13 Jun 2019
  Sun          13 Jun 2019   12 Jun 2020
  Moon         12 Jun 2020   11 Feb 2022
  Mars         11 Feb 2022   13 Apr 2023
  Rahu         13 Apr 2023   13 Apr 2026
  Jupiter      13 Apr 2026   12 Dec 2028
  Saturn       12 Dec 2028   11 Feb 2032
  Mercury      11 Feb 2032   12 Dec 2034
  Ketu         12 Dec 2034   11 Feb 2036

Current Vedaansh period as of the report: - Venus Mahadasha - Jupiter
Antardasha

------------------------------------------------------------------------

# 20. Yogini Dasha

## Vedaansh timeline

  Period lord   Start         End
  ------------- ------------- -------------
  Mars          19 Jan 2003   23 Jun 2004
  Mercury       23 Jun 2004   24 Jun 2009
  Saturn        24 Jun 2009   24 Jun 2015
  Venus         24 Jun 2015   24 Jun 2022
  Rahu          24 Jun 2022   24 Jun 2030
  Moon          24 Jun 2030   24 Jun 2031
  Sun           24 Jun 2031   24 Jun 2033
  Jupiter       24 Jun 2033   23 Jun 2036

Earlier supplied naming: - Bhramari - Bhadrika - Ulka - Siddha - Sankata
(Rahu) 2022--2030 - Mangala - Pingla - Dhanya

Current: Sankata / Rahu.

------------------------------------------------------------------------

# 21. Chara and Other Dasha Systems

## Vedaansh Chara --- K.N. Rao

-   Sagittarius: 19 Jan 2003 -- 19 Jan 2010
-   Scorpio: 19 Jan 2010 -- 19 Jan 2022
-   Libra: 19 Jan 2022 -- 19 Jan 2023
-   Virgo: 19 Jan 2023 -- 20 Jan 2032 --- active in that report
-   Leo: 20 Jan 2032 -- 19 Jan 2039
-   Cancer: 19 Jan 2039 -- 19 Jan 2051
-   Gemini: 19 Jan 2051 -- 19 Jan 2057
-   Taurus: 19 Jan 2057 -- 19 Jan 2063
-   Aries: 19 Jan 2063 -- 19 Jan 2070
-   Pisces: 19 Jan 2070 -- 19 Jan 2078
-   Aquarius: 19 Jan 2078 -- 19 Jan 2087
-   Capricorn: 19 Jan 2087 -- 19 Jan 2095

## Vedaansh Chara --- Rangacharya FE

-   Pisces 2003--2007
-   Aries 2007--2012
-   Taurus 2012--2022
-   Gemini 2022--2032 --- active
-   Cancer 2032--2042
-   Leo 2042--2049
-   Virgo 2049--2052
-   Libra 2052--2062
-   Scorpio 2062--2072
-   Sagittarius 2072--2077
-   Capricorn 2077--2081
-   Aquarius 2081--2090

## Earlier separately supplied Chara dataset

-   Pisces major: 20 Jan 2023 -- 20 Jan 2027
-   Capricorn subperiod: 21 May 2026 -- 20 Sep 2026

This is a different Chara calculation method/output. Preserve
separately.

## Mandook (K.N. Rao)

-   Sagittarius 2003--2011
-   Pisces 2011--2020
-   Gemini 2020--2030 --- active
-   Virgo 2030--2040
-   Capricorn 2040--2049
-   Aries 2049--2057
-   Cancer 2057--2069
-   Libra 2069--2071
-   Aquarius 2071--2075
-   Taurus 2075--2085
-   Leo 2085--2091
-   Scorpio 2091--2103

## Sthir

-   Cancer 2003--2010
-   Leo 2010--2018
-   Virgo 2018--2027 --- active
-   Libra 2027--2034
-   Scorpio 2034--2042
-   Sagittarius 2042--2051
-   Capricorn 2051--2058
-   Aquarius 2058--2066
-   Pisces 2066--2075
-   Aries 2075--2082
-   Taurus 2082--2090
-   Gemini 2090--2099

## Ashtottari

-   Moon 2003--2004
-   Mars 2004--2012
-   Mercury 2012--2029 --- active
-   Saturn 2029--2039
-   Jupiter 2039--2058
-   Rahu 2058--2070
-   Venus 2070--2091
-   Sun 2091--2097

------------------------------------------------------------------------

# 22. KP Paddhati --- Vedaansh Cuspal Table

    House Sign          Sign Lord   Star Lord   Sub Lord   Sub-Sub Lord
  ------- ------------- ----------- ----------- ---------- --------------
        1 Sagittarius   Jupiter     Ketu        Ketu       Ketu
        2 Capricorn     Saturn      Sun         Rahu       Saturn
        3 Aquarius      Saturn      Mars        Saturn     Jupiter
        4 Pisces        Jupiter     Jupiter     Moon       Saturn
        5 Aries         Mars        Ketu        Ketu       Ketu
        6 Taurus        Venus       Sun         Rahu       Saturn
        7 Gemini        Mercury     Mars        Saturn     Jupiter
        8 Cancer        Moon        Jupiter     Moon       Saturn
        9 Leo           Sun         Ketu        Ketu       Ketu
       10 Virgo         Mercury     Sun         Rahu       Saturn
       11 Libra         Venus       Mars        Saturn     Jupiter
       12 Scorpio       Mars        Jupiter     Moon       Saturn

Ruling planets shown in the report at calculation time: - Day lord:
Moon - Lagna sign lord: Jupiter - Lagna star lord: Ketu - Moon sign
lord: Moon - Moon star lord: Mercury

------------------------------------------------------------------------

# 23. Jaimini Karakamsha / Swamsha Availability

AstroSage includes: - Karakamsha chart - Swamsha chart - Sthira and
Chara Karaka table

The parsed excerpt confirms their presence but does not safely encode
every chart sign placement in linear text. Use the original AstroSage
page for exact visual placement if required.

------------------------------------------------------------------------

# 24. Varshaphala 2026 --- AstroSage

AstroSage includes a 2026 solar-return / Varshaphala section.

Report metadata: - Solar-return date: 20 Jan 2026 - Solar-return time
shown: 02:54:50 - Varsha Lagna: Scorpio - Varsha Moon sign: Capricorn -
Varsha Nakshatra: Shravana - Varsha Yoga: Siddhi - Varsha Karana:
Balava - Ayanamsha: Lahiri, approximately 24°13′13″

Do not substitute this annual chart for natal D1.

------------------------------------------------------------------------

# 25. Traditional Workbook Transcriptions

The following are transcriptions from photographed Sanskrit/Hindi
workbook pages and may use a special chart convention.

## Trimsha Chakra

1 Mars\
2 Ketu\
3 Venus\
4 Jupiter\
5 Saturn\
6 Sun\
7 Mercury\
8 Moon\
9 Rahu\
10 Mars + Jupiter\
11 blank\
12 Saturn + Ketu

## Chalit Bhava Chakra

1 Venus\
2 Saturn\
3 Mars\
4 Jupiter + Mercury\
5 blank\
6 blank\
7 blank\
8 Mars\
9 Venus\
10 Sun\
11 Moon\
12 Rahu

## Hora Chakra

1 Ketu + Jupiter\
2 blank\
3 Mars\
4 Venus + Mercury\
5 Jupiter\
6 blank\
7 blank\
8 blank\
9 blank\
10 blank\
11 blank\
12 Sun + Saturn

## Drekkana Chakra

1 Ketu\
2 Mars\
3 Saturn\
4 Rahu\
5 Mars\
6 Saturn\
7 Jupiter\
8 Saturn\
9 Sun\
10 Sun + Saturn\
11 Jupiter\
12 Ketu + Jupiter

## Saptamsha Chakra

1 Saturn\
2 Mars\
3 Jupiter\
4 Ketu\
5 Sun\
6 Mars\
7 Jupiter\
8 Rahu\
9 Jupiter\
10 Moon\
11 Saturn\
12 Mars

## Navamsha Chakra

1 Rahu\
2 Saturn\
3 Mars\
4 Mars + Jupiter\
5 Ketu\
6 Mars + Saturn\
7 Jupiter\
8 Ketu\
9 Venus\
10 Rahu + Jupiter\
11 Moon\
12 Sun

## Dwadashamsha Chakra

1 Mars + Saturn\
2 Moon + Sun\
3 Venus\
4 Ketu\
5 Mars\
6 Saturn\
7 Rahu\
8 Jupiter\
9 Mars\
10 Sun\
11 Mars\
12 Sun

**Warning:** Do not assume these numbered positions are modern
whole-sign houses without establishing the workbook convention.

------------------------------------------------------------------------

# 26. Traditional Remedies Found in Supplied Reports

These are preserved as source data, **not endorsements**.

## Rahu --- Lal Kitab / AstroSage

-   Care for / keep a black dog
-   Carry a lead nail
-   Do not harm brothers/sisters

## Ketu --- Lal Kitab / AstroSage

-   Worship Lord Ganesha
-   Maintain sexual/relationship discipline
-   Care for a dog
-   Saunf + khand under pillow was listed for sleep

## Saturn behavioural remedies

Earlier supplied report recommendations included: - kindness to needy
people - respectful treatment of helpers/service staff -
cleanliness/order around shoes/shoe rack

## Venus Mahadasha-related devotional remedy

Earlier supplied report: - Durga Stotra - symbolic white-cow donation /
related charity in the referenced tradition

## Mercury-period remedy

Earlier supplied: - Vishnu Sahasranama - food donation

## Mars/Manglik-related

Earlier supplied: - Hanuman Chalisa - Mahamrityunjaya Mantra - Hanuman
worship

## Dashavatara mapping supplied by user

-   Sun → Rama
-   Moon → Krishna
-   Mars → Narasimha
-   Mercury → Buddha
-   Jupiter → Vamana
-   Venus → Parashurama
-   Saturn → Kurma
-   Rahu → Varaha
-   Ketu → Matsya

Treat this as a devotional/traditional mapping, not a guaranteed
corrective mechanism.

------------------------------------------------------------------------

# 27. Life-Event / Validation Data Known to the AI

This section is included only to help an AI compare astrology timing
with known chronology.

-   2021--2025: B.Tech ECE
-   10 Jun 2025: joined CoPilot Networks as Trainee Engineer
-   Nov 2025: left the job
-   2026: major focus on CAT/MBA preparation
-   2026: active consideration of finance, strategy, business, investing
    and entrepreneurship
-   Relationship history/current relationship information has been
    discussed in prior conversations, but no full date-stamped
    relationship chronology is embedded here.
-   Health/fitness milestones have been discussed, but this file is not
    a medical record.

An AI should not use vague memories as "proof" of astrological accuracy.

------------------------------------------------------------------------

# 28. High-Value Analysis Questions for Another AI

Use this dataset to analyse:

## Life architecture

-   Which 5--10 factors dominate the chart?
-   Which 10% of the chart produces \~90% of traditional effects?

## Wealth

-   D1 2/5/9/10/11 houses and lords
-   D2
-   D9
-   D10
-   Indu Lagna / Shri Lagna / Hora Lagna
-   A2 / A11 where consistent
-   Ashtakavarga
-   Shadbala
-   Yogas
-   Dashas

## Career

-   10H / 10L
-   D10
-   Amatyakaraka
-   A10 / Rajyapada
-   Ghati Lagna
-   Mercury/Jupiter/Mars
-   dasha activation

## Business vs job

Compare: 1. lifelong employment 2. job → business 3. immediate
entrepreneurship 4. professional career + investing 5. career + side
business → ownership

## Marriage

-   7H / 7L
-   Venus
-   DK
-   UL
-   A7
-   D9
-   relevant dashas

## Children

-   5H / 5L
-   Jupiter
-   D7
-   Bija / Kshetra Sphuta

## Education

-   4H / 5H / 9H
-   Mercury/Jupiter
-   D24

## Property

-   4H / 4L
-   Mars
-   D4

## Spirituality

-   5H / 8H / 9H / 12H
-   Jupiter/Ketu
-   D20
-   D60 with caution

## Health

Astrological themes only; never diagnose. - 1H, 6H, 8H, 12H - Lagna
lord - Moon/Sun - D6/D30 - dasha timing

------------------------------------------------------------------------

# 29. Source-Conflict Rules for Analysis

The following conflicts must be surfaced, not hidden:

1.  Ascendant degree: \~25°36′ vs \~11°35′.
2.  Moon degree: \~22°04′ vs \~25°14′.
3.  Rahu/Ketu: \~12°09′ vs \~13°30′.
4.  Earlier full Arudha A7/A10 vs Vedaansh selected Arudha table.
5.  Earlier Bhava Bala numerical set vs AstroSage/Vedaansh later values.
6.  Earlier SAV transcription differs slightly from the later Vedaansh
    matrix.
7.  Vedaansh software detects several Parivartana yogas that a manual
    sign-exchange audit disputed.
8.  Multiple Chara Dasha calculation traditions give different active
    signs.
9.  Some reports use differing coordinate values for Warud/Varud.

The correct analytical response is to: - identify the chosen source, -
explain why it is chosen, - and avoid pretending all source systems are
identical.

------------------------------------------------------------------------

# 30. Suggested AI Analysis Protocol

For every major claim:

**Claim:**\
**Raw evidence:**\
**Relevant D1 houses/lords:**\
**Relevant Varga:**\
**Strength evidence:**\
**Yoga evidence:**\
**Jaimini/Arudha evidence:**\
**KP evidence:**\
**Dasha activation:**\
**Counter-evidence:**\
**Confidence:** Very strong / Strong / Moderate / Weak / Speculative\
**Traditional interpretation:**\
**Practical implication:**\
**What cannot be concluded:**

------------------------------------------------------------------------

# 31. Final Data Status

## Strongly populated

-   Birth identity
-   D1 sign/house structure
-   two competing longitude datasets
-   Panchanga
-   planetary dignity/nakshatra states from Vedaansh
-   special lagnas
-   Shadbala
-   Bhava Bala
-   Vimsopaka summary
-   Baladi/Jagratadi/Deeptadi
-   Ashtakavarga matrix
-   Jaimini Karakas
-   Arudha data
-   KP cuspal table
-   Vimshottari
-   Yogini
-   multiple Chara systems
-   Mandook
-   Sthir
-   Ashtottari
-   yoga detections and manual audit
-   Varshaphala availability
-   remedies
-   traditional workbook transcriptions

## Available in source PDFs but not safely flattened into text here

-   exact visual placements for every advanced Varga (especially D20,
    D24, D27, D30, D40, D45, D60)
-   exact Karakamsha/Swamsha visual chart placements
-   some astrocartography/Vastu/Sarvatobhadra graphics

For those items, another AI should preferably receive the original PDFs
alongside this master dataset if exact degree-sensitive analysis is
required.

------------------------------------------------------------------------

# 32. Universal Prompt for Another AI

Copy this after uploading the file:

> Analyse the attached `Rahul_Gadge_Complete_Astrology_Dataset_v3.md` as
> a traditional Vedic Jyotish research dataset. First perform a
> data-integrity audit and explicitly list source conflicts. Do not
> silently reconcile differing ascendant degrees, Moon degrees, Arudha
> values, Chara dasha systems, or software-detected yogas. Use only data
> actually contained in the file. For each conclusion distinguish raw
> fact, traditional interpretation, inference, and speculation.
> Cross-check D1 with relevant Vargas, strength systems, Ashtakavarga,
> Jaimini/Arudha/KP and dasha activation. Give counter-evidence for
> every major claim. Do not give deterministic medical, financial,
> death-date, lottery, exact salary, exact exam-score, or exact spouse
> predictions. If information is insufficient, say so. Start with the
> 10% of the chart that appears to drive 90% of the traditional
> interpretation, then analyse wealth, career/business, marriage,
> education, property, foreign connections, children, health themes,
> spirituality, timing windows, and remedies.

------------------------------------------------------------------------

**END OF MASTER DATASET --- VERSION 2.0**

------------------------------------------------------------------------

# 33. August 2026 Verification Update --- Drik Panchang + Vedaansh Screenshots

This section records the newest screenshots supplied directly by the
native. For the specific charts/tables below, these values supersede
older *transcriptions* when the same calculation convention is being
used. Older source variants remain preserved elsewhere in this file for
auditability.

## 33.1 Current canonical birth input used in the new screenshots

-   Name: Rahul Nathuji Gadge
-   Date: 20 January 2003
-   Time: 05:24:00 AM
-   Place: Warud, Maharashtra, India
-   Timezone: Asia/Kolkata / IST
-   Vedaansh URL coordinates previously supplied: 21.4714062 N,
    78.2828795 E

## 33.2 Drik Panchang D1 precision snapshot

The latest Drik Panchang Graha Details screenshots show the following
sidereal positions. Note that Drik Panchang simultaneously exposes
mean-node and true-node rows; do not mix them.

  -----------------------------------------------------------------------
  Body              Longitude         Nakshatra / Pada  Motion note
  ----------------- ----------------- ----------------- -----------------
  Ascendant         Sagittarius       Mula 4            ---
                    11°46′00″                           

  Sun               Capricorn         Uttara Ashadha 3  direct
                    05°35′08″                           

  Moon              Cancer 25°14′10″  Ashlesha 3        direct

  Mars              Scorpio 07°54′25″ Anuradha 2        direct

  Mercury           Sagittarius       Purva Ashadha 2   retrograde
                    19°03′37″                           

  Jupiter           Cancer 20°56′31″  Ashlesha 2        retrograde

  Venus             Scorpio 18°57′36″ Jyeshtha 1        direct

  Saturn            Taurus 29°13′57″  Mrigashira 2      retrograde

  Rahu (displayed   Taurus 12°07′16″  Rohini 1          retrograde
  node row)                                             

  Ketu (displayed   Scorpio 12°07′16″ Anuradha 3        retrograde
  node row)                                             

  True Rahu         Taurus 13°30′00″  Rohini 2          retrograde

  True Ketu         Scorpio 13°30′00″ Anuradha 4        retrograde
  -----------------------------------------------------------------------

### D1 sign/house structure under Sagittarius whole-sign rising

-   H1 Sagittarius: Mercury Rx
-   H2 Capricorn: Sun
-   H6 Taurus: Saturn Rx + Rahu
-   H8 Cancer: Moon + Jupiter Rx
-   H12 Scorpio: Mars + Venus + Ketu

### Node handling rule

Vedaansh was configured with true nodes and therefore uses approximately
13°30′ Taurus/Scorpio. The Drik Panchang table also shows an
approximately 12°07′ node pair. For degree-sensitive work, always state
whether **true** or **mean/displayed** nodes are being used.

## 33.3 Verified D2 Hora --- Drik Panchang

Purpose label on source: Wealth, Family.

  Body        D2 longitude         House Dignity shown
  ----------- ------------------ ------- ---------------
  Ascendant   Leo 23°32′00″            1 ---
  Sun         Cancer 11°10′17″        12 ---
  Moon        Leo 20°28′21″            1 ---
  Mars        Cancer 15°48′50″        12 Debilitated
  Mercury     Cancer 08°07′14″        12 ---
  Jupiter     Leo 11°53′03″            1 ---
  Venus       Leo 07°55′13″            1 ---
  Saturn      Leo 28°27′54″            1 ---
  Rahu        Cancer 24°14′33″        12 ---
  Ketu        Cancer 24°14′33″        12 ---

Classical-graha grouping: Leo/1H = Moon, Jupiter, Venus, Saturn;
Cancer/12H = Sun, Mars, Mercury, Rahu, Ketu.

## 33.4 Verified D7 Saptamsha --- Drik Panchang

Purpose label on source: Children/Progeny.

  Body        D7 longitude            House Dignity shown
  ----------- --------------------- ------- -------------------------
  Ascendant   Aquarius 22°22′01″          1 ---
  Sun         Leo 09°06′00″               7 Own sign / Moolatrikona
  Moon        Gemini 26°39′16″            5 Friend's house
  Mars        Gemini 25°20′57″            5 Enemy's house
  Mercury     Aries 13°25′22″             3 Neutral
  Jupiter     Taurus 26°35′43″            4 Enemy's house
  Venus       Virgo 12°43′16″             8 Debilitated
  Saturn      Taurus 24°37′39″            4 Friend's house
  Rahu        Capricorn 24°50′57″        12 Friend's house
  Ketu        Cancer 24°50′57″            6 Enemy's house

## 33.5 Verified D12 Dwadashamsha --- Drik Panchang

Purpose label on source: Parents.

  Body        D12 longitude          House Dignity shown
  ----------- -------------------- ------- --------------------
  Ascendant   Aries 21°12′01″            1 ---
  Sun         Pisces 07°01′43″          12 Friend's house
  Moon        Taurus 02°50′11″           2 Deep Exalted
  Mars        Aquarius 04°53′03″        11 Neutral
  Mercury     Cancer 18°43′29″           4 Enemy's house
  Jupiter     Pisces 11°18′23″          12 Own house
  Venus       Gemini 17°31′20″           3 Friend's house
  Saturn      Aries 20°47′24″            1 Debilitated
  Rahu        Virgo 25°27′21″            6 Moolatrikona shown
  Ketu        Pisces 25°27′21″          12 Moolatrikona shown

## 33.6 Verified D30 Trimshamsha --- Drik Panchang

Purpose label on source: Evils, Failure and Bad Luck.

  Body        D30 longitude             House Dignity shown
  ----------- ----------------------- ------- --------------------
  Ascendant   Sagittarius 23°00′04″         1 ---
  Sun         Virgo 17°34′17″              10 Neutral
  Moon        Scorpio 07°05′28″            12 Debilitated
  Mars        Virgo 27°12′39″              10 Enemy's house
  Mercury     Gemini 01°48′43″              7 Own house
  Jupiter     Capricorn 28°15′57″           2 Debilitated
  Venus       Pisces 28°48′20″              4 Exalted
  Saturn      Scorpio 06°58′31″            12 Enemy's house
  Rahu        Pisces 03°38′23″              4 Friend's house
  Ketu        Pisces 03°38′23″              4 Moolatrikona shown

## 33.7 Verified D60 Shashtiamsha --- Drik Panchang

Purpose label on source: Past birth and Karma.

  Body        D60 longitude             House Dignity shown
  ----------- ----------------------- ------- ----------------
  Ascendant   Scorpio 16°00′08″             1 ---
  Sun         Sagittarius 05°08′35″         2 Friend's house
  Moon        Virgo 14°10′57″              11 Friend's house
  Mars        Aquarius 24°25′18″            4 Neutral
  Mercury     Aquarius 03°37′26″            4 Neutral
  Jupiter     Sagittarius 26°31′55″         2 Own house
  Venus       Sagittarius 27°36′40″         2 Neutral
  Saturn      Pisces 13°57′02″              5 Neutral
  Rahu        Taurus 07°16′47″              7 Friend's house
  Ketu        Scorpio 07°16′47″             1 Friend's house

**D60 caution:** one D60 sign spans only about 30 seconds of birth time.
Treat this chart as valid for the entered time **05:24:00**, not as
proof that the birth time has been independently rectified to the
second.

## 33.8 Jaimini / Arudha verification --- Vedaansh

The newest Jaimini screenshots verify: - Atmakaraka (AK): Saturn -
Amatyakaraka (AmK): Moon - Bhratrikaraka (BK): Jupiter - Matrikaraka
(MK): Mercury - Putrakaraka/PK display: Venus in the current Vedaansh
Jaimini screen - Gnatikaraka (GK): Mars - Darakaraka (DK): Sun - Arudha
Lagna (AL): Aquarius - Upapada Lagna (UL): Scorpio in the displayed
raw-pada chart (shown as A4 · UL) - Pranapada Lagna: Virgo 18°17′55″ -
Indu Lagna: Libra 25°14′43″ - Bhrigu Bindu: Gemini 19°22′32″

### Arudha convention warning

Vedaansh explicitly states that its **raw pada** output can differ from
BPHS exceptions. Therefore the raw-pada UL/Arudha values in this section
must not be silently merged with older BPHS-style or separately
calculated pada tables.

## 33.9 Verified Chara Dasha --- K.N. Rao method, Vedaansh

The current Vedaansh Dasha screen explicitly selects **Chara Dasha (K.N.
Rao)**.

  Sign MD         Duration Start shown
  ------------- ---------- --------------------------------------
  Sagittarius           7y 20 Jan 2003 05:24 AM
  Scorpio              12y 19 Jan 2010 10:08 PM
  Libra                 1y 19 Jan 2022 07:58 PM
  **Virgo**         **9y** **20 Jan 2023 01:48 AM --- current**
  Leo                   7y 20 Jan 2032 06:10 AM
  Cancer               12y 19 Jan 2039 10:55 PM
  Gemini                6y 19 Jan 2051 08:45 PM
  Taurus                6y 19 Jan 2057 07:46 AM
  Aries                 7y 19 Jan 2063 06:36 PM
  Pisces                8y 19 Jan 2070 11:20 AM
  Aquarius              9y 19 Jan 2078 09:54 AM
  Capricorn             6y 19 Jan 2087 02:16 PM

**Canonical rule for K.N. Rao Chara analysis:** current Mahadasha is
**Virgo**, beginning 20 January 2023 and running roughly nine years. The
older "Pisces 2023--2027" Chara sequence is a different calculation
tradition and must not be substituted for this K.N. Rao timeline.

## 33.10 Verified raw Ashtakavarga matrix --- Vedaansh

The newest screenshot confirms the raw JHora/Parashara-style matrix from
Lagna. Houses correspond to Sagittarius rising: H1 Sg, H2 Cp, H3 Aq, H4
Pi, H5 Ar, H6 Ta, H7 Ge, H8 Cn, H9 Le, H10 Vi, H11 Li, H12 Sc.

  ------------------------------------------------------------------------------------------------------------------------------------
  Graha             H1 Sg    H2 Cp    H3 Aq    H4 Pi    H5 Ar    H6 Ta    H7 Ge    H8 Cn    H9 Le   H10 Vi   H11 Li   H12 Sc     Total
  -------------- -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- -------- ---------
  Sun                   4        2        5        3        4        7        2        2        4        5        4        6        48

  Moon                  3        4        4        6        4        4        2        6        4        6        5        1        49

  Mars                  5        1        4        2        3        7        4        0        2        4        4        3        39

  Mercury               8        3        6        3        2        7        5        3        4        5        3        5        54

  Jupiter               4        5        3        5        6        5        2        4        7        7        5        3        56

  Venus                 4        4        7        5        4        3        2        5        6        4        4        4        52

  Saturn                3        2        2        3        3        4        1        3        3        6        6        3        39

  **SAV**          **31**   **21**   **31**   **27**   **26**   **37**   **18**   **23**   **30**   **37**   **31**   **25**   **337**

  Ascendant             5        4        3        5        4        5        3        4        3        4        5        4        49
  contribution                                                                                                               
  row                                                                                                                        
  ------------------------------------------------------------------------------------------------------------------------------------

### SAV summary

-   Total: 337
-   Strongest: Taurus/H6 = 37 and Virgo/H10 = 37
-   Next: Sagittarius/H1, Aquarius/H3, Libra/H11 = 31
-   Weakest: Gemini/H7 = 18
-   Capricorn/H2 = 21
-   Cancer/H8 = 23

### Verified Shodhya Pindas

  Graha       Rasi Pinda   Graha Pinda   Shodhya Pinda
  --------- ------------ ------------- ---------------
  Sun                145            85             230
  Moon               152            75             227
  Mars               129            90             219
  Mercury            163            80             243
  Jupiter            116            15             131
  Venus               72            20              92
  Saturn              69            10              79

## 33.11 Verification status after August 2026 collection

### Directly re-verified in the latest screenshots

-   D1 exact Drik Panchang graha positions
-   D2 Hora
-   D7 Saptamsha
-   D12 Dwadashamsha
-   D30 Trimshamsha
-   D60 Shashtiamsha
-   Jaimini Karakas display
-   Arudha Lagna
-   Raw-pada Upapada Lagna
-   Pranapada Lagna
-   Indu Lagna
-   Bhrigu Bindu
-   K.N. Rao Chara Dasha full MD sequence
-   Full BAV matrix
-   SAV = 337
-   Shodhya Pindas

### Already present elsewhere in the source package

-   D3, D4, D9, D10, D16
-   D20, D24, D27, D40, D45
-   Panchanga
-   Vimshottari Dasha and Venus-MD antardashas
-   Yogini Dasha
-   alternate Chara/Dasha systems
-   Bhava Bala
-   Shadbala
-   Vimsopaka Bala
-   Baladi/Jagratadi/Deeptadi avasthas
-   yoga detections and manual yoga audit
-   KP cuspal data
-   Varshaphala availability
-   traditional remedies
-   life-event/validation information

## 33.12 Canonical-source hierarchy for future AI analysis

When multiple values conflict, use this hierarchy rather than averaging
them:

1.  **Latest direct Drik Panchang screenshots** for the specific D-chart
    or exact table shown there.
2.  **Latest Vedaansh Jaimini/Ashtakavarga/Dasha screenshots** for those
    named systems and conventions.
3.  **Vedaansh master dossier** for its own calculation framework.
4.  **AstroSage/KP source reports** for calculations unique to those
    systems.
5.  **Earlier user-established master values** as historical/source
    variants when not superseded by a newly verified equivalent.
6.  **Workbook/photo transcriptions** only as secondary corroboration.

Never combine values from different systems into a synthetic chart.
Preserve the source and convention next to every degree-sensitive
conclusion.

------------------------------------------------------------------------

# 34. Portable Analysis Prompt

Use this dataset as the complete supplied Jyotish research record for
Rahul Nathuji Gadge. Before answering any astrology question, identify
which calculation system and source you are using. Prefer the August
2026 verification hierarchy in §33.12 for conflicts. Cross-check D1 with
the relevant divisional chart, dignity/avastha, strength systems,
Ashtakavarga, Jaimini/Arudha/KP, dasha activation, and current transits
when timing is requested. Distinguish raw source fact from traditional
interpretation and inference. Do not manufacture missing values or
silently reconcile conflicting conventions. D60 must remain
birth-time-sensitive. Treat astrology as a traditional symbolic
framework rather than scientifically established prediction.
