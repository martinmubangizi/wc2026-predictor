# 2026 FIFA World Cup — ML Predictor

Predicts group winners, the best 8 third-placed teams, and the full knockout bracket for the 2026 FIFA World Cup using a Dixon-Coles + XGBoost ensemble and Monte Carlo simulation.

**Predicted champion: Spain — 16.9% win probability across 15,000 simulations.**


## How it works

Three-phase pipeline:

1. **Feature engineering** — World Football Elo ratings, attack/defence xG parameters, squad market value, player form ratings from confirmed June 2026 squads, EWMA recent form, host advantage, tournament experience
2. **Match outcome prediction** — Dixon-Coles corrected Poisson regression (rho = -0.13) ensembled with XGBoost classifier trained on 25,000 matches
3. **Monte Carlo simulation** — 15,000 complete tournament runs through all 12 groups, Round of 32, Quarter-finals, Semi-finals and Final, with FIFA tiebreakers and nation-weighted penalty shootouts

## Top predictions

| Team | Win% | Final% | Semi% |
|------|------|--------|-------|
| Spain | 16.9% | 27.4% | 40.7% |
| Argentina | 11.9% | 20.1% | 31.9% |
| France | 11.8% | 19.9% | 31.6% |
| Brazil | 11.4% | 20.5% | 34.7% |
| England | 8.1% | 14.2% | 24.9% |

## Usage

```bash
pip install -r requirements.txt
python predict.py --sims 15000
```

Outputs: `output/predictions.json`, `output/predictions.csv`, `output/bracket.html`

## Stack

Python · NumPy · SciPy · XGBoost · LightGBM · Monte Carlo simulation

---

*Martin Mubangizi — Fraud Risk Analyst, Wave Mobile Money · MSc Big Data Analytics*
