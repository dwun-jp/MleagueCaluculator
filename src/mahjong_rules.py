ROUND_TO_DEALER = {
    "東1局": "東",
    "東2局": "南",
    "東3局": "西",
    "東4局": "北",
    "南1局": "東",
    "南2局": "南",
    "南3局": "西",
    "南4局": "北",
}


def get_dealer(round_value):
    if round_value not in ROUND_TO_DEALER:
        raise ValueError(f"不明な局情報: {round_value}")

    return ROUND_TO_DEALER[round_value]
