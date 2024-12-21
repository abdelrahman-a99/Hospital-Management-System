// when the user scroll down, the header will be change the bg color
window.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    if (window.scrollY > 0) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Copyright Date
let time = document.querySelector(".time")
time.innerHTML = new Date().getFullYear() // 2024

// Profile Icon Click Toggle
document.querySelector('.profile i').addEventListener('click', function (e) {
    e.stopPropagation(); // Prevent event from bubbling to document
    document.getElementById('subMenu').classList.toggle('open');
});

// ==============================================================================

// close the submenu anywhere
document.addEventListener('click', function (e) {
    const subMenu = document.getElementById('subMenu');
    const profileIcon = document.querySelector('.profile i');

    // If the click is outside the profile icon and submenu, close the submenu
    if (!subMenu.contains(e.target) && e.target !== profileIcon) {
        subMenu.classList.remove('open');
    }
});

//Chatbot 
document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("toggleChat");
    const chatWindow = document.getElementById("chatWindow");
    const chatHistory = document.getElementById("chatHistory");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const history = [];

    toggleButton.addEventListener("click", () => {
        if (chatWindow.style.display === "none" || chatWindow.style.display === "") {
            chatWindow.style.display = "block"; // Show the window
        } else {
            chatWindow.style.display = "none"; // Hide the window
        }
    });

    function appendMessage(author, content) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${author}-message`;
        const messageContent = document.createElement("div");
        messageContent.className = "content";
        messageContent.textContent = content;
        messageDiv.appendChild(messageContent);
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight; 
    }

    async function sendMessage() {
        const prompt = userInput.value.trim();
        if (!prompt) return;

        // Add user message to chat
        history.push({ author: "user", content: prompt });
        appendMessage("user", prompt);

        // Clear input
        userInput.value = "";

        // Send message to backend (replace with actual API call)
        try {
            const response = await fetch("/api/get_response", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ history, prompt })
            });
            const data = await response.json();
            const assistantResponse = data.response;
            history.push({ author: "model", content: assistantResponse });
            appendMessage("assistant", assistantResponse);
        } catch (error) {
            console.error("Error:", error);
            appendMessage("assistant", "Sorry, there was an error!");
        }
    }

    sendButton.addEventListener("click", sendMessage);

    userInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});