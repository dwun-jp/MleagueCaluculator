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


from search_conditions import (
    search_non_dealer_tsumo,
    search_non_dealer_ron,
    search_dealer_tsumo,
    search_dealer_ron,
)

from ranking import get_ranking, get_places


def test_non_dealer_tsumo_with_south_dealer():
    scores = {
        "東": 25000,
        "南": 23000,
        "西": 30000,
        "北": 22000,
    }

    before_places = get_places(get_ranking(scores))

    score_table = pd.DataFrame(
        [
            {
                "non_dealer_pay": 1000,
                "dealer_pay": 2000,
                "label": "1000-2000",
            }
        ]
    )

    results = search_non_dealer_tsumo(
        scores,
        before_places,
        top_players=["西"],
        score_table=score_table,
        counters=0,
        deposit=0,
        dealer="南",
    )

    assert len(results) == 2

    assert {result["winner"] for result in results} == {
        "東",
        "北",
    }

    east_result = next(result for result in results if result["winner"] == "東")

    assert east_result["after_places"] == [
        (1, "東", 29000),
        (1, "西", 29000),
        (3, "南", 21000),
        (3, "北", 21000),
    ]


def test_non_dealer_ron_with_south_dealer():
    scores = {
        "東": 25000,
        "南": 23000,
        "西": 30000,
        "北": 22000,
    }

    before_places = get_places(get_ranking(scores))

    score_table = pd.DataFrame(
        [
            {
                "point": 5200,
                "label": "5200",
            }
        ]
    )

    results = search_non_dealer_ron(
        scores,
        before_places,
        top_players=["西"],
        score_table=score_table,
        counters=0,
        deposit=0,
        dealer="南",
    )

    # 親の南家とトップの西家は探索対象外
    assert len(results) == 2

    assert {result["winner"] for result in results} == {
        "東",
        "北",
    }

    # 東家が西家から5200点ロン
    east_result = next(result for result in results if result["winner"] == "東")

    assert east_result["discarder"] == "西"
    assert east_result["label"] == "5200"

    assert east_result["after_places"] == [
        (1, "東", 30200),
        (2, "西", 24800),
        (3, "南", 23000),
        (4, "北", 22000),
    ]


def test_dealer_tsumo_with_south_dealer():
    scores = {
        "東": 25000,
        "南": 23000,
        "西": 30000,
        "北": 22000,
    }

    before_places = get_places(get_ranking(scores))

    score_table = pd.DataFrame(
        [
            {
                "pay": 2000,
                "label": "2000オール",
            }
        ]
    )

    results = search_dealer_tsumo(
        scores,
        before_places,
        top_players=["西"],
        score_table=score_table,
        counters=0,
        deposit=0,
        dealer="南",
    )

    assert len(results) == 1

    result = results[0]

    assert result["winner"] == "南"
    assert result["method"] == "tsumo"
    assert result["discarder"] is None
    assert result["label"] == "2000オール"

    assert result["after_places"] == [
        (1, "南", 29000),
        (2, "西", 28000),
        (3, "東", 23000),
        (4, "北", 20000),
    ]


def test_dealer_ron_with_south_dealer():
    scores = {
        "東": 25000,
        "南": 23000,
        "西": 30000,
        "北": 22000,
    }

    before_places = get_places(get_ranking(scores))

    score_table = pd.DataFrame(
        [
            {
                "point": 12000,
                "label": "満貫",
            }
        ]
    )

    results = search_dealer_ron(
        scores,
        before_places,
        top_players=["西"],
        score_table=score_table,
        counters=0,
        deposit=0,
        dealer="南",
    )

    assert len(results) == 1

    result = results[0]

    assert result["winner"] == "南"
    assert result["method"] == "ron"
    assert result["discarder"] == "西"
    assert result["label"] == "満貫"

    assert result["after_places"] == [
        (1, "南", 35000),
        (2, "東", 25000),
        (3, "北", 22000),
        (4, "西", 18000),
    ]


from main import calculate_conditions

"""
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

    score_tables = make_score_tables()

    results = calculate_conditions(
        confirmed_state,
        score_tables,
    )

    print("戻り値の型:", type(results))
    print("結果の件数:", len(results))

    for result in results:
        print(
            result["winner"],
            result["method"],
            result["discarder"],
            result["label"],
        )
        print("和了後:", result["after_places"])
"""
