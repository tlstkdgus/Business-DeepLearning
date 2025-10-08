
import yaml
import google.generativeai as genai
import markdown
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 개발 중 모든 출처에서 오는 요청을 허용합니다.
CORS(app) 

# --- 모델 설정 ---
try:
    # config.yaml 파일에서 API 키를 로드합니다.
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    api_key = config.get('api_key')

    if not api_key or api_key == 'YOUR_API_KEY':
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("! backend/config.yaml 파일에 API 키를 설정해야 합니다.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # 실제 운영 환경에서는 여기서 애플리케이션을 종료하거나,
        # 키가 없으면 특정 기능을 비활성화하는 로직이 필요합니다.
        # 지금은 경고만 출력하고 진행합니다。
        genai.configure(api_key="DUMMY_KEY_FOR_INITIALIZATION") # 임시 키로 초기화
    else:
        genai.configure(api_key=api_key)

    # 사용할 모델을 설정합니다。
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    # 채팅 세션을 시작합니다. 이 세션은 서버가 실행되는 동안 유지됩니다.
    chat = model.start_chat(history=[])

except FileNotFoundError:
    print("backend/config.yaml 파일을 찾을 수 없습니다.")
    chat = None
except Exception as e:
    print(f"모델 초기화 중 오류 발생: {e}")
    chat = None

# --- API 엔드포인트 ---
@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    if not chat:
        return jsonify({"error": "모델이 제대로 초기화되지 않았습니다. API 키와 설정을 확인하세요."}), 500

    data = request.get_json()
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "메시지가 없습니다."}), 400

    try:
        # 모델에 메시지를 보냅니다.
        response = chat.send_message(user_input)
        # 모델의 응답을 Markdown에서 HTML로 변환합니다.
        html_response = markdown.markdown(response.text)
        # HTML 응답을 JSON 형태로 반환합니다.
        return jsonify({"reply": html_response})
    except Exception as e:
        print(f"메시지 전송 중 오류 발생: {e}")
        return jsonify({"error": "메시지 처리 중 서버에서 오류가 발생했습니다."}), 500

if __name__ == '__main__':
    # host='0.0.0.0'으로 설정하여 외부에서도 접속 가능하게 합니다.
    app.run(host='0.0.0.0', port=5000, debug=True)
