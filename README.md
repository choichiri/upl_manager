# 영업일지 관리 시스템

국내/해외 영업일지를 관리하는 데스크톱 애플리케이션입니다.

## 데이터 소스

- `국내_영업일지.xlsm` — 국내 고객사 영업일지
- `해외_영업일지.xlsm` — 해외 고객사 영업일지

## 기술 스택

- Python 3.10+
- PyQt6 (UI)
- openpyxl (엑셀 읽기/쓰기, VBA 매크로 보존)

## 설치 및 실행

```bash
pip install -r requirements.txt
python main.py
```

## 프로젝트 구조

```
customerManager/
├── main.py                 # 앱 진입점
├── requirements.txt
├── data/                   # 엑셀 원본 + UI 디자인 참고
├── src/
│   ├── __init__.py
│   ├── excel_handler.py    # 엑셀 읽기/쓰기 로직
│   ├── models.py           # 데이터 모델 (Customer, ProgressEntry)
│   ├── main_window.py      # 메인 윈도우 UI
│   └── widgets/            # 커스텀 위젯
└── README.md
```

## 개발 단계

1. 엑셀 데이터 읽기 + 콘솔 출력 (데이터 구조 검증)
2. 메인 UI (읽기 전용)
3. 수정/저장/등록 기능
4. 설정 + PyInstaller 배포
