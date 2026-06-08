import numpy as np
from typing import Dict, Tuple
from models.dixon_coles import DixonColesModel, expected_goals, scoreline_probability_matrix
from models.xgboost_model import XGBoostMatchPredictor

def player_form_multiplier(team: dict) -> float:
    star = team.get("star_rating", 7.5)
    depth = team.get("depth_rating", 7.0)
    composite = 0.7 * star + 0.3 * depth
    # Map [5.0, 10.0] → [0.92, 1.10]
    mult = 0.92 + (composite - 5.0) / (10.0 - 5.0) * (1.10 - 0.92)
    return round(float(np.clip(mult, 0.88, 1.12)), 4)

class EnsemblePredictor:
    def __init__(self, dc_weight=0.50, xgb_weight=0.50, rho=-0.13, xgb_backend="xgboost"):
        self.dc_weight  = dc_weight
        self.xgb_weight = xgb_weight
        self.dc_model   = DixonColesModel(rho=rho)
        self.xgb_model  = XGBoostMatchPredictor(backend=xgb_backend)
        self._cache      = {}
        self._score_cache = {}

    def fit(self, train_xgb=True, n_synthetic=20000):
        if train_xgb:
            self.xgb_model.train_on_synthetic(n=n_synthetic)
        return self

    def _apply_player_form(self, team_a: dict, team_b: dict) -> Tuple[dict, dict]:
        ta, tb = team_a.copy(), team_b.copy()
        ta["att_xg"] = ta["att_xg"] * player_form_multiplier(ta)
        tb["att_xg"] = tb["att_xg"] * player_form_multiplier(tb)
        ta["def_xg"] = ta.get("def_xg", 1.1) * (2.0 - player_form_multiplier(tb) * 0.5)
        tb["def_xg"] = tb.get("def_xg", 1.1) * (2.0 - player_form_multiplier(ta) * 0.5)
        return ta, tb

    def predict_proba(self, team_a: dict, team_b: dict, neutral=True) -> Dict[str, float]:
        key = (team_a["name"], team_b["name"], neutral)
        if key in self._cache:
            return self._cache[key]

        ta, tb = self._apply_player_form(team_a, team_b)
        dc  = self.dc_model.predict_proba(ta, tb, neutral=neutral)
        xgb = self.xgb_model.predict_proba(ta, tb)

        p_win_a = self.dc_weight * dc["p_win_a"] + self.xgb_weight * xgb["p_win_a"]
        p_draw  = self.dc_weight * dc["p_draw"]  + self.xgb_weight * xgb["p_draw"]
        p_win_b = self.dc_weight * dc["p_win_b"] + self.xgb_weight * xgb["p_win_b"]
        total   = p_win_a + p_draw + p_win_b
        result  = {
            "p_win_a": round(p_win_a / total, 4),
            "p_draw":  round(p_draw  / total, 4),
            "p_win_b": round(p_win_b / total, 4),
        }
        self._cache[key] = result
        return result

    def simulate_score(self, team_a: dict, team_b: dict, neutral=True) -> Tuple[int, int]:
        key = (team_a["name"], team_b["name"], neutral)
        if key not in self._score_cache:
            ta, tb = self._apply_player_form(team_a, team_b)
            lam_a, lam_b = expected_goals(ta, tb, neutral=neutral)
            matrix = scoreline_probability_matrix(lam_a, lam_b, self.dc_model.rho)
            flat = np.clip(matrix.flatten(), 0, None)
            flat /= flat.sum()
            self._score_cache[key] = flat
        flat = self._score_cache[key]
        idx  = np.random.choice(81, p=flat)
        return int(idx // 9), int(idx % 9)

    def clear_cache(self):
        self._cache.clear()
        self._score_cache.clear()

    def update_weights(self, dc_rps: float, xgb_rps: float):
        dc_inv  = 1.0 / max(dc_rps,  1e-6)
        xgb_inv = 1.0 / max(xgb_rps, 1e-6)
        total = dc_inv + xgb_inv
        self.dc_weight  = round(dc_inv  / total, 3)
        self.xgb_weight = round(xgb_inv / total, 3)
        return self.dc_weight, self.xgb_weight
