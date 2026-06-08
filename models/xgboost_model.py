import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional

try:
    from xgboost import XGBClassifier
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

try:
    from lightgbm import LGBMClassifier
    LGB_AVAILABLE = True
except ImportError:
    LGB_AVAILABLE = False

def build_match_features(team_a: dict, team_b: dict) -> np.ndarray:
    elo_diff = (team_a["elo"] - team_b["elo"]) / 400.0  # Normalised
    att_diff = team_a["att_xg"] - team_b["att_xg"]
    def_diff = team_b["def_xg"] - team_a["def_xg"]
    squad_diff = (team_a["squad_val"] - team_b["squad_val"]) / 100.0
    form_diff = team_a.get("form", 0.0) - team_b.get("form", 0.0)
    t_exp_diff = team_a.get("t_exp", 3) - team_b.get("t_exp", 3)
    pen_diff = team_a.get("pen_skill", 0.65) - team_b.get("pen_skill", 0.65)
    peak_diff = team_a.get("peak_pct", 0.55) - team_b.get("peak_pct", 0.55)
    home_a = float(team_a.get("is_host", False))
    home_b = float(team_b.get("is_host", False))
    alt_a = float(team_a.get("altitude_penalty", False))
    alt_b = float(team_b.get("altitude_penalty", False))
    rest_diff = team_a.get("rest_days", 4) - team_b.get("rest_days", 4)
    xg_ratio = team_a["att_xg"] / max(team_b["att_xg"], 0.01)
    def_ratio = team_a["def_xg"] / max(team_b["def_xg"], 0.01)
    interaction_elo_form = elo_diff * form_diff
    interaction_val_exp = squad_diff * (t_exp_diff / 5.0)

    features = np.array([
        elo_diff,
        team_a["elo"] / 2000.0,
        team_b["elo"] / 2000.0,
        att_diff,
        def_diff,
        squad_diff,
        form_diff,
        team_a.get("form", 0.0),
        team_b.get("form", 0.0),
        t_exp_diff / 5.0,
        pen_diff,
        peak_diff,
        home_a,
        home_b,
        alt_a,
        alt_b,
        rest_diff / 7.0,
        xg_ratio,
        def_ratio,
        interaction_elo_form,
        interaction_val_exp,
    ], dtype=np.float32)

    return features

FEATURE_NAMES = [
    "elo_diff", "elo_a_norm", "elo_b_norm",
    "att_diff", "def_diff", "squad_val_diff",
    "form_diff", "form_a", "form_b",
    "t_exp_diff", "pen_skill_diff", "peak_pct_diff",
    "home_adv_a", "home_adv_b",
    "altitude_pen_a", "altitude_pen_b",
    "rest_days_diff",
    "xg_ratio", "def_ratio",
    "elo_x_form", "val_x_exp"
]

def generate_synthetic_training_data(n_matches: int = 20000, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    X_rows = []
    y_labels = []

    for _ in range(n_matches):
        # Random team profiles
        def random_team(host_prob=0.1):
            elo = float(rng.integers(1600, 2100))
            att = float(rng.uniform(0.8, 2.0))
            dfc = float(rng.uniform(0.7, 1.6))
            return {
                "elo": elo, "att_xg": att, "def_xg": dfc,
                "squad_val": float(rng.integers(40, 220)),
                "form": float(rng.uniform(-0.5, 0.8)),
                "t_exp": int(rng.integers(0, 6)),
                "pen_skill": float(rng.uniform(0.48, 0.78)),
                "peak_pct": float(rng.uniform(0.40, 0.70)),
                "is_host": rng.random() < host_prob,
                "altitude_penalty": rng.random() < 0.05,
                "rest_days": int(rng.integers(2, 8)),
            }

        ta = random_team()
        tb = random_team()
        feats = build_match_features(ta, tb)

        # Ground truth: Elo-based win probability + noise
        elo_diff = ta["elo"] - tb["elo"]
        p_win_a = 1 / (1 + 10 ** (-elo_diff / 400))
        p_win_b = 1 / (1 + 10 ** (elo_diff / 400))
        p_draw = 1 - p_win_a - p_win_b
        # Typical draw rate ~25% in international football
        draw_baseline = 0.25
        p_win_a_adj = p_win_a * (1 - draw_baseline)
        p_win_b_adj = p_win_b * (1 - draw_baseline)
        p_draw_adj = draw_baseline

        outcome = rng.choice([0, 1, 2], p=[p_win_a_adj, p_draw_adj, p_win_b_adj])
        X_rows.append(feats)
        y_labels.append(outcome)

    return np.vstack(X_rows), np.array(y_labels)

class XGBoostMatchPredictor:

    def __init__(self, backend: str = "xgboost"):
        self.backend = backend
        self.model = None
        self.fitted = False

        if backend == "xgboost" and XGB_AVAILABLE:
            self.model = XGBClassifier(
                n_estimators=500,
                max_depth=5,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                use_label_encoder=False,
                eval_metric="mlogloss",
                random_state=42,
                n_jobs=-1,
            )
        elif backend == "lightgbm" and LGB_AVAILABLE:
            self.model = LGBMClassifier(
                n_estimators=500,
                max_depth=5,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1,
                verbose=-1,
            )
        else:
            # Fallback: simple Elo-based logistic approximation
            self.model = None
            self.backend = "elo_fallback"

    def fit(self, X: np.ndarray, y: np.ndarray):
        if self.model is not None:
            self.model.fit(X, y)
            self.fitted = True
        else:
            self.fitted = True  # fallback doesn't need fitting

    def predict_proba(self, team_a: dict, team_b: dict) -> Dict[str, float]:
        feats = build_match_features(team_a, team_b).reshape(1, -1)

        if self.fitted and self.model is not None:
            probs = self.model.predict_proba(feats)[0]
            return {
                "p_win_a": float(probs[0]),
                "p_draw":  float(probs[1]),
                "p_win_b": float(probs[2]),
                "model":   self.backend
            }
        else:
            # Elo fallback
            elo_diff = team_a["elo"] - team_b["elo"]
            p_win_a = 1 / (1 + 10 ** (-elo_diff / 400))
            p_win_b = 1 / (1 + 10 ** (elo_diff / 400))
            draw_rate = 0.25
            p_win_a_adj = p_win_a * (1 - draw_rate)
            p_win_b_adj = p_win_b * (1 - draw_rate)
            return {
                "p_win_a": round(p_win_a_adj, 4),
                "p_draw":  round(draw_rate, 4),
                "p_win_b": round(p_win_b_adj, 4),
                "model":   "elo_fallback"
            }

    def get_feature_importance(self) -> Optional[Dict[str, float]]:
        if self.model is not None and self.fitted and hasattr(self.model, "feature_importances_"):
            return dict(zip(FEATURE_NAMES, self.model.feature_importances_))
        return None

    def train_on_synthetic(self, n: int = 20000):
        X, y = generate_synthetic_training_data(n)
        self.fit(X, y)
        return self
