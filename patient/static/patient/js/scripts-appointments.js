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
    const chatInput = document.getElementById("chatInput");
    const sendChat = document.getElementById("sendChat");

    toggleButton.addEventListener("click", () => {
        if (chatWindow.style.display === "none" || chatWindow.style.display === "") {
            chatWindow.style.display = "block"; // Show the window
        } else {
            chatWindow.style.display = "none"; // Hide the window
        }
    });

    const appendMessage = (author, content) => {
        const messageDiv = document.createElement("div");
        messageDiv.innerHTML = `<strong>${author}:</strong> ${content}`;
        chatHistory.appendChild(messageDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    };

    sendChat.addEventListener("click", () => {
        const userInput = chatInput.value.trim();
        if (userInput) {
            appendMessage("user", userInput);
            chatInput.value = "";

            // Simulate backend call
            fetch("/api/getResponse", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ userInput })
            })
                .then(response => response.json())
                .then(data => {
                    appendMessage("Assistant", data.response);
                })
                .catch(error => {
                    console.error("Error:", error);
                    appendMessage("Assistant", "Sorry, something went wrong.");
                });
        }
    });

    chatInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendChat.click();
        }
    });
});