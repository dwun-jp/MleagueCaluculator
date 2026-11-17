import app as app_module


def test_update_and_get_state(monkeypatch):
    # テスト用のデータに切り替える
    monkeypatch.setattr(
        app_module,
        "current_display_data",
        {},
    )

    test_data = {
        "round": "南4局",
        "counters": 3,
        "deposit": 1,
        "status": "ready",
        "players": {
            "東": {"diff": 0, "tsumo": "-", "ron": "-"},
            "南": {"diff": 5000, "tsumo": "1000-2000", "ron": "3900"},
            "西": {"diff": 10000, "tsumo": "跳満", "ron": "跳満"},
            "北": {"diff": 15000, "tsumo": "倍満", "ron": "倍満"},
        },
    }

    client = app_module.app.test_client()

    # POSTでデータを送信
    response = client.post(
        "/api/update",
        json=test_data,
    )

    assert response.status_code == 200
    assert response.get_json() == {"message": "updated"}

    # GETで保存されたデータを取得
    response = client.get("/api/state")

    assert response.status_code == 200
    assert response.get_json() == test_data


def test_update_missing_keys(monkeypatch):
    original_data = {
        "round": "東2局",
        "status": "ready",
    }

    monkeypatch.setattr(
        app_module,
        "current_display_data",
        original_data,
    )

    client = app_module.app.test_client()

    # 必須項目が不足しているデータを送信
    response = client.post(
        "/api/update",
        json={"round": "南4局"},
    )

    # エラーが返ることを確認
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required keys"}

    # 保存済みデータが書き換わっていないことを確認
    response = client.get("/api/state")
    assert response.get_json() == original_data


from copy import deepcopy


def test_update_invalid_data():
    client = app_module.app.test_client()

    # 現在の表示データを取得
    original_data = client.get("/api/state").get_json()

    # 点差を不正な文字列に変更
    invalid_data = deepcopy(original_data)
    invalid_data["players"]["東"]["diff"] = "不明"

    response = client.post(
        "/api/update",
        json=invalid_data,
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid display data"}

    # 保存済みデータが変更されていないことを確認
    response = client.get("/api/state")
    assert response.get_json() == original_data
