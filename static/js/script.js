const messageInput = document.getElementById("message");

if (messageInput) {

    messageInput.addEventListener("keypress", function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    });

}


async function sendMessage() {

    const input = document.getElementById("message");
    const chatBox = document.getElementById("chatBox");

    if (!input || !chatBox) {
        return;
    }

    const message = input.value.trim();

    if (message === "") {
        return;
    }


    // User message
    const userMessage = document.createElement("div");

    userMessage.className = "message user";

    userMessage.textContent = message;

    chatBox.appendChild(userMessage);


    input.value = "";


    // Loading message
    const loading = document.createElement("div");

    loading.className = "message bot";

    loading.textContent = "Thinking...";

    chatBox.appendChild(loading);


    chatBox.scrollTop = chatBox.scrollHeight;


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        loading.textContent = data.response;


    } catch (error) {

        loading.textContent =
            "Sorry, I couldn't connect to the AI assistant.";

    }


    chatBox.scrollTop = chatBox.scrollHeight;

}