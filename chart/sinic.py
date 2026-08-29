"""BaZi (Four Pillars) with declared schools and a transparent strength rule set."""
import datetime as dt
from lunar_python import Solar

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
STEM_EL = {"甲":"Wood","乙":"Wood","丙":"Fire","丁":"Fire","戊":"Earth",
           "己":"Earth","庚":"Metal","辛":"Metal","壬":"Water","癸":"Water"}
STEM_YIN = {"甲":False,"乙":True,"丙":False,"丁":True,"戊":False,
            "己":True,"庚":False,"辛":True,"壬":False,"癸":True}
BRANCH_EL = {"子":"Water","丑":"Earth","寅":"Wood","卯":"Wood","辰":"Earth","巳":"Fire",
             "午":"Fire","未":"Earth","申":"Metal","酉":"Metal","戌":"Earth","亥":"Water"}
BRANCH_ANIMAL = {"子":"Rat","丑":"Ox","寅":"Tiger","卯":"Rabbit","辰":"Dragon","巳":"Snake",
                 "午":"Horse","未":"Goat","申":"Monkey","酉":"Rooster","戌":"Dog","亥":"Pig"}
STEM_PY = {"甲":"Jia","乙":"Yi","丙":"Bing","丁":"Ding","戊":"Wu",
           "己":"Ji","庚":"Geng","辛":"Xin","壬":"Ren","癸":"Gui"}
BRANCH_PY = {"子":"Zi","丑":"Chou","寅":"Yin","卯":"Mao","辰":"Chen","巳":"Si",
             "午":"Wu","未":"Wei","申":"Shen","酉":"You","戌":"Xu","亥":"Hai"}

# hidden stems: main qi, then secondary, then residual
HIDDEN = {"子":["癸"],"丑":["己","癸","辛"],"寅":["甲","丙","戊"],"卯":["乙"],
          "辰":["戊","乙","癸"],"巳":["丙","庚","戊"],"午":["丁","己"],"未":["己","丁","乙"],
          "申":["庚","壬","戊"],"酉":["辛"],"戌":["戊","辛","丁"],"亥":["壬","甲"]}

PRODUCES = {"Wood":"Fire","Fire":"Earth","Earth":"Metal","Metal":"Water","Water":"Wood"}
CONTROLS = {"Wood":"Earth","Earth":"Water","Water":"Fire","Fire":"Metal","Metal":"Wood"}
PRODUCED_BY = {v:k for k,v in PRODUCES.items()}
CONTROLLED_BY = {v:k for k,v in CONTROLS.items()}

TEN_GOD_EN = {"比肩":"Friend (Bi Jian)","劫财":"Rob Wealth (Jie Cai)","食神":"Eating God (Shi Shen)",
  "伤官":"Hurting Officer (Shang Guan)","偏财":"Indirect Wealth (Pian Cai)","正财":"Direct Wealth (Zheng Cai)",
  "七杀":"Seven Killings (Qi Sha)","正官":"Direct Officer (Zheng Guan)","偏印":"Indirect Resource (Pian Yin)",
  "正印":"Direct Resource (Zheng Yin)","日主":"Day Master"}

SIX_HARM = [("子","未"),("丑","午"),("寅","巳"),("卯","辰"),("申","亥"),("酉","戌")]
SIX_CLASH = [("子","午"),("丑","未"),("寅","申"),("卯","酉"),("辰","戌"),("巳","亥")]
SIX_COMBINE = [("子","丑"),("寅","亥"),("卯","戌"),("辰","酉"),("巳","申"),("午","未")]
DESTRUCTION = [("子","酉"),("卯","午"),("辰","丑"),("未","戌"),("寅","亥"),("巳","申")]
TRINE = [("申","子","辰","Water"),("亥","卯","未","Wood"),("寅","午","戌","Fire"),("巳","酉","丑","Metal")]
DIRECTIONAL = [("寅","卯","辰","Wood"),("巳","午","未","Fire"),("申","酉","戌","Metal"),("亥","子","丑","Water")]
PUNISH_TRIPLE = [("寅","巳","申"),("丑","未","戌")]
PUNISH_SELF = ["辰","午","酉","亥"]
PUNISH_UNGRATEFUL = ("子","卯")
STEM_COMBINE = [("甲","己","Earth"),("乙","庚","Metal"),("丙","辛","Water"),
                ("丁","壬","Wood"),("戊","癸","Fire")]

# Transparent weighting scheme -- DECLARED HERE, not a classical authority.
W_MONTH_BRANCH, W_DAY_BRANCH, W_OTHER_BRANCH, W_STEM = 3.0, 2.0, 1.5, 1.0
W_HIDDEN = [0.60, 0.30, 0.10]


def pillars_for(y, m, d, hh, mi, ss, gender_male=True):
    ec = Solar.fromYmdHms(y, m, d, hh, mi, ss).getLunar().getEightChar()
    gz = [ec.getYear(), ec.getMonth(), ec.getDay(), ec.getTime()]
    names = ["year", "month", "day", "hour"]
    tg_gan = [ec.getYearShiShenGan(), ec.getMonthShiShenGan(), ec.getDayShiShenGan(), ec.getTimeShiShenGan()]
    tg_zhi = [ec.getYearShiShenZhi(), ec.getMonthShiShenZhi(), ec.getDayShiShenZhi(), ec.getTimeShiShenZhi()]
    nayin = [ec.getYearNaYin(), ec.getMonthNaYin(), ec.getDayNaYin(), ec.getTimeNaYin()]
    out = {}
    for i, nm in enumerate(names):
        st, br = gz[i][0], gz[i][1]
        out[nm] = {
            "ganzhi": gz[i], "stem": st, "branch": br,
            "stem_pinyin": STEM_PY[st], "branch_pinyin": BRANCH_PY[br],
            "stem_element": STEM_EL[st], "stem_polarity": "yin" if STEM_YIN[st] else "yang",
            "branch_element": BRANCH_EL[br], "branch_animal": BRANCH_ANIMAL[br],
            "hidden_stems": HIDDEN[br],
            "hidden_stem_elements": [STEM_EL[x] for x in HIDDEN[br]],
            "ten_god_stem": tg_gan[i], "ten_god_stem_en": TEN_GOD_EN.get(tg_gan[i], tg_gan[i]),
            "ten_gods_hidden": tg_zhi[i],
            "ten_gods_hidden_en": [TEN_GOD_EN.get(x, x) for x in tg_zhi[i]],
            "na_yin": nayin[i],
        }
    return out, ec


def element_tally(p):
    """Weighted element tally under the declared scheme."""
    tally = {e: 0.0 for e in ["Wood", "Fire", "Earth", "Metal", "Water"]}
    detail = []
    bw = {"year": W_OTHER_BRANCH, "month": W_MONTH_BRANCH,
          "day": W_DAY_BRANCH, "hour": W_OTHER_BRANCH}
    for nm, pill in p.items():
        tally[pill["stem_element"]] += W_STEM
        detail.append({"source": f"{nm} stem {pill['stem']}", "element": pill["stem_element"], "weight": W_STEM})
        w = bw[nm]
        for k, hs in enumerate(pill["hidden_stems"]):
            ww = w * (W_HIDDEN[k] if k < len(W_HIDDEN) else 0.1)
            tally[STEM_EL[hs]] += ww
            detail.append({"source": f"{nm} branch {pill['branch']} hidden {hs}",
                           "element": STEM_EL[hs], "weight": round(ww, 4)})
    return {e: round(v, 4) for e, v in tally.items()}, detail


def day_master_strength(p, tally):
    dm = p["day"]["stem"]; dme = STEM_EL[dm]
    support = {dme: tally[dme], PRODUCED_BY[dme]: tally[PRODUCED_BY[dme]]}
    oppose = {PRODUCES[dme]: tally[PRODUCES[dme]], CONTROLS[dme]: tally[CONTROLS[dme]],
              CONTROLLED_BY[dme]: tally[CONTROLLED_BY[dme]]}
    s, o = sum(support.values()), sum(oppose.values())
    ratio = s / (s + o)
    if ratio >= 0.60: label = "strong"
    elif ratio >= 0.50: label = "moderately strong"
    elif ratio >= 0.40: label = "moderately weak"
    else: label = "weak"

    month_branch = p["month"]["branch"]
    mb_hidden_els = [STEM_EL[x] for x in HIDDEN[month_branch]]
    rooted_in_month = dme in mb_hidden_els
    if BRANCH_EL[month_branch] in (dme, PRODUCED_BY[dme]):
        seasonal = "supported by season"
    elif rooted_in_month:
        seasonal = ("month branch is not the day-master element, but stores it as a hidden stem "
                    "-- residual seasonal qi, neither clear support nor clean drainage")
    elif BRANCH_EL[month_branch] in oppose:
        seasonal = "drained/controlled by season"
    else:
        seasonal = "neutral season"
    roots = [nm for nm, pill in p.items() if dm in pill["hidden_stems"] or BRANCH_EL[pill["branch"]] == dme]
    return {
        "day_master": dm, "day_master_pinyin": STEM_PY[dm], "day_master_element": dme,
        "day_master_polarity": "yin" if STEM_YIN[dm] else "yang",
        "support_elements": {k: round(v, 4) for k, v in support.items()},
        "opposing_elements": {k: round(v, 4) for k, v in oppose.items()},
        "support_total": round(s, 4), "oppose_total": round(o, 4),
        "support_ratio": round(ratio, 4), "strength_label": label,
        "month_command_branch": month_branch,
        "month_command_element": BRANCH_EL[month_branch],
        "seasonal_verdict": seasonal,
        "day_master_rooted_in_month_branch": rooted_in_month,
        "month_branch_hidden_elements": mb_hidden_els,
        "rooted_in_pillars": roots,
        "rule_set": ("Weighted tally declared in CALCULATION_MANIFEST.json: month branch 3.0, "
                     "day branch 2.0, other branches 1.5, visible stems 1.0; hidden stems take "
                     "0.60/0.30/0.10 of their branch weight. Support = same element + producing "
                     "element. This is a transparent arithmetic scheme adopted for reproducibility, "
                     "NOT a classical authority; other schools weight rooting, season and "
                     "combination differently and can reach a different label."),
    }


def branch_relations(p):
    br = {nm: p[nm]["branch"] for nm in ["year", "month", "day", "hour"]}
    items = list(br.items())
    rel = []
    def add(kind, a, b, extra=None):
        e = {"type": kind, "pillars": [a[0], b[0]], "branches": [a[1], b[1]]}
        if extra: e.update(extra)
        rel.append(e)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            pair = {a[1], b[1]}
            for x, y in SIX_CLASH:
                if pair == {x, y}: add("six_clash (冲)", a, b)
            for x, y in SIX_HARM:
                if pair == {x, y}: add("six_harm (害)", a, b)
            for x, y in SIX_COMBINE:
                if pair == {x, y}: add("six_combination (六合)", a, b)
            for x, y in DESTRUCTION:
                if pair == {x, y}: add("destruction (破)", a, b)
            if pair == set(PUNISH_UNGRATEFUL): add("punishment (刑, 子卯)", a, b)
            for t in TRINE:
                if pair <= set(t[:3]) and len(pair) == 2:
                    third = [z for z in t[:3] if z not in pair][0]
                    add("half/partial trine (半合)", a, b,
                        {"trine_element": t[3], "missing_member": third,
                         "note": "Incomplete: the third branch is absent, so no full transformation is claimed."})
    allb = list(br.values())
    for t in TRINE:
        if all(x in allb for x in t[:3]):
            rel.append({"type": "full trine (三合)", "branches": list(t[:3]), "element": t[3]})
    for t in DIRECTIONAL:
        if all(x in allb for x in t[:3]):
            rel.append({"type": "directional combination (三会)", "branches": list(t[:3]), "element": t[3]})
    for t in PUNISH_TRIPLE:
        present = [x for x in t if x in allb]
        if len(present) == 3:
            rel.append({"type": "triple punishment (三刑)", "branches": present})
        elif len(present) == 2:
            rel.append({"type": "partial punishment (刑, two of three)", "branches": present,
                        "missing_member": [x for x in t if x not in present][0]})
    for b in PUNISH_SELF:
        if allb.count(b) >= 2:
            rel.append({"type": "self-punishment (自刑)", "branch": b, "count": allb.count(b)})
    return rel


def stem_relations(p):
    st = {nm: p[nm]["stem"] for nm in ["year", "month", "day", "hour"]}
    items = list(st.items()); rel = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            for x, y, el in STEM_COMBINE:
                if {a[1], b[1]} == {x, y}:
                    rel.append({"type": "stem combination (天干合)", "pillars": [a[0], b[0]],
                                "stems": [a[1], b[1]], "nominal_transformation_element": el,
                                "transformation_claimed": False,
                                "note": ("Combination noted. Transformation is NOT asserted: it "
                                         "requires seasonal command and absence of a breaking "
                                         "element, which is not established here.")})
    return rel


def da_yun(ec, gender_male=True, count=9):
    yun = ec.getYun(1 if gender_male else 0)
    out = {"start_age_years": yun.getStartYear(), "start_months": yun.getStartMonth(),
           "start_days": yun.getStartDay(), "start_solar_date": yun.getStartSolar().toYmd(),
           "direction": "forward (順行)" if _forward(ec, gender_male) else "reverse (逆行)",
           "direction_rule": ("Yang-stem year + male, or yin-stem year + female -> forward; "
                              "otherwise reverse. Year stem here decides."),
           "periods": []}
    for d in yun.getDaYun()[:count]:
        gz = d.getGanZhi()
        out["periods"].append({
            "ganzhi": gz or None,
            "is_pre_luck_period": not gz,
            "start_age": d.getStartAge(), "end_age": d.getEndAge(),
            "start_year": d.getStartYear(), "end_year": d.getEndYear(),
            "stem": gz[0] if gz else None, "branch": gz[1] if gz else None,
            "stem_element": STEM_EL[gz[0]] if gz else None,
            "branch_element": BRANCH_EL[gz[1]] if gz else None,
            "branch_animal": BRANCH_ANIMAL[gz[1]] if gz else None,
        })
    return out


def _forward(ec, male):
    ys = ec.getYear()[0]
    return (not STEM_YIN[ys]) == male


def ten_god_of(day_stem, other_stem):
    dme, oe = STEM_EL[day_stem], STEM_EL[other_stem]
    same_pol = STEM_YIN[day_stem] == STEM_YIN[other_stem]
    if oe == dme:            return "比肩" if same_pol else "劫财"
    if oe == PRODUCES[dme]:  return "食神" if same_pol else "伤官"
    if oe == CONTROLS[dme]:  return "偏财" if same_pol else "正财"
    if oe == CONTROLLED_BY[dme]: return "七杀" if same_pol else "正官"
    if oe == PRODUCED_BY[dme]:   return "偏印" if same_pol else "正印"
    return "?"


def annual_pillars(day_stem, years):
    """Annual (流年) pillars, with the BaZi year boundary at Lichun."""
    out = []
    for y in years:
        lun = Solar.fromYmdHms(y, 6, 1, 12, 0, 0).getLunar()
        gz = lun.getYearInGanZhiExact()
        st, br = gz[0], gz[1]
        out.append({"year": y, "ganzhi": gz, "stem": st, "branch": br,
                    "stem_element": STEM_EL[st], "branch_element": BRANCH_EL[br],
                    "branch_animal": BRANCH_ANIMAL[br],
                    "ten_god_stem": ten_god_of(day_stem, st),
                    "ten_god_stem_en": TEN_GOD_EN.get(ten_god_of(day_stem, st)),
                    "boundary_note": "BaZi year runs Lichun-to-Lichun, not Jan 1 to Jan 1."})
    return out


TIAO_HOU = {
    # Qiong Tong Bao Jian climate prescriptions for a Gui (yin Water) day master.
    ("癸", "子"): ("丙", "warm the frozen water"), ("癸", "丑"): ("丙", "warm the frozen water"),
    ("癸", "寅"): ("辛", "generate the source"), ("癸", "卯"): ("庚", "generate the source"),
    ("癸", "辰"): ("丙", "warmth with drainage"), ("癸", "巳"): ("辛", "resist the heat"),
    ("癸", "午"): ("庚", "resist the heat"), ("癸", "未"): ("庚", "resist the heat"),
    ("癸", "申"): ("丁", "temper the metal"), ("癸", "酉"): ("辛", "refine"),
    ("癸", "戌"): ("辛", "generate the source"), ("癸", "亥"): ("庚", "generate the source"),
}


def yong_shen_by_school(pillars, tally, strength):
    """Favourable-element judgement under each NAMED school, side by side.

    These schools genuinely disagree for this chart, so no single answer is selected.
    """
    dm = pillars["day"]["stem"]; dme = STEM_EL[dm]
    mb = pillars["month"]["branch"]
    weak = strength["support_ratio"] < 0.5

    fu_yi = ([dme, PRODUCED_BY[dme]] if weak
             else [PRODUCES[dme], CONTROLS[dme], CONTROLLED_BY[dme]])
    th = TIAO_HOU.get((dm, mb))
    tiao_hou = [STEM_EL[th[0]]] if th else []

    # Tong Guan: bridge the two heaviest opposed elements, if they are in a control relation.
    ordered = sorted(tally.items(), key=lambda kv: -kv[1])
    tong_guan, tg_why = [], "no dominant control clash to bridge"
    for i in range(len(ordered)):
        for j in range(len(ordered)):
            a, b = ordered[i][0], ordered[j][0]
            if CONTROLS.get(a) == b and ordered[i][1] >= 2.0 and ordered[j][1] >= 2.0:
                bridge = PRODUCES[a]
                if bridge == b:
                    continue
                tong_guan = [PRODUCED_BY[b]] if PRODUCED_BY[b] != a else []
                tg_why = f"{a} controls {b}, both heavy; the bridging element is {PRODUCED_BY[b]}"
                break
        if tong_guan:
            break

    schools = {
        "扶抑 Fu Yi (support / suppress)": {
            "favourable_elements": fu_yi,
            "reasoning": (f"Day Master {dm} ({dme}) computes as {strength['strength_label']} "
                          f"(ratio {strength['support_ratio']}), so the school supports it with "
                          f"its own element and its resource."),
            "depends_on_hour_pillar": True},
        "調候 Tiao Hou (climate regulation)": {
            "favourable_elements": tiao_hou,
            "reasoning": (f"{dm} born in the {mb} month: the classical prescription is "
                          f"{th[0]} -- {th[1]}." if th else "no prescription found"),
            "depends_on_hour_pillar": False},
        "通關 Tong Guan (bridging)": {
            "favourable_elements": tong_guan, "reasoning": tg_why,
            "depends_on_hour_pillar": True},
    }
    picks = {k: set(v["favourable_elements"]) for k, v in schools.items() if v["favourable_elements"]}
    agreed = set.intersection(*picks.values()) if len(picks) > 1 else set()
    conflict = len(picks) > 1 and not agreed
    return {
        "schools": schools,
        "elements_all_schools_agree_on": sorted(agreed),
        "schools_conflict": conflict,
        "verdict": ("NOT RESOLVED -- the named schools select different favourable elements for "
                    "this chart, and the Fu Yi answer additionally depends on the hour pillar, "
                    "which is itself school-divergent here. Reported side by side rather than "
                    "collapsed into one answer."
                    if conflict else "schools converge"),
    }
