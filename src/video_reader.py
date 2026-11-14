import cv2

from pathlib import Path
from validation import validate_scores
from ocr import read_scores


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
                print(frame.shape)
            else:
                print(f"読み取り失敗: {scores}, " f"wrong_player={wrong_player}")

        frame_count += 1

    return results


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parent.parent
    video_path = project_dir / "images" / "recording 2025-04-28 22.20.28.mov"

    cap = cv2.VideoCapture(str(video_path))

    try:
        if not cap.isOpened():
            raise RuntimeError("動画を開けませんでした")

        # 座標設定は、現在の ocr.py から一時的に読み込む
        from ocr import crp_900_1440

        result = read_video_scores(cap, crp_900_1440)
        print(result)

    finally:
        cap.release()
