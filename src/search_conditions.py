"""
探索処理

入力:
- scores
- score_tables
- counters=0
- deposit=0

探索前:
- before_ranking
- before_places
- top_score
- top_player
- score_diff

探索後:
- after_places

出力:
- results
"""

from ranking import get_ranking, get_places
from score import apply_ron, apply_dealer_tsumo, apply_non_dealer_tsumo


def search_non_dealer_tsumo(
    scores, before_places, top_player, score_table, counters, deposit
):
    results = []
    for winner in ["南", "西", "北"]:
        if winner == top_player:
            continue

        for _, row in score_table.iterrows():
            new_scores = apply_non_dealer_tsumo(
                scores,
                winner=winner,
                dealer="東",
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
    scores, before_places, top_player, score_table, counters, deposit
):
    results = []
    for winner in ["南", "西", "北"]:
        if winner == top_player:
            continue

        for _, row in score_table.iterrows():

            new_scores = apply_ron(
                scores,
                winner=winner,
                discarder=top_player,
                point=row["point"],
                counters=counters,
                deposit=deposit,
            )

            after_places = get_places(get_ranking(new_scores))

            result = {
                "winner": winner,
                "method": "ron",
                "discarder": top_player,
                "label": row["label"],
                "before_places": before_places,
                "after_places": after_places,
            }

            results.append(result)

    return results


def search_dealer_tsumo(
    scores, before_places, top_player, score_table, counters, deposit
):
    results = []
    for _, row in score_table.iterrows():

        new_scores = apply_dealer_tsumo(
            scores, winner="東", pay=row["pay"], counters=counters, deposit=deposit
        )

        after_places = get_places(get_ranking(new_scores))

        result = {
            "winner": "東",
            "method": "tsumo",
            "discarder": None,
            "label": row["label"],
            "before_places": before_places,
            "after_places": after_places,
        }

        results.append(result)

    return results


def search_dealer_ron(
    scores, before_places, top_player, score_table, counters, deposit
):
    results = []
    for _, row in score_table.iterrows():

        new_scores = apply_ron(
            scores,
            winner="東",
            discarder=top_player,
            point=row["point"],
            counters=counters,
            deposit=deposit,
        )

        after_places = get_places(get_ranking(new_scores))

        result = {
            "winner": "東",
            "method": "ron",
            "discarder": top_player,
            "label": row["label"],
            "before_places": before_places,
            "after_places": after_places,
        }

        results.append(result)

    return results


def search_conditions(scores, score_tables, counters=0, deposit=0):
    before_ranking = get_ranking(scores)
    before_places = get_places(before_ranking)

    non_dealer_tsumo = score_tables["non_dealer_tsumo"]
    non_dealer_ron = score_tables["non_dealer_ron"]
    dealer_tsumo = score_tables["dealer_tsumo"]
    dealer_ron = score_tables["dealer_ron"]

    top_score = max(scores.values())
    score_diff = {player: top_score - score for player, score in scores.items()}

    top_player = before_places[0][1]

    results = []

    results.extend(
        search_non_dealer_tsumo(
            scores, before_places, top_player, non_dealer_tsumo, counters, deposit
        )
    )
    results.extend(
        search_non_dealer_ron(
            scores, before_places, top_player, non_dealer_ron, counters, deposit
        )
    )
    results.extend(
        search_dealer_tsumo(
            scores, before_places, top_player, dealer_tsumo, counters, deposit
        )
    )
    results.extend(
        search_dealer_ron(
            scores, before_places, top_player, dealer_ron, counters, deposit
        )
    )

    return results
