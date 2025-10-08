#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import random
import yaml
import google.generativeai as genai
from typing import List, Dict, Any
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

class TarotChatbotAPI:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self.load_config(config_path)
        self.tarot_cards = self.load_tarot_cards()

        genai.configure(api_key=self.config['gemini']['api_key'])
        self.model = genai.GenerativeModel(self.config['gemini']['model'])

    def load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def load_tarot_cards(self) -> Dict[str, Any]:
        cards_file = self.config['tarot']['cards_file']
        with open(cards_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def draw_cards(self, num_cards: int = 3) -> List[Dict[str, Any]]:
        max_cards = self.config['tarot']['max_cards_per_reading']
        num_cards = min(num_cards, max_cards)

        major_arcana = self.tarot_cards['major_arcana']
        drawn_cards = random.sample(major_arcana, num_cards)

        for card in drawn_cards:
            card['is_reversed'] = random.choice([True, False])

        return drawn_cards

    def format_card_info(self, card: Dict[str, Any]) -> str:
        orientation = "역방향" if card['is_reversed'] else "정방향"
        meaning = card['reversed_meaning'] if card['is_reversed'] else card['upright_meaning']

        card_info = f"""
🃏 **{card['name']} ({card['name_korean']})** - {orientation}
📝 설명: {card['description']}
🔍 의미: {meaning}
"""
        return card_info

    def create_reading_prompt(self, user_question: str, drawn_cards: List[Dict[str, Any]]) -> str:
        cards_info = "\n".join([self.format_card_info(card) for card in drawn_cards])

        prompt = f"""
당신은 전문적이고 통찰력 있는 타로 카드 리더입니다. 다음 질문에 대해 뽑힌 카드들을 바탕으로 심도 있는 타로 리딩을 제공해주세요.

**질문**: {user_question}

**뽑힌 카드들**:
{cards_info}

다음 구조로 답변해주세요:

1. **전체적인 메시지**: 카드들이 전달하는 핵심 메시지
2. **각 카드 해석**: 각 카드가 질문에 어떤 의미를 주는지 구체적 설명
3. **종합적인 조언**: 카드들을 종합하여 실용적인 조언 제공
4. **주의사항**: 앞으로 주의해야 할 점들

답변은 한국어로, 따뜻하고 격려적인 톤으로 작성해주세요. 타로는 미래를 확정하는 것이 아닌 현재 상황을 통찰하고 가능성을 제시하는 도구임을 강조해주세요.
"""
        return prompt

    def get_tarot_reading(self, user_question: str, num_cards: int = 3) -> Dict[str, Any]:
        try:
            drawn_cards = self.draw_cards(num_cards)
            prompt = self.create_reading_prompt(user_question, drawn_cards)

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.config['chat']['temperature']
                )
            )

            return {
                'success': True,
                'cards': drawn_cards,
                'reading': response.text,
                'question': user_question
            }

        except Exception as e:
            return {
                'success': False,
                'error': f"타로 리딩 중 오류가 발생했습니다: {str(e)}"
            }

tarot_bot = TarotChatbotAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/card_image/<filename>')
def serve_card_image(filename):
    return send_from_directory('card_image', filename)

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

        if question.lower() in ['도움말', 'help']:
            return jsonify({
                'success': True,
                'is_help': True,
                'message': """
🔮 **타로 챗봇 사용법**

**명령어:**
- 일반적인 질문을 하면 선택한 수의 카드로 타로를 봐드립니다
- 카드 수를 1-3장 중에서 선택할 수 있습니다

**질문 예시:**
- "오늘 하루 어떻게 보낼까요?"
- "새로운 일을 시작하는 것에 대해 어떻게 생각하세요?"
- "연애운은 어떤가요?"
- "직장에서의 문제를 어떻게 해결해야 할까요?"

편안하게 질문해보세요! 🌟
                """,
                'cards': []
            })

        print(f"질문 받음: {question}, 카드 수: {num_cards}")
        result = tarot_bot.get_tarot_reading(question, num_cards)
        print(f"결과: {result['success']}")

        return jsonify(result)

    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({
            'success': False,
            'error': f'서버 오류가 발생했습니다: {str(e)}'
        })

if __name__ == '__main__':
    print("🔮 타로 챗봇 서버를 시작합니다...")
    app.run(debug=True, host='127.0.0.1', port=5000)