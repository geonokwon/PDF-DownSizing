# PDF DownSizing Tool 사용법

## 🚀 빠른 시작

### 방법 1: 실행 파일 사용 (권장)
1. `dist/PDF-DownSizing-Tool.app` 파일을 더블클릭하여 실행
2. 또는 `dist/PDF-DownSizing-Tool` 실행 파일을 터미널에서 실행

### 방법 2: 개발 환경에서 실행
```bash
# 가상환경 활성화
source venv/bin/activate

# 애플리케이션 실행
python main.py
```

## 📋 사용 방법

1. **PDF 파일 선택**
   - "Browse" 버튼을 클릭하여 PDF 파일 선택
   - 또는 PDF 파일을 창에 드래그 앤 드롭

2. **압축 품질 설정**
   - 품질 슬라이더로 1-100 사이 값 설정
   - 높은 값 = 더 좋은 품질, 더 큰 파일 크기
   - 낮은 값 = 더 낮은 품질, 더 작은 파일 크기

3. **압축 시작**
   - "Start Compression" 버튼 클릭
   - 진행률 표시줄에서 압축 진행 상황 확인

4. **결과 확인**
   - 압축된 파일이 원본과 같은 폴더에 저장됨
   - 파일명: `원본파일명_compressed.pdf`

## 🔧 빌드 방법

### 맥용 실행 파일 생성
```bash
source venv/bin/activate
python build_macos.py
```

### 윈도우용 실행 파일 생성
```bash
source venv/bin/activate
python build_windows.py
```

## 📁 파일 구조
```
PDF-DownSizing/
├── main.py                 # 메인 GUI 애플리케이션
├── pdf_compressor.py       # PDF 압축 로직
├── drag_drop_handler.py    # 드래그 앤 드롭 처리
├── requirements.txt        # Python 의존성
├── build_macos.py         # 맥 빌드 스크립트
├── build_windows.py       # 윈도우 빌드 스크립트
├── test_app.py            # 테스트 스크립트
├── dist/                  # 빌드된 실행 파일
│   ├── PDF-DownSizing-Tool.app  # 맥 앱 번들
│   └── PDF-DownSizing-Tool      # 실행 파일
└── venv/                  # Python 가상환경
```

## ⚠️ 주의사항

- 원본 PDF 파일은 보존됩니다
- 압축된 파일은 원본과 같은 폴더에 저장됩니다
- 이미지가 많은 PDF에서 압축 효과가 더 큽니다
- 텍스트만 있는 PDF는 압축 효과가 제한적입니다

## 🐛 문제 해결

### 애플리케이션이 실행되지 않는 경우
1. Python 3.8 이상이 설치되어 있는지 확인
2. 가상환경을 활성화하고 의존성 설치:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 드래그 앤 드롭이 작동하지 않는 경우
- "Browse" 버튼을 사용하여 파일을 선택하세요

### 압축이 실패하는 경우
- PDF 파일이 손상되지 않았는지 확인
- 파일에 읽기/쓰기 권한이 있는지 확인
- 충분한 디스크 공간이 있는지 확인
