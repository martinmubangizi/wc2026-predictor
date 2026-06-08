import numpy as np
from typing import Tuple, Dict, Optional

def simulate_penalty_shootout(team_a: dict, team_b: dict) -> str:
    pen_a = team_a.get("pen_skill", 0.72)  # P(team A converts a kick)
    pen_b = team_b.get("pen_skill", 0.72)  # P(team B converts a kick)

    # Run standard 5-kick shootout
    def take_kicks(n: int) -> Tuple[int, int]:
        a_goals = sum(np.random.random() < pen_a for _ in range(n))
        b_goals = sum(np.random.random() < pen_b for _ in range(n))
        return a_goals, b_goals

    a_score, b_score = take_kicks(5)

    # Sudden death if still tied
    max_sudden_death = 20
    kicks = 0
    while a_score == b_score and kicks < max_sudden_death:
        a_k = int(np.random.random() < pen_a)
        b_k = int(np.random.random() < pen_b)
        a_score += a_k
        b_score += b_k
        kicks += 1

    if a_score == b_score:
        return "A" if np.random.random() < 0.5 else "B"

    return "A" if a_score > b_score else "B"

def simulate_extra_time(team_a: dict, team_b: dict, model) -> Tuple[int, int]:
    from models.dixon_coles import expected_goals
    lam_a, lam_b = expected_goals(team_a, team_b, neutral=True)

    et_factor = 0.33 * 0.85  # fatigue reduction
    et_lam_a = lam_a * et_factor
    et_lam_b = lam_b * et_factor

    et_goals_a = np.random.poisson(et_lam_a)
    et_goals_b = np.random.poisson(et_lam_b)
    return int(et_goals_a), int(et_goals_b)

def simulate_match(
    team_a: dict,
    team_b: dict,
    model,
    knockout: bool = False,
    neutral: bool = True,
    rest_days_a: int = 4,
    rest_days_b: int = 4,
    altitude_match: bool = False,
) -> Dict:
    ta = team_a.copy()
    tb = team_b.copy()

    if rest_days_a < 3:
        ta["form"] = ta.get("form", 0.0) - 0.10
    if rest_days_b < 3:
        tb["form"] = tb.get("form", 0.0) - 0.10

    # Altitude penalty
    if altitude_match:
        ta["altitude_penalty"] = True
        tb["altitude_penalty"] = True

    # Simulate 90-minute score
    goals_a, goals_b = model.simulate_score(ta, tb, neutral=neutral)

    result = {
        "team_a": team_a["name"],
        "team_b": team_b["name"],
        "goals_a": goals_a,
        "goals_b": goals_b,
        "method": "regular",
        "pen_winner": None,
    }

    # Determine winner
    if goals_a > goals_b:
        result["winner"] = team_a["name"]
    elif goals_b > goals_a:
        result["winner"] = team_b["name"]
    else:
        if not knockout:
            result["winner"] = "D"  # Draw
        else:
            # Extra time
            et_a, et_b = simulate_extra_time(ta, tb, model)
            result["goals_a"] += et_a
            result["goals_b"] += et_b

            if result["goals_a"] > result["goals_b"]:
                result["winner"] = team_a["name"]
                result["method"] = "extra_time"
            elif result["goals_b"] > result["goals_a"]:
                result["winner"] = team_b["name"]
                result["method"] = "extra_time"
            else:
                # Penalties
                pen_winner_id = simulate_penalty_shootout(ta, tb)
                result["winner"] = team_a["name"] if pen_winner_id == "A" else team_b["name"]
                result["pen_winner"] = result["winner"]
                result["method"] = "penalties"

    return result
