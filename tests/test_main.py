from main import calculate_conditions
import pandas as pd


def make_score_tables():
    return {
        "non_dealer_tsumo": pd.DataFrame(
            [
                {
                    "label": "1000/2000",
                    "non_dealer_pay": 1000,
                    "dealer_pay": 2000,
                }
            ]
        ),
        "non_dealer_ron": pd.DataFrame([{"label": "3900", "point": 3900}]),
        "dealer_tsumo": pd.DataFrame([{"label": "2000オール", "pay": 2000}]),
        "dealer_ron": pd.DataFrame([{"label": "8000", "point": 8000}]),
    }


def test_calculate_conditions_south_dealer():
    confirmed_state = {
        "round": "東2局",
        "counters": 0,
        "deposit": 0,
        "scores": {
            "東": 25000,
            "南": 23000,
            "西": 30000,
            "北": 22000,
        },
    }

    results = calculate_conditions(
        confirmed_state,
        make_score_tables(),
    )

    south_tsumo = next(
        result
        for result in results
        if result["winner"] == "南" and result["method"] == "tsumo"
    )

    assert south_tsumo["label"] == "2000オール"

    assert south_tsumo["after_places"] == [
        (1, "南", 29000),
        (2, "西", 28000),
        (3, "東", 23000),
        (4, "北", 20000),
    ]


def test_calculate_conditions_west_dealer():
    confirmed_state = {
        "round": "南3局",
        "counters": 0,
        "deposit": 0,
        "scores": {
            "東": 25000,
            "南": 30000,
            "西": 23000,
            "北": 22000,
        },
    }

    results = calculate_conditions(
        confirmed_state,
        make_score_tables(),
    )

    west_tsumo = next(
        result
        for result in results
        if result["winner"] == "西" and result["method"] == "tsumo"
    )

    assert west_tsumo["label"] == "2000オール"

    assert west_tsumo["after_places"] == [
        (1, "西", 29000),
        (2, "南", 28000),
        (3, "東", 23000),
        (4, "北", 20000),
    ]


def test_calculate_conditions_north_dealer():
    confirmed_state = {
        "round": "南4局",
        "counters": 0,
        "deposit": 0,
        "scores": {
            "東": 25000,
            "南": 30000,
            "西": 23000,
            "北": 22000,
        },
    }

    results = calculate_conditions(
        confirmed_state,
        make_score_tables(),
    )

    north_tsumo = next(
        result
        for result in results
        if result["winner"] == "北" and result["method"] == "tsumo"
    )

    assert north_tsumo["label"] == "2000オール"

    assert north_tsumo["after_places"] == [
        (1, "南", 28000),
        (1, "北", 28000),
        (3, "東", 23000),
        (4, "西", 21000),
    ]


def test_calculate_conditions_dealer_ron():
    confirmed_state = {
        "round": "南3局",
        "counters": 0,
        "deposit": 0,
        "scores": {
            "東": 25000,
            "南": 30000,
            "西": 23000,
            "北": 22000,
        },
    }

    results = calculate_conditions(
        confirmed_state,
        make_score_tables(),
    )

    dealer_ron = next(
        result
        for result in results
        if result["winner"] == "西" and result["method"] == "ron"
    )

    assert dealer_ron["label"] == "8000"
    assert dealer_ron["discarder"] == "南"
    assert dealer_ron["after_places"] == [
        (1, "西", 31000),
        (2, "東", 25000),
        (3, "南", 22000),
        (3, "北", 22000),
    ]


def test_calculate_conditions_non_dealer_tsumo():
    confirmed_state = {
        "round": "南4局",
        "counters": 0,
        "deposit": 0,
        "scores": {
            "東": 25000,
            "南": 30000,
            "西": 23000,
            "北": 22000,
        },
    }

    results = calculate_conditions(
        confirmed_state,
        make_score_tables(),
    )

    non_dealer_tsumo = next(
        result
        for result in results
        if result["winner"] == "東" and result["method"] == "tsumo"
    )

    assert non_dealer_tsumo["label"] == "1000/2000"

    assert non_dealer_tsumo["after_places"] == [
        (1, "東", 29000),
        (1, "南", 29000),
        (3, "西", 22000),
        (4, "北", 20000),
    ]
