document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.querySelector('.messages-container');
    const sendMessageButton = document.querySelector('#send-message-button');
    const messageContentInput = document.querySelector('#message-content');

    // Fetch messages on page load
    fetchMessages();

    // Send message on button click
    sendMessageButton.addEventListener('click', async () => {
        const content = messageContentInput.value.trim();
        if (!content) {
            alert('Please type a message.');
            return;
        }

        try {
            const response = await fetch('/appointments/messages/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ content })
            });

            const data = await response.json();
            if (data.success) {
                messageContentInput.value = ''; // Clear input field
                addMessageToUI({ sender: 'You', content, timestamp: new Date() }); // Optimistic update
                fetchMessages(); // Refresh messages to get the latest data
            } else {
                alert('Failed to send message: ' + data.error);
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
    });

    // Fetch messages
    async function fetchMessages() {
        try {
            const response = await fetch('/appointments/messages/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });
            const data = await response.json();
            if (data.success) {
                renderMessages(data.messages);
            } else {
                console.error('Failed to fetch messages:', data.error);
            }
        } catch (error) {
            console.error('Error fetching messages:', error);
        }
    }

    // Render messages
    function renderMessages(messages) {
        messagesContainer.innerHTML = ''; // Clear existing messages
        messages.forEach(msg => {
            addMessageToUI(msg);
        });
    }

    // Add a single message to the UI
    function addMessageToUI(msg) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ' + (msg.sender === 'You' ? 'sent' : 'received');
        messageDiv.innerHTML = `
            <div class="message-info">
                <span>${msg.sender}</span>
                <span>${new Date(msg.timestamp).toLocaleString()}</span>
            </div>
            <p class="message-content">${msg.content}</p>
        `;
        messagesContainer.appendChild(messageDiv);

        // Scroll to the bottom of the container
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Get CSRF token
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                return decodeURIComponent(cookie.split('=')[1]);
            }
        }
        return null;
    }
});
