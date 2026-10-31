import pytest
from game_state import (
    create_reading_trackers,
    get_stable_readings,
    check_round_change,
)


def test_reading_tracker_reset():
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
        **first,
        "counters": 2,
    }

    results = []

    for data in [first] * 3 + [second] * 3:
        results.append(get_stable_readings(data, trackers))

    # 最初の局で3回目に全項目を取得
    assert results[0] is None
    assert results[2]["scores"] == first["scores"]

    # 局が変わったら照合し直す
    assert results[3] is None
    assert results[4]["scores"]["東"] is None
    assert results[5]["scores"] == second["scores"]
    assert results[5]["counters"] == 2


def test_round_change():
    confirmed_state = {
        "round": "南3局",
        "counters": 0,
    }

    test_rounds = [
        ("南3局", 0),
        ("南3局", 1),
        ("南3局", 0),
        ("南3局", 1),
        ("南3局", 1),
    ]

    candidate = None
    count = 0
    results = []

    for round_value, counters in test_rounds:
        changed, candidate, count = check_round_change(
            confirmed_state,
            round_value,
            counters,
            candidate,
            count,
        )
        results.append(changed)

    # 最後の2回が一致したときだけ切り替え
    assert results == [False, False, False, False, True]
    assert count == 2


from game_state import is_valid_round_transition


@pytest.mark.parametrize(
    "round_value, counters, expected",
    [
        ("南2局", 2, True),
        ("南3局", 2, True),
        ("南3局", 0, True),
        ("南2局", 7, False),
        ("南3局", 1, False),
        ("南4局", 0, False),
        ("南2局", 0, False),
    ],
)
def test_valid_round_transition(round_value, counters, expected):
    confirmed_state = {
        "round": "南2局",
        "counters": 1,
    }

    result = is_valid_round_transition(
        confirmed_state,
        round_value,
        counters,
    )

    assert result == expected


from game_state import create_empty_state, is_complete


def test_is_complete():
    state = create_empty_state()

    state["round"] = "南2局"
    state["counters"] = 0
    state["deposit"] = 0
    state["scores"] = {
        "東": 25000,
        "南": 25000,
        "西": 25000,
        "北": 25000,
    }

    # 全項目が揃っている
    assert is_complete(state) is True

    # 1人分の点数が未取得
    state["scores"]["東"] = None
    assert is_complete(state) is False

    # 点数を戻し、供託を未取得にする
    state["scores"]["東"] = 25000
    state["deposit"] = None
    assert is_complete(state) is False
