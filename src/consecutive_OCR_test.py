import time
import capture

from ocr import read_game_info, extract_round, read_number
import configration
from game_state import (
    create_empty_state,
    update_pending_state,
    is_complete,
    confirm_state,
    check_round_change,
    is_valid_round_transition,
)
from game_state import (
    create_reading_trackers,
    get_stable_readings,
)

from csv_loader import load_score_tables
from main import calculate_conditions


def monitor_round(confirmed_state):
    candidate = None
    count = 0

    while True:
        frame = capture.capture_screen()

        round_value = extract_round(frame, configration.ROUND_COORDS)
        counters = read_number(frame, configration.COUNTER_COORDS)

        if not is_valid_round_transition(
            confirmed_state,
            round_value,
            counters,
        ):
            candidate = None
            count = 0
            print(
                f"次局を確認中: {confirmed_state['round']}, {confirmed_state['counters']} -> {round_value}, {counters}"
            )
            time.sleep(3)
            continue

        changed, candidate, count = check_round_change(
            confirmed_state,
            round_value,
            counters,
            candidate,
            count,
        )

        print(
            f"局: {round_value}, 本場: {counters}, "
            f"切替候補: {candidate}, 回数: {count}"
        )

        if changed:
            print("新しい局を検出しました")
            return

        time.sleep(3)


def main():
    score_tables = load_score_tables()

    while True:
        pending_state = create_empty_state()
        confirmed_state = None
        trackers = create_reading_trackers()

        while confirmed_state is None:
            frame = capture.capture_screen()
            ocr_result = read_game_info(frame)

            # ★追加：OCR結果を複数回照合
            stable_result = get_stable_readings(
                ocr_result,
                trackers,
            )

            # ★追加：局・本場がまだ安定していない場合
            if stable_result is None:
                time.sleep(1)
                continue

            # ★変更：照合済みの局・本場で比較
            if pending_state["round"] is not None:
                if (
                    pending_state["round"],
                    pending_state["counters"],
                ) != (
                    stable_result["round"],
                    stable_result["counters"],
                ):
                    pending_state = create_empty_state()

            # ★変更：照合済みの値だけを保存
            pending_state = update_pending_state(
                pending_state,
                stable_result,
            )

            if is_complete(pending_state):
                confirmed_state = confirm_state(pending_state)

                if confirmed_state is None:
                    print("妥当性チェック失敗：再取得します")
                    pending_state = create_empty_state()
                    trackers = create_reading_trackers()

            print("照合結果:", stable_result)
            print("一時保存:", pending_state)
            print("確定:", confirmed_state)

            time.sleep(1)

        print("ゲーム状態を確定しました")

        top_conditions = calculate_conditions(
            confirmed_state,
            score_tables,
        )

        for top_condition in top_conditions:
            print(top_condition)

        monitor_round(confirmed_state)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("終了しました")
