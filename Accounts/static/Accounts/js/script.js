// document.addEventListener("DOMContentLoaded", () => {
//     const messageBox = document.getElementById("message-box");
//     if (messageBox) {
//         setTimeout(() => {
//             messageBox.style.opacity = "0";
//             messageBox.style.transition = "opacity 1s ease";
//             setTimeout(() => {
//                 messageBox.style.display = "none";
//             }, 1000);
//         }, 5000);
//     }
// });

// document.querySelector('select[name="user_type"]').addEventListener('change', function () {
//     var specialtyField = document.getElementById('specialty_field');
//     if (this.value === 'doctor') {
//         specialtyField.style.display = 'block';
//     } else {
//         specialtyField.style.display = 'none';
//     }
// });

// function validatePassword(password) {
//     const hasUpperCase = /[A-Z]/.test(password);
//     const hasLowerCase = /[a-z]/.test(password);
//     const hasNumber = /\d/.test(password);
//     const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

//     if (password.length < 8) {
//         return "Password must be at least 8 characters.";
//     }
//     if (!hasUpperCase) {
//         return "Password must include at least one uppercase letter.";
//     }
//     if (!hasLowerCase) {
//         return "Password must include at least one lowercase letter.";
//     }
//     if (!hasNumber) {
//         return "Password must include at least one number.";
//     }
//     if (!hasSpecialChar) {
//         return "Password must include at least one special character.";
//     }

//     return ""; // Valid password
// }

// document.addEventListener('DOMContentLoaded', () => {
//     const passwordField = document.getElementById('password');
//     const confirmPasswordField = document.getElementById('confirm_password');
//     const passwordError = document.getElementById('password_error');
//     const confirmPasswordError = document.getElementById('confirm_password_error');

//     // Validate password on input
//     passwordField.addEventListener('input', () => {
//         const errorMessage = validatePassword(passwordField.value);
//         passwordError.textContent = errorMessage;
//     });

//     // Validate confirm password
//     confirmPasswordField.addEventListener('input', () => {
//         if (passwordField.value !== confirmPasswordField.value) {
//             confirmPasswordError.textContent = "Passwords do not match.";
//         } else {
//             confirmPasswordError.textContent = "";
//         }
//     });

//     // Prevent form submission if passwords are invalid
//     const form = document.querySelector('form');
//     form.addEventListener('submit', (e) => {
//         const passwordErrorMessage = validatePassword(passwordField.value);
//         if (passwordErrorMessage || passwordField.value !== confirmPasswordField.value) {
//             e.preventDefault();
//             if (passwordErrorMessage) {
//                 passwordError.textContent = passwordErrorMessage;
//             }
//             if (passwordField.value !== confirmPasswordField.value) {
//                 confirmPasswordError.textContent = "Passwords do not match.";
//             }
//         }
//     });
// });

// ==================================================================================

// refactored version

document.addEventListener("DOMContentLoaded", () => {
    const messageBox = document.getElementById("message-box");
    if (messageBox) {
        setTimeout(() => {
            messageBox.style.opacity = "0";
            messageBox.style.transition = "opacity 1s ease";
            setTimeout(() => {
                messageBox.style.display = "none";
            }, 1000); // Hide the message box after 5 seconds
        }, 5000);
    }

    // Handle specialty field visibility when the user selects 'doctor'
    const userTypeSelect = document.querySelector('select[name="user_type"]');
    if (userTypeSelect) {
        userTypeSelect.addEventListener('change', function () {
            const specialtyField = document.getElementById('specialty_field');
            if (specialtyField) {
                // Show the specialty field only if the user selects 'doctor'
                specialtyField.style.display = this.value === 'doctor' ? 'block' : 'none';
            }
        });
    }

    // Function to validate the password (checks for length, uppercase, lowercase, number, and special character)
    function validatePassword(password) {
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumber = /\d/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

        // Validate that the password is at least 8 characters long and includes all required elements
        if (password.length < 8) {
            return "Password must be at least 8 characters.";
        }
        if (!hasUpperCase) {
            return "Password must include at least one uppercase letter.";
        }
        if (!hasLowerCase) {
            return "Password must include at least one lowercase letter.";
        }
        if (!hasNumber) {
            return "Password must include at least one number.";
        }
        if (!hasSpecialChar) {
            return "Password must include at least one special character.";
        }

        // If the password is valid, return an empty string
        return "";
    }

    // Get references to the password fields and error messages
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const passwordError = document.getElementById('password_error');
    const confirmPasswordError = document.getElementById('confirm_password_error');
    const form = document.querySelector('form');

    // Check password and confirm password on input
    if (passwordField && confirmPasswordField) {
        // Check the password input and validate in real-time
        passwordField.addEventListener('input', () => {
            const errorMessage = validatePassword(passwordField.value);
            if (passwordError) passwordError.textContent = errorMessage;
        });

        // Validate that the confirm password matches the password
        confirmPasswordField.addEventListener('input', () => {
            if (passwordField.value !== confirmPasswordField.value) {
                confirmPasswordError.textContent = "Passwords do not match."; // Display mismatch error
            } else {
                confirmPasswordError.textContent = ""; // Clear the error if passwords match
            }
        });

        // Prevent form submission if the password is invalid or passwords do not match
        if (form) {
            form.addEventListener('submit', (e) => {
                const passwordErrorMessage = validatePassword(passwordField.value);
                if (passwordErrorMessage || passwordField.value !== confirmPasswordField.value) {
                    e.preventDefault(); // Prevent form submission
                    if (passwordErrorMessage) {
                        passwordError.textContent = passwordErrorMessage; // Display password errors
                    }
                    if (passwordField.value !== confirmPasswordField.value) {
                        confirmPasswordError.textContent = "Passwords do not match."; // Display mismatch error
                    }
                }
            });
        }
    }
});
