// when the user scroll down, the header will be change the bg color
window.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    if (window.scrollY > 0) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// ================================================================================

// Copyright Date
let time = document.querySelector(".time")
time.innerHTML = new Date().getFullYear() // Display current year -> 2024

// ================================================================================

// Get the CSRF token from the cookie (Django sets this in the browser automatically)
// function getCsrfToken() {
//     const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//     return csrfToken;
// }

// document.querySelector('form').addEventListener('submit', function (event) {
//     event.preventDefault(); // Prevent form from submitting directly

//     // Select input fields
//     const name = document.querySelector('input[name="name"]');
//     const email = document.querySelector('input[name="email"]');
//     const message = document.querySelector('textarea[name="message"]');

//     // Regular expression for basic email validation
//     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

//     let valid = true;

//     // Clear previous messages
//     document.querySelectorAll('.alert').forEach(alert => alert.remove());

//     // Validate name (at least 3 characters and only letters)
//     if (name.value.trim() === '' || name.value.length < 3 || !/^[A-Za-z]+$/.test(name.value)) {
//         valid = false;

//         // const error = document.createElement('div');
//         // error.classList.add('alert', 'error');
//         // error.textContent = "Please enter a valid name with at least 2 letters.";
//         // document.querySelector('.messages').appendChild(error);
//         addMessage("Please enter a valid name.", "error");
//     }

//     // Validate email
//     else if (!emailRegex.test(email.value)) {
//         valid = false;

//         // const error = document.createElement('div');
//         // error.classList.add('alert', 'error');
//         // error.textContent = "Please enter a valid email address.";
//         // document.querySelector('.messages').appendChild(error);
//         addMessage("Please enter a valid email address.", "error");
//     }

//     // Validate message
//     else if (message.value.trim().length < 10) {
//         valid = false;

//         // const error = document.createElement('div');
//         // error.classList.add('alert', 'error');
//         // error.textContent = "Please enter a message with at least 10 characters.";
//         // document.querySelector('.messages').appendChild(error);
//         addMessage("Please enter a message with at least 10 characters.", "error");
//     }

//     // // If all validations pass, submit the form
//     // if (valid) {
//     //     // Submit the form via AJAX or simply submit the form
//     //     // alert("Your message has been successfully sent from js!");

//     //     addMessage("Thank you for reaching out! We'll get back to you soon.", "success");

//     //     // Clear input fields
//     //     name.value = '';
//     //     email.value = '';
//     //     message.value = '';

//     //     // Redirect back to the homepage
//     //     // window.location.href = '/';  // Redirect to the home page (index)

//     //     // Redirect back to the homepage
//     //     // setTimeout(() => {
//     //     //     window.location.href = '/';  // Redirect to the home page (index)
//     //     // }, 3000); // Delay the redirect to allow the alert to show
//     // }

//     // If all validations pass, submit the form via AJAX
//     if (valid) {
//         const formData = new FormData();
//         formData.append('name', name.value);
//         formData.append('email', email.value);
//         formData.append('message', message.value);

//         fetch('/contact/', {
//             method: 'POST',
//             body: formData,
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest', // Indicate that this is an AJAX request
//                 'X-CSRFToken': getCsrfToken(), // Add the CSRF token to the headers
//             },
//         })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     addMessage("Thank you for reaching out! We'll get back to you soon.", "success");
//                     name.value = '';
//                     email.value = '';
//                     message.value = '';
//                 } else {
//                     addMessage("There was an error. Please try again later.", "error");
//                 }
//             })
//             .catch(error => {
//                 addMessage("An unexpected error occurred. Please try again.", "error");
//             });
//     }
// });

// function addMessage(message, type) {
//     const alert = document.createElement('div');
//     alert.classList.add('alert', type);
//     alert.textContent = message;

//     document.querySelector('.messages').appendChild(alert);

//     // Set a timeout to remove the alert after 5 seconds
//     setTimeout(() => {
//         alert.style.opacity = '0'; // Start fade-out effect
//     }, 3000); // Delay before fading out

//     // Remove the alert from DOM after 6 seconds (allow for fade-out)
//     setTimeout(() => {
//         alert.remove();
//     }, 4000); // 1s for fading + 5s display time
// }

// document.addEventListener('DOMContentLoaded', function () {
//     // Check if there are any Django messages (alerts) on the page
//     const messages = document.querySelectorAll('.alert');

//     // Loop through each message and set it to fade out after 3 seconds
//     messages.forEach(function (alert) {
//         setTimeout(() => {
//             alert.style.opacity = '0'; // Fade out effect
//         }, 5000); // After 5 seconds fade out

//         setTimeout(() => {
//             alert.remove(); // Remove the alert from the DOM after it fades out
//         }, 6000); // After 6 seconds, remove from the DOM completely
//     });
// });

<<<<<<< HEAD
=======
// ================================================================================

>>>>>>> 067bcdb18d365fdd3ece4a8dbf966b70f177c33e
document.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = 0;
            setTimeout(() => {
                message.remove();
            }, 500); // Delay to allow opacity transition to complete
        }, 3000); // 3 seconds before fading
    });
});
<<<<<<< HEAD
=======

// ================================================================================

document.addEventListener("DOMContentLoaded", () => {
    const doctoricon = document.querySelector('.signup-options .option i');
    const patienticon = document.querySelector('.signup-options .option i');


    doctoricon.addEventListener("click", () => {
        window.location.href = "{% url 'signup' %}";
    });

    patienticon.addEventListener("click", () => {
        window.location.href = "{% url 'signup' %}";
    });

    const signUpButton = document.querySelector("header .auth button");
    const modal = document.getElementById("signup-modal");
    const closeModal = document.querySelector(".modal-close");

    // Open modal on sign-up button click
    signUpButton.addEventListener("click", () => {
        modal.style.display = "block";
    });

    // Close modal when clicking the close button
    closeModal.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Close modal when clicking outside the modal content
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

>>>>>>> 067bcdb18d365fdd3ece4a8dbf966b70f177c33e
