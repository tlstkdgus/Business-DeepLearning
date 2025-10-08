#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import yaml
import google.generativeai as genai
from typing import List, Dict, Any
import os
import sys
from pathlib import Path

# 윈도우 환경에서 UTF-8 출력 설정
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class TarotChatbot:
    def __init__(self, config_path: str = "config.yaml"):
        """타로 챗봇 초기화"""
        self.config = self.load_config(config_path)
        self.tarot_cards = self.load_tarot_cards()
        self.chat_history = []

        # Gemini API 설정
        genai.configure(api_key=self.config['gemini']['api_key'])
        self.model = genai.GenerativeModel(self.config['gemini']['model'])

        print("🔮 타로 챗봇이 준비되었습니다!")
        print("궁금한 것을 물어보시면 타로로 점을 봐드리겠습니다.\n")

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {config_path}")

    def load_tarot_cards(self) -> Dict[str, Any]:
        """타로 카드 정보 로드"""
        cards_file = self.config['tarot']['cards_file']
        try:
            with open(cards_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"타로 카드 파일을 찾을 수 없습니다: {cards_file}")

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

    def format_card_info(self, card: Dict[str, Any]) -> str:
        """카드 정보를 포맷팅"""
        orientation = "역방향" if card['is_reversed'] else "정방향"
        meaning = card['reversed_meaning'] if card['is_reversed'] else card['upright_meaning']

        card_info = f"""
🃏 **{card['name']} ({card['name_korean']})** - {orientation}
📝 설명: {card['description']}
🔍 의미: {meaning}
🖼️ 이미지: {card['local_image']}
"""
        return card_info

    def create_reading_prompt(self, user_question: str, drawn_cards: List[Dict[str, Any]]) -> str:
        """타로 리딩을 위한 프롬프트 생성"""
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

    def get_tarot_reading(self, user_question: str, num_cards: int = 3) -> str:
        """타로 리딩 수행"""
        try:
            # 카드 뽑기
            drawn_cards = self.draw_cards(num_cards)

            # 프롬프트 생성
            prompt = self.create_reading_prompt(user_question, drawn_cards)

            # Gemini API 호출
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.config['chat']['temperature']
                )
            )

            # 뽑힌 카드 정보 추가
            cards_summary = f"\n🎴 **뽑힌 카드들**:\n"
            for i, card in enumerate(drawn_cards, 1):
                orientation = "역방향" if card['is_reversed'] else "정방향"
                cards_summary += f"{i}. {card['name']} ({card['name_korean']}) - {orientation}\n"

            return cards_summary + "\n" + response.text

        except Exception as e:
            return f"죄송합니다. 타로 리딩 중 오류가 발생했습니다: {str(e)}"

    def add_to_history(self, user_input: str, bot_response: str):
        """채팅 히스토리에 추가"""
        self.chat_history.append({
            'user': user_input,
            'bot': bot_response
        })

        # 최대 히스토리 개수 제한
        max_history = self.config['chat']['max_history']
        if len(self.chat_history) > max_history:
            self.chat_history = self.chat_history[-max_history:]

    def show_help(self):
        """도움말 표시"""
        help_text = """
🔮 **타로 챗봇 사용법**

**명령어:**
- 일반적인 질문을 하면 3장의 카드로 타로를 봐드립니다
- `1카드`, `2카드`, `3카드`: 지정된 수의 카드로 타로 점 보기
- `도움말` 또는 `help`: 이 도움말 보기
- `종료` 또는 `quit`: 챗봇 종료

**질문 예시:**
- "오늘 하루 어떻게 보낼까요?"
- "새로운 일을 시작하는 것에 대해 어떻게 생각하세요?"
- "연애운은 어떤가요?"
- "직장에서의 문제를 어떻게 해결해야 할까요?"

편안하게 질문해보세요! 🌟
"""
        print(help_text)

    def run(self):
        """챗봇 실행"""
        self.show_help()

        while True:
            try:
                user_input = input("\n💭 질문을 입력해주세요 (도움말: help, 종료: quit): ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ['quit', '종료', 'exit']:
                    print("\n🌙 타로 챗봇을 종료합니다. 좋은 하루 되세요!")
                    break

                if user_input.lower() in ['help', '도움말']:
                    self.show_help()
                    continue

                # 카드 수 지정 확인
                num_cards = 3  # 기본값
                if user_input.endswith('카드'):
                    try:
                        num_str = user_input.replace('카드', '').strip()
                        if num_str.isdigit():
                            num_cards = int(num_str)
                            user_input = f"{num_cards}장의 카드로 타로를 봐주세요."
                    except:
                        pass

                print(f"\n🔮 {num_cards}장의 카드를 뽑고 있습니다...")
                print("⏳ 타로 리딩 중...")

                # 타로 리딩 수행
                reading = self.get_tarot_reading(user_input, num_cards)

                print(f"\n{reading}")

                # 히스토리에 추가
                self.add_to_history(user_input, reading)

            except KeyboardInterrupt:
                print("\n\n🌙 타로 챗봇을 종료합니다. 좋은 하루 되세요!")
                break
            except Exception as e:
                print(f"\n❌ 오류가 발생했습니다: {str(e)}")
                print("다시 시도해주세요.")

def main():
    """메인 함수"""
    try:
        chatbot = TarotChatbot()
        chatbot.run()
    except FileNotFoundError as e:
        print(f"❌ 파일 오류: {e}")
        print("config.yaml과 tarot_cards.json 파일이 있는지 확인해주세요.")
    except Exception as e:
        print(f"❌ 챗봇 초기화 중 오류 발생: {e}")

if __name__ == "__main__":
    main()