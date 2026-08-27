from search_conditions import search_conditions
from csv_loader import load_score_tables

# 仮置き score, score_tables
scores = {
    "東": 20000,
    "南": 30000,
    "西": 20000,
    "北": 15000,
}
score_tables = load_score_tables()

results = search_conditions(scores, score_tables, counters=0, deposit=0)

for result in results:

    winner = result["winner"]
    before_places = result["before_places"]
    after_places = result["after_places"]

    for place, player, score in before_places:
        if player == winner:
            before_place = place

    for place, player, score in after_places:
        if player == winner:
            after_place = place

    if after_places == 1:
        print(
            "条件達成",
            winner,
            result["method"],
            result["label"],
            result["after_places"],
        )
