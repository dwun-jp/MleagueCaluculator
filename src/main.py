from csv_loader import load_score_tables
from ranking import get_ranking, get_places
from score import apply_ron, apply_dealer_tsumo, apply_non_dealer_tsumo


def main():
    score_tables = load_score_tables()

    non_dealer_tsumo = score_tables["non_dealer_tsumo"]
    non_dealer_ron = score_tables["non_dealer_ron"]
    dealer_tsumo = score_tables["dealer_tsumo"]
    dealer_ron = score_tables["dealer_ron"]

    scores = {
        "東": 20000,
        "南": 30000,
        "西": 20000,
        "北": 15000,
    }

    new_scores = apply_dealer_tsumo(
        scores, winner="東", pay=2000, counters=0, deposit=0
    )

    ranking = get_ranking(new_scores)
    print(get_places(ranking))


if __name__ == "__main__":
    main()
