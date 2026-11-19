import time
import capture
import configration

from game_state import (
    create_empty_state,
    update_pending_state,
    is_complete,
    confirm_state,
    check_round_change,
    is_valid_round_transition,
    create_reading_trackers,
    get_stable_readings,
)
from ocr import read_game_info, extract_round, read_number
from display_formatter import create_loading_display_data
from api_client import send_display_data


def should_notify_confirmation_error(
    confirmed_state,
    error_notified,
    elapsed_time,
    timeout=30,
):
    return confirmed_state is None and not error_notified and elapsed_time >= timeout


def get_confirmed_state():
    pending_state = create_empty_state()
    confirmed_state = None
    trackers = create_reading_trackers()

    # エラー判定用
    start_time = time.monotonic()
    error_notified = False
    error_timeout = 30
    elapsed_time = time.monotonic() - start_time

    while confirmed_state is None:
        frame = capture.capture_screen()
        ocr_result = read_game_info(frame)

        stable_result = get_stable_readings(
            ocr_result,
            trackers,
        )

        if stable_result is not None:
            if pending_state["round"] is not None:
                if (
                    pending_state["round"],
                    pending_state["counters"],
                ) != (
                    stable_result["round"],
                    stable_result["counters"],
                ):
                    pending_state = create_empty_state()

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

        # 一定時間確定できなかった場合
        if should_notify_confirmation_error(
            confirmed_state,
            error_notified,
            elapsed_time,
            error_timeout,
        ):
            error_data = create_loading_display_data()
            error_data["status"] = "error"

            if send_display_data(error_data):
                print("ゲーム情報の確定に時間がかかっています")
                error_notified = True

        if confirmed_state is None:
            time.sleep(1)

    return confirmed_state


def monitor_round(confirmed_state, ready_display_data):
    candidate = None
    count = 0

    last_valid_time = time.monotonic()
    error_timeout = 30
    error_notified = False

    while True:
        frame = capture.capture_screen()

        round_value = extract_round(
            frame,
            configration.ROUND_COORDS,
        )
        counters = read_number(
            frame,
            configration.COUNTER_COORDS,
        )

        now = time.monotonic()

        # ① 確定済みの局と同じ場合
        is_same_round = (
            round_value == confirmed_state["round"]
            and counters == confirmed_state["counters"]
        )

        if is_same_round:
            last_valid_time = now
            candidate = None
            count = 0

            # エラーから復旧
            if error_notified:
                if send_display_data(ready_display_data):
                    print("OCRの読み取りが復旧しました")
                    error_notified = False

        # ② 次局への妥当な移行の場合
        elif is_valid_round_transition(
            confirmed_state,
            round_value,
            counters,
        ):
            last_valid_time = now

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

        # ③ 正常な読み取りでも妥当な移行でもない場合
        else:
            candidate = None
            count = 0

            if not error_notified and now - last_valid_time >= error_timeout:
                error_data = create_loading_display_data()
                error_data["status"] = "error"

                if send_display_data(error_data):
                    print("局情報の読み取り異常が継続しています")
                    error_notified = True

        time.sleep(3)
