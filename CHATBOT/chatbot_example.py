import google.generativeai as genai
import yaml

# config.yaml 파일에서 API 키를 로드합니다.
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

api_key = config.get('api_key')

if not api_key:
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("! config.yaml 파일에 API 키가 없습니다.")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    exit()

genai.configure(api_key=api_key)


# 사용할 모델을 설정합니다.
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# 채팅 세션을 시작합니다.
chat = model.start_chat(history=[])

print("Gemini 챗봇에 오신 것을 환영합니다! 'quit'를 입력하면 종료됩니다.")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break

    # 모델에 메시지를 보냅니다.
    response = chat.send_message(user_input)

    # 모델의 응답을 출력합니다.
    print(f"Gemini: {response.text}")
