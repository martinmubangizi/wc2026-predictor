import numpy as np
from typing import Dict, List, Tuple
from simulator.match import simulate_match

def initialise_table(teams):
    return {t: {"pts":0,"gf":0,"ga":0,"gd":0,"h2h":{}} for t in teams}

def apply_result(table, result):
    ta, tb = result["team_a"], result["team_b"]
    ga, gb = result["goals_a"], result["goals_b"]
    table[ta]["gf"] += ga; table[ta]["ga"] += gb; table[ta]["gd"] += ga-gb
    table[tb]["gf"] += gb; table[tb]["ga"] += ga; table[tb]["gd"] += gb-ga
    for a,b in [(ta,tb),(tb,ta)]:
        if b not in table[a]["h2h"]:
            table[a]["h2h"][b] = {"pts":0,"gd":0,"gf":0}
    if result["winner"] == ta:
        table[ta]["pts"] += 3
        table[ta]["h2h"][tb]["pts"] += 3
    elif result["winner"] == tb:
        table[tb]["pts"] += 3
        table[tb]["h2h"][ta]["pts"] += 3
    else:
        table[ta]["pts"] += 1; table[tb]["pts"] += 1
        table[ta]["h2h"][tb]["pts"] += 1; table[tb]["h2h"][ta]["pts"] += 1
    table[ta]["h2h"][tb]["gd"] += ga-gb; table[ta]["h2h"][tb]["gf"] += ga
    table[tb]["h2h"][ta]["gd"] += gb-ga; table[tb]["h2h"][ta]["gf"] += gb

def sort_group(table, team_names):
    def sort_key(n):
        t = table[n]
        return (-t["pts"], -t["gd"], -t["gf"])
    sorted_t = sorted(team_names, key=sort_key)
    # H2H tiebreaker for equal pts/gd/gf
    result = []
    i = 0
    while i < len(sorted_t):
        j = i+1
        while j < len(sorted_t):
            ta,tb = sorted_t[i],sorted_t[j]
            if table[ta]["pts"]==table[tb]["pts"] and table[ta]["gd"]==table[tb]["gd"] and table[ta]["gf"]==table[tb]["gf"]:
                j+=1
            else: break
        tied = sorted_t[i:j]
        if len(tied)>1:
            def h2h_key(n):
                h2h_pts = sum(table[n]["h2h"].get(o,{}).get("pts",0) for o in tied if o!=n)
                h2h_gd  = sum(table[n]["h2h"].get(o,{}).get("gd",0)  for o in tied if o!=n)
                h2h_gf  = sum(table[n]["h2h"].get(o,{}).get("gf",0)  for o in tied if o!=n)
                return (-h2h_pts,-h2h_gd,-h2h_gf)
            tied = sorted(tied, key=h2h_key)
            np.random.shuffle(tied)  # lots for still-tied
        result.extend(tied)
        i = j
    return result

def simulate_group(group_name, team_list, model):
    names = [t["name"] for t in team_list]
    tmap  = {t["name"]:t for t in team_list}
    table = initialise_table(names)
    schedule = [[(0,1),(2,3)],[(0,2),(1,3)],[(0,3),(1,2)]]
    results = []
    for matchday_idx, matchday in enumerate(schedule, 1):
        for (i,j) in matchday:
            ta, tb = tmap[names[i]], tmap[names[j]]
            result = simulate_match(ta, tb, model, knockout=False)
            apply_result(table, result)
            results.append(result)
    standings = sort_group(table, names)
    return standings, table, results

def simulate_all_groups(groups, team_lookup, model):
    group_results = {}
    for gname, team_names in groups.items():
        team_list = [team_lookup[n] for n in team_names]
        standings, table, results = simulate_group(gname, team_list, model)
        group_results[gname] = {"standings": standings, "table": table, "results": results}
    return group_results

def extract_qualifiers(group_results):
    group_winners = {}
    runners_up    = {}
    third_placed_candidates = []
    for gname, data in group_results.items():
        s = data["standings"]
        t = data["table"]
        group_winners[gname] = s[0]
        runners_up[gname]    = s[1]
        t3 = s[2]
        third_placed_candidates.append({
            "team": t3, "group": gname,
            "pts": t[t3]["pts"], "gd": t[t3]["gd"], "gf": t[t3]["gf"]
        })
    third_placed_candidates.sort(key=lambda x: (-x["pts"],-x["gd"],-x["gf"],np.random.random()))
    advancing_third  = [t["team"] for t in third_placed_candidates[:8]]
    eliminated_third = [t["team"] for t in third_placed_candidates[8:]]
    eliminated_fourth = [data["standings"][3] for data in group_results.values()]
    return {
        "group_winners": group_winners,
        "runners_up": runners_up,
        "advancing_third": advancing_third,
        "third_placed_details": third_placed_candidates,
        "eliminated": eliminated_third + eliminated_fourth,
    }
