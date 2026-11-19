from game_session import should_notify_confirmation_error


def test_should_notify_confirmation_error():
    check = should_notify_confirmation_error

    # 30秒未満
    assert check(None, False, 29) is False

    # 30秒経過
    assert check(None, False, 30) is True

    # すでにエラーを通知済み
    assert check(None, True, 35) is False

    # ゲーム状態は確定済み
    assert check({"round": "東2局"}, False, 35) is False


from types import SimpleNamespace
import game_session


def test_monitor_round_same_round_no_error(monkeypatch):
    confirmed_state = {
        "round": "東2局",
        "counters": 1,
    }

    ready_data = {"status": "ready"}

    readings = iter(
        [
            ("東2局", 1),
            ("東2局", 1),
            ("東3局", 0),
            ("東3局", 0),
        ]
    )

    clock = iter([0, 10, 45, 46, 47])

    # 画面キャプチャを置き換え
    monkeypatch.setattr(
        game_session.capture,
        "capture_screen",
        lambda: next(readings),
    )

    # OCR処理を置き換え
    monkeypatch.setattr(
        game_session,
        "extract_round",
        lambda frame, coords: frame[0],
    )

    monkeypatch.setattr(
        game_session,
        "read_number",
        lambda frame, coords: frame[1],
    )

    # 時間の経過を再現
    monkeypatch.setattr(
        game_session,
        "time",
        SimpleNamespace(
            monotonic=lambda: next(clock),
            sleep=lambda seconds: None,
        ),
    )

    # Flaskへの送信内容を記録
    sent_data = []

    def mock_send_display_data(data):
        sent_data.append(data)
        return True

    monkeypatch.setattr(
        game_session,
        "send_display_data",
        mock_send_display_data,
    )

    game_session.monitor_round(
        confirmed_state,
        ready_data,
    )

    assert sent_data == []


def test_monitor_round_error_and_recovery(monkeypatch):
    confirmed_state = {
        "round": "東2局",
        "counters": 1,
    }

    ready_data = {"status": "ready"}

    readings = iter(
        [
            ("東2局", 1),
            (None, None),
            (None, None),
            ("東2局", 1),
            ("東3局", 0),
            ("東3局", 0),
        ]
    )

    clock = iter([0, 10, 41, 44, 45, 46, 47])

    # 画面キャプチャ・OCRを置き換える
    monkeypatch.setattr(
        game_session.capture,
        "capture_screen",
        lambda: next(readings),
    )

    monkeypatch.setattr(
        game_session,
        "extract_round",
        lambda frame, coords: frame[0],
    )

    monkeypatch.setattr(
        game_session,
        "read_number",
        lambda frame, coords: frame[1],
    )

    # 時間経過を再現
    monkeypatch.setattr(
        game_session,
        "time",
        SimpleNamespace(
            monotonic=lambda: next(clock),
            sleep=lambda seconds: None,
        ),
    )

    # Flaskへの送信を記録
    sent_data = []

    def mock_send_display_data(data):
        sent_data.append(data)
        return True

    monkeypatch.setattr(
        game_session,
        "send_display_data",
        mock_send_display_data,
    )

    game_session.monitor_round(
        confirmed_state,
        ready_data,
    )

    # error → ready の順番で1回ずつ送信
    assert [data["status"] for data in sent_data] == [
        "error",
        "ready",
    ]

    # エラー時の表示内容
    assert sent_data[0]["round"] == "確認中"
    assert sent_data[0]["players"]["東"]["tsumo"] == "-"

    # 復旧時は元のreadyデータを再送信
    assert sent_data[1] == ready_data


def test_monitor_round_retry_send(monkeypatch):
    confirmed_state = {
        "round": "東2局",
        "counters": 1,
    }

    ready_data = {"status": "ready"}

    readings = iter(
        [
            ("東2局", 1),
            (None, None),
            (None, None),
            ("東2局", 1),
            ("東2局", 1),
            ("東3局", 0),
            ("東3局", 0),
        ]
    )

    clock = iter([0, 10, 41, 44, 45, 46, 47, 48])

    monkeypatch.setattr(
        game_session.capture,
        "capture_screen",
        lambda: next(readings),
    )

    monkeypatch.setattr(
        game_session,
        "extract_round",
        lambda frame, coords: frame[0],
    )

    monkeypatch.setattr(
        game_session,
        "read_number",
        lambda frame, coords: frame[1],
    )

    monkeypatch.setattr(
        game_session,
        "time",
        SimpleNamespace(
            monotonic=lambda: next(clock),
            sleep=lambda seconds: None,
        ),
    )

    sent_statuses = []

    # 1回目は失敗、2回目は成功
    responses = iter([False, True, False, True])

    def mock_send_display_data(data):
        sent_statuses.append(data["status"])
        return next(responses)

    monkeypatch.setattr(
        game_session,
        "send_display_data",
        mock_send_display_data,
    )

    game_session.monitor_round(
        confirmed_state,
        ready_data,
    )

    assert sent_statuses == [
        "error",
        "error",
        "ready",
        "ready",
    ]
