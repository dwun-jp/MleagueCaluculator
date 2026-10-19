import cv2
import pytesseract
import re
import capture
from validation import validate_scores
import configuration


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

        cv2.imshow("Cropped Image", gray)
        cv2.waitKey(0)

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
    img = read_scores(img, configuration.crop_1600_2560)
    result = validate_scores(img, deposit=0)

    print(result)
