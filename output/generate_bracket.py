"""
output/generate_bracket.py
Generates the tournament bracket HTML visual from predictions.json
"""

import json, os, sys

def generate_bracket_html(predictions_path="output/predictions.json",
                           output_path="output/bracket.html"):
    with open(predictions_path) as f:
        p = json.load(f)

    groups = {
        "A": ["Mexico","South Africa","South Korea","Czechia"],
        "B": ["Canada","Bosnia & Herzegovina","Qatar","Switzerland"],
        "C": ["Brazil","Morocco","Haiti","Scotland"],
        "D": ["USA","Paraguay","Australia","Türkiye"],
        "E": ["Germany","Curaçao","Ivory Coast","Ecuador"],
        "F": ["Netherlands","Japan","Sweden","Tunisia"],
        "G": ["Belgium","Egypt","Iran","New Zealand"],
        "H": ["Spain","Cape Verde","Saudi Arabia","Uruguay"],
        "I": ["France","Senegal","Iraq","Norway"],
        "J": ["Argentina","Algeria","Austria","Jordan"],
        "K": ["Portugal","DR Congo","Uzbekistan","Colombia"],
        "L": ["England","Croatia","Ghana","Panama"],
    }

    # Get group winners and runner-ups by probability
    def get_top2(group_name):
        gw = p["group_winners"].get(group_name, {})
        gr = p.get("group_runners_up", {}).get(group_name, {})
        w  = max(gw.items(), key=lambda x:x[1])[0] if gw else groups[group_name][0]
        ru = max(gr.items(), key=lambda x:x[1])[0] if gr else groups[group_name][1]
        return w, ru

    # Build group data
    group_data = {}
    for g, teams in groups.items():
        winner, runner_up = get_top2(g)
        group_data[g] = {"teams": teams, "winner": winner, "runner_up": runner_up}

    # Build predicted knockout path (most likely teams)
    champ_sorted = sorted(p["champion"].items(), key=lambda x: -x[1])
    champion     = champ_sorted[0][0]
    finalist     = champ_sorted[1][0]

    semi_sorted  = sorted(p["semifinalist"].items(), key=lambda x: -x[1])
    semis        = [s[0] for s in semi_sorted[:4] if s[0] not in [champion, finalist]][:2]
    semi1 = champion; semi2 = finalist
    semi3 = semis[0] if len(semis)>0 else champ_sorted[2][0]
    semi4 = semis[1] if len(semis)>1 else champ_sorted[3][0]

    qf_sorted = sorted(p["quarterfinalist"].items(), key=lambda x: -x[1])
    qf_teams  = [q[0] for q in qf_sorted[:8]]

    # Get champion win probability
    champ_pct   = round(p["champion"][champion] * 100, 1)
    finalist_pct = round(p["champion"].get(finalist, 0) * 100, 1)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2026 FIFA World Cup Predictions — Martin Mubangizi</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@400;500;600&display=swap');

  :root {{
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2235;
    --border: rgba(255,255,255,0.08);
    --gold: #f5b942;
    --gold2: #e8963a;
    --silver: #c0c8d8;
    --green: #22c55e;
    --blue: #3b82f6;
    --red: #ef4444;
    --text: #e8ecf4;
    --muted: #6b7a99;
    --accent: #3b82f6;
  }}
  * {{ box-sizing: border-box; margin:0; padding:0; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Barlow', sans-serif;
    min-height: 100vh;
    padding: 0;
  }}

  /* ── HEADER ── */
  .header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    border-bottom: 1px solid var(--gold);
    padding: 32px 40px 28px;
    text-align: center;
  }}
  .header-badge {{
    display: inline-block;
    background: rgba(245,185,66,0.15);
    border: 1px solid rgba(245,185,66,0.4);
    border-radius: 999px;
    padding: 4px 16px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 2px;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 14px;
  }}
  .header h1 {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 48px;
    font-weight: 800;
    line-height: 1;
    color: #fff;
    margin-bottom: 6px;
  }}
  .header h1 span {{ color: var(--gold); }}
  .header-sub {{
    font-size: 14px;
    color: var(--muted);
    letter-spacing: 0.5px;
  }}

  /* ── PREDICTION HERO ── */
  .hero {{
    background: linear-gradient(135deg, rgba(59,130,246,0.12) 0%, rgba(245,185,66,0.08) 100%);
    border: 1px solid rgba(245,185,66,0.25);
    border-radius: 16px;
    margin: 32px 40px;
    padding: 32px 40px;
    display: flex;
    align-items: center;
    gap: 40px;
  }}
  .hero-trophy {{
    font-size: 72px;
    line-height: 1;
    filter: drop-shadow(0 0 24px rgba(245,185,66,0.4));
  }}
  .hero-content h2 {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 8px;
  }}
  .hero-content .winner-name {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 54px;
    font-weight: 800;
    color: #fff;
    line-height: 1;
    margin-bottom: 8px;
  }}
  .hero-stats {{
    display: flex;
    gap: 24px;
    margin-top: 16px;
  }}
  .hero-stat {{
    text-align: center;
  }}
  .hero-stat .val {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--gold);
  }}
  .hero-stat .lbl {{
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
  }}
  .methodology-note {{
    margin: 0 40px 20px;
    padding: 14px 20px;
    background: rgba(59,130,246,0.08);
    border-left: 3px solid var(--blue);
    border-radius: 4px;
    font-size: 13px;
    color: var(--muted);
    line-height: 1.6;
  }}

  /* ── SECTION TITLE ── */
  .section-title {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    padding: 0 40px;
    margin: 32px 0 16px;
  }}

  /* ── ODDS TABLE ── */
  .odds-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    padding: 0 40px;
    margin-bottom: 32px;
  }}
  .odds-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: border-color 0.2s;
  }}
  .odds-card.gold {{ border-color: rgba(245,185,66,0.5); background: rgba(245,185,66,0.06); }}
  .odds-card.silver {{ border-color: rgba(192,200,216,0.4); }}
  .odds-card.bronze {{ border-color: rgba(180,120,60,0.4); }}
  .rank-badge {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 20px;
    font-weight: 800;
    min-width: 28px;
    color: var(--muted);
  }}
  .rank-badge.r1 {{ color: var(--gold); }}
  .rank-badge.r2 {{ color: var(--silver); }}
  .rank-badge.r3 {{ color: #cd7f32; }}
  .odds-info .team-name {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
  }}
  .odds-info .prob-bar-wrap {{
    margin-top: 5px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .prob-bar {{
    height: 3px;
    background: var(--border);
    border-radius: 2px;
    flex: 1;
    overflow: hidden;
  }}
  .prob-bar-fill {{
    height: 100%;
    background: var(--gold);
    border-radius: 2px;
  }}
  .prob-pct {{
    font-size: 12px;
    font-weight: 600;
    color: var(--gold);
    min-width: 36px;
    text-align: right;
  }}

  /* ── GROUPS ── */
  .groups-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    padding: 0 40px;
    margin-bottom: 32px;
  }}
  .group-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }}
  .group-header {{
    background: var(--surface2);
    padding: 8px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .group-letter {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: var(--gold);
  }}
  .group-label {{
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
  }}
  .group-team {{
    padding: 7px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid var(--border);
    font-size: 13px;
  }}
  .group-team:first-of-type {{ border-top: none; }}
  .group-team.advances {{ background: rgba(34,197,94,0.06); }}
  .group-team.winner {{ background: rgba(245,185,66,0.08); }}
  .team-name-g {{
    font-weight: 500;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .adv-dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--green);
  }}
  .win-dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--gold);
  }}
  .elim-dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--muted);
    opacity: 0.5;
  }}
  .group-pct {{
    font-size: 11px;
    color: var(--muted);
  }}
  .group-pct.win {{ color: var(--gold); font-weight: 600; }}

  /* ── KNOCKOUT BRACKET ── */
  .bracket-container {{
    padding: 0 40px 40px;
  }}
  .bracket {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
    gap: 0;
    align-items: center;
  }}
  .bracket-col {{
    display: flex;
    flex-direction: column;
    gap: 0;
    align-items: stretch;
  }}
  .bracket-match {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin: 4px 6px;
    overflow: hidden;
  }}
  .bracket-team {{
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 500;
    color: var(--muted);
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
    overflow: hidden;
  }}
  .bracket-team:last-child {{ border-bottom: none; }}
  .bracket-team.predicted {{
    color: var(--text);
    background: rgba(59,130,246,0.06);
  }}
  .bracket-team.champion {{
    color: var(--gold);
    font-weight: 700;
    background: rgba(245,185,66,0.1);
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 14px;
  }}
  .bracket-pct {{
    font-size: 10px;
    color: var(--gold);
    font-weight: 600;
    margin-left: 4px;
  }}
  .col-label {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    text-align: center;
    padding: 0 6px;
    margin-bottom: 8px;
  }}
  .final-box {{
    background: linear-gradient(135deg, rgba(245,185,66,0.15), rgba(245,185,66,0.05));
    border: 1px solid rgba(245,185,66,0.4);
    border-radius: 12px;
    margin: 4px 2px;
    overflow: hidden;
  }}
  .final-label {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--gold);
    text-align: center;
    padding: 6px 4px 2px;
  }}

  /* ── FOOTER ── */
  .footer {{
    text-align: center;
    padding: 24px 40px;
    border-top: 1px solid var(--border);
    font-size: 12px;
    color: var(--muted);
    line-height: 1.8;
  }}
  .footer a {{ color: var(--blue); text-decoration: none; }}
</style>
</head>
<body>

<!-- HEADER -->
<div class="header">
  <div class="header-badge">Machine Learning Prediction</div>
  <h1>2026 FIFA <span>World Cup</span></h1>
  <div class="header-sub">Dixon-Coles + XGBoost + Player Form Weighting &nbsp;·&nbsp; {p['metadata']['simulations']:,} Monte Carlo Simulations</div>
</div>

<!-- HERO WINNER -->
<div class="hero">
  <div class="hero-trophy">🏆</div>
  <div class="hero-content">
    <h2>Predicted Champion</h2>
    <div class="winner-name">{champion}</div>
    <div style="font-size:14px; color:var(--muted); margin-top:4px;">Based on Elo ratings · player form · squad depth · historical data</div>
    <div class="hero-stats">
      <div class="hero-stat">
        <div class="val">{champ_pct}%</div>
        <div class="lbl">Win probability</div>
      </div>
      <div class="hero-stat">
        <div class="val">{round(p['finalist'].get(champion,0)*100,1)}%</div>
        <div class="lbl">Final probability</div>
      </div>
      <div class="hero-stat">
        <div class="val">{round(p['semifinalist'].get(champion,0)*100,1)}%</div>
        <div class="lbl">Semi probability</div>
      </div>
      <div class="hero-stat">
        <div class="val">{round(p['quarterfinalist'].get(champion,0)*100,1)}%</div>
        <div class="lbl">QF probability</div>
      </div>
    </div>
  </div>
</div>

<!-- METHODOLOGY -->
<div class="methodology-note">
  <strong style="color:var(--text);">Model methodology:</strong> This prediction engine combines a <em>Dixon-Coles corrected bivariate Poisson model</em> (for low-score calibration), an <em>XGBoost gradient-boosted classifier</em> trained on 25,000 synthetic international matches, and a <em>player form multiplier</em> that adjusts each team's attack/defence parameters based on their key players' current-season ratings. {p['metadata']['simulations']:,} complete tournament simulations were run to produce stable probability estimates.
</div>

<!-- TOP CONTENDERS -->
<div class="section-title">Tournament favourites — win probability</div>
<div class="odds-grid">
"""

    # Top 12 teams
    top12 = champ_sorted[:12]
    max_p  = top12[0][1] if top12 else 1

    for i, (team, prob) in enumerate(top12):
        rank_class = "gold" if i==0 else ("silver" if i==1 else ("bronze" if i==2 else ""))
        badge_class = f"r{i+1}" if i<3 else ""
        bar_width   = round(prob / max_p * 100)
        pct_str     = f"{prob*100:.1f}%"
        fin_pct     = round(p["finalist"].get(team,0)*100, 1)
        html += f"""  <div class="odds-card {rank_class}">
    <div class="rank-badge {badge_class}">{i+1}</div>
    <div class="odds-info" style="flex:1; min-width:0;">
      <div class="team-name">{team}</div>
      <div class="prob-bar-wrap">
        <div class="prob-bar"><div class="prob-bar-fill" style="width:{bar_width}%"></div></div>
        <span class="prob-pct">{pct_str}</span>
      </div>
      <div style="font-size:10px; color:var(--muted); margin-top:3px;">Final: {fin_pct}%</div>
    </div>
  </div>
"""

    html += """</div>

<!-- GROUPS -->
<div class="section-title">Group stage — predicted outcomes</div>
<div class="groups-grid">
"""

    # Get group advance and winner probabilities
    for g in sorted(groups.keys()):
        teams = groups[g]
        gw_probs = p["group_winners"].get(g, {})
        gr_probs = p.get("group_runners_up", {}).get(g, {})
        adv_probs = p["group_advance"]

        # Predict 1st and 2nd
        predicted_winner = max(gw_probs.items(), key=lambda x:x[1])[0] if gw_probs else teams[0]
        predicted_runner = max(gr_probs.items(), key=lambda x:x[1])[0] if gr_probs else teams[1]

        html += f"""  <div class="group-card">
    <div class="group-header">
      <span class="group-letter">Group {g}</span>
      <span class="group-label">Predicted 1st: {predicted_winner}</span>
    </div>
"""
        for team in teams:
            is_winner  = team == predicted_winner
            is_runner  = team == predicted_runner
            adv_p      = round(adv_probs.get(team, 0) * 100)
            gw_p       = round(gw_probs.get(team, 0) * 100)

            if is_winner:
                row_class  = "group-team winner"
                dot_html   = '<span class="win-dot"></span>'
                pct_class  = "group-pct win"
                pct_txt    = f"{gw_p}% to win"
            elif is_runner:
                row_class  = "group-team advances"
                dot_html   = '<span class="adv-dot"></span>'
                pct_class  = "group-pct"
                pct_txt    = f"{adv_p}% advance"
            else:
                row_class  = "group-team"
                dot_html   = '<span class="elim-dot"></span>'
                pct_class  = "group-pct"
                pct_txt    = f"{adv_p}% advance"

            html += f"""    <div class="{row_class}">
      <span class="team-name-g">{dot_html} {team}</span>
      <span class="{pct_class}">{pct_txt}</span>
    </div>
"""
        html += "  </div>\n"

    html += "</div>\n"

    # ── KNOCKOUT BRACKET ─────────────────────────────────────────────────────
    # Build a simplified R16 → QF → SF → F → W bracket
    # Use most likely teams per round
    qf_sorted  = sorted(p["quarterfinalist"].items(), key=lambda x:-x[1])
    sf_sorted  = sorted(p["semifinalist"].items(), key=lambda x:-x[1])
    fin_sorted = sorted(p["finalist"].items(), key=lambda x:-x[1])

    qf8  = [t for t,_ in qf_sorted[:8]]
    sf4  = [t for t,_ in sf_sorted[:4]]
    fin2 = [champion, finalist]

    def match_box(t1, t2, cls1="predicted", cls2="predicted", col_span=1):
        p1 = round(p["quarterfinalist"].get(t1,0)*100,0)
        p2 = round(p["quarterfinalist"].get(t2,0)*100,0)
        return f"""<div class="bracket-match">
  <div class="bracket-team {cls1}">{t1} <span class="bracket-pct">{int(p1)}%</span></div>
  <div class="bracket-team {cls2}">{t2} <span class="bracket-pct">{int(p2)}%</span></div>
</div>"""

    html += """<!-- KNOCKOUT BRACKET -->
<div class="section-title">Predicted knockout path</div>
<div class="bracket-container">
<div style="display:grid; grid-template-columns: 2fr 1.5fr 1fr auto 1fr 1.5fr 2fr; gap:0; align-items:start;">

<div>
  <div class="col-label">Quarterfinals</div>
"""

    def bracket_entry(team, pct_key="quarterfinalist"):
        pct = round(p[pct_key].get(team,0)*100,1)
        return (team, pct)

    # Left QF
    for i in range(0, min(4, len(qf8)), 2):
        t1 = qf8[i]   if len(qf8)>i   else "TBD"
        t2 = qf8[i+1] if len(qf8)>i+1 else "TBD"
        pct1 = round(p["quarterfinalist"].get(t1,0)*100,0)
        pct2 = round(p["quarterfinalist"].get(t2,0)*100,0)
        html += f"""  <div class="bracket-match">
    <div class="bracket-team predicted">{t1} <span class="bracket-pct">{int(pct1)}%</span></div>
    <div class="bracket-team predicted">{t2} <span class="bracket-pct">{int(pct2)}%</span></div>
  </div>
"""

    html += "</div>\n<div>\n  <div class='col-label'>Semifinals</div>\n"

    # Left SF
    for i in range(0, min(2, len(sf4)), 1):
        t = sf4[i]
        pct = round(p["semifinalist"].get(t,0)*100,0)
        html += f"""  <div class="bracket-match">
    <div class="bracket-team predicted">{t} <span class="bracket-pct">{int(pct)}%</span></div>
  </div>
"""

    html += f"""</div>
<div>
  <div class="col-label">Finalists</div>
  <div class="bracket-match">
    <div class="bracket-team predicted">{fin2[0]} <span class="bracket-pct">{round(p['finalist'].get(fin2[0],0)*100,0)}%</span></div>
  </div>
  <div class="bracket-match">
    <div class="bracket-team predicted">{fin2[1] if len(fin2)>1 else 'TBD'} <span class="bracket-pct">{round(p['finalist'].get(fin2[1],0)*100,0) if len(fin2)>1 else 0}%</span></div>
  </div>
</div>

<div>
  <div class="col-label" style="text-align:center;">&#x1F3C6; Final</div>
  <div class="final-box">
    <div class="final-label">🏆 Champion</div>
    <div class="bracket-team champion" style="justify-content:center; padding:10px 12px; font-size:16px;">{champion}</div>
    <div style="text-align:center; font-size:11px; color:var(--gold); padding:0 8px 8px; font-weight:600;">{champ_pct}% win probability</div>
    <div style="text-align:center; font-size:10px; color:var(--muted); padding:0 8px 8px;">vs. {fin2[1] if len(fin2)>1 else 'TBD'} ({finalist_pct}%)</div>
  </div>
</div>

<div>
  <div class="col-label">Finalists</div>
  <div class="bracket-match">
    <div class="bracket-team predicted">{sf4[2] if len(sf4)>2 else 'TBD'} <span class="bracket-pct">{round(p['semifinalist'].get(sf4[2],0)*100,0) if len(sf4)>2 else 0}%</span></div>
  </div>
  <div class="bracket-match">
    <div class="bracket-team predicted">{sf4[3] if len(sf4)>3 else 'TBD'} <span class="bracket-pct">{round(p['semifinalist'].get(sf4[3],0)*100,0) if len(sf4)>3 else 0}%</span></div>
  </div>
</div>

<div>
  <div class="col-label">Semifinals</div>
"""

    for i in range(2, min(4, len(sf4))):
        t = sf4[i]
        pct = round(p["semifinalist"].get(t,0)*100,0)
        html += f"""  <div class="bracket-match">
    <div class="bracket-team predicted">{t} <span class="bracket-pct">{int(pct)}%</span></div>
  </div>
"""

    html += """</div>
<div>
  <div class="col-label">Quarterfinals</div>
"""

    for i in range(4, min(8, len(qf8)), 2):
        t1 = qf8[i]   if len(qf8)>i   else "TBD"
        t2 = qf8[i+1] if len(qf8)>i+1 else "TBD"
        pct1 = round(p["quarterfinalist"].get(t1,0)*100,0)
        pct2 = round(p["quarterfinalist"].get(t2,0)*100,0)
        html += f"""  <div class="bracket-match">
    <div class="bracket-team predicted">{t1} <span class="bracket-pct">{int(pct1)}%</span></div>
    <div class="bracket-team predicted">{t2} <span class="bracket-pct">{int(pct2)}%</span></div>
  </div>
"""

    html += """</div>
</div>
</div>

<!-- FOOTER -->
<div class="footer">
  <strong style="color:var(--text);">Martin Mubangizi</strong> &nbsp;·&nbsp; Fraud Risk Analyst &amp; Data Science Educator &nbsp;·&nbsp; Kampala, Uganda<br>
  Built with Python (Dixon-Coles + XGBoost + Monte Carlo Simulation) &nbsp;·&nbsp;
  <a href="https://github.com/martinmubangizi" target="_blank">github.com/martinmubangizi</a><br>
  <span style="font-size:11px;">⚠️ Probabilistic model — football is beautifully unpredictable. This is statistical inference, not certainty.</span>
</div>

</body>
</html>
"""

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


if __name__ == "__main__":
    path = generate_bracket_html()
    print(f"Bracket saved to: {path}")
