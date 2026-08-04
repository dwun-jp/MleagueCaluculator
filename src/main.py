import pandas as pd
from pathlib import Path

# データ読み取り
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"

non_dealer_tsumo = pd.read_csv(DATA_DIR / "子ツモ@点数計算.csv")
non_dealer_ron = pd.read_csv(DATA_DIR / "子ロン@点数計算.csv")
dealer_tsumo = pd.read_csv(DATA_DIR / "親ツモ@点数計算.csv")
dealer_ron = pd.read_csv(DATA_DIR / "親ロン@点数計算.csv")


# 順番に並べ替えて、同点なら同じ順位にする
def get_ranking(scores):
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def get_places(ranking):
    places = []

    previous_score = None
    previous_place = None

    for index, (player, score) in enumerate(ranking, start=1):
        if score == previous_score:
            place = previous_place
        else:
            place = index

        places.append((place, player, score))

        previous_score = score
        previous_place = place

    return places


# 点数処理 ロン、子ツモ、親ツモ
def apply_ron(scores, winner, loser, point, counters=0, deposit=0):

    new_scores = scores.copy()
    total_point = point + counters * 300

    new_scores[winner] += total_point + deposit * 1000
    new_scores[loser] -= total_point

    return new_scores


def apply_dealer_tsumo(scores, winner, pay, counters=0, deposit=0):
    new_scores = scores.copy()
    payment = pay + counters * 100

    for player in new_scores:
        if player == winner:
            new_scores[player] += payment * 3 + deposit * 1000
        else:
            new_scores[player] -= payment

    return new_scores


def apply_non_dealer_tsumo(
    scores, winner, dealer, non_dealer_pay, dealer_pay, counters=0, deposit=0
):
    new_scores = scores.copy()
    non_dealer_payment = non_dealer_pay + counters * 100
    dealer_payment = dealer_pay + counters * 100

    for player in new_scores:
        if player == winner:
            new_scores[player] += (
                non_dealer_payment * 2 + dealer_payment + deposit * 1000
            )
        elif player == dealer:
            new_scores[player] -= dealer_payment
        else:
            new_scores[player] -= non_dealer_payment

    return new_scores


scores = {
    "東": 20000,
    "南": 30000,
    "西": 20000,
    "北": 15000,
}

new_scores = apply_non_dealer_tsumo(
    scores, winner="南", dealer="東", non_dealer_pay=1000, dealer_pay=2000
)

ranking = get_ranking(new_scores)

for rank, (player, score) in enumerate(ranking, start=1):
    print(rank, player, score)
