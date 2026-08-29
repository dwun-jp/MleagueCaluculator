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

            if not exists:
                top_conditions.append(result)

    return top_conditions
