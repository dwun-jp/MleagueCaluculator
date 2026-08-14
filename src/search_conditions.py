from csv_loader import load_score_tables
from ranking import get_ranking, get_places
from score import apply_ron, apply_dealer_tsumo, apply_non_dealer_tsumo

scores = {
    "東": 25000,
    "南": 25000,
    "西": 25000,
    "北": 25000,
}

score_tables = load_score_tables()

non_dealer_tsumo = score_tables["non_dealer_tsumo"]
non_dealer_ron = score_tables["non_dealer_ron"]
dealer_tsumo = score_tables["dealer_tsumo"]
dealer_ron = score_tables["dealer_ron"]

before_places = get_places(get_ranking(scores))

for _, row in non_dealer_tsumo.iterrows():

    new_scores = apply_non_dealer_tsumo(
        scores,
        winner="南",
        dealer="東",
        non_dealer_pay=row["non_dealer_pay"],
        dealer_pay=row["dealer_pay"],
        counters=0,
        deposit=0,
    )

    ranking = get_ranking(new_scores)
    places = get_places(ranking)

    after_places = get_places(get_ranking(new_scores))

    print(after_places)
    print(places)

print("--------------------------------------------------")

for _, row in non_dealer_ron.iterrows():

    new_scores = apply_ron(
        scores, winner="南", discarder="西", point=row["point"], counters=0, deposit=0
    )

    ranking = get_ranking(new_scores)
    places = get_places(ranking)

    after_places = get_places(get_ranking(new_scores))

    print(after_places)
    print(places)

print("--------------------------------------------------")

for _, row in dealer_tsumo.iterrows():

    new_scores = apply_dealer_tsumo(
        scores, winner="東", pay=row["pay"], counters=0, deposit=0
    )

    ranking = get_ranking(new_scores)
    places = get_places(ranking)

    after_places = get_places(get_ranking(new_scores))

    print(after_places)
    print(places)

print("--------------------------------------------------")

for _, row in dealer_ron.iterrows():

    new_scores = apply_ron(
        scores, winner="東", discarder="南", point=row["point"], counters=0, deposit=0
    )

    ranking = get_ranking(new_scores)
    places = get_places(ranking)

    after_places = get_places(get_ranking(new_scores))

    print(after_places)
    print(places)
