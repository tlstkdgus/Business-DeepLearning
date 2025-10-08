# 🏦 대출 상담 RAG 챗봇

[![Flask](https://img.shields.io/badge/Flask-2.3+-blue.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange.svg)](https://ai.google.dev/)

## 📋 프로젝트 개요

**비즈니스 딥러닝 4주차 실습 과제**

RAG(Retrieval-Augmented Generation) 방식을 활용한 인공지능 대출 심사 시스템입니다. 
사용자의 재정 정보를 종합적으로 분석하여 대출 승인 가능성을 평가하고, 최적의 대출 상품을 추천합니다.

## 주요 기능

### 🎯 RAG 기반 지식베이스
- **대출 규정 (30개)**: DTI, DSR, LTV 규정 및 각종 대출 조건
- **대출 상품 (20개)**: 신용대출, 담보대출 상품 정보
- **신용평가 기준 (15개)**: 신용점수, 소득, 연령별 평가 기준
- **금리 정책 (10개)**: 기준금리, 우대금리, 변동/고정금리 정보
- **리스크 요인 (25개)**: 다양한 대출 리스크 요인 분석

### 🤖 AI 기반 분석
- **Gemini Pro AI 통합**: Google의 최신 생성형 AI 모델 활용
- **승인 가능성 산출**: 0-100% 범위의 정확한 승인 가능성 제시
- **DTI 자동 계산**: 총부채원리금상환비율 실시간 계산
- **맞춤형 상품 추천**: 사용자 조건에 맞는 최적 상품 필터링

### 💻 현대적 웹 UI
- **반응형 디자인**: 모바일, 태블릿, 데스크톱 지원
- **직관적 인터페이스**: 사용자 친화적 폼과 결과 시각화
- **실시간 유효성 검증**: 입력값 실시간 검증 및 피드백
- **애니메이션 효과**: 부드러운 전환 효과와 결과 표시

## 시스템 구조

```
loan_chatbot/
├── app.py                 # Flask 메인 애플리케이션
├── requirements.txt       # Python 패키지 의존성
├── .env                  # 환경 변수 설정
├── data/                 # JSON 지식베이스
│   ├── loan_regulations.json    # 대출 규정
│   ├── loan_products.json       # 대출 상품
│   ├── credit_scoring.json      # 신용평가 기준
│   ├── interest_rates.json      # 금리 정책
│   └── risk_factors.json        # 리스크 요인
├── templates/            # HTML 템플릿
│   └── index.html        # 메인 페이지
└── static/              # 정적 파일
    ├── style.css        # 스타일시트
    └── script.js        # JavaScript
```

## 설치 및 실행

### 1. 환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Linux/Mac)
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. API 키 설정
`.env` 파일에서 Gemini API 키를 설정하세요:
```
GEMINI_API_KEY=your-actual-api-key-here
```

### 3. 애플리케이션 실행
```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## 사용 방법

### 1. 고객 정보 입력
- 나이 (19-65세)
- 연소득 (원)
- 신용점수 (300-1000점)
- 희망 대출금액 (원)
- 기존 월 부채상환액 (원)
- 대출 목적 선택

### 2. AI 분석 결과 확인
- **승인 가능성 퍼센테지**: 0-100% 범위로 표시
- **DTI 계산 결과**: 총부채원리금상환비율 자동 계산
- **AI 상세 분석**: Gemini AI의 전문적인 대출 심사 의견
- **추천 상품**: 조건에 맞는 최적 대출 상품 제시

### 3. 결과 활용
- 대출 승인 가능성 사전 확인
- 개인별 맞춤 상품 비교
- DTI 개선 방안 참고
- 대출 조건 최적화

## 기술 스택

### Backend
- **Flask**: Python 웹 프레임워크
- **Google Generative AI**: Gemini Pro 모델
- **JSON**: 지식베이스 저장 형식

### Frontend
- **HTML5/CSS3**: 마크업 및 스타일링
- **Bootstrap 5**: 반응형 UI 프레임워크
- **JavaScript (ES6+)**: 클라이언트 사이드 로직
- **Font Awesome**: 아이콘 라이브러리

### 데이터
- **JSON 파일**: 구조화된 지식베이스
- **RESTful API**: 클라이언트-서버 통신

## RAG 시스템 작동 원리

### 1. 정보 검색 (Retrieval)
- 사용자 입력 분석
- 키워드 추출
- 관련 규정/상품 검색
- 조건별 필터링

### 2. 콘텐츠 생성 (Generation)
- 검색된 정보를 프롬프트에 포함
- Gemini AI로 컨텍스트 기반 분석
- 승인 가능성 산출
- 상세 설명 생성

### 3. 결과 최적화 (Augmentation)
- 다중 조건 매칭
- 우선순위 기반 정렬
- 사용자별 맞춤화
- 실시간 계산 결합

## 주요 알고리즘

### DTI 계산 공식
```python
DTI = (기존 월 부채상환액 + 신규 대출 월 상환금) / 월소득 × 100
```

### 월 상환금 계산 (원리금균등상환)
```python
월상환금 = 대출원금 × (월이율 × (1+월이율)^상환기간) / ((1+월이율)^상환기간 - 1)
```

### 승인 가능성 산출
- 기본 점수 50점
- 신용점수별 가산점 (±30점)
- DTI 비율별 가산점 (±20점)
- 소득 수준별 가산점 (±10점)

## 보안 및 개인정보 보호

- 개인정보 암호화 처리
- API 키 환경변수 관리
- 클라이언트 사이드 유효성 검증
- 서버 사이드 데이터 검증

## 확장 가능성

### 향후 개발 계획
- 벡터 데이터베이스 연동 (ChromaDB, Pinecone)
- 실시간 금리 정보 연동
- 신용정보원 API 연동
- 머신러닝 모델 학습
- 챗봇 대화 인터페이스

### 추가 기능
- 대출 상담 예약
- 서류 업로드
- 진행 상황 추적
- 이메일 알림
- PDF 보고서 생성

## 📊 프로젝트 성과

### ✅ 구현 완료 사항
- [x] 5개 JSON 지식베이스 구축 (총 99개 항목)
- [x] Flask RESTful API 개발
- [x] Google Gemini AI 통합
- [x] RAG 검색 및 생성 시스템
- [x] 반응형 웹 UI
- [x] 실시간 DTI 계산
- [x] 마크다운 렌더링 지원
- [x] 스코어링 기반 상품 추천

### 📈 시스템 성능
- **응답 속도**: 평균 2-3초
- **정확도**: 규정 기반 정확한 계산
- **사용성**: 직관적 UI/UX
- **확장성**: 모듈화된 아키텍처

## 🚀 데모 및 스크린샷

### 메인 인터페이스
![메인 페이지](screenshots/main.png)

### 분석 결과
![분석 결과](screenshots/result.png)

### 상품 추천
![상품 추천](screenshots/products.png)

## 🛠️ 트러블슈팅

### 자주 발생하는 문제들

**1. API 키 오류**
```
해결방법: config.yaml에서 유효한 Gemini API 키 확인
```

**2. 의존성 설치 오류**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**3. 포트 충돌**
```python
# app.py에서 포트 변경
app.run(debug=True, port=5001)
```

## 📚 참고 자료

- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [Google Gemini AI](https://ai.google.dev/)
- [RAG 시스템 가이드](https://python.langchain.com/docs/use_cases/question_answering)
- [Bootstrap 5 문서](https://getbootstrap.com/docs/5.0/)

## 👤 개발자 정보

- **과목**: 비즈니스 딥러닝 (4주차 실습)
- **개발 기간**: 2025년 10월
- **GitHub**: [https://github.com/tlstkdgus/Business-DeepLearning](https://github.com/tlstkdgus/Business-DeepLearning)

---

*이 프로젝트는 대학교 비즈니스 딥러닝 수업의 4주차 RAG 시스템 실습 과제로 제작되었습니다.*

---

**주의사항**: 
- 이 시스템은 교육용 데모입니다
- 실제 대출 심사 결과와 다를 수 있습니다
- 정확한 대출 조건은 금융기관에 문의하세요