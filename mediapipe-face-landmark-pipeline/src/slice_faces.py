import argparse
import subprocess
from pathlib import Path

import cv2
import mediapipe as mp


def detected_intervals(video: Path, min_duration: float) -> list[tuple[float, float]]:
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"영상을 열 수 없습니다: {video}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        cap.release()
        raise RuntimeError(f"FPS를 확인할 수 없습니다: {video}")

    intervals: list[tuple[float, float]] = []
    start: float | None = None
    frame_index = 0

    with mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.5) as detector:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            timestamp = frame_index / fps
            result = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if result.detections and start is None:
                start = timestamp
            elif not result.detections and start is not None:
                if timestamp - start >= min_duration:
                    intervals.append((start, timestamp))
                start = None

            frame_index += 1

    end = frame_index / fps
    if start is not None and end - start >= min_duration:
        intervals.append((start, end))

    cap.release()
    return intervals


def slice_video(video: Path, output_dir: Path, min_duration: float = 3.0) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    intervals = detected_intervals(video, min_duration)

    for index, (start, end) in enumerate(intervals, start=1):
        output = output_dir / f"{video.stem}_segment_{index:02d}.mp4"
        command = [
            "ffmpeg", "-y", "-i", str(video),
            "-ss", str(start), "-to", str(end),
            "-c:v", "libx264", "-c:a", "aac", str(output),
        ]
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[segment] {output}")


def process_directory(input_dir: Path, output_dir: Path, min_duration: float) -> None:
    for video in sorted(input_dir.glob("*.mp4")):
        slice_video(video, output_dir, min_duration)


def main() -> None:
    parser = argparse.ArgumentParser(description="얼굴이 연속 검출되는 영상 구간을 분할합니다.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--min-duration", type=float, default=3.0)
    args = parser.parse_args()
    process_directory(args.input, args.output, args.min_duration)


if __name__ == "__main__":
    main()
