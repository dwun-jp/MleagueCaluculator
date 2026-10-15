import cv2
import pytesseract
import re
import capture
from validation import validate_scores

crp_900_1440 = {
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

crp_1600_2560 = {
    "東": {
        "coords": (1250, 1500, 200, 700),
    },
    "南": {
        "coords": (1250, 1500, 800, 1300),
    },
    "西": {
        "coords": (1250, 1500, 1400, 1850),
    },
    "北": {
        "coords": (1250, 1500, 1950, 2400),
    },
}


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


if __name__ == "__main__":

    img = capture.capture_screen()
    img = read_scores(img, crp_1600_2560)
    result = validate_scores(img, deposit=0)

    print(result)
