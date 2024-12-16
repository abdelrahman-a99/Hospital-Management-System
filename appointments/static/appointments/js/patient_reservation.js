
function selectDoctor(doctorName) {
    const doctorField = document.getElementById("doctor");
    doctorField.value = doctorName;
}


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

        
        const availableTimes = [
            "09:00 AM", "10:00 AM", "11:00 AM", "01:00 PM", "02:00 PM", "03:00 PM"
        ];

        
        timeSelect.innerHTML = '<option value="" disabled selected>Choose a time</option>';

       
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

    
    document.getElementById('doctorName').value = doctorName + " (" + specialty + ")";
});
