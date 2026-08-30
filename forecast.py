#!/usr/bin/env python
"""Period activation forecaster.

  ./forecast.py --on 2026-08-29                 what is active on one date
  ./forecast.py --from 2026-01-01 --to 2030-01-01
  ./forecast.py --years 5 --log                 seal a forecast for later scoring
  ./forecast.py --score outcomes.json           score a sealed forecast

This reports which life domains the traditions FLAG AS SALIENT in a window, with the
exact dates and the computed basis. It does not predict events, outcomes, or whether
anything will go well. See the module docstring in chart/forecast.py.
"""
import argparse, datetime as dt, json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

# Re-exec under the project venv if this interpreter lacks the dependencies, so
# `./forecast.py` works without the caller having to know about .venv.
_VENV = os.path.join(ROOT, ".venv", "bin", "python")
if os.path.exists(_VENV) and not os.environ.get("_FORECAST_REEXEC"):
    try:
        import swisseph  # noqa: F401
    except ImportError:
        os.environ["_FORECAST_REEXEC"] = "1"
        os.execv(_VENV, [_VENV, os.path.abspath(__file__)] + sys.argv[1:])
from chart.forecast import (Engine, DOMAINS, seal, score, aggregate,
                            effective_window, BACKGROUND_RATIO)

LOGDIR = os.path.join(ROOT, "forecast_log")

BANNER = (
    "Domain activation, not event prediction. A flagged domain means the traditions mark\n"
    "that area as salient in the window -- not that anything specific will happen, and not\n"
    "that it will go well or badly. The source dataset records 4 of 9 domains in active\n"
    "contradiction between clusters. No medical, lifespan, fertility, financial or legal\n"
    "inference is available from this program, by construction."
)


def show_date(eng, date):
    zw = eng.ziwei_batch([date]).get(date.isoformat())
    reads = [r for r in (eng.jyotisha_at(date), eng.western_at(date), eng.sinic_at(date, zw)) if r]
    print(f"\n=== ACTIVE ON {date.isoformat()} ===\n")
    for r in reads:
        print(f"  [{r['cluster'].upper():8s}] {r['technique']}")
        print(f"             period : {r['period']}")
        print(f"             window : {r['window_start']} -> {r['window_end']}")
        print(f"             derived from: {r['mechanism']}")
        if r.get("note"):
            print(f"             note   : {r['note']}")
        print()
    lo, hi, wdays = effective_window(reads)
    agg, bg = aggregate(reads)
    print(f"  Effective window (intersection of all active periods): {lo} -> {hi}  ({wdays} days)")
    print(f"  A cluster votes with its finest active period, counted only if within")
    print(f"  {int(BACKGROUND_RATIO)}x the finest period any cluster offers. Coarser periods are")
    print(f"  background: listed, never counted.\n")
    print("  domain               n    grade      basis")
    print("  " + "-" * 98)
    for dm in sorted(agg, key=lambda d: (-len(agg[d]), d)):
        byc = agg[dm]; n = len(byc)
        grade = "STRONG" if n >= 3 else ("MODERATE" if n == 2 else "weak")
        first = True
        for c, whys in sorted(byc.items()):
            for w in whys:
                lead = (f"  {dm} {DOMAINS[dm][:17]:17s} {n}/3  {grade:9s}" if first else " " * 40)
                print(f"{lead}  {c}: {w}")
                first = False
    if bg:
        print("\n  BACKGROUND -- too coarse to discriminate this window, deliberately not counted:")
        for dm, byc in sorted(bg.items()):
            for c, whys in sorted(byc.items()):
                for w in whys:
                    print(f"    {dm}  {c}: {w}")
    quiet = [d for d in DOMAINS if d not in agg and d not in bg]
    if quiet:
        print(f"\n  not activated at all: {', '.join(quiet)}")


def show_windows(eng, start, end, min_clusters):
    wins, _ = eng.windows(start, end, min_clusters)
    print(f"\n=== ACTIVATION WINDOWS  {start} -> {end} ===")
    print(f"    (>= {min_clusters} of 3 primary clusters agreeing on the same domain)\n")
    if not wins:
        print("  No window in this range reaches the threshold.")
        return wins
    strong = [w for w in wins if w["grade"] == "STRONG"]
    print(f"  {len(wins)} windows; {len(strong)} reach STRONG (all three clusters).\n")
    print("  start        end          days  dom  domain              n  grade     clusters")
    print("  " + "-" * 100)
    for w in wins:
        days = (dt.date.fromisoformat(w["end"]) - dt.date.fromisoformat(w["start"])).days
        print(f"  {w['start']}   {w['end']}   {days:4d}  {w['domain']}   "
              f"{w['domain_name'][:18]:18s}  {w['cluster_count']}  {w['grade']:8s}  "
              f"{', '.join(w['clusters'])}")
    return wins


def detail(wins, n=3):
    print("\n=== BASIS FOR THE FIRST %d WINDOWS ===\n" % min(n, len(wins)))
    for w in wins[:n]:
        print(f"  {w['domain']} {w['domain_name']}  |  {w['start']} -> {w['end']}  |  {w['grade']}")
        for c, whys in sorted(w["basis"].items()):
            for x in whys:
                print(f"      {c:9s} {x}")
        if w.get("basis_changes_mid_window"):
            print("      (the basis changes partway through this window -- all reasons listed)")
        nat = w.get("underlying_cluster_windows") or {}
        for c, (a2, b2) in sorted(nat.items()):
            if a2 > w["start"] or b2 < w["end"] or a2 < w["start"]:
                print(f"      (the {c} period actually spans {a2} -> {b2})")
        print(f"      TESTABLE: reviewing this window afterwards, did anything notable fall in "
              f"{w['domain_name']}?")
        print(f"      A MISS   : nothing notable in {w['domain']}, while something notable fell "
              f"in a domain no cluster flagged.\n")


def main():
    ap = argparse.ArgumentParser(description="Period activation forecaster (not an event predictor).")
    ap.add_argument("--on", help="single date YYYY-MM-DD")
    ap.add_argument("--from", dest="frm", help="range start")
    ap.add_argument("--to", help="range end")
    ap.add_argument("--years", type=int, help="range of N years from today")
    ap.add_argument("--min-clusters", type=int, default=2, choices=[1, 2, 3])
    ap.add_argument("--log", action="store_true", help="seal this forecast for later scoring")
    ap.add_argument("--score", help="score a sealed forecast against an outcomes JSON file")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of text")
    a = ap.parse_args()

    eng = Engine()

    if a.score:
        if not os.path.exists(a.score):
            print(f"No such outcomes file: {a.score}")
            sys.exit(1)
        outcomes = json.load(open(a.score))
        logged = json.load(open(outcomes["forecast_file"]))
        if seal(logged["windows"]) != logged["seal"]:
            print("SEAL MISMATCH -- the logged forecast was edited after sealing. Refusing to score.")
            sys.exit(1)
        print(json.dumps(score(logged, outcomes["observed"]), indent=1, ensure_ascii=False))
        return

    print(BANNER)

    if a.on:
        show_date(eng, dt.date.fromisoformat(a.on))
        return

    today = dt.date.today()
    start = dt.date.fromisoformat(a.frm) if a.frm else today
    end = (dt.date.fromisoformat(a.to) if a.to
           else start.replace(year=start.year + (a.years or 3)))
    wins = show_windows(eng, start, end, a.min_clusters)
    if wins:
        detail(wins)

    if a.log and wins:
        os.makedirs(LOGDIR, exist_ok=True)
        rec = {"generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "range": [start.isoformat(), end.isoformat()],
               "min_clusters": a.min_clusters, "windows": wins}
        rec["seal"] = seal(wins)
        base = f"forecast_{start}_{end}_{rec['seal']}.json"
        path = os.path.join(LOGDIR, base)
        json.dump(rec, open(path, "w"), indent=1, ensure_ascii=False)
        tmpl = {"forecast_file": path,
                "_how_to_use": ("For each window, list the domain codes (D1..D9) in which something "
                                "genuinely notable happened. Leave a window empty to skip it. Record "
                                "these from memory or a diary BEFORE re-reading the forecast, or the "
                                "score is just hindsight."),
                "observed": {f"{w['start']}..{w['end']}": [] for w in wins}}
        tpath = os.path.join(LOGDIR, "outcomes_template_" + base[len("forecast_"):])
        json.dump(tmpl, open(tpath, "w"), indent=1, ensure_ascii=False)
        print(f"\n  Sealed  : {path}")
        print(f"  Seal    : {rec['seal']}  (editing the file after this invalidates scoring)")
        print(f"  Template: {tpath}")
        print(f"  Fill in the domains that actually turned out notable per window, then:")
        print(f"      ./forecast.py --score {tpath}")


if __name__ == "__main__":
    main()
