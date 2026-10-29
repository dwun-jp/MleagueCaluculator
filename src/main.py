from csv_loader import load_score_tables
from search_conditions import search_conditions
from conditions import get_top_conditions


def calculate_conditions(confirmed_state, score_tables):

    results = search_conditions(
        confirmed_state["scores"],
        score_tables,
        counters=confirmed_state["counters"],
        deposit=confirmed_state["deposit"],
    )

    return get_top_conditions(results)


if __name__ == "__main__":
    main()
