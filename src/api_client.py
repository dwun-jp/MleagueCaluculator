import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def send_display_data(display_data):
    url = "http://127.0.0.1:5000/api/update"

    # Pythonの辞書をJSON形式に変換
    json_data = json.dumps(
        display_data,
        ensure_ascii=False,
    ).encode("utf-8")

    # POSTリクエストを作成
    request = Request(
        url,
        data=json_data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    # Flaskへ送信
    try:
        with urlopen(request, timeout=3) as response:
            return response.status == 200

    except (HTTPError, URLError, TimeoutError) as error:
        print(f"Flaskへの送信に失敗しました: {error}")
        return False
