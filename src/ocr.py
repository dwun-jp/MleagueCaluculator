import cv2
import pytesseract
import re
from pathlib import Path
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = PROJECT_DIR / "images"

video_path = IMAGE_DIR / "recording 2025-04-28 22.20.28.mov"

cap = cv2.VideoCapture(str(video_path))

players = {
    "東": {
        "coords": (680, 850, 50, 400),
    },
    "南": {
        "coords": (680, 850, 400, 750),
    },
    "西": {
        "coords": (680, 850, 800, 1100),
    },
    "北": {
        "coords": (680, 850, 1100, 1400),
    },
}


# OCR score extraction
def extract_score(img):
    config = "--psm 6 -c tessedit_char_whitelist=0123456789,"

    text = pytesseract.image_to_string(img, config=config)

    print("OCR結果")
    print(repr(text))

    match = re.search(r"[0-9][0-9,]*", text)
    if match:
        try:
            return int(match.group().replace(",", ""))
        except ValueError:
            return None
    return None


def read_scores(img, players):
    scores = {}

    for seat, info in players.items():
        y1, y2, x1, x2 = info["coords"]

        cropped = img[y1:y2, x1:x2]
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        scores[seat] = extract_score(binary)

    return scores


def validate_scores(scores, deposit=0):
    for player, score in scores.items():
        if score is None:
            return False, player

        elif not (-200000 < score < 200000):
            return False, player

    all_players_score = sum(scores.values())
    all_score = all_players_score + deposit * 1000

    if all_score != 100000:
        return False, None
    return True, None


def read_video_scores(cap, players):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0

    results = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if frame_count % int(fps) == 0:
            scores = read_scores(frame, players)

            is_valid, wrong_player = validate_scores(scores, deposit=0)

            if is_valid:
                results.append(scores)
            else:
                print(f"読み取り失敗: {scores}, " f"wrong_player={wrong_player}")

        frame_count += 1

    return results


result = read_video_scores(cap, players)

cap.release()

print(result)
