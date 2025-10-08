# Business Deep Learning Projects

대학교 비즈니스 딥러닝 수업의 실습 프로젝트들입니다.

## 📂 프로젝트 구조

### 🎯 LOAN - 대출 상담 RAG 챗봇 (4주차)
대출 심사를 위한 RAG(Retrieval-Augmented Generation) 시스템입니다.

**주요 기능:**
- 🏦 대출 상품 추천 및 심사
- 🤖 Google Gemini AI 기반 상담
- 📊 신용 점수 기반 평가
- 🔍 RAG 기반 지식 검색

**기술 스택:**
- Backend: Flask, Python
- AI: Google Gemini API
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Data: JSON 기반 지식베이스

**실행 방법:**
```bash
cd LOAN/loan_chatbot
pip install -r requirements.txt
python app.py
```

### 🔮 TAROT - 타로 카드 챗봇 (2주차)
AI 기반 타로 카드 점술 서비스입니다.

**주요 기능:**
- 🎴 22장 메이저 아르카나 카드
- 🔮 AI 기반 해석 및 조언
- 🖼️ 카드 이미지 표시
- 💫 개인화된 운세 제공

**기술 스택:**
- Backend: Flask, Python
- AI: Google Gemini API
- Frontend: HTML, CSS, JavaScript
- Assets: 타로 카드 이미지

**실행 방법:**
```bash
cd tarot
pip install -r requirements.txt
python app.py
```

### 💬 CHATBOT - 일반 챗봇 (1주차)
기본적인 AI 챗봇 구현입니다.

**주요 기능:**
- 🗨️ 자연어 대화
- 🎯 다양한 주제 상담
- 📱 반응형 웹 인터페이스

**기술 스택:**
- Backend: Flask, Python
- Frontend: HTML, CSS, JavaScript, TypeScript
- AI: Google Gemini API

**실행 방법:**
```bash
cd CHATBOT/backend
pip install -r requirements.txt
python app.py
```

## 🚀 공통 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/tlstkdgus/Business-DeepLearning.git
cd Business-DeepLearning
```

### 2. Python 가상 환경 설정
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치
각 프로젝트 디렉토리에서:
```bash
pip install -r requirements.txt
```

### 4. API 키 설정
각 프로젝트의 `config.yaml` 파일에 Google Gemini API 키를 설정해주세요:
```yaml
gemini:
  api_key: "YOUR_API_KEY_HERE"
```

## 📋 요구사항

- Python 3.8+
- Flask 2.3+
- Google Gemini API 키
- 모던 웹 브라우저

## 🔧 개발 환경

- **IDE**: Visual Studio Code
- **언어**: Python, JavaScript, TypeScript, HTML, CSS
- **프레임워크**: Flask, Bootstrap
- **AI**: Google Gemini API
- **버전 관리**: Git

## 📚 학습 목표

각 주차별 실습을 통해 다음을 학습합니다:

1. **기본 챗봇 구현** - Flask 기반 웹 애플리케이션
2. **특화 서비스 개발** - 타로 카드 도메인 특화 AI
3. **RAG 시스템 구축** - 검색 증강 생성을 통한 고도화된 AI 서비스

## 🤝 기여

이 프로젝트는 교육용 목적으로 제작되었습니다. 개선사항이나 버그 발견 시 이슈를 등록해주세요.

## 📄 라이선스

MIT License

## 👤 작성자

- **이름**: [Your Name]
- **학번**: [Your Student ID]
- **과목**: 비즈니스 딥러닝
- **GitHub**: [tlstkdgus](https://github.com/tlstkdgus)

---

*이 프로젝트는 대학교 비즈니스 딥러닝 수업의 일환으로 제작되었습니다.*