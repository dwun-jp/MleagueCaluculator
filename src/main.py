from csv_loader import load_score_tables
from search_conditions import search_conditions


def main():

    scores = {
        "東": 20000,
        "南": 30000,
        "西": 20000,
        "北": 15000,
    }

    score_tables = load_score_tables()

    results = search_conditions(scores, score_tables, counters=0, deposit=0)

    print(results)


if __name__ == "__main__":
    main()
