from flask import Flask, jsonify, send_from_directory

app = Flask(
    __name__,
    static_folder="web",
    static_url_path="",
)


@app.get("/")
def index():
    return send_from_directory(
        app.static_folder,
        "index.html",
    )


@app.get("/api/state")
def get_state():
    display_data = {
        "round": "東2局",
        "counters": 1,
        "deposit": 2,
        "status": "ready",
        "players": {
            "東": {
                "diff": 5000,
                "tsumo": "700オール",
                "ron": "1500",
            },
            "南": {
                "diff": 0,
                "tsumo": "-",
                "ron": "-",
            },
            "西": {
                "diff": 4600,
                "tsumo": "600-1200",
                "ron": "1000",
            },
            "北": {
                "diff": 4600,
                "tsumo": "500-1000",
                "ron": "3000",
            },
        },
    }

    return jsonify(display_data)


if __name__ == "__main__":
    app.run(debug=False)
