# README.md

## MediaPipe를 이용한 얼굴 랜드마크 비디오 데이터셋 

### 파일 구조
```
20223196.zip
├── README.md
├── 20223196.pdf
├── source_code/
│   ├── crop_final.py
│   ├── download_final.py
│   ├── landmark_final.py
│   ├── slice_final.py
├── results/
│   ├── youtube_video/
│   ├── my_video/
├── input/
    ├── metadata.csv
```

### 파일 설명

- **20223196.pdf**: 과제 구현 과정과 결과물을 설명하는 보고서입니다.
- **source_code/**: 프로젝트에 사용된 Python 소스코드 디렉토리입니다.
  - `download_final.py`: 유튜브 동영상을 다운로드하는 스크립트.
  - `slice_final.py`: 동영상을 얼굴 검출 구간별로 분할하는 스크립트.
  - `crop_final.py`: 얼굴 영역을 자르고 리사이즈하는 스크립트.
  - `landmark_final.py`: 얼굴 랜드마크를 생성하고 다양한 옵션으로 시각화하는 스크립트.
- **results/**: 실행 결과로 생성된 랜드마크 동영상.
  - **youtube_video/**: 유튜브 동영상 처리 결과.
  - **my_video/**: 직접 촬영한 동영상 처리 결과.
- **input/**: 입력 데이터 디렉토리.
  - `metadata.csv`: 유튜브 동영상 ID가 포함된 메타데이터 파일.

### 실행 방법

1. **Python 환경 설정**:
   - 필수 패키지 설치:
     ```bash
     pip install mediapipe yt-dlp opencv-python moviepy
     ```

2. **유튜브 동영상 다운로드**:
   - `download_final.py` 스크립트 실행:
     ```bash
     python download_final.py
     ```

3. **비디오 분할**:
   - `slice_final.py` 스크립트 실행:
     ```bash
     python slice_final.py
     ```

4. **얼굴 영역 자르기**:
   - `crop_final.py` 스크립트 실행:
     ```bash
     python crop_final.py
     ```

5. **얼굴 랜드마크 생성**:
   - `landmark_final.py` 스크립트 실행:
     ```bash
     python landmark_final.py
     ```

### 참고 사항
- 입력 데이터는 `input/metadata.csv`에 포함되어 있어야 합니다.
- 실행 과정에서 생성된 모든 결과물은 `results/` 디렉토리에 저장됩니다.
