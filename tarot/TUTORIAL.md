# 🔮 타로 챗봇 웹 애플리케이션 개발 튜토리얼

Flask와 AI를 사용한 타로 챗봇 웹 애플리케이션을 단계별로 구현해보겠습니다.

## 📋 목차
1. [프로젝트 개요](#1-프로젝트-개요)
2. [개발 환경 설정](#2-개발-환경-설정)
3. [백엔드 개발](#3-백엔드-개발)
4. [프론트엔드 개발](#4-프론트엔드-개발)
5. [스타일링](#5-스타일링)
6. [테스트 및 배포](#6-테스트-및-배포)

---

## 1. 프로젝트 개요

### 🎯 학습 목표
- Flask 웹 프레임워크 사용법
- REST API 설계 및 구현
- Google Gemini AI API 활용
- HTML/CSS/JavaScript 웹 개발
- JSON 데이터 처리
- 비동기 JavaScript (async/await) 사용

### 🌟 주요 기능
- **AI 타로 리딩**: Google Gemini API를 사용한 타로 카드 해석
- **실시간 채팅 인터페이스**: 사용자 친화적인 채팅 UI
- **카드 시각화**: 정방향/역방향 타로 카드 표시
- **반응형 디자인**: 모바일/데스크톱 지원

### 🔧 기술 스택
- **백엔드**: Python, Flask
- **AI**: Google Gemini API
- **프론트엔드**: HTML5, CSS3, JavaScript
- **데이터**: JSON, YAML

---

## 2. 개발 환경 설정

### 2.1 필요한 소프트웨어 설치

```bash
# Python 3.8 이상 확인
python --version

# 필요한 패키지 설치
pip install Flask PyYAML google-generativeai
```

### 2.2 프로젝트 폴더 구조 만들기

```
tarot-chatbot/
├── app.py                 # Flask 메인 애플리케이션
├── config.yaml           # 설정 파일
├── tarot_cards.json      # 타로 카드 데이터
├── requirements.txt      # Python 패키지 의존성
├── templates/
│   └── index.html       # 메인 웹 페이지
├── static/
│   ├── style.css        # 스타일시트
│   └── script.js        # 클라이언트 JavaScript
└── card_image/          # 타로 카드 이미지들
```

### 2.3 Google Gemini API 키 발급

1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. 새 API 키 생성
3. `config.yaml`에 API 키 설정

---

## 3. 백엔드 개발

### 3.1 Flask 애플리케이션 기본 구조

**단계 1: app.py 파일 생성**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import random
import yaml
import google.generativeai as genai
from typing import List, Dict, Any

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# 기본 라우트 설정
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
```

**학습 포인트:**
- Flask 애플리케이션 인스턴스 생성
- 라우트 데코레이터 사용법
- 템플릿 렌더링

### 3.2 타로 챗봇 클래스 구현

**단계 2: TarotChatbotAPI 클래스 추가**

```python
class TarotChatbotAPI:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self.load_config(config_path)
        self.tarot_cards = self.load_tarot_cards()

        # Gemini AI 설정
        genai.configure(api_key=self.config['gemini']['api_key'])
        self.model = genai.GenerativeModel(self.config['gemini']['model'])

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """YAML 설정 파일 로드"""
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def load_tarot_cards(self) -> Dict[str, Any]:
        """JSON 타로 카드 데이터 로드"""
        cards_file = self.config['tarot']['cards_file']
        with open(cards_file, 'r', encoding='utf-8') as file:
            return json.load(file)
```

**학습 포인트:**
- 클래스 기반 설계
- 파일 I/O 처리 (YAML, JSON)
- AI API 초기화

### 3.3 카드 뽑기 로직 구현

**단계 3: 랜덤 카드 선택 메서드**

```python
def draw_cards(self, num_cards: int = 3) -> List[Dict[str, Any]]:
    """랜덤으로 타로 카드 뽑기"""
    max_cards = self.config['tarot']['max_cards_per_reading']
    num_cards = min(num_cards, max_cards)

    major_arcana = self.tarot_cards['major_arcana']
    drawn_cards = random.sample(major_arcana, num_cards)

    # 각 카드에 대해 정방향/역방향 결정
    for card in drawn_cards:
        card['is_reversed'] = random.choice([True, False])

    return drawn_cards
```

**학습 포인트:**
- `random.sample()` 사용법
- 리스트 조작
- 딕셔너리 수정

### 3.4 AI 프롬프트 생성

**단계 4: 타로 리딩 프롬프트 생성**

```python
def create_reading_prompt(self, user_question: str, drawn_cards: List[Dict[str, Any]]) -> str:
    """타로 리딩을 위한 프롬프트 생성"""
    cards_info = "\n".join([self.format_card_info(card) for card in drawn_cards])

    prompt = f"""
당신은 전문적이고 통찰력 있는 타로 카드 리더입니다.
질문: {user_question}
뽑힌 카드들: {cards_info}

다음 구조로 답변해주세요:
1. **전체적인 메시지**: 카드들이 전달하는 핵심 메시지
2. **각 카드 해석**: 각 카드가 질문에 어떤 의미를 주는지
3. **종합적인 조언**: 실용적인 조언 제공
4. **주의사항**: 앞으로 주의해야 할 점들
"""
    return prompt
```

**학습 포인트:**
- 문자열 포맷팅
- AI 프롬프트 엔지니어링
- 리스트 컴프리헨션

### 3.5 REST API 엔드포인트

**단계 5: API 엔드포인트 구현**

```python
@app.route('/api/tarot', methods=['POST'])
def get_tarot_reading():
    try:
        data = request.get_json()
        question = data.get('question', '')
        num_cards = data.get('num_cards', 3)

        if not question.strip():
            return jsonify({
                'success': False,
                'error': '질문을 입력해주세요.'
            })

        result = tarot_bot.get_tarot_reading(question, num_cards)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'서버 오류가 발생했습니다: {str(e)}'
        })
```

**학습 포인트:**
- REST API 설계
- JSON 요청/응답 처리
- 오류 처리 (try-except)

---

## 4. 프론트엔드 개발

### 4.1 HTML 구조 설계

**단계 6: index.html 템플릿 생성**

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔮 타로 챗봇</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>🔮 타로 챗봇</h1>
            <div class="connection-status connected">✅ 준비됨</div>
        </header>

        <div class="main-content">
            <!-- 왼쪽: 타로 카드 표시 -->
            <div class="cards-panel">
                <h2>🎴 뽑힌 카드들</h2>
                <div class="cards-container" id="cardsContainer">
                    <div class="no-cards">
                        <p>아직 카드가 뽑히지 않았습니다.</p>
                    </div>
                </div>
            </div>

            <!-- 오른쪽: 채팅 인터페이스 -->
            <div class="chat-panel">
                <div class="chat-messages" id="chatMessages"></div>
                <div class="chat-input-container">
                    <select id="numCards">
                        <option value="1">1장</option>
                        <option value="3" selected>3장</option>
                    </select>
                    <input type="text" id="messageInput" placeholder="질문을 입력해주세요...">
                    <button id="sendButton">전송</button>
                </div>
            </div>
        </div>
    </div>
    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
```

**학습 포인트:**
- 시맨틱 HTML 구조
- Flask 템플릿 문법 (`url_for`)
- 반응형 레이아웃 설계

### 4.2 JavaScript 클래스 구현

**단계 7: script.js 클라이언트 로직**

```javascript
class TarotChatApp {
    constructor() {
        this.isWaitingForResponse = false;
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.cardsContainer = document.getElementById('cardsContainer');
        this.numCardsSelect = document.getElementById('numCards');
    }

    bindEvents() {
        this.sendButton.addEventListener('click', () => this.sendMessage());

        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }
}
```

**학습 포인트:**
- ES6 클래스 문법
- DOM 조작
- 이벤트 리스너 등록

### 4.3 비동기 API 호출

**단계 8: fetch API를 사용한 서버 통신**

```javascript
async sendMessage() {
    const message = this.messageInput.value.trim();
    if (!message || this.isWaitingForResponse) return;

    const numCards = parseInt(this.numCardsSelect.value);

    // UI 업데이트
    this.addUserMessage(message);
    this.messageInput.value = '';
    this.isWaitingForResponse = true;
    this.addThinkingMessage('🔮 카드를 뽑고 있습니다...');

    try {
        const response = await fetch('/api/tarot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: message,
                num_cards: numCards
            })
        });

        const data = await response.json();

        this.removeThinkingMessage();

        if (data.success) {
            this.addBotMessage(data.reading);
            if (data.cards) {
                this.displayCards(data.cards);
            }
        } else {
            this.addBotMessage(`❌ ${data.error}`);
        }

    } catch (error) {
        this.removeThinkingMessage();
        this.addBotMessage(`❌ 연결 오류: ${error.message}`);
    }

    this.isWaitingForResponse = false;
}
```

**학습 포인트:**
- `async/await` 비동기 처리
- `fetch()` API 사용법
- JSON 데이터 송수신
- 오류 처리

### 4.4 동적 UI 업데이트

**단계 9: 채팅 메시지 및 카드 표시**

```javascript
addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.textContent = message;
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
}

displayCards(cards) {
    this.cardsContainer.innerHTML = '';

    cards.forEach((card, index) => {
        const cardDiv = document.createElement('div');
        cardDiv.className = `card-item ${card.is_reversed ? 'reversed' : ''}`;

        cardDiv.innerHTML = `
            <img src="/card_image/${card.local_image.split('/')[1]}"
                 alt="${card.name}" class="card-image">
            <div class="card-name">${card.name_korean}</div>
            <div class="card-orientation">
                ${card.is_reversed ? '역방향' : '정방향'}
            </div>
        `;

        this.cardsContainer.appendChild(cardDiv);

        // 애니메이션 효과
        setTimeout(() => {
            cardDiv.style.opacity = '1';
            cardDiv.style.transform = 'translateY(0)';
        }, 100 * index);
    });
}
```

**학습 포인트:**
- DOM 요소 동적 생성
- CSS 클래스 조작
- 애니메이션 타이밍 제어

---

## 5. 스타일링

### 5.1 CSS 기본 레이아웃

**단계 10: style.css 반응형 디자인**

```css
/* 전체 레이아웃 */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

.main-content {
    flex: 1;
    display: flex;
    gap: 20px;
}

/* 카드 패널 */
.cards-panel {
    flex: 1;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    overflow: hidden;
}

/* 채팅 패널 */
.chat-panel {
    flex: 1;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    display: flex;
    flex-direction: column;
}
```

**학습 포인트:**
- Flexbox 레이아웃
- CSS Grid (선택적)
- 반응형 디자인 원칙

### 5.2 카드 애니메이션 효과

**단계 11: 카드 회전 및 애니메이션**

```css
.card-item {
    background: white;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    transition: transform 0.3s ease;
}

.card-item:hover {
    transform: translateY(-5px);
}

/* 역방향 카드 */
.card-item.reversed {
    transform: rotate(180deg);
}

.card-item.reversed:hover {
    transform: rotate(180deg) translateY(5px);
}

/* 로딩 애니메이션 */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid #e2e8f0;
    border-top: 2px solid #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
```

**학습 포인트:**
- CSS 애니메이션
- Transform 속성
- Keyframes 정의

---

## 6. 테스트 및 배포

### 6.1 로컬 테스트

**단계 12: 애플리케이션 실행 및 테스트**

```bash
# 서버 실행
python app.py

# 브라우저에서 접속
# http://127.0.0.1:5000
```

**테스트 체크리스트:**
- [ ] 웹 페이지가 정상적으로 로드되는가?
- [ ] 메시지 전송이 작동하는가?
- [ ] 카드가 올바르게 표시되는가?
- [ ] 역방향 카드가 뒤집어져 보이는가?
- [ ] 반응형 디자인이 작동하는가?

### 6.2 코드 개선 및 최적화

**추가 구현 과제:**
1. **오류 처리 강화**: 네트워크 오류, API 한도 초과 등
2. **사용자 경험 개선**: 로딩 상태 표시, 입력 검증
3. **접근성 향상**: 스크린 리더 지원, 키보드 네비게이션
4. **성능 최적화**: 이미지 최적화, 캐싱 전략

---

## 📚 추가 학습 자료

### 관련 기술 문서
- [Flask 공식 문서](https://flask.palletsprojects.com/)
- [Google Gemini API 가이드](https://ai.google.dev/docs)
- [MDN Web Docs - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

### 프로젝트 확장 아이디어
1. **데이터베이스 연동**: 사용자 질문 및 결과 저장
2. **사용자 인증**: 개인별 타로 히스토리 관리
3. **실시간 채팅**: WebSocket을 사용한 실시간 통신
4. **모바일 앱**: React Native 또는 Flutter로 앱 개발

### 🔧 문제 해결 가이드

**자주 발생하는 문제들:**

1. **API 키 오류**
   ```
   오류: Invalid API key
   해결: config.yaml에서 올바른 Gemini API 키 확인
   ```

2. **CORS 오류**
   ```python
   # Flask-CORS 추가 설치 및 설정
   from flask_cors import CORS
   CORS(app)
   ```

3. **이미지 로딩 실패**
   ```javascript
   // 이미지 오류 처리 개선
   onerror="this.src='data:image/svg+xml;base64,...'"
   ```

---

## 🎯 학습 성과 평가

### 기본 수준 (필수)
- [ ] Flask 웹 서버 실행
- [ ] 기본 HTML/CSS 구현
- [ ] API 호출 성공
- [ ] 타로 카드 표시

### 중급 수준 (권장)
- [ ] 반응형 디자인 구현
- [ ] 오류 처리 개선
- [ ] 애니메이션 효과 추가
- [ ] 코드 모듈화

### 고급 수준 (도전)
- [ ] 데이터베이스 연동
- [ ] 사용자 인증 구현
- [ ] 성능 최적화
- [ ] 테스트 코드 작성

---

**축하합니다! 🎉**

이제 여러분만의 AI 기반 타로 챗봇 웹 애플리케이션을 완성했습니다. 이 프로젝트를 통해 풀스택 웹 개발의 전체적인 흐름을 경험하고, 현대적인 웹 기술들을 실습할 수 있었습니다.

다음 단계로는 이 프로젝트를 확장하거나, 다른 AI API들을 활용한 새로운 프로젝트에 도전해보세요!