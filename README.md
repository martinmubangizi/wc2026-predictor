# 2026 FIFA World Cup: Probabilistic Tournament Prediction

A hybrid statistical model for estimating win probabilities across all stages of the 2026 FIFA World Cup. The system combines a Dixon-Coles corrected bivariate Poisson regression model with an XGBoost gradient-boosted classifier, calibrated via Ranked Probability Score (RPS) on held-out tournament data and ensembled through Monte Carlo simulation over the full 48-team draw structure.

**Point estimate: Spain (P(champion) = 0.169, 95% CI: [0.161, 0.177]) across N = 15,000 simulation runs.**


## Model Architecture

### 1. Match Outcome Distribution

Each match is modelled as a pair of conditionally independent Poisson random variables:

X ~ Poisson(λ_A),  Y ~ Poisson(λ_B)

where λ_A and λ_B represent the expected goal counts for teams A and B respectively. The joint density is corrected using the Dixon-Coles adjustment (Dixon & Coles, 1997):

P(X=x, Y=y) = τ(x, y, λ_A, λ_B, ρ) · P_Pois(x; λ_A) · P_Pois(y; λ_B)

The correction factor τ adjusts the four low-score cells {(0,0), (1,0), (0,1), (1,1)}, which standard Poisson systematically underestimates. The parameter ρ is estimated via MLE on historical international match data; empirical fit yields ρ = -0.13.

Expected goals are parameterised as:

λ_A = α_A · β_B · γ · φ_A

where α_A is team A's attack strength (xG-based, 24-month exponentially weighted), β_B is opponent B's defensive weakness, γ encodes host-nation advantage (fitted at +17% for USA/Canada/Mexico), and φ_A is a player-form multiplier derived from the squad's composite star and depth ratings.

### 2. XGBoost Classifier

A gradient-boosted decision tree ensemble (500 estimators, max depth 5, learning rate 0.05) is trained to predict the ternary outcome {Win, Draw, Loss} from a 21-dimensional feature vector including:

- Elo rating differential (normalised by 400)
- Attack and defence xG differentials
- Squad market value ratio
- EWMA form score (span = 15 matches)
- Tournament experience (appearances in last 5 World Cups)
- Host advantage indicator
- Altitude penalty flag
- Rest days differential
- Penalty conversion skill differential
- Cross-interaction terms (Elo x form, squad value x experience)

Trained on N = 25,000 synthetic international match samples generated from Elo-based outcome probabilities. Evaluated using multi-class log-loss and RPS on held-out data.

### 3. Ensemble

Predictions from both models are combined as a calibration-weighted linear blend:

P_ensemble(outcome) = w_DC · P_DC(outcome) + w_XGB · P_XGB(outcome)

Weights are derived from backtested RPS: w_DC = 0.503, w_XGB = 0.497. Both models are near-identically calibrated on international match data (RPS_DC = 0.220, RPS_XGB = 0.222 vs. naive baseline of 0.333).

### 4. Tournament Simulation

The full 48-team 2026 structure is simulated N = 15,000 times. Each run:

1. Simulates all 72 group-stage matches using the ensemble predictor
2. Applies FIFA tiebreakers (points > GD > GF > H2H > drawing of lots)
3. Identifies the 8 best third-placed teams by points, GD and GF
4. Generates the Round of 32 bracket per the official FIFA draw seeding matrix
5. Resolves knockout ties via simulated extra time and penalty shootout (Bernoulli trials weighted by national historical conversion rates)

All 2,256 ordered team-pair matchup probabilities and scoreline distributions are pre-computed and cached prior to the simulation loop, achieving ~4ms per full tournament run.


## Results (N = 15,000)

| Rank | Team | P(Champion) | P(Final) | P(Semi) | P(QF) |
|------|------|-------------|----------|---------|-------|
| 1 | Spain | 0.169 | 0.274 | 0.407 | 0.584 |
| 2 | Argentina | 0.119 | 0.201 | 0.319 | 0.502 |
| 3 | France | 0.118 | 0.199 | 0.316 | 0.493 |
| 4 | Brazil | 0.114 | 0.205 | 0.347 | 0.509 |
| 5 | England | 0.081 | 0.142 | 0.249 | 0.438 |
| 6 | Germany | 0.062 | 0.125 | 0.226 | 0.421 |

Model uncertainty is quantified via bootstrap resampling across simulation runs. Convergence was assessed by monitoring the standard error of P(champion) estimates across progressive batch sizes; estimates stabilise at N ≈ 8,000 for top-ranked teams.


## Calibration

Backtested using a rolling-window approach on three prior tournaments:

- Train on matches up to 2013, evaluate on 2014 World Cup
- Train on matches up to 2017, evaluate on 2018 World Cup
- Train on matches up to 2021, evaluate on 2022 World Cup

Primary evaluation metric: Ranked Probability Score (RPS), defined as:

RPS = (1/2) · Σ_{k=1}^{K-1} (F_k - O_k)²

where F_k is the predicted CDF and O_k is the observed CDF over the ordered outcome space {Win, Draw, Loss}. Lower RPS indicates better calibration. A uniformly distributed predictor scores RPS = 0.333.


## Usage

pip install -r requirements.txt
python predict.py --sims 15000

Outputs to `output/`: `predictions.json`, `predictions.csv`, `bracket.html`


## References

Dixon, M.J. & Coles, S.G. (1997). Modelling Association Football Scores and Inefficiencies in the Football Betting Market. *Applied Statistics*, 46(2), 265-280.

Maher, M.J. (1982). Modelling Association Football Scores. *Statistica Neerlandica*, 36(3), 109-118.

Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. *KDD 2016*.


*Martin Mubangizi — Fraud Risk Analyst, Wave Mobile Money. MSc Big Data Analytics, Victoria University.*
