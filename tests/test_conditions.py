from conditions import get_player_place, get_top_conditions

BEFORE = [
    (1, "東", 35000),
    (2, "南", 30000),
    (3, "西", 20000),
    (4, "北", 15000),
]

AFTER_TOP = [
    (1, "西", 38000),
    (2, "東", 27000),
    (3, "南", 20000),
    (4, "北", 15000),
]

AFTER_SECOND = [
    (1, "東", 35000),
    (2, "西", 28000),
    (3, "南", 22000),
    (4, "北", 15000),
]

AFTER_TIED = [
    (1, "東", 30000),
    (1, "西", 30000),
    (3, "南", 25000),
    (4, "北", 15000),
]


def make_result(
    method="ron",
    discarder="東",
    label="3900",
    after_places=None,
):
    if after_places is None:
        after_places = AFTER_TOP

    return {
        "winner": "西",
        "method": method,
        "discarder": discarder,
        "label": label,
        "before_places": BEFORE,
        "after_places": after_places,
    }


def test_get_player_place():
    assert get_player_place(BEFORE, "東") == 1
    assert get_player_place(BEFORE, "西") == 3
    assert get_player_place(BEFORE, "不明") is None


def test_extract_only_top():
    second = make_result(after_places=AFTER_SECOND)
    top = make_result(label="8000")

    result = get_top_conditions([second, top])

    assert result == [top]


def test_tied_first_is_included():
    tied = make_result(after_places=AFTER_TIED)

    result = get_top_conditions([tied])

    assert result == [tied]


def test_keep_first_condition_per_method():
    ron_small = make_result(label="3900")
    ron_large = make_result(label="8000")
    tsumo = make_result(
        method="tsumo",
        discarder=None,
        label="1000/2000",
    )

    result = get_top_conditions([ron_small, ron_large, tsumo])

    assert result == [ron_small, tsumo]


def test_distinguish_ron_discarders():
    ron_east = make_result(discarder="東")
    ron_south = make_result(discarder="南")

    result = get_top_conditions([ron_east, ron_south])

    assert result == [ron_east, ron_south]


from csv_loader import load_score_tables
from search_conditions import search_conditions
from conditions import get_top_conditions


def test_csv_loader_and_search_conditions():
    score_tables = load_score_tables()

    score = {
        "東": 35100,
        "南": 30000,
        "西": 20100,
        "北": 14800,
    }

    results = search_conditions(
        score,
        score_tables,
        counters=0,
        deposit=0,
    )

    top_conditions = get_top_conditions(results)

    assert len(top_conditions) == 6

    conditions = {
        (
            result["winner"],
            result["method"],
            result["discarder"],
        ): result
        for result in top_conditions
    }

    assert set(conditions.keys()) == {
        ("南", "tsumo", None),
        ("西", "tsumo", None),
        ("北", "tsumo", None),
        ("南", "ron", "東"),
        ("西", "ron", "東"),
        ("北", "ron", "東"),
    }

    south_tsumo = conditions[("南", "tsumo", None)]
    assert south_tsumo["label"] == "900-1800"
    assert south_tsumo["after_places"] == [
        (1, "南", 33600),
        (2, "東", 33300),
        (3, "西", 19200),
        (4, "北", 13900),
    ]

    west_tsumo = conditions[("西", "tsumo", None)]
    assert west_tsumo["label"] == "跳満"
    assert west_tsumo["after_places"] == [
        (1, "西", 32100),
        (2, "東", 29100),
        (3, "南", 27000),
        (4, "北", 11800),
    ]

    north_tsumo = conditions[("北", "tsumo", None)]
    assert north_tsumo["label"] == "倍満"
    assert north_tsumo["after_places"] == [
        (1, "北", 30800),
        (2, "東", 27100),
        (3, "南", 26000),
        (4, "西", 16100),
    ]

    south_ron = conditions[("南", "ron", "東")]
    assert south_ron["label"] == "2600"
    assert south_ron["after_places"] == [
        (1, "南", 32600),
        (2, "東", 32500),
        (3, "西", 20100),
        (4, "北", 14800),
    ]

    west_ron = conditions[("西", "ron", "東")]
    assert west_ron["label"] == "跳満"
    assert west_ron["after_places"] == [
        (1, "西", 32100),
        (2, "南", 30000),
        (3, "東", 23100),
        (4, "北", 14800),
    ]

    north_ron = conditions[("北", "ron", "東")]
    assert north_ron["label"] == "倍満"
    assert north_ron["after_places"] == [
        (1, "北", 30800),
        (2, "南", 30000),
        (3, "西", 20100),
        (4, "東", 19100),
    ]


def test_conditions_with_counters_and_deposit():
    score_tables = load_score_tables()

    scores = {
        "東": 35100,
        "南": 30000,
        "西": 20100,
        "北": 13800,
    }

    results = search_conditions(
        scores,
        score_tables,
        counters=2,
        deposit=1,
    )

    top_conditions = get_top_conditions(results)

    # ① ロン2600点の結果を取得
    south_ron = next(
        result
        for result in results
        if result["winner"] == "南"
        and result["method"] == "ron"
        and result["discarder"] == "東"
        and result["label"] == "2600"
    )

    assert south_ron["after_places"] == [
        (1, "南", 34200),
        (2, "東", 31900),
        (3, "西", 20100),
        (4, "北", 13800),
    ]

    # ② ツモ900-1800の結果を取得
    south_tsumo = next(
        result
        for result in results
        if result["winner"] == "南"
        and result["method"] == "tsumo"
        and result["label"] == "900-1800"
    )

    assert south_tsumo["after_places"] == [
        (1, "南", 35200),
        (2, "東", 33100),
        (3, "西", 19000),
        (4, "北", 12700),
    ]

    # ③ トップ条件の抽出まで確認
    assert len(top_conditions) == 6

    for condition in top_conditions:
        winner = condition["winner"]
        after_places = condition["after_places"]

        assert any(
            place == 1 and player == winner for place, player, score in after_places
        )
