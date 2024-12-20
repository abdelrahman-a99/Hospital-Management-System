function sendMessage() {
    const content = document.getElementById('message-content').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (!content.trim()) {
        alert('Message cannot be empty.');
        return;
    }

    fetch('/appointments/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            content: content,
            receiver_id: receiverId,  // Replace with the appropriate receiver ID
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('message-content').value = '';
            location.reload(); // Refresh the page to display the new message
        } else {
            alert(data.error || 'Failed to send message.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An unexpected error occurred.');
    });
}
