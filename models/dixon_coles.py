import numpy as np
from scipy.optimize import minimize
from typing import Tuple, Dict
from math import lgamma, exp

def _poisson_pmf_vec(lam: float, max_k: int) -> np.ndarray:
    k = np.arange(max_k + 1, dtype=np.float64)
    log_pmf = k * np.log(lam) - lam - np.array([lgamma(ki + 1) for ki in k])
    return np.exp(log_pmf)

def scoreline_probability_matrix(
    lambda_a: float,
    lambda_b: float,
    rho: float = -0.13,
    max_goals: int = 8
) -> np.ndarray:
    pmf_a = _poisson_pmf_vec(lambda_a, max_goals)  # shape (9,)
    pmf_b = _poisson_pmf_vec(lambda_b, max_goals)  # shape (9,)

    matrix = np.outer(pmf_a, pmf_b)

    matrix[0, 0] *= (1 - lambda_a * lambda_b * rho)
    matrix[1, 0] *= (1 + lambda_b * rho)
    matrix[0, 1] *= (1 + lambda_a * rho)
    matrix[1, 1] *= (1 - rho)

    # Renormalise to ensure probabilities sum to 1
    total = matrix.sum()
    if total > 0:
        matrix /= total
    return matrix

def outcome_probabilities(
    lambda_a: float,
    lambda_b: float,
    rho: float = -0.13
) -> Tuple[float, float, float]:
    matrix = scoreline_probability_matrix(lambda_a, lambda_b, rho)
    p_win_a = float(np.tril(matrix, -1).sum())   # i > j
    p_draw   = float(np.trace(matrix))            # i == j
    p_win_b  = float(np.triu(matrix, 1).sum())    # j > i
    return p_win_a, p_draw, p_win_b

def expected_goals(team_a: dict, team_b: dict, neutral: bool = True) -> Tuple[float, float]:
    BASE_GOALS = 1.35  # Average international goals per team per game

    def form_multiplier(form: float) -> float:
        return 1.0 + 0.15 * np.clip(form, -1, 1)

    def defence_factor(conceded_xg: float) -> float:
        return conceded_xg / BASE_GOALS

    home_att_boost_a = 1.17 if (not neutral and team_a.get("is_host")) else 1.0
    home_att_boost_b = 1.17 if (not neutral and team_b.get("is_host")) else 1.0

    lambda_a = (
        team_a["att_xg"]
        * defence_factor(team_b["def_xg"])
        * form_multiplier(team_a["form"])
        * home_att_boost_a
    )

    lambda_b = (
        team_b["att_xg"]
        * defence_factor(team_a["def_xg"])
        * form_multiplier(team_b["form"])
        * home_att_boost_b
    )

    if team_a.get("altitude_penalty"):
        lambda_a *= 0.92
    if team_b.get("altitude_penalty"):
        lambda_b *= 0.92

    return max(lambda_a, 0.1), max(lambda_b, 0.1)

class DixonColesModel:

    def __init__(self, rho: float = -0.13):
        self.rho = rho
        self.fitted = False

    def predict_proba(self, team_a: dict, team_b: dict, neutral: bool = True) -> Dict[str, float]:
        lam_a, lam_b = expected_goals(team_a, team_b, neutral=neutral)
        p_win, p_draw, p_loss = outcome_probabilities(lam_a, lam_b, self.rho)

        return {
            "p_win_a":  round(p_win,  4),
            "p_draw":   round(p_draw, 4),
            "p_win_b":  round(p_loss, 4),
            "lambda_a": round(lam_a,  3),
            "lambda_b": round(lam_b,  3),
            "model":    "dixon_coles"
        }

    def simulate_score(self, team_a: dict, team_b: dict, neutral: bool = True) -> Tuple[int, int]:
        lam_a, lam_b = expected_goals(team_a, team_b, neutral=neutral)
        matrix = scoreline_probability_matrix(lam_a, lam_b, self.rho)

        # Flatten the probability matrix and sample
        flat_probs = matrix.flatten()
        flat_probs = np.clip(flat_probs, 0, None)
        flat_probs /= flat_probs.sum()

        n = matrix.shape[0]
        idx = np.random.choice(len(flat_probs), p=flat_probs)
        goals_a = idx // n
        goals_b = idx % n
        return int(goals_a), int(goals_b)

    def fit_rho(self, match_history: list) -> float:
        def neg_log_likelihood(params):
            rho = params[0]
            ll = 0.0
            for m in match_history:
                lam_a, lam_b = m["lambda_a"], m["lambda_b"]
                ga, gb = int(m["goals_a"]), int(m["goals_b"])
                ga_c, gb_c = min(ga, 8), min(gb, 8)
                mat = scoreline_probability_matrix(lam_a, lam_b, rho)
                p = max(float(mat[ga_c, gb_c]), 1e-10)
                ll -= np.log(p)
            return ll

        result = minimize(neg_log_likelihood, x0=[-0.13],
                          bounds=[(-0.5, 0.0)], method="L-BFGS-B")
        self.rho = float(result.x[0])
        self.fitted = True
        return self.rho
