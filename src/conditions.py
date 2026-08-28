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

top_conditions = []


def get_player_place(places, player_name):
    for place, player, _ in places:
        if player == player_name:
            return place


for result in results:

    winner = result["winner"]
    before_places = result["before_places"]
    after_places = result["after_places"]

    before_place = get_player_place(before_places, winner)
    after_place = get_player_place(after_places, winner)

    if after_place == 1:
        method = result["method"]

        exists = False

        for top_checker in top_conditions:
            top_winner = top_checker["winner"]
            top_method = top_checker["method"]

            if top_winner == winner and top_method == method:
                exists = True
                break

        if exists == False:
            top_conditions.append(result)

for top_result in top_conditions:
    print(top_result)
