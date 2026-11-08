import pytest

from validation import validate_scores


@pytest.mark.parametrize(
    "scores, deposit, expected",
    [
        # ① 正常な点数
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 25000},
            0,
            (True, None),
        ),
        # ② 供託1本
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 24000},
            1,
            (True, None),
        ),
        # ③ 合計点が不正
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 24000},
            0,
            (False, None),
        ),
        # ④ 一部の点数がNone
        (
            {"東": 25000, "南": None, "西": 25000, "北": 25000},
            0,
            (False, "南"),
        ),
        # ⑤ マイナス点数を含む正常な点数
        (
            {"東": -1000, "南": 31000, "西": 35000, "北": 35000},
            0,
            (True, None),
        ),
        # ⑥ 点数が許容範囲外
        (
            {"東": 200000, "南": 25000, "西": 25000, "北": 25000},
            0,
            (False, "東"),
        ),
        # ⑥ 供託がNone
        (
            {"東": 25000, "南": 25000, "西": 25000, "北": 25000},
            None,
            (False, None),
        ),
    ],
)
def test_validate_scores(scores, deposit, expected):
    result = validate_scores(scores, deposit)

    assert result == expected
