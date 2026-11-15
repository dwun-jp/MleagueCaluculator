from display_formatter import create_display_data


def test_create_display_data():
    confirmed_state = {
        "round": "南2局",
        "counters": 1,
        "deposit": 0,
        "scores": {
            "東": 35100,
            "南": 30000,
            "西": 20100,
            "北": 14800,
        },
    }

    top_conditions = [
        {
            "winner": "南",
            "method": "tsumo",
            "discarder": None,
            "label": "900-1800",
        },
        {
            "winner": "南",
            "method": "ron",
            "discarder": "東",
            "label": "2600",
        },
    ]

    result = create_display_data(
        confirmed_state,
        top_conditions,
    )

    assert result["round"] == "南2局"
    assert result["counters"] == 1
    assert result["deposit"] == 0
    assert result["status"] == "ready"

    assert result["players"]["東"] == {
        "diff": 0,
        "tsumo": "-",
        "ron": "-",
    }

    assert result["players"]["南"] == {
        "diff": 5100,
        "tsumo": "900-1800",
        "ron": "2600",
    }

    assert result["players"]["西"]["diff"] == 15000
    assert result["players"]["北"]["diff"] == 20300


def test_create_same_rank_display_data():
    confirmed_state = {
        "round": "南2局",
        "counters": 0,
        "deposit": 0,
        "scores": {
            "東": 30000,
            "南": 30000,
            "西": 25000,
            "北": 15000,
        },
    }

    top_conditions = [
        {
            "winner": "西",
            "method": "ron",
            "discarder": "東",
            "label": "5200",
        },
        {
            "winner": "西",
            "method": "ron",
            "discarder": "南",
            "label": "5200",
        },
    ]

    result = create_display_data(
        confirmed_state,
        top_conditions,
    )

    # 同じ条件が1つにまとめられる
    assert result["players"]["西"]["ron"] == "5200"

    # 同点トップの点差は両方0
    assert result["players"]["東"]["diff"] == 0
    assert result["players"]["南"]["diff"] == 0

    # 西と北の点差
    assert result["players"]["西"]["diff"] == 5000
    assert result["players"]["北"]["diff"] == 15000


import pytest


def test_conflicting_ron_conditions():
    confirmed_state = {
        "round": "南2局",
        "counters": 0,
        "deposit": 0,
        "scores": {
            "東": 30000,
            "南": 30000,
            "西": 25000,
            "北": 15000,
        },
    }

    top_conditions = [
        {
            "winner": "西",
            "method": "ron",
            "discarder": "東",
            "label": "5200",
        },
        {
            "winner": "西",
            "method": "ron",
            "discarder": "南",
            "label": "8000",
        },
    ]

    with pytest.raises(ValueError):
        create_display_data(confirmed_state, top_conditions)
