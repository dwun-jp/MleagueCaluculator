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
)


def monitor_round(confirmed_state):
    candidate = None
    count = 0

    while True:
        frame = capture.capture_screen()

        round_value = extract_round(frame, configration.ROUND_COORDS)
        counters = read_number(frame, configration.COUNTER_COORDS)

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

        time.sleep(5)


def main():
    pending_state = create_empty_state()
    confirmed_state = None

    while confirmed_state is None:
        frame = capture.capture_screen()
        ocr_result = read_game_info(frame)

        # 局・本場が読み取れなければ補完しない
        if ocr_result["round"] is None or ocr_result["counters"] is None:
            time.sleep(1)
            continue

        # 同じ局・本場の情報だけを補完
        if pending_state["round"] is not None:
            if (
                pending_state["round"],
                pending_state["counters"],
            ) != (
                ocr_result["round"],
                ocr_result["counters"],
            ):
                pending_state = create_empty_state()

        pending_state = update_pending_state(pending_state, ocr_result)

        if is_complete(pending_state):
            confirmed_state = confirm_state(pending_state)

            if confirmed_state is None:
                print("妥当性チェック失敗：再取得します")
                pending_state = create_empty_state()

        print("一時保存:", pending_state)
        print("確定:", confirmed_state)

        time.sleep(1)

    print("ゲーム状態を確定しました")
    monitor_round(confirmed_state)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("終了しました")
