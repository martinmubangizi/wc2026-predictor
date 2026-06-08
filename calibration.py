import numpy as np
from typing import List, Dict, Tuple

def ranked_probability_score(
    p_win: float, p_draw: float, p_loss: float,
    actual: str  # "win", "draw", "loss" for Team A
) -> float:
    # Predicted CDF
    pred_cdf = np.array([p_win, p_win + p_draw, 1.0])

    # Actual CDF
    if actual == "win":
        act_cdf = np.array([1.0, 1.0, 1.0])
    elif actual == "draw":
        act_cdf = np.array([0.0, 1.0, 1.0])
    else:  # loss
        act_cdf = np.array([0.0, 0.0, 1.0])

    rps = 0.5 * np.sum((pred_cdf - act_cdf) ** 2)
    return float(rps)

def log_loss_match(
    p_win: float, p_draw: float, p_loss: float,
    actual: str
) -> float:
    eps = 1e-10
    if actual == "win":
        return -np.log(max(p_win, eps))
    elif actual == "draw":
        return -np.log(max(p_draw, eps))
    else:
        return -np.log(max(p_loss, eps))

def evaluate_predictions(predictions: List[Dict]) -> Dict:
    rps_scores = []
    ll_scores = []
    correct_outcomes = []

    for pred in predictions:
        p_w = pred["p_win_a"]
        p_d = pred["p_draw"]
        p_l = pred["p_win_b"]
        actual = pred["actual"]

        rps_scores.append(ranked_probability_score(p_w, p_d, p_l, actual))
        ll_scores.append(log_loss_match(p_w, p_d, p_l, actual))

        predicted_outcome = max(["win", "draw", "loss"],
                                key=lambda o: {"win": p_w, "draw": p_d, "loss": p_l}[o])
        correct_outcomes.append(int(predicted_outcome == actual))

    return {
        "mean_rps": float(np.mean(rps_scores)),
        "mean_log_loss": float(np.mean(ll_scores)),
        "accuracy": float(np.mean(correct_outcomes)),
        "n_matches": len(predictions),
        "rps_scores": rps_scores,
    }

def backtest_model(model, historical_matches: List[Dict]) -> Dict:
    predictions = []

    for match in historical_matches:
        ta = match["team_a"]
        tb = match["team_b"]
        probs = model.predict_proba(ta, tb)

        ga, gb = match["goals_a"], match["goals_b"]
        if ga > gb:
            actual = "win"
        elif gb > ga:
            actual = "loss"
        else:
            actual = "draw"

        predictions.append({
            "p_win_a": probs["p_win_a"],
            "p_draw": probs["p_draw"],
            "p_win_b": probs["p_win_b"],
            "actual": actual,
        })

    return evaluate_predictions(predictions)

def compare_with_bookmaker(
    model_probs: Dict[str, float],
    bookmaker_probs: Dict[str, float],
    tolerance: float = 0.08
) -> Dict:
    deviations = {}
    flags = []

    for key in ["p_win_a", "p_draw", "p_win_b"]:
        dev = model_probs.get(key, 0) - bookmaker_probs.get(key, 0)
        deviations[key] = round(dev, 4)
        if abs(dev) > tolerance:
            flags.append(f"{key}: model={model_probs[key]:.3f}, market={bookmaker_probs[key]:.3f} (Δ={dev:+.3f})")

    return {
        "deviations": deviations,
        "recalibration_needed": len(flags) > 0,
        "flags": flags,
    }

def generate_synthetic_backtest_matches(n: int = 500, seed: int = 99) -> List[Dict]:
    from data.teams import TEAMS, get_team
    import random

    rng = random.Random(seed)
    team_names = list(TEAMS.keys())
    matches = []

    for _ in range(n):
        ta_name, tb_name = rng.sample(team_names, 2)
        ta = get_team(ta_name)
        tb = get_team(tb_name)

        # Elo-based synthetic outcome
        elo_diff = ta["elo"] - tb["elo"]
        p_win = 1 / (1 + 10 ** (-elo_diff / 400))
        rand = rng.random()
        if rand < p_win * 0.75:
            ga = rng.randint(1, 4)
            gb = rng.randint(0, ga - 1)
        elif rand < p_win * 0.75 + 0.25:
            score = rng.randint(0, 2)
            ga, gb = score, score
        else:
            gb = rng.randint(1, 4)
            ga = rng.randint(0, gb - 1)

        matches.append({"team_a": ta, "team_b": tb, "goals_a": ga, "goals_b": gb})

    return matches
