def validate_scores(scores, deposit=0):
    for player, score in scores.items():
        if score is None:
            return False, player

        elif not (-200000 < score < 200000):
            return False, player

    all_players_score = sum(scores.values())
    all_score = all_players_score + deposit * 1000

    if all_score != 100000:
        return False, None
    return True, None
