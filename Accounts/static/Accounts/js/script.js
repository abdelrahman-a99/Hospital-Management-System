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
                // specialtyField.style.display = this.value === 'doctor' ? 'block' : 'none';
                specialtyField.style.display = this.value === 'doctor' ? 'flex' : 'none';
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
        // Focus event to hide error message when user focuses on the password field
        passwordField.addEventListener('focus', () => {
            if (passwordError) {
                passwordError.classList.remove('show');
            }
        });

        // Blur event to show error message if password is invalid when user leaves the field
        passwordField.addEventListener('blur', () => {
            const errorMessage = validatePassword(passwordField.value);
            if (passwordError) {
                passwordError.textContent = errorMessage;
                if (errorMessage) {
                    passwordError.classList.add('show');
                } else {
                    passwordError.classList.remove('show');
                }
            }
        });

        // Validate that the confirm password matches the password
        confirmPasswordField.addEventListener('input', () => {
            if (passwordField.value !== confirmPasswordField.value) {
                confirmPasswordError.textContent = "Passwords do not match."; // Display mismatch error
                confirmPasswordError.classList.add('show');
            } else {
                confirmPasswordError.textContent = ""; // Clear the error if passwords match
                confirmPasswordError.classList.remove('show');
            }
        });

        // Prevent form submission if the password is invalid or passwords do not match
        if (form) {
            form.addEventListener('submit', (e) => {
                const passwordErrorMessage = validatePassword(passwordField.value);
                if (passwordErrorMessage || passwordField.value !== confirmPasswordField.value) {
                    e.preventDefault(); // Prevent form submission
                    passwordError.classList.add('show');
                    if (passwordErrorMessage) {
                        passwordError.textContent = passwordErrorMessage; // Display password errors
                    }
                    if (passwordField.value !== confirmPasswordField.value) {
                        confirmPasswordError.textContent = "Passwords do not match."; // Display mismatch error
                        confirmPasswordError.classList.add('show');
                    }
                }
            });
        }
    }

    // Password toggle functionality
    function togglePassword(inputId) {
        const input = document.getElementById(inputId);
        const icon = input.nextElementSibling.querySelector('i');
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }

    // Make togglePassword function globally available
    window.togglePassword = togglePassword;

    // Form submission handling
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const button = document.getElementById('loginButton');
            const buttonText = button.querySelector('.button_text');
            const buttonLoader = button.querySelector('.button_loader');
            
            // Show loading state
            button.disabled = true;
            buttonText.style.opacity = '0';
            buttonLoader.style.display = 'block';
        });
    }

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message-box');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.animation = 'slide-down 0.5s ease-out forwards';
            setTimeout(() => {
                message.style.display = 'none';
            }, 500);
        }, 5000);
    });
});
