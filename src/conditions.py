def get_player_place(places, player_name):
    for place, player, _ in places:
        if player == player_name:
            return place


def get_top_conditions(results):
    top_conditions = []

    for result in results:

        winner = result["winner"]
        before_places = result["before_places"]
        after_places = result["after_places"]

        # 和了前の順位を利用する条件計算で使用するかも？
        before_place = get_player_place(before_places, winner)
        after_place = get_player_place(after_places, winner)

        if after_place == 1:
            method = result["method"]

            exists = False

            for top_checker in top_conditions:
                top_winner = top_checker["winner"]
                top_method = top_checker["method"]

                if (
                    top_winner == winner
                    and top_method == method
                    and top_checker["discarder"] == result["discarder"]
                ):
                    exists = True
                    break

            if not exists:
                top_conditions.append(result)

    return top_conditions


if __name__ == "__main__":
    from search_conditions import search_conditions
    from csv_loader import load_score_tables

    score_tables = load_score_tables()

    score = {
        "東": 35100,
        "南": 30000,
        "西": 20100,
        "北": 14800,
    }

    results = search_conditions(
        score,
        score_tables,
        counters=0,
        deposit=0,
    )

    top_conditions = get_top_conditions(results)

    print(top_conditions)
