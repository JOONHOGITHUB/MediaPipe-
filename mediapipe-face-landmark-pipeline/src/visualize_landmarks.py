import argparse
from pathlib import Path

import cv2
import mediapipe as mp


STYLES = ("mesh", "contours", "grayscale-contours")


def visualize_video(video: Path, output: Path, style: str = "mesh") -> None:
    cap = cv2.VideoCapture(str(video))
    if not cap.isOpened():
        raise RuntimeError(f"영상을 열 수 없습니다: {video}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )

    drawing = mp.solutions.drawing_utils
    face_mesh_module = mp.solutions.face_mesh
    specification = drawing.DrawingSpec(thickness=1, circle_radius=1)
    connections = (
        face_mesh_module.FACEMESH_TESSELATION
        if style == "mesh"
        else face_mesh_module.FACEMESH_CONTOURS
    )

    with face_mesh_module.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as model:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            result = model.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            canvas = frame
            if style == "grayscale-contours":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                canvas = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

            for landmarks in result.multi_face_landmarks or []:
                drawing.draw_landmarks(
                    image=canvas,
                    landmark_list=landmarks,
                    connections=connections,
                    landmark_drawing_spec=specification,
                    connection_drawing_spec=specification,
                )
            writer.write(canvas)

    cap.release()
    writer.release()
    print(f"[landmarks] {output}")


def process_directory(input_dir: Path, output_dir: Path, style: str) -> None:
    for video in sorted(input_dir.glob("*.mp4")):
        visualize_video(video, output_dir / video.name, style)


def main() -> None:
    parser = argparse.ArgumentParser(description="Face Mesh 랜드마크를 영상에 시각화합니다.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--style", choices=STYLES, default="mesh")
    args = parser.parse_args()
    process_directory(args.input, args.output, args.style)


if __name__ == "__main__":
    main()
