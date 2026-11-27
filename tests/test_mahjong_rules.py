import pytest

from mahjong_rules import get_dealer


@pytest.mark.parametrize(
    "round_value, expected",
    [
        ("東1局", "東"),
        ("東2局", "南"),
        ("東3局", "西"),
        ("東4局", "北"),
        ("南1局", "東"),
        ("南2局", "南"),
        ("南3局", "西"),
        ("南4局", "北"),
    ],
)
def test_get_dealer(round_value, expected):
    assert get_dealer(round_value) == expected
