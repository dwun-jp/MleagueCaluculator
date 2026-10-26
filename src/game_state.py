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


test_rounds = [
    ("南3局", 0),
    ("南3局", 1),
    ("南3局", 0),
    ("南3局", 1),
    ("南3局", 1),
]

pending = create_empty_state()

frame = capture.capture_screen()

result = read_game_info(frame)

print(f"OCR結果: {result}")

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
