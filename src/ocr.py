import cv2
import pytesseract
import re
from pathlib import Path
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = PROJECT_DIR / "images"

image_path = IMAGE_DIR / "frame_59_success.png"

image = cv2.imdecode(
    np.fromfile(image_path, dtype=np.uint8),
    cv2.IMREAD_COLOR,
)


# Image preprocessing
def preprocess_image(img, method):
    if method == "gray":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif method == "enlarge":
        resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        return cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    elif method == "honda":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        blurred = cv2.GaussianBlur(equalized, (0, 0), sigmaX=2)
        sharpened = cv2.addWeighted(equalized, 1.5, blurred, -0.5, 0)
        binary = cv2.adaptiveThreshold(
            sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        return binary
    return img


# OCR score extraction
def extract_score(img):
    config = "--psm 6 -c tessedit_char_whitelist=0123456789,"

    text = pytesseract.image_to_string(img, config=config)

    print("OCR結果")
    print(repr(text))

    match = re.search(r"[0-9,]+", text)
    if match:
        return int(match.group().replace(",", ""))
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


result = read_scores(image, players)
print(result)
