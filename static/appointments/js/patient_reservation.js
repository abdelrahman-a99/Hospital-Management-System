function openReservationForm(doctorId, doctorName) {
    document.getElementById('doctorName').textContent = doctorName;
    document.getElementById('doctorId').value = doctorId;
    document.getElementById('reservation-modal').style.display = 'flex';
}

function closeReservationForm() {
    document.getElementById('reservation-modal').style.display = 'none';
}

function closeConfirmation() {
    document.getElementById('confirmation-modal').style.display = 'none';
    // Optional: Redirect to upcoming appointments after confirmation
    window.location.href = "/appointments/upcoming_appointments/";
}

function submitReservation(event) {
    event.preventDefault(); // Prevent form reload

    const doctorId = document.getElementById('doctorId').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    if (!date || !time) {
        alert('Please select both a date and a time.');
        return;
    }

    console.log("Submitting reservation: ", { doctorId, date, time }); // Debugging

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/appointments/patient_reservation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            doctorId: doctorId,
            date: date,
            time: time,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update confirmation modal with submitted values
            document.getElementById('confirmedDoctorName').textContent = document.getElementById('doctorName').textContent;
            document.getElementById('confirmedDate').textContent = date;
            document.getElementById('confirmedTime').textContent = time;

            // Hide reservation modal and show confirmation modal
            closeReservationForm();
            document.getElementById('confirmation-modal').style.display = 'flex';
        } else {
            console.log("Error: ", data); // Log error response
            alert(data.error || 'Failed to book appointment. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An unexpected error occurred. Please try again.');
    });
}
