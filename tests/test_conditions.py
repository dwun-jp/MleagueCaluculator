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
