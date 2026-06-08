from data.teams import get_groups, get_team, TEAMS
from simulator.group_stage import simulate_all_groups, extract_qualifiers
from simulator.knockout import build_r32_bracket, simulate_knockout_stage
from typing import Dict

def _prewarm_cache(model, team_lookup):
    teams = list(team_lookup.values())
    for ta in teams:
        for tb in teams:
            if ta["name"] != tb["name"]:
                model.predict_proba(ta, tb, neutral=True)
                model.simulate_score(ta, tb, neutral=True)

def run_one_tournament(model) -> Dict:
    groups      = get_groups()
    team_lookup = {name: get_team(name) for name in TEAMS}

    group_results = simulate_all_groups(groups, team_lookup, model)
    qualifiers    = extract_qualifiers(group_results)

    bracket = build_r32_bracket(
        qualifiers["group_winners"],
        qualifiers["runners_up"],
        qualifiers["advancing_third"],
    )
    knockout_results = simulate_knockout_stage(bracket, team_lookup, model)

    return {
        "group_results":   group_results,
        "qualifiers":      qualifiers,
        "knockout":        knockout_results,
        "champion":        knockout_results["champion"],
        "finalist":        knockout_results["finalist"],
        "semifinalists":   knockout_results["semifinalists"],
        "quarterfinalists":knockout_results["quarterfinalists"],
        "r16":             knockout_results["r16"],
    }
