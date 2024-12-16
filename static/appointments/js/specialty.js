// appointments/static/appointments/js/specialty.js
document.addEventListener("DOMContentLoaded", function () {
    const specialtyCards = document.querySelectorAll('.icon-box');

    specialtyCards.forEach(function(card) {
        card.addEventListener('click', function() {
            const specialty = this.getAttribute('data-specialty');
            window.location.href = `/appointments/doctors/?specialty=${specialty}`;
        });
    });
});
