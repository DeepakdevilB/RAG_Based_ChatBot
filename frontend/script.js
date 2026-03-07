async function sendMessage() {

    const inputField = document.getElementById("message-input");
    const message = inputField.value.trim();

    if (!message) return;

    const chatBox = document.getElementById("chat-box");

    // User bubble
    chatBox.innerHTML += `
    <div class="message user">
        <div class="bubble user-bubble">${message}</div>
    </div>
    `;

    inputField.value = "";

    // Bot typing animation
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

        // Remove typing bubble
        document.getElementById(typingId).remove();

        // Bot response
        chatBox.innerHTML += `
        <div class="message bot">
            <div class="bubble bot-bubble">
                ${data.answer}

                <div class="latency">
                    🧠 Embedding: ${data.latency.embedding}s<br>
                    🔎 Retrieval: ${data.latency.retrieval}s<br>
                    🤖 LLM: ${data.latency.llm}s<br>
                    ⏱ Total: ${data.latency.total}s
                </div>
            </div>
        </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

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

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}