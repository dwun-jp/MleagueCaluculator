from ranking import get_ranking, get_places
from score import apply_ron, apply_dealer_tsumo, apply_non_dealer_tsumo


def search_non_dealer_tsumo(
    scores,
    before_places,
    top_players,
    score_table,
    counters,
    deposit,
    dealer="東",
):
    results = []

    for winner in scores:
        if winner == dealer or winner in top_players:
            continue

        for _, row in score_table.iterrows():
            new_scores = apply_non_dealer_tsumo(
                scores,
                winner=winner,
                dealer=dealer,
                non_dealer_pay=row["non_dealer_pay"],
                dealer_pay=row["dealer_pay"],
                counters=counters,
                deposit=deposit,
            )

            after_places = get_places(get_ranking(new_scores))

            result = {
                "winner": winner,
                "method": "tsumo",
                "discarder": None,
                "label": row["label"],
                "before_places": before_places,
                "after_places": after_places,
            }

            results.append(result)

    return results


def search_non_dealer_ron(
    scores,
    before_places,
    top_players,
    score_table,
    counters,
    deposit,
    dealer="東",
):
    results = []

    for winner in scores:
        if winner == dealer or winner in top_players:
            continue

        for discarder in top_players:
            for _, row in score_table.iterrows():
                new_scores = apply_ron(
                    scores,
                    winner=winner,
                    discarder=discarder,
                    point=row["point"],
                    counters=counters,
                    deposit=deposit,
                )

                after_places = get_places(get_ranking(new_scores))

                result = {
                    "winner": winner,
                    "method": "ron",
                    "discarder": discarder,
                    "label": row["label"],
                    "before_places": before_places,
                    "after_places": after_places,
                }

                results.append(result)

    return results


def search_dealer_tsumo(
    scores,
    before_places,
    top_players,
    score_table,
    counters,
    deposit,
    dealer="東",
):
    results = []

    for _, row in score_table.iterrows():

        new_scores = apply_dealer_tsumo(
            scores,
            winner=dealer,
            pay=row["pay"],
            counters=counters,
            deposit=deposit,
        )

        after_places = get_places(get_ranking(new_scores))

        result = {
            "winner": dealer,
            "method": "tsumo",
            "discarder": None,
            "label": row["label"],
            "before_places": before_places,
            "after_places": after_places,
        }

        results.append(result)

    return results


def search_dealer_ron(
    scores,
    before_places,
    top_players,
    score_table,
    counters,
    deposit,
    dealer="東",
):
    results = []

    for discarder in top_players:
        for _, row in score_table.iterrows():

            new_scores = apply_ron(
                scores,
                winner=dealer,
                discarder=discarder,
                point=row["point"],
                counters=counters,
                deposit=deposit,
            )

            after_places = get_places(get_ranking(new_scores))

            result = {
                "winner": dealer,
                "method": "ron",
                "discarder": discarder,
                "label": row["label"],
                "before_places": before_places,
                "after_places": after_places,
            }

            results.append(result)

    return results


def search_conditions(
    scores,
    score_tables,
    counters=0,
    deposit=0,
    dealer="東",
):
    before_ranking = get_ranking(scores)
    before_places = get_places(before_ranking)

    non_dealer_tsumo = score_tables["non_dealer_tsumo"]
    non_dealer_ron = score_tables["non_dealer_ron"]
    dealer_tsumo = score_tables["dealer_tsumo"]
    dealer_ron = score_tables["dealer_ron"]

    top_score = max(scores.values())
    score_diff = {player: top_score - score for player, score in scores.items()}

    top_players = [player for place, player, score in before_places if place == 1]

    results = []

    results.extend(
        search_non_dealer_tsumo(
            scores,
            before_places,
            top_players,
            non_dealer_tsumo,
            counters,
            deposit,
            dealer=dealer,
        )
    )

    results.extend(
        search_non_dealer_ron(
            scores,
            before_places,
            top_players,
            non_dealer_ron,
            counters,
            deposit,
            dealer=dealer,
        )
    )

    if dealer not in top_players:
        results.extend(
            search_dealer_tsumo(
                scores,
                before_places,
                top_players,
                dealer_tsumo,
                counters,
                deposit,
                dealer=dealer,
            )
        )

        results.extend(
            search_dealer_ron(
                scores,
                before_places,
                top_players,
                dealer_ron,
                counters,
                deposit,
                dealer=dealer,
            )
        )

    return results
