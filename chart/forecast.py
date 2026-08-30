"""Period activation engine.

WHAT THIS DOES: for any date range, computes which time-lords are active in each
primary cluster, projects them onto the nine life domains through a declared
registry, and reports the EXACT windows where clusters agree.

WHAT THIS DOES NOT DO: predict events. The underlying dataset records that 4 of 9
domains are in active contradiction between clusters, that the BaZi hour pillar is
unresolved between schools, and that none of this is a validated forecasting method.
A domain being "activated" means the traditions flag it as salient in that window --
not that anything in particular will happen, and not that it will go well or badly.

Every emitted line carries the computed basis that produced it. Outcome, health,
lifespan, fertility, financial and legal claims are structurally impossible to emit:
the registry maps to domain salience only, and there is no verb vocabulary here.
"""
import datetime as dt
import hashlib
import json
import subprocess
import os

from . import core

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOMAINS = {
    "D1": "Self / identity", "D2": "Career / status", "D3": "Wealth / gains",
    "D4": "Partnership", "D5": "Family / roots / home", "D6": "Children / creation",
    "D7": "Health / routine", "D8": "Mind / education / craft",
    "D9": "Fortune / spirituality / worldview",
}

# --- declared registry: whole-sign house -> domain(s) ---
HOUSE_DOMAIN = {
    1: ["D1"], 2: ["D3", "D5"], 3: ["D8"], 4: ["D5"], 5: ["D6"], 6: ["D7"],
    7: ["D4"], 8: ["D9"], 9: ["D9"], 10: ["D2"], 11: ["D3"], 12: ["D9"],
}
# --- BaZi Ten God -> domain(s) ---
TEN_GOD_DOMAIN = {
    "比肩": ["D1"], "劫财": ["D1"], "食神": ["D6", "D8"], "伤官": ["D6", "D8"],
    "正财": ["D3"], "偏财": ["D3"], "正官": ["D2"], "七杀": ["D2"],
    "正印": ["D8", "D5"], "偏印": ["D8", "D5"],
}
# --- Zi Wei natal palace -> domain(s) ---
PALACE_DOMAIN = {
    "命宫": ["D1"], "兄弟": ["D4"], "夫妻": ["D4"], "子女": ["D6"], "财帛": ["D3"],
    "疾厄": ["D7"], "迁移": ["D2"], "仆役": ["D4"], "官禄": ["D2"], "田宅": ["D5"],
    "福德": ["D9"], "父母": ["D5"],
}


def _d(s):
    return dt.date.fromisoformat(s[:10])


def _span(period):
    """Length in days of a dasha period."""
    return (_d(period["end"]) - _d(period["start"])).days


def _add(doms, dm, why, scale_days):
    doms.setdefault(dm, []).append({"why": why, "scale_days": scale_days})


def aggregate(reads, window_days=None):
    """Split cluster contributions into discriminating votes and background-only.

    Each cluster votes with its finest period. That vote counts only if the period is
    within BACKGROUND_RATIO of the RESOLUTION IN PLAY -- the shortest active period any
    cluster offers -- not of the scan segment.

    Gating against the segment was wrong: the scan slices at every transition, so a
    segment can be arbitrarily short (a 15-day gap between two boundaries, or a segment
    truncated by the caller's start date). That shrank the gate and demoted real signals
    to background, and in the extreme nullified every cluster at once. The resolution in
    play does not depend on how the range happens to be sliced.
    """
    finest_overall = min(
        (e["scale_days"] for r in reads for entries in r["domains"].values() for e in entries),
        default=365)
    limit = BACKGROUND_RATIO * max(finest_overall, 1)
    counted, background = {}, {}
    for r in reads:
        for dm, entries in r["domains"].items():
            finest = min(e["scale_days"] for e in entries)
            if finest <= limit:
                counted.setdefault(dm, {})[r["cluster"]] = [
                    e["why"] for e in entries if e["scale_days"] <= limit]
            else:
                background.setdefault(dm, {})[r["cluster"]] = [
                    f"{e['why']} [{e['scale_days']} d = {e['scale_days']/max(finest_overall,1):.1f}x "
                    f"the finest active period -- background, not counted]" for e in entries]
    return counted, background


def effective_window(reads):
    """Intersection of every active cluster window: the span this reading actually pins."""
    starts = [_d(r["window_start"]) for r in reads]
    ends = [_d(r["window_end"]) for r in reads]
    lo, hi = max(starts), min(ends)
    return lo, hi, max((hi - lo).days, 1)


# A cluster votes for a domain using its FINEST active period pointing there. That vote
# counts only if the period is comparable to the window: a period many times longer is
# constant background across the whole range and cannot distinguish this window from any
# other inside it, so counting it as agreement manufactures convergence. This rule is why
# a ten-year Zi Wei decadal palace does not turn a two-cluster window into a three-cluster
# one.
BACKGROUND_RATIO = 4.0


class Engine:
    def __init__(self, master_path=None):
        self.md = json.load(open(master_path or os.path.join(ROOT, "MASTER_DATASET.json")))
        self.J = self.md["jyotisha"]["chart_mean_node"]
        self.W = self.md["western"]
        self.B = self.md["bazi"]
        self.vim = self.md["jyotisha"]["vimshottari_gregorian_year"]
        self.birth = _d(self.md["time_audit"]["original_local_civil"])
        self.j_rules = self._rulerships(self.J["houses"], "lord")
        self.w_rules = self._rulerships(self.W["houses"], "ruler")
        self.j_sits = {g: self.J["planets"][g]["house_whole_sign"] for g in self.J["planets"]}
        self.w_sits = {p: self.W["planets"][p]["whole_sign_house"] for p in self.W["planets"]}
        self._zw_cache = {}
        self._lichun_cache = {}

    @staticmethod
    def _rulerships(houses, key):
        out = {}
        for h in range(1, 13):
            out.setdefault(houses[str(h)][key], []).append(h)
        return out

    # ---------------------------------------------------------------- clusters
    def jyotisha_at(self, date):
        iso = date.isoformat()
        md = ad = None
        for m in self.vim["mahadashas"]:
            if m["start"][:10] <= iso < m["end"][:10]:
                md = m
                for a in m["children"]:
                    if a["start"][:10] <= iso < a["end"][:10]:
                        ad = a
                break
        if not md:
            return None
        doms, basis = {}, []
        spans = {"mahadasha": _span(md), "antardasha": _span(ad) if ad else 0}
        for lord, level in ((md["lord"], "mahadasha"), (ad["lord"] if ad else None, "antardasha")):
            if not lord:
                continue
            sc = spans[level]
            for h in self.j_rules.get(lord, []):
                for dm in HOUSE_DOMAIN[h]:
                    _add(doms, dm, f"{level} lord {lord} rules house {h}", sc)
            sh = self.j_sits.get(lord)
            if sh:
                for dm in HOUSE_DOMAIN[sh]:
                    _add(doms, dm, f"{level} lord {lord} occupies house {sh}", sc)
            basis.append(f"{level} {lord}")
        return {"cluster": "jyotisha", "technique": "Vimshottari dasha",
                "mechanism": "position of the Moon within its nakshatra at birth",
                "period": f"{md['lord']}" + (f" / {ad['lord']}" if ad else ""),
                "window_start": max(md["start"][:10], ad["start"][:10] if ad else md["start"][:10]),
                "window_end": min(md["end"][:10], ad["end"][:10] if ad else md["end"][:10]),
                "domains": doms, "summary": " / ".join(basis)}

    def western_at(self, date):
        age = date.year - self.birth.year - ((date.month, date.day) < (self.birth.month, self.birth.day))
        house = age % 12 + 1
        asc_sign = self.W["ascendant"]["sign_index"]
        sign = (asc_sign + age) % 12
        lord = self.W["houses"][str(house)]["ruler"]
        start = self.birth.replace(year=self.birth.year + age)
        end = self.birth.replace(year=self.birth.year + age + 1)
        doms = {}
        yr = (end - start).days
        for dm in HOUSE_DOMAIN[house]:
            _add(doms, dm, f"profected house {house} itself", yr)
        for h in self.w_rules.get(lord, []):
            for dm in HOUSE_DOMAIN[h]:
                _add(doms, dm, f"Lord of the Year {lord} rules house {h}", yr)
        sh = self.w_sits.get(lord)
        if sh:
            for dm in HOUSE_DOMAIN[sh]:
                _add(doms, dm, f"Lord of the Year {lord} occupies house {sh}", yr)
        return {"cluster": "western", "technique": "annual profection",
                "mechanism": "whole years of age counted from the Ascendant",
                "period": f"age {age}, house {house}, Lord of the Year {lord}",
                "window_start": start.isoformat(), "window_end": end.isoformat(),
                "domains": doms, "summary": f"profection h{house}, LoY {lord}"}

    def lichun(self, year):
        """Exact Lichun (Sun at 315 deg) for a year -- the BaZi year boundary.

        Not hardcoded to 4 February: the instant drifts, and the natal chart in this
        repository turns on precisely this boundary.
        """
        if year not in self._lichun_cache:
            guess = core.jd_ut(dt.datetime(year, 2, 4, tzinfo=dt.timezone.utc))
            j = core.solar_longitude_crossing(315.0, guess)
            self._lichun_cache[year] = core.jd_to_utc(j).date()
        return self._lichun_cache[year]

    def bazi_year(self, date):
        """The BaZi year a date belongs to. Runs Lichun to Lichun, not January to January."""
        return date.year - 1 if date < self.lichun(date.year) else date.year

    def sinic_at(self, date, zw):
        doms, basis = {}, []
        byear = self.bazi_year(date)
        ap = next((a for a in self.B["annual_pillars"] if a["year"] == byear), None)
        if ap:
            for dm in TEN_GOD_DOMAIN.get(ap["ten_god_stem"], []):
                _add(doms, dm,
                     f"BaZi annual pillar {ap['ganzhi']} is {ap['ten_god_stem']} to the Day Master", 365)
            basis.append(f"annual {ap['ganzhi']} {ap['ten_god_stem']}")
        dy = next((p for p in self.B["da_yun"]["periods"]
                   if p["ganzhi"] and p["start_year"] <= byear <= p["end_year"]), None)
        if dy:
            basis.append(f"Da Yun {dy['ganzhi']} (10 yr, background)")
        if zw:
            for key, label, sc in (("decadal_natal_palace_zh", "Zi Wei decadal palace", 3652),
                                   ("yearly_natal_palace_zh", "Zi Wei annual palace", 365)):
                pal = zw.get(key)
                for dm in PALACE_DOMAIN.get(pal, []):
                    _add(doms, dm, f"{label} falls on natal {pal}", sc)
            basis.append(f"decadal {zw.get('decadal_natal_palace_zh')}, "
                         f"annual {zw.get('yearly_natal_palace_zh')}")
        return {"cluster": "sinic", "technique": "BaZi luck pillars + Zi Wei periods",
                "mechanism": "solar-term distance at birth; Five-Elements Bureau from the Ming palace",
                "period": " | ".join(basis),
                "window_start": self.lichun(byear).isoformat(),
                "window_end": self.lichun(byear + 1).isoformat(),
                "domains": doms, "summary": " | ".join(basis),
                "note": "BaZi and Zi Wei corroborate internally but contribute ONE cross-cultural vote."}

    # ---------------------------------------------------------------- zi wei
    def ziwei_batch(self, dates):
        todo = [d.isoformat() for d in dates if d.isoformat() not in self._zw_cache]
        for i in range(0, len(todo), 60):
            chunk = todo[i:i + 60]
            r = subprocess.run(["node", os.path.join(ROOT, "scripts", "ziwei_range.js"),
                                "2003-01-20", "3", "male"] + chunk,
                               capture_output=True, text=True, cwd=ROOT)
            if r.returncode != 0:
                continue
            data = json.loads(r.stdout)
            self._zw_cache.update(data["targets"])
        return self._zw_cache

    # ---------------------------------------------------------------- windows
    def transitions(self, start, end):
        pts = {start, end}
        for m in self.vim["mahadashas"]:
            for x in (m["start"], m["end"]):
                d = _d(x)
                if start <= d <= end:
                    pts.add(d)
            for a in m["children"]:
                for x in (a["start"], a["end"]):
                    d = _d(x)
                    if start <= d <= end:
                        pts.add(d)
        y = start.year - 1
        while y <= end.year + 1:
            for cand in (self.birth.replace(year=y), self.lichun(y)):
                if start <= cand <= end:
                    pts.add(cand)
            y += 1
        for p in self.B["da_yun"]["periods"]:
            if p["ganzhi"]:
                cand = self.lichun(p["start_year"])
                if start <= cand <= end:
                    pts.add(cand)
        return sorted(pts)

    def scan(self, start, end):
        pts = self.transitions(start, end)
        mids = []
        for i in range(len(pts) - 1):
            mids.append(pts[i] + (pts[i + 1] - pts[i]) / 2)
        self.ziwei_batch(mids)
        out = []
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            if (b - a).days < 1:
                continue
            mid = mids[i]
            zw = self._zw_cache.get(mid.isoformat())
            reads = [self.jyotisha_at(mid), self.western_at(mid), self.sinic_at(mid, zw)]
            reads = [r for r in reads if r]
            agg, bg = aggregate(reads)
            out.append({"start": a.isoformat(), "end": b.isoformat(),
                        "days": (b - a).days, "reads": reads,
                        "domains": agg, "background_only": bg})
        return out

    def windows(self, start, end, min_clusters=2):
        raw = self.scan(start, end)
        hits = []
        for seg in raw:
            for dm, byc in seg["domains"].items():
                if len(byc) >= min_clusters:
                    bgc = seg["background_only"].get(dm, {})
                    natural = {r["cluster"]: [r["window_start"], r["window_end"]]
                               for r in seg["reads"] if r["cluster"] in byc}
                    hits.append({"domain": dm, "domain_name": DOMAINS[dm],
                                 "start": seg["start"], "end": seg["end"],
                                 "underlying_cluster_windows": natural,
                                 "clusters": sorted(byc), "cluster_count": len(byc),
                                 "grade": "STRONG" if len(byc) >= 3 else "MODERATE",
                                 "basis": {c: v for c, v in byc.items()},
                                 "background_not_counted": {c: v for c, v in bgc.items()}})
        # merge adjacent segments carrying the same domain and the same cluster set
        hits.sort(key=lambda h: (h["domain"], h["start"]))
        merged = []
        for h in hits:
            if merged:
                p = merged[-1]
                if (p["domain"] == h["domain"] and p["end"] == h["start"]
                        and p["clusters"] == h["clusters"]):
                    p["end"] = h["end"]
                    continue
            merged.append(dict(h))
        merged.sort(key=lambda h: (h["start"], -h["cluster_count"], h["domain"]))
        return merged, raw


# ---------------------------------------------------------------- falsifiability
def seal(record):
    """Content hash, so a logged forecast cannot be quietly edited after the fact."""
    body = json.dumps(record, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(body.encode()).hexdigest()[:16]


def score(logged, outcomes):
    """Score flagged domains against domains the person reports as actually notable.

    Grouped by TIME WINDOW, not by (window, domain) pair -- a window flagging three
    domains is one trial, not three, or the denominator is inflated.

    The baseline is hypergeometric and exact: if a window flags f of the 9 domains and
    the person reports r as notable, the chance of at least one overlap under random
    flagging is 1 - C(9-r, f) / C(9, f). Summing that across windows gives the number
    of hits blind guessing would produce. Beating it by a little means nothing; the
    sample sizes available to one person are tiny.
    """
    from math import comb
    N = 9
    by_window = {}
    for w in logged["windows"]:
        key = f"{w['start']}..{w['end']}"
        by_window.setdefault(key, {"flagged": set(), "grades": set()})
        by_window[key]["flagged"].add(w["domain"])
        by_window[key]["grades"].add(w["grade"])

    rows, observed, expected = [], 0, 0.0
    for key, info in sorted(by_window.items()):
        reported = set(outcomes.get(key, []))
        if not reported:
            continue
        flagged = info["flagged"]
        f, r = len(flagged), len(reported)
        hit = bool(flagged & reported)
        p_chance = 1.0 - (comb(N - r, f) / comb(N, f)) if f <= N - r else 1.0
        observed += hit
        expected += p_chance
        rows.append({"window": key, "flagged": sorted(flagged), "reported": sorted(reported),
                     "overlap": sorted(flagged & reported), "hit": hit,
                     "chance_of_hit_if_random": round(p_chance, 4),
                     "grade": "STRONG" if "STRONG" in info["grades"] else "MODERATE"})
    if not rows:
        return {"scored_windows": 0,
                "note": ("No outcomes supplied yet. Fill the template and re-run. Record what was "
                         "notable BEFORE re-reading the forecast, or this measures hindsight.")}

    n = len(rows)
    verdict = ("above chance in this sample" if observed > expected else
               "at or below chance -- no signal demonstrated")
    return {
        "scored_windows": n,
        "observed_hits": observed,
        "expected_hits_if_random": round(expected, 3),
        "observed_rate": round(observed / n, 4),
        "chance_rate": round(expected / n, 4),
        "lift_over_chance": round((observed - expected) / n, 4),
        "verdict": verdict,
        "statistical_reality_check": (
            f"With {n} scored window{'s' if n != 1 else ''}, a difference of "
            f"{abs(observed - expected):.1f} hits is well inside what noise produces. "
            f"Dozens of windows would be needed before the comparison meant anything, and "
            f"a single person's life supplies only a few per year."),
        "known_biases": [
            "The scorer knows which domains were flagged, which invites hindsight fitting.",
            "'Notable' is judged by the same person the forecast is about.",
            "Domains are broad; many life events could be filed under more than one.",
            "Windows overlap in time, so trials are not fully independent.",
        ],
        "rows": rows,
    }
