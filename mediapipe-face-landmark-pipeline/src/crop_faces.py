import argparse
from pathlib import Path

import cv2
import mediapipe as mp


def find_face_bounds(video: Path) -> tuple[int, int, int, int] | None:
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"영상을 열 수 없습니다: {video}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    left, top, right, bottom = width, height, 0, 0
    found = False

    with mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5) as detector:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            result = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            for detection in result.detections or []:
                box = detection.location_data.relative_bounding_box
                x1 = max(0, int(box.xmin * width))
                y1 = max(0, int(box.ymin * height))
                x2 = min(width, int((box.xmin + box.width) * width))
                y2 = min(height, int((box.ymin + box.height) * height))
                left, top = min(left, x1), min(top, y1)
                right, bottom = max(right, x2), max(bottom, y2)
                found = True

    cap.release()
    if not found:
        return None

    side = max(right - left, bottom - top)
    center_x, center_y = (left + right) // 2, (top + bottom) // 2
    half = side // 2
    x1, y1 = max(0, center_x - half), max(0, center_y - half)
    x2, y2 = min(width, x1 + side), min(height, y1 + side)
    x1, y1 = max(0, x2 - side), max(0, y2 - side)
    return x1, y1, x2, y2


def crop_video(video: Path, output: Path, size: int = 256) -> bool:
    bounds = find_face_bounds(video)
    if bounds is None:
        print(f"[skip] 얼굴을 찾지 못했습니다: {video}")
        return False

    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (size, size)
    )
    x1, y1, x2, y2 = bounds

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        cropped = frame[y1:y2, x1:x2]
        writer.write(cv2.resize(cropped, (size, size)))

    cap.release()
    writer.release()
    print(f"[crop] {output}")
    return True


def process_directory(input_dir: Path, output_dir: Path, size: int) -> None:
    for video in sorted(input_dir.glob("*.mp4")):
        crop_video(video, output_dir / video.name, size)


def main() -> None:
    parser = argparse.ArgumentParser(description="영상의 얼굴 영역을 정사각형으로 정규화합니다.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--size", type=int, default=256)
    args = parser.parse_args()
    process_directory(args.input, args.output, args.size)


if __name__ == "__main__":
    main()
