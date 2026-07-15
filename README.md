# MediaPipe 얼굴 랜드마크 비디오 파이프라인

MediaPipe와 OpenCV를 활용해 영상 수집부터 얼굴 구간 추출, 얼굴 영역 정규화, Face Mesh 시각화까지 자동화한 컴퓨터 비전 파이프라인입니다.

## 주요 기능

- CSV에 기록된 영상 ID를 이용한 입력 영상 수집
- 일정 시간 이상 얼굴이 검출되는 구간 자동 분할
- 영상 전체의 얼굴 영역을 계산해 정사각형으로 크롭 및 리사이즈
- MediaPipe Face Mesh 기반 랜드마크 시각화
- 원본 영상, 얼굴 구간, 크롭 영상 및 랜드마크 결과를 단계별 디렉터리에 저장

## 처리 과정

```text
metadata.csv
    ↓
영상 다운로드
    ↓
얼굴 검출 구간 분할
    ↓
얼굴 중심 크롭 및 256×256 정규화
    ↓
Face Mesh 랜드마크 생성
    ↓
결과 영상 저장
```

## 프로젝트 구조

```text
mediapipe-face-landmark-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── input/
│   └── metadata.example.csv
├── src/
│   ├── download_videos.py
│   ├── slice_faces.py
│   ├── crop_faces.py
│   ├── visualize_landmarks.py
│   └── pipeline.py
└── outputs/
    ├── downloads/
    ├── segments/
    ├── cropped/
    └── landmarks/
```

`outputs/`의 폴더 구조는 `.gitkeep`으로 유지됩니다. 실행 과정에서 생성되는 영상 파일은 용량과 개인정보 보호를 위해 Git에 포함되지 않습니다.

## 설치

Python 3.9~3.11 환경을 권장합니다. 영상 분할을 위해 시스템에 FFmpeg가 설치되어 있어야 합니다.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

macOS에서는 다음 명령으로 FFmpeg를 설치할 수 있습니다.

```bash
brew install ffmpeg
```

## 실행

### 전체 파이프라인

```bash
python src/pipeline.py --metadata input/metadata.csv
```

### 직접 보유한 영상 처리

저작권과 개인정보 이용 권한을 보유한 MP4 파일을 `outputs/downloads/`에 넣은 후 다운로드 단계를 생략할 수 있습니다.

```bash
python src/pipeline.py --skip-download
```

### 단계별 실행

```bash
python src/download_videos.py --metadata input/metadata.csv --output outputs/downloads
python src/slice_faces.py --input outputs/downloads --output outputs/segments --min-duration 3
python src/crop_faces.py --input outputs/segments --output outputs/cropped --size 256
python src/visualize_landmarks.py --input outputs/cropped --output outputs/landmarks --style mesh
```

랜드마크 스타일은 `mesh`, `contours`, `grayscale-contours` 중에서 선택할 수 있습니다.

## 구현 포인트

- 프레임별 얼굴 검출 결과를 시간 구간으로 변환해 연속 검출 구간만 추출합니다.
- 영상 전체에서 검출된 얼굴 바운딩 박스의 합집합을 계산합니다.
- 합집합 영역을 정사각형으로 보정하고 동일한 해상도로 정규화합니다.
- 얼굴이 검출되지 않은 영상은 오류를 발생시키지 않고 건너뜁니다.
- 외부 명령 실행 시 문자열 셸 명령 대신 인자 리스트를 사용합니다.

## 활용 기술

Python · MediaPipe · OpenCV · FFmpeg · yt-dlp

## 데이터 및 저작권

- 저장소에는 원본 영상과 얼굴이 포함된 결과 영상을 포함하지 않습니다.
- 직접 촬영했거나 사용 권한을 확보한 영상만 처리해야 합니다.
- 외부 플랫폼의 영상을 사용할 때는 해당 서비스의 이용약관과 저작권을 확인해야 합니다.

## 프로젝트 배경

컴퓨터 비전 학습 과정에서 시작한 구현을 포트폴리오용으로 재구성했습니다. Colab에 종속된 코드를 일반 Python 환경에서 실행 가능한 CLI 파이프라인으로 정리하고, 입력·출력 구조와 실행 방법을 문서화했습니다.

## 프로젝트 배경

컴퓨터 비전 학습 과정에서 시작한 구현을 포트폴리오용으로 재구성했습니다.  
기존 코드를 실행 가능한 파이프라인 형태로 정리하고 문서화했습니다.
