import cv2
import pytesseract
import re
import capture
from validation import validate_scores
import configration


def extract_score(img):
    config = "--psm 6 -c tessedit_char_whitelist=0123456789,-"

    text = pytesseract.image_to_string(img, config=config)

    match = re.search(r"-?[0-9][0-9,]*", text)
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


def extract_round(img, coords):
    y1, y2, x1, x2 = coords
    cropped = img[y1:y2, x1:x2]

    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    text = pytesseract.image_to_string(
        binary,
        lang="jpn",
        config="--psm 13",
    )

    return parse_round(text)


def parse_round(text):
    text = re.sub(r"\s+", "", text)

    match = re.search(r"([東南西北])([1-4])局", text)

    if match:
        return match.group(1) + match.group(2) + "局"

    return None


def extract_number(img):
    config = "--psm 10 -c tessedit_char_whitelist=0123456789"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(
        gray,
        config=config,
    )

    match = re.search(r"\d+", text)

    if match:
        return int(match.group())

    return None


def read_number(img, coords):
    y1, y2, x1, x2 = coords
    cropped = img[y1:y2, x1:x2]

    return extract_number(cropped)


def read_game_info(frame):
    return {
        "scores": read_scores(
            frame,
            configration.crop_1600_2560,
        ),
        "round": extract_round(
            frame,
            configration.ROUND_COORDS,
        ),
        "deposit": read_number(
            frame,
            configration.DEPOSIT_COORDS,
        ),
        "counters": read_number(
            frame,
            configration.COUNTER_COORDS,
        ),
    }


if __name__ == "__main__":

    frame = capture.capture_screen()

    scores = read_scores(frame, configration.crop_1600_2560)
    round = extract_round(frame, configration.ROUND_COORDS)
    deposit = read_number(frame, configration.DEPOSIT_COORDS)
    counters = read_number(frame, configration.COUNTER_COORDS)

    is_valid, wrong_player = validate_scores(scores, deposit)
    if is_valid:
        print(f"読み取り成功: {scores}, {round}, 供託:{deposit}, {counters}本場")
    else:
        print(
            f"読み取り失敗: {scores}, {round}, 供託:{deposit}, {counters}本場, "
            f"wrong_player={wrong_player}"
        )

    """
    cv2.imshow("Round OCR", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    img = capture.capture_screen()
    img = read_scores(img, configration.crop_1600_2560)
    result = validate_scores(img, deposit=0)

    print(result)
    """
