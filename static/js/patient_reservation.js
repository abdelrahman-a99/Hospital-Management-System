document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("reservationForm");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const doctor = document.getElementById("doctor").value;
        const date = document.getElementById("date").value;
        const time = document.getElementById("time").value;

        alert(`Appointment Reserved!\nDoctor: ${doctor}\nDate: ${date}\nTime: ${time}`);
        form.reset();
    });
});
