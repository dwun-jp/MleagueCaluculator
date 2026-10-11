import cv2
import mss
import numpy as np


def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    return frame


if __name__ == "__main__":
    frame = capture_screen()

    print(frame.shape)

    cv2.imshow("Screen Capture", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
