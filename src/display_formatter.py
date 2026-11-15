def create_display_data(confirmed_state, top_conditions):
    scores = confirmed_state["scores"]
    top_score = max(scores.values())

    players = {}

    # ① プレイヤーごとの初期表示データ
    for seat in ("東", "南", "西", "北"):
        players[seat] = {
            "diff": top_score - scores[seat],
            "tsumo": "-",
            "ron": "-",
        }

    # ② トップ条件を表示データに反映
    for condition in top_conditions:
        winner = condition["winner"]
        method = condition["method"]
        label = str(condition["label"])

        current = players[winner][method]

        # 同点トップからの直撃など、同一条件が
        # 複数存在する場合は同じラベルにまとめる
        if current != "-" and current != label:
            raise ValueError(f"条件が一致しません: {winner}, {method}")

        players[winner][method] = label

    # ③ 画面表示用データを返す
    return {
        "round": confirmed_state["round"],
        "counters": confirmed_state["counters"],
        "deposit": confirmed_state["deposit"],
        "status": "ready",
        "players": players,
    }
