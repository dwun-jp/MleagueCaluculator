from copy import deepcopy
from validation import validate_scores
from ocr import read_game_info
import capture


def create_empty_state():
    return {
        "round": None,
        "counters": None,
        "deposit": None,
        "scores": {
            "東": None,
            "南": None,
            "西": None,
            "北": None,
        },
    }


def create_reading_tracker():
    return {
        "candidate": None,
        "count": 0,
    }


def create_reading_trackers():
    return {
        "active_round": None,
        "round_info": create_reading_tracker(),
        "deposit": create_reading_tracker(),
        "scores": {seat: create_reading_tracker() for seat in ("東", "南", "西", "北")},
    }


def update_pending_state(pending_state, ocr_result):

    for key in ("round", "counters", "deposit"):
        if pending_state[key] is None and ocr_result[key] is not None:
            pending_state[key] = ocr_result[key]

    for seat, score in ocr_result["scores"].items():
        if pending_state["scores"][seat] is None and score is not None:
            pending_state["scores"][seat] = score

    return pending_state


def is_complete(state):

    if any(state[key] is None for key in ("round", "counters", "deposit")):
        return False

    if any(score is None for score in state["scores"].values()):
        return False

    return True


def confirm_state(pending_state):
    if not is_complete(pending_state):
        return None

    is_valid, wrong_player = validate_scores(
        pending_state["scores"],
        pending_state["deposit"],
    )

    if not is_valid:
        return None

    return deepcopy(pending_state)


def is_round_changed(confirmed_state, round_value, counters):
    if confirmed_state is None:
        return False

    if round_value is None or counters is None:
        return False

    return (
        confirmed_state["round"],
        confirmed_state["counters"],
    ) != (round_value, counters)


def check_round_change(
    confirmed_state,
    round_value,
    counters,
    candidate,
    count,
):
    if round_value is None or counters is None:
        return False, None, 0

    current = (round_value, counters)

    if not is_round_changed(confirmed_state, round_value, counters):
        return False, None, 0

    if current == candidate:
        count += 1
    else:
        candidate = current
        count = 1

    return count >= 2, candidate, count


ROUNDS = [f"{wind}{num}局" for wind in ("東", "南") for num in range(1, 5)]


def is_valid_round_transition(
    confirmed_state,
    round_value,
    counters,
):
    if confirmed_state is None:
        return False

    if round_value is None or counters is None:
        return False

    old_round = confirmed_state["round"]
    old_counters = confirmed_state["counters"]

    if (
        old_round not in ROUNDS
        or round_value not in ROUNDS
        or old_counters is None
        or counters < 0
    ):
        return False

    # 同じ局で連荘する場合
    if round_value == old_round:
        return counters == old_counters + 1

    # 次の局を取得
    old_index = ROUNDS.index(old_round)

    if old_index + 1 >= len(ROUNDS):
        return False

    next_round = ROUNDS[old_index + 1]

    # 次の局に進む場合
    if round_value == next_round:
        return counters in (0, old_counters + 1)

    return False


def check_stable_reading(tracker, value, required_count=2):

    if value is None:
        tracker["candidate"] = None
        tracker["count"] = 0
        return None

    if tracker["candidate"] == value:
        tracker["count"] += 1
    else:
        tracker["candidate"] = value
        tracker["count"] = 1

    if tracker["count"] >= required_count:
        return value

    return None


def get_stable_readings(ocr_result, trackers):

    round_value = ocr_result["round"]
    counters = ocr_result["counters"]

    if round_value is None or counters is None:
        round_info = None
    else:
        round_info = (round_value, counters)

    stable_round = check_stable_reading(
        trackers["round_info"],
        round_info,
    )

    if stable_round is None:
        return None

    if stable_round != trackers["active_round"]:
        trackers["active_round"] = stable_round

        trackers["deposit"] = create_reading_tracker()

        for seat in trackers["scores"]:
            trackers["scores"][seat] = create_reading_tracker()

    stable_result = {
        "round": stable_round[0],
        "counters": stable_round[1],
        "deposit": check_stable_reading(
            trackers["deposit"],
            ocr_result["deposit"],
        ),
        "scores": {},
    }

    for seat, score in ocr_result["scores"].items():
        stable_result["scores"][seat] = check_stable_reading(
            trackers["scores"][seat],
            score,
        )

    return stable_result


if __name__ == "__main__":
    trackers = create_reading_trackers()

    first = {
        "round": "南2局",
        "counters": 1,
        "deposit": 0,
        "scores": {
            "東": 27300,
            "南": 13700,
            "西": 29300,
            "北": 29700,
        },
    }

    second = {
        "round": "南2局",
        "counters": 2,
        "deposit": 0,
        "scores": {
            "東": 27300,
            "南": 13700,
            "西": 29300,
            "北": 29700,
        },
    }

    for data in [first] * 3 + [second] * 3:
        result = get_stable_readings(data, trackers)

        print(f"入力: {data['round']} {data['counters']}本場, " f"結果: {result}")

"""

pending = update_pending_state(pending, result)
confirmed_state = confirm_state(pending)

candidate = None
count = 0

for round_value, counters in test_rounds:

    # OCR結果を受け取るたびに実行
    changed, candidate, count = check_round_change(
        confirmed_state,
        round_value,
        counters,
        candidate,
        count,
    )

    print(
        f"Round: {round_value}, Counters: {counters}, Changed: {changed}, Candidate: {candidate}, Count: {count}"
    )

    if changed:
        pending_state = create_empty_state()
        confirmed_state = None

"""
