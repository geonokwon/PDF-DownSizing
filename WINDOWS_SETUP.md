# 윈도우용 PDF DownSizing Tool 설치 및 사용 가이드

## 🖥️ 윈도우에서 실행하기 위한 준비사항

### 1. Ghostscript 설치 (필수)
PDF 압축을 위해 Ghostscript가 필요합니다.

#### 방법 1: 공식 웹사이트에서 다운로드
1. [Ghostscript 공식 사이트](https://www.ghostscript.com/download/gsdnld.html) 방문
2. "Windows" 버전 다운로드
3. 설치 프로그램 실행하여 설치

#### 방법 2: Chocolatey 사용 (권장)
```powershell
# PowerShell을 관리자 권한으로 실행
choco install ghostscript
```

#### 방법 3: Winget 사용
```powershell
winget install ArtifexSoftware.GhostScript
```

### 2. 실행 파일 다운로드
`dist/PDF-DownSizing-Tool.exe` 파일을 윈도우 컴퓨터로 복사

## 🚀 사용 방법

### 1. 실행
- `PDF-DownSizing-Tool.exe` 파일을 더블클릭하여 실행
- 또는 파일을 우클릭 → "관리자 권한으로 실행" (권장)

### 2. PDF 압축
1. **파일 선택**: "Browse" 버튼 클릭 또는 PDF 파일을 드래그 앤 드롭
2. **품질 설정**: 슬라이더로 압축 품질 조절 (1-100)
3. **압축 시작**: "Start Compression" 버튼 클릭
4. **결과 확인**: 압축된 파일이 원본과 같은 폴더에 저장됨

## ⚠️ 문제 해결

### Ghostscript 관련 오류
- **오류**: "gs is not recognized as an internal or external command"
- **해결**: Ghostscript가 PATH에 추가되지 않았습니다
  - Ghostscript 재설치
  - 또는 환경변수 PATH에 Ghostscript 설치 경로 추가

### 실행 파일이 실행되지 않는 경우
1. **Windows Defender 확인**: 실행 파일이 차단되었을 수 있습니다
   - Windows Defender → 바이러스 및 위협 방지 → 제외 항목 추가
2. **관리자 권한으로 실행**: 파일 우클릭 → "관리자 권한으로 실행"

### 압축이 되지 않는 경우
1. **Ghostscript 설치 확인**: 명령 프롬프트에서 `gs --version` 입력
2. **파일 권한 확인**: PDF 파일에 읽기/쓰기 권한이 있는지 확인
3. **디스크 공간 확인**: 충분한 여유 공간이 있는지 확인

## 🔧 개발자용 정보

### 윈도우에서 빌드하기
```bash
# Python 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 윈도우용 실행 파일 생성
python build_windows.py
```

### 필요한 패키지
- Python 3.8 이상
- tkinter (Python과 함께 설치됨)
- PyPDF2
- Pillow
- pyinstaller
- tkinterdnd2

## 📁 파일 구조 (윈도우)
```
PDF-DownSizing-Tool/
├── PDF-DownSizing-Tool.exe    # 메인 실행 파일
├── README.md                  # 사용 설명서
└── (필요시 추가 파일들)
```

## 🎯 성능 최적화 팁

1. **품질 설정**: 
   - 높은 품질 (80-100): 큰 파일 크기, 좋은 화질
   - 중간 품질 (50-79): 균형잡힌 압축
   - 낮은 품질 (1-49): 작은 파일 크기, 낮은 화질

2. **파일 유형별 압축 효과**:
   - 이미지가 많은 PDF: 높은 압축 효과
   - 텍스트 중심 PDF: 제한적인 압축 효과
   - 스캔 문서: 가장 높은 압축 효과

3. **시스템 요구사항**:
   - RAM: 최소 4GB (8GB 권장)
   - 디스크: 충분한 여유 공간
   - OS: Windows 10 이상 (Windows 11 권장)

## 🆘 지원

문제가 발생하면 다음을 확인하세요:
1. Ghostscript가 올바르게 설치되었는지
2. 실행 파일이 관리자 권한으로 실행되고 있는지
3. PDF 파일이 손상되지 않았는지
4. 충분한 디스크 공간이 있는지
