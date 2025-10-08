const chatBox = document.getElementById('chat-box') as HTMLDivElement;
const chatForm = document.getElementById('chat-form') as HTMLFormElement;
const userInput = document.getElementById('user-input') as HTMLInputElement;

const API_URL = 'http://127.0.0.1:5000/api/chat';

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, 'user');
    userInput.value = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            appendMessage(`오류: ${data.error}`, 'bot');
        } else {
            appendMessage(data.reply, 'bot');
        }

    } catch (error) {
        console.error('Fetch 오류:', error);
        appendMessage('서버와 통신 중 오류가 발생했습니다.', 'bot');
    }
});

function appendMessage(text: string, sender: 'user' | 'bot') {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    messageElement.textContent = text;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // 새 메시지로 스크롤
}
