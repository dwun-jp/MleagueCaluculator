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
