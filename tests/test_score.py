import pytest

from score import (
    apply_ron,
    apply_dealer_tsumo,
    apply_non_dealer_tsumo,
)


@pytest.mark.parametrize(
    "scores, counters, deposit, expected",
    [
        # 通常のロン
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 25000},
            0,
            0,
            {"東": 28900, "南": 25000, "西": 25000, "北": 21100},
        ),
        # 2本場・供託1本
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 24000},
            2,
            1,
            {"東": 30500, "南": 25000, "西": 25000, "北": 19500},
        ),
    ],
)
def test_apply_ron(scores, counters, deposit, expected):
    original = scores.copy()

    result = apply_ron(
        scores,
        winner="東",
        discarder="北",
        point=3900,
        counters=counters,
        deposit=deposit,
    )

    assert result == expected
    assert scores == original


@pytest.mark.parametrize(
    "scores, counters, deposit, expected",
    [
        # 通常の親ツモ
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 25000},
            0,
            0,
            {"東": 31000, "南": 23000, "西": 23000, "北": 23000},
        ),
        # 2本場・供託1本
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 24000},
            2,
            1,
            {"東": 32600, "南": 22800, "西": 22800, "北": 21800},
        ),
    ],
)
def test_apply_dealer_tsumo(scores, counters, deposit, expected):
    original = scores.copy()

    result = apply_dealer_tsumo(
        scores,
        winner="東",
        pay=2000,
        counters=counters,
        deposit=deposit,
    )

    assert result == expected
    assert scores == original


@pytest.mark.parametrize(
    "scores, counters, deposit, expected",
    [
        # 通常の子ツモ
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 25000},
            0,
            0,
            {"東": 23000, "南": 29000, "西": 24000, "北": 24000},
        ),
        # 2本場・供託1本
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 24000},
            2,
            1,
            {"東": 22800, "南": 30600, "西": 23800, "北": 22800},
        ),
    ],
)
def test_apply_non_dealer_tsumo(scores, counters, deposit, expected):
    original = scores.copy()

    result = apply_non_dealer_tsumo(
        scores,
        winner="南",
        dealer="東",
        non_dealer_pay=1000,
        dealer_pay=2000,
        counters=counters,
        deposit=deposit,
    )

    assert result == expected
    assert scores == original
