from copy import deepcopy
from threading import Lock

from flask import Flask, jsonify, request, send_from_directory

app = Flask(
    __name__,
    static_folder="web",
    static_url_path="",
)

app.json.ensure_ascii = False

state_lock = Lock()

# 現在表示しているデータ
current_display_data = {
    "round": "確認中",
    "counters": 0,
    "deposit": 0,
    "status": "loading",
    "players": {
        seat: {
            "diff": 0,
            "tsumo": "-",
            "ron": "-",
        }
        for seat in ("東", "南", "西", "北")
    },
}


def validate_display_data(data):
    if not isinstance(data, dict):
        return False

    if not isinstance(data.get("round"), str):
        return False

    if not data["round"].strip():
        return False

    for key in ("counters", "deposit"):
        if type(data.get(key)) is not int:
            return False
        if data[key] < 0:
            return False

    if data.get("status") not in ("ready", "loading", "error"):
        return False

    players = data.get("players")

    if not isinstance(players, dict):
        return False

    if set(players.keys()) != {"東", "南", "西", "北"}:
        return False

    for seat in ("東", "南", "西", "北"):
        player = players[seat]

        if not isinstance(player, dict):
            return False

        if type(player.get("diff")) is not int:
            return False

        if player["diff"] < 0:
            return False

        if not isinstance(player.get("tsumo"), str):
            return False

        if not isinstance(player.get("ron"), str):
            return False

    return True


@app.get("/")
def index():
    return send_from_directory(
        app.static_folder,
        "index.html",
    )


@app.get("/api/state")
def get_state():
    with state_lock:
        data = deepcopy(current_display_data)

    return jsonify(data)


@app.post("/api/update")
def update_state():
    global current_display_data

    # データ送信は同じPCからのみ許可
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return jsonify({"error": "Local access only"}), 403

    # 送信されたJSONを取得
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    # 必須項目の確認
    required_keys = {
        "round",
        "counters",
        "deposit",
        "status",
        "players",
    }

    if not required_keys.issubset(data.keys()):
        return jsonify({"error": "Missing required keys"}), 400

    if not validate_display_data(data):
        return jsonify({"error": "Invalid display data"}), 400

    # 表示データを更新
    with state_lock:
        current_display_data = deepcopy(data)

    return jsonify({"message": "updated"}), 200


if __name__ == "__main__":
    app.run(debug=False)
