# 🔮 타로 카드 AI 챗봇

[![Flask](https://img.shields.io/badge/Flask-2.3+-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange.svg)](https://ai.google.dev/)

**비즈니스 딥러닝 2주차 실습 과제**

Google Gemini AI를 활용한 인터랙티브 타로 카드 점술 웹 애플리케이션입니다.

## ✨ 주요 기능

- **🎴 22장 메이저 아르카나**: 전체 타로 카드 덱 지원
- **🤖 AI 타로 리딩**: Gemini AI 기반 전문적인 해석
- **🖼️ 카드 시각화**: 고품질 타로 카드 이미지 표시
- **🔄 정방향/역방향**: 카드 방향에 따른 다른 해석
- **📱 반응형 UI**: 모바일과 데스크톱 최적화
- **🎯 맞춤형 상담**: 1-3장 카드 선택 가능

## 🚀 설치 및 실행

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. Gemini API 키 설정

`config.yaml` 파일에서 본인의 Gemini API 키를 설정하세요:

```yaml
gemini:
  api_key: "YOUR_GEMINI_API_KEY"
  model: "gemini-1.5-flash"
```

### 3. 애플리케이션 실행

```bash
python app.py
```

### 4. 웹 브라우저에서 접속

http://127.0.0.1:5000 으로 접속하세요.

## 📁 프로젝트 구조

```
zodiac/
├── app.py                 # Flask 메인 애플리케이션
├── tarot_chatbot.py      # 기존 콘솔 챗봇 (참고용)
├── config.yaml           # 설정 파일
├── tarot_cards.json      # 타로 카드 데이터
├── requirements.txt      # Python 패키지 의존성
├── templates/
│   └── index.html       # 메인 웹 페이지
├── static/
│   ├── style.css        # 스타일시트
│   └── script.js        # 클라이언트 JavaScript
└── card_image/          # 타로 카드 이미지들
    ├── 00_The_Fool.jpg
    ├── 01_The_Magician.jpg
    └── ...
```

## 🎮 사용법

1. 웹 페이지에 접속하면 자동으로 챗봇에 연결됩니다
2. 오른쪽 채팅창에서 질문을 입력하세요
3. 카드 수를 1-3장 중에서 선택할 수 있습니다
4. 뽑힌 카드들은 왼쪽 패널에 표시됩니다
5. "도움말"을 입력하면 사용법을 확인할 수 있습니다

## 🔧 기술 스택

- **백엔드**: Flask, Python
- **프론트엔드**: HTML5, CSS3, JavaScript
- **AI**: Google Gemini API
- **통신**: REST API, AJAX (fetch)
- **스타일링**: CSS Grid, Flexbox, 애니메이션

## 📱 화면 구성

- **왼쪽 패널**: 뽑힌 타로 카드들 시각화
  - 정방향/역방향 표시
  - 카드 이름 (한국어/영어)
  - 호버 애니메이션

- **오른쪽 패널**: 채팅 인터페이스
  - 실시간 메시지 교환
  - 카드 수 선택 옵션
  - 타이핑 상태 표시

## 🎨 특징

- **반응형 디자인**: 모바일과 데스크톱 모두 최적화
- **아름다운 UI**: 그라데이션 배경과 글라스모피즘 효과
- **카드 애니메이션**: 역방향 카드는 180도 회전되어 표시
- **로딩 애니메이션**: 스피너와 타이핑 효과
- **사용자 친화적**: 직관적인 인터페이스와 명확한 피드백

## ⚠️ 주의사항

- Gemini API 키가 필요합니다
- 인터넷 연결이 필요합니다
- 카드 이미지 파일들이 모두 있어야 정상 동작합니다