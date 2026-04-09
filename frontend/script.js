let ttsEnabled = false;
const avatar = document.getElementById("avatar");

function formatLinks(text) {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return `<a href="${url}" target="_blank">${url}</a>`;
    });
}

/* ------------------------------
   SEND MESSAGE
--------------------------------*/

async function sendMessage() {
    // Stop any ongoing speech
    window.speechSynthesis.cancel();

    const inputField = document.getElementById("message-input");
    const message = inputField.value.trim();

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    // USER MESSAGE
    chatBox.innerHTML += `
    <div class="message user">
        <div class="bubble user-bubble">
            ${message}
        </div>
    </div>
    `;

    inputField.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    /* BOT TYPING INDICATOR */

    const typingId = "typing-" + Date.now();

    chatBox.innerHTML += `
    <div class="message bot" id="${typingId}">
        <div class="bubble bot-bubble typing">
            Bot is typing<span class="dots"></span>
        </div>
    </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        document.getElementById(typingId).remove();

        const botAnswer = data.answer;

        chatBox.innerHTML += `
        <div class="message bot">
            <div class="bubble bot-bubble">

                ${formatLinks(botAnswer)}

                <div class="latency">
                    🧠 Embedding: ${data.latency.embedding}s <br>
                    🔎 Retrieval: ${data.latency.retrieval}s <br>
                    🤖 LLM: ${data.latency.llm}s <br>
                    ⏱ Total: ${data.latency.total}s
                </div>

            </div>
        </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

        /* SPEAK ANSWER IF TTS ENABLED */

        speakText(botAnswer);

    }
    catch (error) {

        document.getElementById(typingId).remove();

        chatBox.innerHTML += `
        <div class="message bot">
            <div class="bubble bot-bubble error">
                Error connecting to server.
            </div>
        </div>
        `;
    }
}


/* ------------------------------
   ENTER KEY SUPPORT
--------------------------------*/

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}


/* ------------------------------
   TEXT TO SPEECH
--------------------------------*/

function toggleTTS() {

    const btn = document.getElementById("tts-btn");

    ttsEnabled = !ttsEnabled;

    if (ttsEnabled) {
        btn.classList.add("tts-active");
        btn.innerText = "🔊";
    }
    else {
        btn.classList.remove("tts-active");
        btn.innerText = "🔇";
    }
}

function speakText(text) {

    if (!ttsEnabled) return;

    // Stop any previous speech
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(" " + text);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;

    speech.onstart = () => {
        showStatus("🔊 Speaking...", "status-speaking");

        avatar.load("talking.json");
        avatar.classList.add("speaking");
    };

    speech.onend = () => {
        clearStatus();

        avatar.load("idle.json");
        avatar.classList.remove("speaking");
    };

    // Small delay fixes clipped first words
    setTimeout(() => {
        window.speechSynthesis.speak(speech);
    }, 120);
}


/* ------------------------------
   VOICE INPUT
--------------------------------*/

function startVoiceInput() {

    window.speechSynthesis.cancel();

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    const micButton = document.querySelector(".mic-btn");
    const inputField = document.getElementById("message-input");

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.start();

    micButton.classList.add("listening");

    showStatus("🎤 Listening...", "status-listening");

    recognition.onresult = (event) => {

        const transcript = event.results[0][0].transcript;

        inputField.value = transcript;

        micButton.classList.remove("listening");

        clearStatus();

        sendMessage();
    };

    recognition.onerror = () => {

        micButton.classList.remove("listening");

        clearStatus();
    };

    recognition.onend = () => {

        micButton.classList.remove("listening");

        clearStatus();
    };
}

function showStatus(message, className) {

    const status = document.getElementById("status-indicator");

    status.innerText = message;
    status.className = className;
}

function clearStatus() {

    const status = document.getElementById("status-indicator");

    status.innerText = "";
    status.className = "";
}