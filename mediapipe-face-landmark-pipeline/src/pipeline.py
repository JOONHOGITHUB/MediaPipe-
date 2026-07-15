import argparse
from pathlib import Path

from crop_faces import process_directory as crop_directory
from download_videos import download_videos
from slice_faces import process_directory as slice_directory
from visualize_landmarks import process_directory as visualize_directory


def main() -> None:
    parser = argparse.ArgumentParser(description="얼굴 랜드마크 비디오 파이프라인")
    parser.add_argument("--metadata", type=Path, default=Path("input/metadata.csv"))
    parser.add_argument("--output-root", type=Path, default=Path("outputs"))
    parser.add_argument("--min-duration", type=float, default=3.0)
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument(
        "--style", choices=("mesh", "contours", "grayscale-contours"), default="mesh"
    )
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    downloads = args.output_root / "downloads"
    segments = args.output_root / "segments"
    cropped = args.output_root / "cropped"
    landmarks = args.output_root / "landmarks"

    if not args.skip_download:
        download_videos(args.metadata, downloads)
    slice_directory(downloads, segments, args.min_duration)
    crop_directory(segments, cropped, args.size)
    visualize_directory(cropped, landmarks, args.style)

    print(f"완료: {landmarks.resolve()}")


if __name__ == "__main__":
    main()
