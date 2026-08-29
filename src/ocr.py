import cv2
import pytesseract
import re


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
def extract_score(img, config):
    text = pytesseract.image_to_string(img, lang="jpn", config=config)
    match = re.search(r"[\d,]+", text)
    if match:
        try:
            return int(match.group().replace(",", ""))
        except ValueError:
            return None
    return None
