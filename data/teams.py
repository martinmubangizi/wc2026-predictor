GROUPS = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Bosnia & Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["USA", "Paraguay", "Australia", "Türkiye"],
    "E": ["Germany", "Curaçao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"],
}

HOST_NATIONS = {"USA", "Canada", "Mexico"}

# Fields:
#   depth_rating  : Quality beyond starting XI (0–10)
#
# KEY PLAYERS (used in narrative + LinkedIn post):

TEAMS = {

    # TIER 1 — TOURNAMENT FAVOURITES

    "France": dict(
        elo=2045, att_xg=1.88, def_xg=0.88, squad_val=195, form=0.65,
        t_exp=5, pen_skill=0.74, peak_pct=0.62, star_rating=9.4, depth_rating=9.5,
        key_players=[
            ("Kylian Mbappé",      "Real Madrid",       9.6),  # #1 ranked player WC 2026
            ("Ousmane Dembélé",    "PSG",               8.8),  # #3 ranked
            ("Michael Olise",      "Bayern Munich",     8.5),  # #9 ranked
            ("Désiré Doué",        "PSG",               8.2),  # #10 ranked
            ("William Saliba",     "Arsenal",           8.7),  # #21 ranked, elite CB
        ],
        notes="Won 2018, finalist 2022. Mbappé in peak form at Real Madrid. "
              "Deepest squad at the tournament (Deschamps's final WC as coach)."
    ),

    "Spain": dict(
        elo=2035, att_xg=1.82, def_xg=0.78, squad_val=210, form=0.70,
        t_exp=5, pen_skill=0.71, peak_pct=0.65, star_rating=9.3, depth_rating=9.2,
        key_players=[
            ("Lamine Yamal",       "Barcelona",         9.4),  # #2 ranked, 18 yrs old
            ("Pedri",              "Barcelona",         8.9),  # #12 ranked
            ("Rodri",              "Man City",          9.1),  # #11 ranked, Ballon d'Or
            ("Raphinha",           "Barcelona",         8.6),  # Barcelona top scorer
            ("Unai Simón",         "Athletic Bilbao",   8.0),
        ],
        notes="Won Euro 2024. Lamine Yamal at 18 is generational. Rodri dictates tempo. "
              "Best defensive record in qualifying. Home continent advantage (North America = mixed)."
    ),

    "Brazil": dict(
        elo=2030, att_xg=1.90, def_xg=0.92, squad_val=215, form=0.58,
        t_exp=5, pen_skill=0.70, peak_pct=0.58, star_rating=9.0, depth_rating=9.0,
        key_players=[
            ("Raphinha",           "Barcelona",         8.8),  # #7 ranked
            ("Vinicius Jr",        "Real Madrid",       8.9),  # #19 ranked
            ("Neymar",             "Al-Hilal",          7.2),  # returning from injury — risk
            ("Rodrygo",            "Real Madrid",       8.3),
            ("Alisson",            "Liverpool",         8.5),
        ],
        notes="Most WC wins (5). Vinicius + Raphinha = terrifying wing duo. "
              "Neymar's fitness is the big question mark. Lost 2-1 to France in March 2026."
    ),

    "Argentina": dict(
        elo=2060, att_xg=1.82, def_xg=0.85, squad_val=188, form=0.72,
        t_exp=5, pen_skill=0.76, peak_pct=0.52, star_rating=9.2, depth_rating=8.5,
        key_players=[
            ("Lionel Messi",       "Inter Miami",       8.5),  # #4 ranked, age 38 — risk
            ("Julian Álvarez",     "Atlético Madrid",   8.9),  # #20 ranked, in peak form
            ("Lautaro Martínez",   "Inter Milan",       8.7),  # #25 ranked
            ("Federico Valverde",  "Real Madrid",       9.0),  # elite, box-to-box
            ("Emiliano Martínez",  "Aston Villa",       8.8),  # best GK at tournament?
        ],
        notes="Reigning champions (2022). Highest Elo at tournament. "
              "Messi's final WC at 38 — inspirational but fitness concern. "
              "Álvarez + Valverde in career-best form. Best GK in Emiliano Martínez."
    ),

    "England": dict(
        elo=2005, att_xg=1.80, def_xg=0.92, squad_val=220, form=0.60,
        t_exp=5, pen_skill=0.72, peak_pct=0.62, star_rating=9.0, depth_rating=9.5,
        key_players=[
            ("Harry Kane",         "Bayern Munich",     9.1),  # #5 ranked
            ("Jude Bellingham",    "Real Madrid",       9.2),  # not in top 25 but elite
            ("Bukayo Saka",        "Arsenal",           8.9),
            ("Declan Rice",        "Arsenal",           8.6),  # #23 ranked
            ("Phil Foden",         "Man City",          8.4),  # left out per ESPN
        ],
        notes="Highest squad value at tournament (£220M index). "
              "Kane in Bundesliga golden boot form. Bellingham world-class. "
              "60 years of hurt — Tuchel's structured setup may finally deliver."
    ),

    "Germany": dict(
        elo=1985, att_xg=1.72, def_xg=0.98, squad_val=188, form=0.52,
        t_exp=5, pen_skill=0.75, peak_pct=0.58, star_rating=8.5, depth_rating=8.8,
        key_players=[
            ("Jamal Musiala",      "Bayern Munich",     9.0),  # #24 ranked
            ("Florian Wirtz",      "Bayer Leverkusen",  8.7),
            ("Thomas Müller",      "Bayern Munich",     7.8),  # veteran final WC
            ("Manuel Neuer",       "Bayern Munich",     7.9),
            ("Antonio Rüdiger",    "Real Madrid",       8.5),
        ],
        notes="Hosts Euro 2024 (semifinalist). Musiala + Wirtz are the future. "
              "Highest penalty skill (0.75) historically. Easy group (E) with Curaçao."
    ),

    # TIER 2 — SERIOUS CONTENDERS

    "Portugal": dict(
        elo=1978, att_xg=1.70, def_xg=0.98, squad_val=175, form=0.62,
        t_exp=5, pen_skill=0.69, peak_pct=0.50, star_rating=8.8, depth_rating=8.2,
        key_players=[
            ("Bruno Fernandes",    "Man United",        8.5),  # #6 ranked
            ("Cristiano Ronaldo",  "Al-Nassr",          7.5),  # #16 ranked, age 41!
            ("João Neves",         "PSG",               8.6),  # #17 ranked
            ("Vitinha",            "PSG",               8.4),  # #14 ranked
            ("Rúben Dias",         "Man City",          8.7),
        ],
        notes="Colombia in group is tricky. Ronaldo at 41 — iconic but Neves/Vitinha carry play. "
              "Bruno Fernandes leads squad. Deep knockout experience."
    ),

    "Netherlands": dict(
        elo=1962, att_xg=1.66, def_xg=1.00, squad_val=172, form=0.56,
        t_exp=4, pen_skill=0.67, peak_pct=0.63, star_rating=8.4, depth_rating=8.0,
        key_players=[
            ("Cody Gakpo",         "Liverpool",         8.6),
            ("Memphis Depay",      "Atlético Madrid",   8.0),
            ("Virgil van Dijk",    "Liverpool",         8.8),
            ("Xavi Simons",        "PSG / Leipzig",     8.4),
            ("Tijjani Reijnders",  "AC Milan",          8.2),
        ],
        notes="Sweden + Japan + Tunisia in group — winnable. Van Dijk leads elite defence. "
              "Gakpo in fine form at Liverpool."
    ),

    "Belgium": dict(
        elo=1945, att_xg=1.62, def_xg=1.02, squad_val=168, form=0.50,
        t_exp=4, pen_skill=0.68, peak_pct=0.48, star_rating=8.5, depth_rating=7.8,
        key_players=[
            ("Kevin De Bruyne",    "Man City",          8.8),  # #18 ranked
            ("Thibaut Courtois",   "Real Madrid",       9.0),  # #22 ranked
            ("Romelu Lukaku",      "Napoli",            7.8),
            ("Youri Tielemans",    "Aston Villa",       8.0),
            ("Axel Witsel",        "Atlético Madrid",   7.5),
        ],
        notes="Egypt + Iran + New Zealand = easiest group in tournament. "
              "De Bruyne + Courtois world-class. 'Golden Generation' last dance?"
    ),

    "Italy": dict(
        elo=1952, att_xg=1.58, def_xg=0.93, squad_val=162, form=0.54,
        t_exp=3, pen_skill=0.73, peak_pct=0.52, star_rating=8.2, depth_rating=7.8,
        key_players=[
            ("Federico Chiesa",    "Liverpool",         8.5),
            ("Sandro Tonali",      "Newcastle",         8.3),
            ("Nicolo Barella",     "Inter Milan",       8.6),
            ("Gianluigi Donnarumma","PSG",              8.7),
            ("Giacomo Raspadori",  "Napoli",            8.0),
        ],
        notes="Not in this tournament — Italy FAILED to qualify for 2026. "
              "One of the biggest absences of the tournament."
    ),

    "Norway": dict(
        elo=1920, att_xg=1.58, def_xg=1.05, squad_val=148, form=0.58,
        t_exp=1, pen_skill=0.65, peak_pct=0.60, star_rating=8.8, depth_rating=7.2,
        key_players=[
            ("Erling Haaland",     "Man City",          9.5),  # #8 ranked, top scorer
            ("Martin Ødegaard",    "Arsenal",           8.7),
            ("Alexander Sørloth",  "Atlético Madrid",   8.0),
            ("Sander Berge",       "Fulham",            7.8),
            ("Ørjan Nyland",       "Southampton",       7.5),
        ],
        notes="First WC in 24 years! Haaland is the most dangerous striker in the tournament. "
              "Group I with France and Senegal — tough but passable for 3rd place."
    ),

    "Morocco": dict(
        elo=1895, att_xg=1.38, def_xg=0.85, squad_val=112, form=0.62,
        t_exp=3, pen_skill=0.62, peak_pct=0.60, star_rating=8.2, depth_rating=7.5,
        key_players=[
            ("Achraf Hakimi",      "PSG",               8.9),  # #13 ranked
            ("Hakim Ziyech",       "Galatasaray",       8.0),
            ("Youssef En-Nesyri",  "Fenerbahçe",        8.2),
            ("Sofyan Amrabat",     "Man United",        8.3),
            ("Bono (Yassine Bounou)","Al-Hilal",        8.1),
        ],
        notes="2022 semifinalists — no fluke. Hakimi is elite. Group C with Brazil + Scotland = tough, "
              "but Morocco have the defensive resilience to upset."
    ),

    "Uruguay": dict(
        elo=1912, att_xg=1.44, def_xg=0.98, squad_val=120, form=0.56,
        t_exp=4, pen_skill=0.66, peak_pct=0.50, star_rating=8.2, depth_rating=7.2,
        key_players=[
            ("Federico Valverde",  "Real Madrid",       9.0),  # #15 ranked
            ("Darwin Núñez",       "Liverpool",         8.4),
            ("Rodrigo Bentancur",  "Tottenham",         8.1),
            ("Ronald Araújo",      "Barcelona",         8.5),
            ("José María Giménez","Atlético Madrid",   8.2),
        ],
        notes="Group H — Saudi Arabia and Cape Verde are beatable. "
              "Spain is the danger. Valverde world-class. Compact and dangerous on counter."
    ),

    "Colombia": dict(
        elo=1902, att_xg=1.46, def_xg=1.05, squad_val=128, form=0.60,
        t_exp=3, pen_skill=0.63, peak_pct=0.56, star_rating=8.0, depth_rating=7.5,
        key_players=[
            ("Luis Díaz",          "Liverpool",         8.8),
            ("James Rodríguez",    "Rayo Vallecano",    7.5),
            ("Richard Ríos",       "Palmeiras",         8.1),
            ("Jhon Durán",         "Aston Villa",       8.3),
            ("David Ospina",       "Al-Qadsiah",        7.8),
        ],
        notes="Group K with Portugal is hard, but Colombia recent Copa América form is excellent. "
              "Luis Díaz in elite form at Liverpool. Potential dark horse."
    ),

    "Japan": dict(
        elo=1855, att_xg=1.40, def_xg=1.03, squad_val=108, form=0.60,
        t_exp=5, pen_skill=0.65, peak_pct=0.58, star_rating=7.8, depth_rating=7.5,
        key_players=[
            ("Takefusa Kubo",      "Real Sociedad",     8.4),
            ("Wataru Endo",        "Liverpool",         8.2),
            ("Kaoru Mitoma",       "Brighton",          8.5),
            ("Shuichi Gonda",      "PSV",               7.8),
            ("Ritsu Doan",         "Freiburg",          8.0),
        ],
        notes="Knocked out Germany + Spain in 2022. Netherlands + Sweden in Group F — tough. "
              "Mitoma + Kubo are dangerous. Tactically disciplined."
    ),

    "Switzerland": dict(
        elo=1882, att_xg=1.36, def_xg=0.93, squad_val=118, form=0.58,
        t_exp=4, pen_skill=0.60, peak_pct=0.55, star_rating=7.8, depth_rating=7.5,
        key_players=[
            ("Granit Xhaka",       "Bayer Leverkusen",  8.5),
            ("Xherdan Shaqiri",    "Chicago Fire",      7.5),
            ("Ricardo Rodríguez",  "Torino",            7.8),
            ("Yann Sommer",        "Inter Milan",       8.2),
            ("Ruben Vargas",       "Augsburg",          7.9),
        ],
        notes="Consistently reach R16. Group B — Canada is the real test. "
              "Xhaka leads from midfield. Underrated tactically."
    ),

    "South Korea": dict(
        elo=1825, att_xg=1.30, def_xg=1.15, squad_val=98, form=0.50,
        t_exp=5, pen_skill=0.60, peak_pct=0.54, star_rating=7.5, depth_rating=7.0,
        key_players=[
            ("Son Heung-min",      "Tottenham",         8.8),
            ("Lee Kang-in",        "PSG",               8.2),
            ("Hwang Hee-chan",      "Wolves",            7.8),
            ("Kim Min-jae",        "Bayern Munich",     8.4),
            ("Cho Gue-sung",       "Midtjylland",       7.5),
        ],
        notes="Son at 34 still the main man. Lee Kang-in excellent at PSG. "
              "Group A — Mexico has home advantage. 4th place 2002 feels distant."
    ),

    "Croatia": dict(
        elo=1922, att_xg=1.52, def_xg=1.08, squad_val=132, form=0.56,
        t_exp=4, pen_skill=0.72, peak_pct=0.45, star_rating=7.8, depth_rating=7.2,
        key_players=[
            ("Luka Modrić",        "Al-Qadsiah",        7.8),  # age 40, final WC
            ("Ivan Perišić",       "Hajduk Split",      7.5),
            ("Mateo Kovačić",      "Man City",          8.3),
            ("Joško Gvardiol",     "Man City",          8.6),
            ("Andrej Kramarić",    "Hoffenheim",        7.9),
        ],
        notes="Runners-up 2018, 3rd 2022. Modric's final WC. Gvardiol world-class. "
              "Group L — England favourite but Croatia always dangerous."
    ),

    # TIER 3 — COMPETITIVE

    "USA": dict(
        elo=1875, att_xg=1.42, def_xg=1.12, squad_val=125, form=0.54,
        t_exp=4, pen_skill=0.65, peak_pct=0.64, star_rating=7.5, depth_rating=7.5,
        key_players=[
            ("Christian Pulisic",  "AC Milan",          8.5),
            ("Gio Reyna",          "Dortmund",          8.0),
            ("Tyler Adams",        "Bournemouth",       8.1),
            ("Ricardo Pepi",       "Groningen",         7.8),
            ("Matt Turner",        "Crystal Palace",    7.5),
        ],
        notes="Co-hosts. Pulisic in outstanding Milan form. Group D — Paraguay + Australia + Türkiye "
              "is winnable. Home crowd factor is massive."
    ),

    "Mexico": dict(
        elo=1882, att_xg=1.40, def_xg=1.10, squad_val=118, form=0.52,
        t_exp=5, pen_skill=0.64, peak_pct=0.54, star_rating=7.2, depth_rating=7.0,
        key_players=[
            ("Raúl Jiménez",       "Fulham",            7.8),
            ("Edson Álvarez",      "Fenerbahçe",        8.2),
            ("Hirving Lozano",     "PSV",               7.5),
            ("Guillermo Ochoa",    "AEL Limassol",      7.5),
            ("Alexis Vega",        "Chivas",            7.2),
        ],
        notes="Opens tournament vs South Africa at Azteca. Home crowd = massive advantage. "
              "Historically exit R16 ('El Quinto Partido' curse). Can they break it?"
    ),

    "Canada": dict(
        elo=1783, att_xg=1.22, def_xg=1.20, squad_val=90, form=0.54,
        t_exp=1, pen_skill=0.58, peak_pct=0.64, star_rating=7.5, depth_rating=6.8,
        key_players=[
            ("Alphonso Davies",    "Bayern Munich",     8.8),
            ("Jonathan David",     "Lille",             8.5),
            ("Cyle Larin",         "Valladolid",        7.8),
            ("Tajon Buchanan",     "Club Brugge",       7.6),
            ("Stephen Eustaquio",  "Porto",             7.8),
        ],
        notes="Co-hosts. Only second WC ever. Davies + David = lethal. "
              "Group B — Bosnia and Switzerland are the tests."
    ),

    "Ecuador": dict(
        elo=1812, att_xg=1.26, def_xg=1.18, squad_val=88, form=0.52,
        t_exp=3, pen_skill=0.57, peak_pct=0.57, star_rating=7.2, depth_rating=6.5,
        key_players=[
            ("Moisés Caicedo",     "Chelsea",           8.7),
            ("Ángel Mena",         "León",              7.5),
            ("Pervis Estupiñán",   "Brighton",          7.8),
            ("Piero Hincapié",     "Bayer Leverkusen",  8.0),
            ("Enner Valencia",     "Independiente",     7.2),
        ],
        notes="Group E — Germany favourite but Ivory Coast is the real fight for 2nd. "
              "Caicedo is Premier League elite. Ecuador surprise packages."
    ),

    "Senegal": dict(
        elo=1842, att_xg=1.34, def_xg=1.10, squad_val=104, form=0.54,
        t_exp=3, pen_skill=0.58, peak_pct=0.58, star_rating=7.8, depth_rating=7.0,
        key_players=[
            ("Sadio Mané",         "Al-Nassr",          7.8),
            ("Nicolas Jackson",    "Bayern Munich",     8.3),  # confirmed in squad
            ("Pape Matar Sarr",    "Tottenham",         8.0),
            ("Kalidou Koulibaly",  "Al-Hilal",          7.8),
            ("Iliman Ndiaye",      "Everton",           7.8),
        ],
        notes="Group I — France is tough but Norway (Haaland) and Iraq also. "
              "Jackson in incredible form at Bayern. Africa's strongest squad."
    ),

    "Austria": dict(
        elo=1803, att_xg=1.26, def_xg=1.15, squad_val=92, form=0.52,
        t_exp=2, pen_skill=0.61, peak_pct=0.58, star_rating=7.4, depth_rating=6.8,
        key_players=[
            ("David Alaba",        "Real Madrid",       8.2),
            ("Marcel Sabitzer",    "Dortmund",          8.0),
            ("Michael Gregoritsch","Freiburg",          7.6),
            ("Marko Arnautovic",   "Man United",        7.3),
            ("Konrad Laimer",      "Bayern Munich",     8.1),
        ],
        notes="Group J — Argentina heavy favourite but Algeria/Jordan beatable. "
              "Alaba still quality. Sabitzer in solid form."
    ),

    # TIER 4 — OUTSIDERS / QUALIFIERS

    "South Africa": dict(elo=1702, att_xg=1.00, def_xg=1.35, squad_val=55, form=0.38, t_exp=2, pen_skill=0.52, peak_pct=0.52, star_rating=6.2, depth_rating=5.5, key_players=[("Lyle Foster","Burnley",7.5),("Percy Tau","Al-Ahly",7.0),("Themba Zwane","Mamelodi Sundowns",6.8),("Ronwen Williams","Mamelodi Sundowns",7.0),("Teboho Mokoena","Mamelodi Sundowns",7.2)], notes="Opens vs Mexico in Mexico City — tough start. Best chance is exploiting 3rd-place route."),
    "Czechia":       dict(elo=1745, att_xg=1.08, def_xg=1.22, squad_val=72, form=0.42, t_exp=3, pen_skill=0.60, peak_pct=0.52, star_rating=6.8, depth_rating=6.2, key_players=[("Patrik Schick","Bayer Leverkusen",8.0),("Tomáš Souček","West Ham",7.8),("Vladimír Coufal","West Ham",7.3),("Adam Hložek","Bayer Leverkusen",7.5),("Jakub Jankto","Sparta Prague",7.0)], notes="Schick is a World Cup-level striker. Group A — dangerous outsiders."),
    "Bosnia & Herzegovina": dict(elo=1738, att_xg=1.10, def_xg=1.28, squad_val=70, form=0.40, t_exp=1, pen_skill=0.55, peak_pct=0.50, star_rating=6.5, depth_rating=5.8, key_players=[("Edin Džeko","Fenerbahçe",7.2),("Miralem Pjanić","Sharjah",7.0),("Sead Kolašinac","Atalanta",7.2),("Niko Kovač","-",0),("Amer Gojak","Trabzonspor",6.8)], notes="Group B — Canada and Switzerland are tough. Džeko veteran experience."),
    "Qatar":         dict(elo=1698, att_xg=0.95, def_xg=1.40, squad_val=50, form=0.35, t_exp=2, pen_skill=0.50, peak_pct=0.50, star_rating=5.8, depth_rating=5.2, key_players=[("Akram Afif","Al-Sadd",7.5),("Almoez Ali","Al-Duhail",7.2),("Abdelkarim Hassan","Al-Sadd",6.8),("Meshaal Barsham","Al-Sadd",6.5),("Assim Madibo","FC Dallas",6.5)], notes="Group B — Switzerland likely dominant. Qatar semi-professional league quality."),
    "Haiti":         dict(elo=1680, att_xg=0.88, def_xg=1.42, squad_val=45, form=0.32, t_exp=1, pen_skill=0.50, peak_pct=0.52, star_rating=5.5, depth_rating=5.0, key_players=[("Duckens Nazon","Karagümrük",6.5),("Frantzdy Pierrot","Atlanta United",6.2),("Mechack Jérome","Red Bulls",6.0),("Steeven Saba","Troyes",5.8),("James Peneau","Lens",6.0)], notes="Group C — Brazil + Scotland + Morocco. Exit expected in groups."),
    "Scotland":      dict(elo=1742, att_xg=1.08, def_xg=1.20, squad_val=75, form=0.44, t_exp=1, pen_skill=0.58, peak_pct=0.54, star_rating=6.8, depth_rating=6.5, key_players=[("Andy Robertson","Liverpool",8.3),("Scott McTominay","Napoli",8.0),("Che Adams","Southampton",7.4),("Lawrence Shankland","Hearts",7.2),("Angus Gunn","Norwich",7.0)], notes="Group C — Brazil is their nemesis but Robertson + McTominay competitive."),
    "Paraguay":      dict(elo=1722, att_xg=1.06, def_xg=1.28, squad_val=62, form=0.38, t_exp=3, pen_skill=0.54, peak_pct=0.50, star_rating=6.5, depth_rating=6.0, key_players=[("Miguel Almirón","Atlético Mineiro",7.8),("Gustavo Gómez","Palmeiras",7.5),("Julio Enciso","Brighton",7.5),("Antonio Sanabria","Torino",7.2),("Antony Silva","Cádiz",6.8)], notes="Group D — USA hosts. Almirón veteran quality."),
    "Australia":     dict(elo=1758, att_xg=1.15, def_xg=1.22, squad_val=74, form=0.48, t_exp=4, pen_skill=0.56, peak_pct=0.55, star_rating=6.8, depth_rating=6.5, key_players=[("Mathew Ryan","AZ Alkmaar",7.5),("Aziz Behich","FC Zurich",6.8),("Martin Boyle","Panathinaikos",7.0),("Ajdin Hrustic","Hellas Verona",7.2),("Jackson Irvine","St Pauli",7.5)], notes="2022 R16. Group D — USA and Türkiye are the main challenges."),
    "Türkiye":       dict(elo=1862, att_xg=1.40, def_xg=1.08, squad_val=122, form=0.56, t_exp=3, pen_skill=0.61, peak_pct=0.58, star_rating=7.6, depth_rating=7.0, key_players=[("Hakan Çalhanoğlu","Inter Milan",8.6),("Arda Güler","Real Madrid",8.4),("Kerem Aktürkoğlu","Barcelona",8.0),("Merih Demiral","Al-Qadsiah",7.8),("Mert Günok","Fenerbahçe",7.5)], notes="Qualified via playoff (beat Kosovo). Arda Güler at Real Madrid is special. Dark horse potential."),
    "Curaçao":       dict(elo=1638, att_xg=0.82, def_xg=1.55, squad_val=35, form=0.28, t_exp=1, pen_skill=0.48, peak_pct=0.50, star_rating=5.2, depth_rating=4.5, key_players=[("Leandro Bacuna","Cardiff",6.5),("Cuco Martina","Stoke",6.0),("Gevaro Nepomuceno","Omonoia",6.0),("Darryl Lachman","Elfsborg",5.8),("Elson Hooi","NA",5.5)], notes="Group E — Germany, Ivory Coast, Ecuador. Group stage exit expected."),
    "Ivory Coast":   dict(elo=1778, att_xg=1.20, def_xg=1.22, squad_val=84, form=0.48, t_exp=3, pen_skill=0.56, peak_pct=0.54, star_rating=7.3, depth_rating=6.8, key_players=[("Sébastien Haller","Borussia Dortmund",7.8),("Franck Kessié","Al-Ahli",7.5),("Simon Adingra","Brighton",7.8),("Serge Aurier","Villarreal",7.0),("Yann M'Vila","-",6.5)], notes="AFCON 2023 champions. Group E — Germany is the danger. Haller + Adingra dangerous."),
    "Sweden":        dict(elo=1815, att_xg=1.28, def_xg=1.15, squad_val=88, form=0.50, t_exp=3, pen_skill=0.62, peak_pct=0.54, star_rating=7.0, depth_rating=6.8, key_players=[("Victor Nilsson Lindelöf","Man United",7.8),("Alexander Isak","Newcastle",8.5),("Dejan Kulusevski","Tottenham",8.2),("Emil Forsberg","RB Leipzig",7.5),("Robin Olsen","Aston Villa",7.5)], notes="Group F — Netherlands is the big test. Isak in Premier League elite form."),
    "Tunisia":       dict(elo=1772, att_xg=1.16, def_xg=1.18, squad_val=77, form=0.46, t_exp=4, pen_skill=0.55, peak_pct=0.53, star_rating=6.8, depth_rating=6.2, key_players=[("Hannibal Mejbri","Sunderland",7.8),("Naim Sliti","Nottingham F",7.2),("Aïssa Laïdouni","Watford",7.0),("Mohamed Drager","Porto",7.0),("Aymen Dahmen","Montpellier",7.0)], notes="Hannibal Mejbri at Sunderland is the standout. Group F — competitive."),
    "Egypt":         dict(elo=1742, att_xg=1.12, def_xg=1.22, squad_val=67, form=0.46, t_exp=2, pen_skill=0.56, peak_pct=0.54, star_rating=7.2, depth_rating=6.5, key_players=[("Mohamed Salah","Liverpool",8.8),("Mostafa Mohamed","Nantes",7.5),("Trezeguet","Trabzonspor",7.0),("Ahmed Hegazi","Al-Ittihad",7.2),("Mohamed El-Shenawy","Al-Ahly",7.0)], notes="SALAH. Group G — Belgium is tough but if Salah is fit, Egypt can advance."),
    "Iran":          dict(elo=1733, att_xg=1.10, def_xg=1.25, squad_val=64, form=0.44, t_exp=4, pen_skill=0.55, peak_pct=0.52, star_rating=6.8, depth_rating=6.2, key_players=[("Mehdi Taremi","Inter Milan",8.3),("Sardar Azmoun","Roma",7.8),("Alireza Jahanbakhsh","Nottingham F",7.5),("Milad Mohammadi","Augsburg",7.0),("Alireza Beiranvand","Club Brugge",7.2)], notes="Taremi excellent at Inter. Group G — Belgium dominant but New Zealand/Egypt beatable."),
    "New Zealand":   dict(elo=1662, att_xg=0.92, def_xg=1.42, squad_val=48, form=0.32, t_exp=2, pen_skill=0.50, peak_pct=0.54, star_rating=5.8, depth_rating=5.2, key_players=[("Chris Wood","Nottingham F",7.8),("Winston Reid","Brentford",6.8),("Clayton Lewis","Western United",6.5),("Stefan Marinovic","Columbus Crew",6.2),("Marco Rojas","Almeria",6.5)], notes="Group G — Chris Wood veteran quality. Unlikely to advance."),
    "Cape Verde":    dict(elo=1708, att_xg=1.00, def_xg=1.32, squad_val=58, form=0.40, t_exp=1, pen_skill=0.52, peak_pct=0.56, star_rating=6.5, depth_rating=5.8, key_players=[("Garry Rodrigues","Olympiakos",7.2),("Nanu","Porto",7.0),("Ryan Mendes","Lorient",6.8),("José Fonte","Vitória Guimarães",7.0),("Steven Fortes","Cruz Azul",6.5)], notes="WC debut. Group H — Spain, Uruguay, Saudi Arabia. Impressive to qualify."),
    "Saudi Arabia":  dict(elo=1703, att_xg=1.00, def_xg=1.32, squad_val=57, form=0.38, t_exp=4, pen_skill=0.52, peak_pct=0.52, star_rating=6.5, depth_rating=6.0, key_players=[("Salem Al-Dawsari","Al-Hilal",7.5),("Mohamed Kanno","Al-Hilal",7.0),("Saleh Al-Shehri","Al-Hilal",7.0),("Mohammed Al-Owais","Al-Hilal",7.2),("Yasser Al-Shahrani","Al-Hilal",7.0)], notes="Upset Argentina in 2022! Group H — Spain is too strong but 2nd place is possible."),
    "Algeria":       dict(elo=1768, att_xg=1.18, def_xg=1.20, squad_val=80, form=0.48, t_exp=2, pen_skill=0.56, peak_pct=0.55, star_rating=7.0, depth_rating=6.5, key_players=[("Riyad Mahrez","Al-Ahli",7.8),("Islam Slimani","Besiktas",7.2),("Samir Nasri","-",0),("Andy Delort","Nice",7.0),("Youcef Atal","Nice",7.3)], notes="Group J — Argentina dominant. Mahrez veteran class. Algeria best hope for AFCON region."),
    "Jordan":        dict(elo=1658, att_xg=0.88, def_xg=1.42, squad_val=45, form=0.35, t_exp=1, pen_skill=0.50, peak_pct=0.52, star_rating=5.8, depth_rating=5.2, key_players=[("Musa Suleiman","Al-Faisaly",6.2),("Ahmad Hayel","Al-Faisaly",6.0),("Baha'a Faisal","Al-Faisaly",5.8),("Amer Shafi","Al-Arabi",6.5),("Mutaz Yaseen","Al-Faisaly",5.8)], notes="First WC ever. Group J — Argentina, Algeria, Austria. Historic participation."),
    "DR Congo":      dict(elo=1712, att_xg=1.02, def_xg=1.30, squad_val=62, form=0.42, t_exp=1, pen_skill=0.54, peak_pct=0.56, star_rating=6.8, depth_rating=6.2, key_players=[("Cedric Bakambu","Olympique Lyon",7.5),("Théo Bongonda","Club Brugge",7.2),("Chancel Mbemba","Porto",7.5),("Arthur Masuaku","Besiktas",7.0),("Joris Kayembe","Reims",6.8)], notes="Group K — Portugal dominant. But DR Congo have quality in Bakambu + Mbemba."),
    "Uzbekistan":    dict(elo=1670, att_xg=0.90, def_xg=1.40, squad_val=48, form=0.36, t_exp=1, pen_skill=0.50, peak_pct=0.54, star_rating=5.8, depth_rating=5.5, key_players=[("Eldor Shomurodov","Cagliari",7.2),("Jasur Yakhshiboyev","FK Andijan",6.0),("Otabek Shukurov","FK Bunyodkor",5.8),("Sanjar Tursunov","FK Pakhtakor",5.5),("Bobir Abdikholikov","FK Lokomotiv",5.5)], notes="First WC. Group K — Portugal + Colombia. Historic achievement."),
    "Ghana":         dict(elo=1722, att_xg=1.06, def_xg=1.28, squad_val=62, form=0.42, t_exp=4, pen_skill=0.54, peak_pct=0.53, star_rating=6.8, depth_rating=6.5, key_players=[("Mohammed Kudus","West Ham",8.3),("Thomas Partey","Arsenal",7.8),("André Ayew","Le Havre",7.2),("Inaki Williams","Athletic Bilbao",7.8),("Jordan Ayew","Crystal Palace",7.2)], notes="Group L — England and Croatia are the tests. Kudus outstanding at West Ham."),
    "Panama":        dict(elo=1692, att_xg=0.98, def_xg=1.36, squad_val=54, form=0.36, t_exp=2, pen_skill=0.52, peak_pct=0.54, star_rating=5.8, depth_rating=5.5, key_players=[("Anibal Godoy","Levante",7.0),("Adalberto Carrasquilla","Club de Foot Montreal",6.8),("Edgar Barcenas","RC Strasbourg",6.8),("César Blackman","Sint-Truiden",6.5),("Orlando Mosquera","CFG",6.5)], notes="Group L — England and Croatia too strong. Group stage exit likely."),
    "Iraq":          dict(elo=1663, att_xg=0.90, def_xg=1.40, squad_val=47, form=0.32, t_exp=1, pen_skill=0.50, peak_pct=0.51, star_rating=5.8, depth_rating=5.0, key_players=[("Aymen Hussein","Al-Zawraa",6.5),("Amjad Attwan","Al-Zawraa",6.2),("Ahmed Yasin","Karbala FC",6.0),("Mohanad Ali","FC Emmen",6.2),("Bashar Resan","Al-Zawraa",5.8)], notes="Group I — France + Norway + Senegal. Historic WC return."),
    "Norway":        dict(elo=1920, att_xg=1.58, def_xg=1.05, squad_val=148, form=0.58, t_exp=1, pen_skill=0.65, peak_pct=0.60, star_rating=8.8, depth_rating=7.2, key_players=[("Erling Haaland","Man City",9.5),("Martin Ødegaard","Arsenal",8.7),("Alexander Sørloth","Atlético Madrid",8.0),("Sander Berge","Fulham",7.8),("Ørjan Nyland","Southampton",7.5)], notes="First WC in 24 years. Haaland is tournament's most dangerous striker."),
}

def get_team(name: str) -> dict:
    if name not in TEAMS:
        raise ValueError(f"Team '{name}' not in TEAMS. Available: {sorted(TEAMS.keys())}")
    t = TEAMS[name].copy()
    t["name"] = name
    t["is_host"] = name in HOST_NATIONS
    return t

def get_groups() -> dict:
    return GROUPS

def get_all_team_names() -> list:
    return sorted(TEAMS.keys())
