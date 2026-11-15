from csv_loader import load_score_tables
from search_conditions import search_conditions
from conditions import get_top_conditions

from game_session import get_confirmed_state, monitor_round
from display_formatter import create_display_data


def calculate_conditions(confirmed_state, score_tables):

    results = search_conditions(
        confirmed_state["scores"],
        score_tables,
        counters=confirmed_state["counters"],
        deposit=confirmed_state["deposit"],
    )

    return get_top_conditions(results)


def main():
    score_tables = load_score_tables()

    while True:

        # ゲーム情報を取得・確定
        confirmed_state = get_confirmed_state()

        print("ゲーム状態を確定しました")

        # 条件計算
        top_conditions = calculate_conditions(
            confirmed_state,
            score_tables,
        )

        display_data = create_display_data(
            confirmed_state,
            top_conditions,
        )

        print(display_data)

        # 次局まで監視
        monitor_round(confirmed_state)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("終了しました")
