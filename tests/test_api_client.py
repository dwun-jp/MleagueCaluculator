import json

import api_client


def test_send_display_data(monkeypatch):
    display_data = {
        "round": "東2局",
        "counters": 1,
        "deposit": 2,
        "status": "ready",
        "players": {
            "東": {"diff": 5200, "tsumo": "700オール", "ron": "1500"},
            "南": {"diff": 0, "tsumo": "-", "ron": "-"},
            "西": {"diff": 4600, "tsumo": "500-1000", "ron": "1000"},
            "北": {"diff": 4600, "tsumo": "500-1000", "ron": "1000"},
        },
    }

    class MockResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

    def mock_urlopen(request, timeout):
        assert request.get_method() == "POST"
        assert timeout == 3

        sent_data = json.loads(request.data.decode("utf-8"))
        assert sent_data == display_data

        return MockResponse()

    monkeypatch.setattr(
        api_client,
        "urlopen",
        mock_urlopen,
    )

    assert api_client.send_display_data(display_data) is True


from urllib.error import URLError


def test_send_display_data_connection_error(monkeypatch):
    display_data = {
        "round": "東2局",
        "counters": 0,
        "deposit": 0,
        "status": "ready",
        "players": {
            seat: {"diff": 0, "tsumo": "-", "ron": "-"}
            for seat in ("東", "南", "西", "北")
        },
    }

    def mock_urlopen(request, timeout):
        raise URLError("Connection refused")

    monkeypatch.setattr(
        api_client,
        "urlopen",
        mock_urlopen,
    )

    assert api_client.send_display_data(display_data) is False
