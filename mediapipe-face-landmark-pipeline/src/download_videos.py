import argparse
import csv
import subprocess
import sys
from pathlib import Path


def download_videos(metadata: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    with metadata.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if "video_id" not in (reader.fieldnames or []):
            raise ValueError("CSV 파일에 'video_id' 열이 필요합니다.")

        for row in reader:
            video_id = row["video_id"].strip()
            if not video_id:
                continue

            output_template = str(output_dir / f"{video_id}.%(ext)s")
            command = [
                sys.executable,
                "-m",
                "yt_dlp",
                "-f",
                "best[ext=mp4]/best",
                "-o",
                output_template,
                f"https://youtu.be/{video_id}",
            ]
            print(f"[download] {video_id}")
            subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="CSV의 영상 ID를 이용해 영상을 다운로드합니다.")
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("outputs/downloads"))
    args = parser.parse_args()
    download_videos(args.metadata, args.output)


if __name__ == "__main__":
    main()
