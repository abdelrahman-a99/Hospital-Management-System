document.addEventListener("DOMContentLoaded", () => {
    const messageBox = document.getElementById("message-box");
    if (messageBox) {
        setTimeout(() => {
            messageBox.style.opacity = "0";
            messageBox.style.transition = "opacity 1s ease";
            setTimeout(() => {
                messageBox.style.display = "none";
            }, 1000);
        }, 5000);
    }
});

document.querySelector('select[name="user_type"]').addEventListener('change', function () {
    var specialtyField = document.getElementById('specialty_field');
    if (this.value === 'doctor') {
        specialtyField.style.display = 'block';
    } else {
        specialtyField.style.display = 'none';
    }
});

function validatePassword(password) {
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

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

    return ""; // Valid password
}

document.addEventListener('DOMContentLoaded', () => {
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');
    const passwordError = document.getElementById('password_error');
    const confirmPasswordError = document.getElementById('confirm_password_error');

    // Validate password on input
    passwordField.addEventListener('input', () => {
        const errorMessage = validatePassword(passwordField.value);
        passwordError.textContent = errorMessage;
    });

    // Validate confirm password
    confirmPasswordField.addEventListener('input', () => {
        if (passwordField.value !== confirmPasswordField.value) {
            confirmPasswordError.textContent = "Passwords do not match.";
        } else {
            confirmPasswordError.textContent = "";
        }
    });

    // Prevent form submission if passwords are invalid
    const form = document.querySelector('form');
    form.addEventListener('submit', (e) => {
        const passwordErrorMessage = validatePassword(passwordField.value);
        if (passwordErrorMessage || passwordField.value !== confirmPasswordField.value) {
            e.preventDefault();
            if (passwordErrorMessage) {
                passwordError.textContent = passwordErrorMessage;
            }
            if (passwordField.value !== confirmPasswordField.value) {
                confirmPasswordError.textContent = "Passwords do not match.";
            }
        }
    });
});
