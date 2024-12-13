document.addEventListener("DOMContentLoaded", function () {
    const reservationForm = document.getElementById('reservationForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const confirmationMessage = document.getElementById('confirmationMessage');

    reservationForm.addEventListener('submit', function (e) {
        e.preventDefault();
        loadingSpinner.classList.remove('hidden');
        confirmationMessage.classList.add('hidden');

        // Simulate form submission
        setTimeout(() => {
            loadingSpinner.classList.add('hidden');
            confirmationMessage.classList.remove('hidden');
            reservationForm.reset();
        }, 2000);
    });
});