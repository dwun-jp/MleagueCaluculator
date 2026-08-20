"""
探索処理

入力:
- scores
- deposit
- counters
- score_tables

探索前:
- before_ranking
- before_places
- top_score
- score_diff

探索後:
- after_places

出力:
- results
"""

from csv_loader import load_score_tables
from ranking import get_ranking, get_places
from score import apply_ron, apply_dealer_tsumo, apply_non_dealer_tsumo

scores = {
    "東": 10000,
    "南": 15000,
    "西": 35000,
    "北": 40000,
}

score_tables = load_score_tables()

non_dealer_tsumo = score_tables["non_dealer_tsumo"]
non_dealer_ron = score_tables["non_dealer_ron"]
dealer_tsumo = score_tables["dealer_tsumo"]
dealer_ron = score_tables["dealer_ron"]

before_ranking = get_ranking(scores)
before_places = get_places(before_ranking)

top_score = max(scores.values())
top_player = before_places[0][1]

score_diff = {player: top_score - score for player, score in scores.items()}

results = []

print(before_ranking)
print(before_places)
print(top_score)
print(score_diff)

for winner in ["南", "西", "北"]:
    if winner == top_player:
        continue

    for _, row in non_dealer_tsumo.iterrows():
        new_scores = apply_non_dealer_tsumo(
            scores,
            winner=winner,
            dealer="東",
            non_dealer_pay=row["non_dealer_pay"],
            dealer_pay=row["dealer_pay"],
            counters=0,
            deposit=0,
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

        print(result)

    print("--------------------------------------------------")

for winner in ["南", "西", "北"]:
    if winner == top_player:
        continue

    for _, row in non_dealer_ron.iterrows():

        new_scores = apply_ron(
            scores,
            winner=winner,
            discarder=top_player,
            point=row["point"],
            counters=0,
            deposit=0,
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

        print(result)

    print("--------------------------------------------------")

for _, row in dealer_tsumo.iterrows():

    new_scores = apply_dealer_tsumo(
        scores, winner="東", pay=row["pay"], counters=0, deposit=0
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

    print(result)

print("--------------------------------------------------")

for _, row in dealer_ron.iterrows():

    new_scores = apply_ron(
        scores,
        winner="東",
        discarder=top_player,
        point=row["point"],
        counters=0,
        deposit=0,
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

    print(result)
