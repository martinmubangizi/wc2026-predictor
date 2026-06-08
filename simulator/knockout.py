import numpy as np
from typing import Dict, List, Tuple, Optional
from simulator.match import simulate_match

STAGES = ["Round of 32", "Round of 16", "Quarterfinals", "Semifinals", "Final"]

def build_r32_bracket(
    group_winners: Dict[str, str],
    runners_up: Dict[str, str],
    advancing_third: List[str],
) -> List[Tuple[str, str]]:
    groups = sorted(group_winners.keys())  # A-L

    winners = [group_winners[g] for g in groups]       # 12 teams
    runners = [runners_up[g] for g in groups]          # 12 teams
    thirds = list(advancing_third)                      # 8 teams

    np.random.shuffle(thirds)

    # Build 16 matches
    # Path 1: 8 winners vs 8 thirds

    # Match 1-8: winner[i] vs third[i]

    bracket = []
    for i in range(8):
        bracket.append((winners[i], thirds[i]))

    for i in range(4):
        bracket.append((winners[8 + i], runners[i]))

    # Remaining runners cross-bracket
    runner_pairs = list(zip(runners[4:8], runners[8:12]))
    bracket.extend(runner_pairs)

    return bracket

def simulate_knockout_stage(
    bracket: List[Tuple[str, str]],
    team_lookup: Dict[str, dict],
    model,
) -> Dict:
    stage_results = {}
    current_bracket = list(bracket)
    stage_names = STAGES.copy()

    # Track each team's furthest stage
    stage_reached = {name: "Group Stage" for name in team_lookup}

    # Track progression
    quarterfinalists = []
    semifinalists = []
    finalist_loser = None
    champion = None

    for stage in stage_names:
        matches = []
        next_bracket_teams = []

        for match_pair in current_bracket:
            ta_name, tb_name = match_pair
            ta = team_lookup[ta_name]
            tb = team_lookup[tb_name]

            result = simulate_match(ta, tb, model, knockout=True, neutral=True)
            matches.append(result)

            winner = result["winner"]
            loser = tb_name if winner == ta_name else ta_name

            stage_reached[winner] = stage
            if stage_reached[loser] == "Group Stage":
                stage_reached[loser] = stage  # At least reached this stage

            next_bracket_teams.append(winner)

        stage_results[stage] = matches

        if stage == "Round of 32":
            pass  # next stage is R16
        elif stage == "Round of 16":
            r16_losers = [m["team_b"] if m["winner"] == m["team_a"] else m["team_a"]
                          for m in matches]
        elif stage == "Quarterfinals":
            quarterfinalists = [m["team_a"] for m in matches] + [m["team_b"] for m in matches]
        elif stage == "Semifinals":
            semifinalists = next_bracket_teams[:]
            finalist_loser_matches = matches
        elif stage == "Final":
            champion = next_bracket_teams[0]
            finalist_loser = (
                matches[0]["team_b"]
                if matches[0]["winner"] == matches[0]["team_a"]
                else matches[0]["team_a"]
            )
            next_bracket_teams = [champion]
            break

        # Pair up winners for next round
        next_bracket = [
            (next_bracket_teams[i], next_bracket_teams[i + 1])
            for i in range(0, len(next_bracket_teams), 2)
        ]
        current_bracket = next_bracket

    # Semifinalists = the 4 teams in the Final 4
    semi_matches = stage_results.get("Semifinals", [])
    semifinalists_all = list({m["team_a"] for m in semi_matches} | {m["team_b"] for m in semi_matches})
    qf_matches = stage_results.get("Quarterfinals", [])
    quarterfinalists_all = list({m["team_a"] for m in qf_matches} | {m["team_b"] for m in qf_matches})
    r16_matches = stage_results.get("Round of 16", [])
    r16_all = list({m["team_a"] for m in r16_matches} | {m["team_b"] for m in r16_matches})

    return {
        "champion": champion,
        "finalist": finalist_loser,
        "semifinalists": semifinalists_all,
        "quarterfinalists": quarterfinalists_all,
        "r16": r16_all,
        "stage_results": stage_results,
        "stage_reached": stage_reached,
    }
