# 点数処理 ロン、子ツモ、親ツモ
def apply_ron(scores, winner, discarder, point, counters=0, deposit=0):

    new_scores = scores.copy()
    total_point = point + counters * 300

    new_scores[winner] += total_point + deposit * 1000
    new_scores[discarder] -= total_point

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
