import pandas as pd

from search_conditions import search_conditions

scores = {
    "東": 20000,
    "南": 35000,
    "西": 25000,
    "北": 20000,
}


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


def test_dealer_ron_changes_ranking():
    scores = {
        "東": 20000,
        "南": 35000,
        "西": 25000,
        "北": 20000,
    }

    results = search_conditions(
        scores,
        make_score_tables(),
    )

    dealer_ron = [
        result
        for result in results
        if result["winner"] == "東" and result["method"] == "ron"
    ]

    assert len(dealer_ron) == 1

    result = dealer_ron[0]

    assert result["discarder"] == "南"
    assert result["label"] == "8000"

    assert result["after_places"] == [
        (1, "東", 28000),
        (2, "南", 27000),
        (3, "西", 25000),
        (4, "北", 20000),
    ]


def test_search_conditions_result_count():
    scores = {
        "東": 20000,
        "南": 35000,
        "西": 25000,
        "北": 20000,
    }

    results = search_conditions(
        scores,
        make_score_tables(),
    )

    assert len(results) == 6

    assert sum(result["method"] == "tsumo" for result in results) == 3

    assert sum(result["method"] == "ron" for result in results) == 3


def test_exclude_dealer_when_already_top():
    scores = {
        "東": 40000,
        "南": 30000,
        "西": 20000,
        "北": 10000,
    }

    results = search_conditions(
        scores,
        make_score_tables(),
    )

    assert len(results) == 6

    assert all(result["winner"] != "東" for result in results)


def test_dealer_ron_with_counters_and_deposit():
    scores = {
        "東": 20000,
        "南": 35000,
        "西": 25000,
        "北": 19000,
    }

    results = search_conditions(
        scores,
        make_score_tables(),
        counters=2,
        deposit=1,
    )

    dealer_ron = [
        result
        for result in results
        if result["winner"] == "東" and result["method"] == "ron"
    ]

    assert len(dealer_ron) == 1

    assert dealer_ron[0]["after_places"] == [
        (1, "東", 29600),
        (2, "南", 26400),
        (3, "西", 25000),
        (4, "北", 19000),
    ]


def test_non_dealer_tsumo_changes_ranking():
    scores = {
        "東": 25000,
        "南": 30000,
        "西": 26000,
        "北": 19000,
    }

    results = search_conditions(
        scores,
        make_score_tables(),
    )

    west_tsumo = [
        result
        for result in results
        if result["winner"] == "西" and result["method"] == "tsumo"
    ]

    assert len(west_tsumo) == 1

    result = west_tsumo[0]

    assert result["discarder"] is None
    assert result["label"] == "1000/2000"

    assert result["after_places"] == [
        (1, "西", 30000),
        (2, "南", 29000),
        (3, "東", 23000),
        (4, "北", 18000),
    ]


def test_non_dealer_tsumo_tied_for_first():
    scores = {
        "東": 25000,
        "南": 30000,
        "西": 25000,
        "北": 20000,
    }

    results = search_conditions(
        scores,
        make_score_tables(),
    )

    west_tsumo = [
        result
        for result in results
        if result["winner"] == "西" and result["method"] == "tsumo"
    ]

    assert len(west_tsumo) == 1

    assert west_tsumo[0]["after_places"] == [
        (1, "南", 29000),
        (1, "西", 29000),
        (3, "東", 23000),
        (4, "北", 19000),
    ]


def test_exclude_tied_top_players():
    scores = {
        "東": 30000,
        "南": 30000,
        "西": 25000,
        "北": 15000,
    }

    results = search_conditions(
        scores,
        make_score_tables(),
    )

    winners = {result["winner"] for result in results}

    assert winners == {"西", "北"}
    assert len(results) == 6

    ron_discarders = {
        result["discarder"] for result in results if result["method"] == "ron"
    }

    assert ron_discarders == {"東", "南"}
