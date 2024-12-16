// Handle selecting a doctor
function selectDoctor(doctorName) {
    const doctorField = document.getElementById("doctor");
    doctorField.value = doctorName;
}

// Handle form submission
const reservationForm = document.getElementById("reservationForm");
const reserveButton = document.getElementById("reserveButton");
const appointmentCard = document.getElementById("appointmentCard");
const doctorNameElement = document.getElementById("doctorName");
const appointmentDateElement = document.getElementById("appointmentDate");
const appointmentTimeElement = document.getElementById("appointmentTime");
const appointmentStatusElement = document.getElementById("appointmentStatus");

reservationForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const doctorName = document.getElementById("doctor").value;
    const appointmentDate = document.getElementById("date").value;
    const appointmentTime = document.getElementById("time").value;

    // Update the upcoming appointment card
    doctorNameElement.innerText = doctorName;
    appointmentDateElement.innerText = appointmentDate;
    appointmentTimeElement.innerText = appointmentTime;
    appointmentStatusElement.classList.remove("pending");
    appointmentStatusElement.classList.add("confirmed");
    appointmentStatusElement.innerText = "Confirmed";
});
document.addEventListener('DOMContentLoaded', function() {
    const doctorSelect = document.getElementById('doctor');
    const timeSelect = document.getElementById('time');

    doctorSelect.addEventListener('change', function() {
        const doctorId = this.value;

        // Here you can filter available times per doctor or fetch them via AJAX if needed
        const availableTimes = [
            "09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "02:00 PM", "03:00 PM"
        ]; // Example, adjust per doctor if necessary

        // Clear previous time options
        timeSelect.innerHTML = '<option value="" disabled selected>Choose a time</option>';

        // Add new time options
        availableTimes.forEach(time => {
            const option = document.createElement('option');
            option.value = time;
            option.textContent = time;
            timeSelect.appendChild(option);
        });
    });
});
document.getElementById('doctor').addEventListener('change', function() {
    var selectedOption = this.options[this.selectedIndex];
    var doctorName = selectedOption.text;
    var specialty = selectedOption.getAttribute('data-specialty');

    // Populate the doctor's name and specialty in the reservation form
    document.getElementById('doctorName').value = doctorName + " (" + specialty + ")";
});
