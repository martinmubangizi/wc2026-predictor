import sys, os, json, time, warnings, argparse
import numpy as np
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

from models.ensemble import EnsemblePredictor
from simulator.tournament import run_one_tournament, _prewarm_cache
from data.teams import TEAMS, get_team, GROUPS
from collections import defaultdict

def run(n_sims=20_000, seed=2026, verbose=True):
    np.random.seed(seed)

    if verbose: print("🏆  2026 FIFA WORLD CUP — ML PREDICTION ENGINE")
    if verbose: print(f"    Model: Dixon-Coles + XGBoost Ensemble")
    if verbose: print(f"    Player form: ACTIVE (star_rating × depth_rating weighted)")
    if verbose: print(f"    Simulations: {n_sims:,}\n")

    if verbose: print("[1/3] Training model...")
    model = EnsemblePredictor(dc_weight=0.50, xgb_weight=0.50)
    model.fit(train_xgb=True, n_synthetic=25_000)

    if verbose: print("[2/3] Pre-computing all matchup predictions...")
    team_lookup = {name: get_team(name) for name in TEAMS}
    _prewarm_cache(model, team_lookup)
    if verbose: print(f"      {len(model._cache):,} matchups cached\n")

    if verbose: print(f"[3/3] Running {n_sims:,} Monte Carlo tournament simulations...")
    counts = {
        "champion": defaultdict(int),
        "finalist": defaultdict(int),
        "semi": defaultdict(int),
        "quarter": defaultdict(int),
        "r16": defaultdict(int),
        "group_advance": defaultdict(int),
        "group_winner": defaultdict(lambda: defaultdict(int)),  # group→team
        "group_runner": defaultdict(lambda: defaultdict(int)),
    }

    t0 = time.time()
    for i in range(n_sims):
        r = run_one_tournament(model)

        champ = r["champion"]
        if champ: counts["champion"][champ] += 1

        finalist = r.get("finalist")
        if champ:    counts["finalist"][champ] += 1
        if finalist: counts["finalist"][finalist] += 1

        for t in r.get("semifinalists", []):   counts["semi"][t] += 1
        for t in r.get("quarterfinalists", []): counts["quarter"][t] += 1
        for t in r.get("r16", []):              counts["r16"][t] += 1

        q = r["qualifiers"]
        for g, team in q["group_winners"].items():
            counts["group_advance"][team] += 1
            counts["group_winner"][g][team] += 1
        for g, team in q["runners_up"].items():
            counts["group_advance"][team] += 1
            counts["group_runner"][g][team] += 1
        for team in q["advancing_third"]:
            counts["group_advance"][team] += 1

        if verbose and (i+1) % 5000 == 0:
            elapsed = time.time() - t0
            rate = (i+1) / elapsed
            eta  = (n_sims - i - 1) / rate
            print(f"      {i+1:>7,} / {n_sims:,}  ({rate:.0f} sims/sec)  ETA: {eta:.0f}s")

    elapsed = time.time() - t0
    if verbose: print(f"\n    ✅ Done: {n_sims:,} sims in {elapsed:.1f}s ({n_sims/elapsed:.0f}/sec)\n")

    n = n_sims

    def pct(d): return {k: round(v/n, 5) for k,v in d.items()}

    predictions = {
        "metadata": {
            "simulations": n_sims,
            "seed": seed,
            "model": "Dixon-Coles + XGBoost + Player Form Weighting",
            "generated": time.strftime("%Y-%m-%d %H:%M UTC")
        },
        "champion":        pct(counts["champion"]),
        "finalist":        pct(counts["finalist"]),
        "semifinalist":    pct(counts["semi"]),
        "quarterfinalist": pct(counts["quarter"]),
        "round_of_16":     pct(counts["r16"]),
        "group_advance":   pct(counts["group_advance"]),
        "group_winners":   {g: pct(dict(d)) for g,d in counts["group_winner"].items()},
        "group_runners_up":{g: pct(dict(d)) for g,d in counts["group_runner"].items()},
    }

    # Top winner and full ranked table
    ranked = sorted(predictions["champion"].items(), key=lambda x: -x[1])
    predictions["ranked_winner"] = ranked

    if verbose:
        _print_summary(predictions)

    os.makedirs("output", exist_ok=True)

    with open("output/predictions.json", "w") as f:
        json.dump(predictions, f, indent=2)

    _save_csv(predictions, "output/predictions.csv")

    if verbose:
        print(f"\n💾 Files saved:")
        print(f"   output/predictions.json")
        print(f"   output/predictions.csv")

    return predictions

def _print_summary(p):
    n = p["metadata"]["simulations"]
    print("=" * 70)
    print(f"  🏆 2026 WORLD CUP PREDICTIONS  ({n:,} simulations)")
    print("=" * 70)
    print(f"\n  {'#':<4} {'TEAM':<22} {'WIN%':>7}  {'FINAL%':>7}  {'SEMI%':>7}  {'QF%':>7}")
    print(f"  {'─'*60}")
    for i, (team, pw) in enumerate(p["ranked_winner"][:20], 1):
        pf = p["finalist"].get(team, 0)
        ps = p["semifinalist"].get(team, 0)
        pq = p["quarterfinalist"].get(team, 0)
        print(f"  {i:<4} {team:<22} {pw*100:>6.2f}%  {pf*100:>6.2f}%  {ps*100:>6.2f}%  {pq*100:>6.2f}%")

    print(f"\n  {'GROUP WINNERS':^70}")
    for g in sorted(p["group_winners"].keys()):
        gw = p["group_winners"][g]
        top = sorted(gw.items(), key=lambda x:-x[1])[:2]
        line = "  ".join(f"{t}:{v*100:.0f}%" for t,v in top)
        print(f"  Group {g}: {line}")
    print("=" * 70)

    # The verdict
    winner = p["ranked_winner"][0][0]
    win_pct = p["ranked_winner"][0][1] * 100
    print(f"\n  🥇 MODEL PREDICTION: {winner.upper()} ({win_pct:.1f}% probability)")
    print()

def _save_csv(p, path):
    import csv
    all_teams = set(p["champion"].keys()) | set(p["finalist"].keys())
    rows = []
    for team in sorted(all_teams):
        rows.append({
            "team": team,
            "p_champion":        p["champion"].get(team, 0),
            "p_finalist":        p["finalist"].get(team, 0),
            "p_semifinalist":    p["semifinalist"].get(team, 0),
            "p_quarterfinalist": p["quarterfinalist"].get(team, 0),
            "p_round_of_16":     p["round_of_16"].get(team, 0),
            "p_group_advance":   p["group_advance"].get(team, 0),
        })
    rows.sort(key=lambda x: -x["p_champion"])
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sims", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    run(n_sims=args.sims, seed=args.seed)
