var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const API_URL = 'http://127.0.0.1:5000/api/chat';
chatForm.addEventListener('submit', (e) => __awaiter(this, void 0, void 0, function* () {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message)
        return;
    appendMessage(message, 'user');
    userInput.value = '';
    try {
        const response = yield fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = yield response.json();
        if (data.error) {
            appendMessage(`오류: ${data.error}`, 'bot');
        }
        else {
            appendMessage(data.reply, 'bot');
        }
    }
    catch (error) {
        console.error('Fetch 오류:', error);
        appendMessage('서버와 통신 중 오류가 발생했습니다.', 'bot');
    }
}));
function appendMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    messageElement.textContent = text;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // 새 메시지로 스크롤
}
