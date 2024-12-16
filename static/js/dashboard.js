const appointments = [
    {
        id: 1,
        patientName: 'John Doe',
        date: '2024-12-18',
        time: '10:00 AM',
        status: 'Scheduled',
        description: 'John Doe is a 45-year-old male with a history of hypertension.',
        age: 45,
        contact: 'john.doe@example.com',
        medicalHistory: 'Hypertension, Allergies'
    },
    {
        id: 2,
        patientName: 'malak ahmed',
        date: '2024-12-17',
        time: '11:00 AM',
        status: 'Waiting',
        description: 'Malak Ahmed is a 20-year-old female with a history of asthma.',
        age: 30,
        contact: 'malak.ahmed@example.com',
        medicalHistory: 'Asthma, Diabetes'
    },
    {
        id: 3,
        patientName: 'haya osama',
        date: '2024-12-03',
        time: '02:00 PM',
        status: 'Engaged',
        description: 'Haya Osama is a 20-year-old female with a history of diabetes.',
        age: 50,
        contact: 'haya.osams@example.com',
        medicalHistory: 'Diabetes, High Cholesterol'
    },
    {
        id: 4,
        patientName: 'Rwan Ashraf',
        date: '2024-12-04',
        time: '09:00 AM',
        status: 'Checkout',
        description: 'Rwan Ashraf is a 20-year-old female with a history of heart disease.',
        age: 60,
        contact: 'rwan.ashraf@example.com',
        medicalHistory: 'Heart Disease, Hypertension'
    },
    {
        id: 5,
        patientName: 'Abdlrehman',
        date: '2024-12-05',
        time: '10:30 AM',
        status: 'Scheduled',
        description: 'Abdlrehman is a 60-year-old male with a history of migraines.',
        age: 35,
        contact: 'abdlrehman.ma3ref4@example.com',
        medicalHistory: 'Migraines, Allergies'
    },
    {
        id: 6,
        patientName: 'sherif',
        date: '2024-12-06',
        time: '11:30 AM',
        status: 'Scheduled',
        description: 'sherif is a 45-year-old male with a history of anemia.',
        age: 28,
        contact: 'sherif.ma3ref4@example.com',
        medicalHistory: 'Anemia, Low Blood Pressure'
    },
    {
        id: 7,
        patientName: 'shams abouda',
        date: '2024-12-07',
        time: '01:00 PM',
        status: 'Scheduled',
        description: 'Shams Abouda is a 40-year-old female with a history of back pain.',
        age: 40,
        contact: 'shams.abouda@example.com',
        medicalHistory: 'Back Pain, Arthritis'
    },
    {
        id: 8,
        patientName: 'mayar shams',
        date: '2024-12-08',
        time: '02:30 PM',
        status: 'Scheduled',
        description: 'Mayar Shams is a 32-year-old female with a history of allergies.',
        age: 32,
        contact: 'mayar.shams@example.com',
        medicalHistory: 'Allergies, Asthma'
    },
    {
        id: 9,
        patientName: 'omnia shams',
        date: '2024-12-09',
        time: '03:00 PM',
        status: 'Scheduled',
        description: 'Omnia Shams is a 50-year-old female with a history of hypertension.',
        age: 50,
        contact: 'omnia.shams@example.com',
        medicalHistory: 'Hypertension, Diabetes'
    },
    {
        id: 10,
        patientName: 'mariam shams',
        date: '2024-12-10',
        time: '04:00 PM',
        status: 'Scheduled',
        description: 'Mariam Shams is a 45-year-old female with a history of migraines.',
        age: 45,
        contact: 'mariam.shams@example.com',
        medicalHistory: 'Migraines, Allergies'
    }
];
let currentYear = 2024;
let currentMonth = 11; // December (months are 0-indexed)

function getStatusIcon(status) {
    switch (status) {
        case 'Scheduled':
            return '<i class="fas fa-clock status-icon"></i>';
        case 'Waiting':
            return '<i class="fas fa-hourglass-half status-icon"></i>';
        case 'Engaged':
            return '<i class="fas fa-user-check status-icon"></i>';
        case 'Checkout':
            return '<i class="fas fa-check-circle status-icon"></i>';
        default:
            return '';
    }
}

function createStickyNote(appointment) {
    const stickyNote = document.createElement("div");
    stickyNote.classList.add("sticky-note", appointment.status.toLowerCase());

    stickyNote.innerHTML = `
        ${getStatusIcon(appointment.status)}
        <p class="patient-name">${appointment.patientName}</p>
        <p class="appointment-time">${appointment.time}</p>
        <button class="edit-btn" data-id="${appointment.id}">Edit</button>
        <button class="delete-btn" data-id="${appointment.id}">Delete</button>
    `;

    stickyNote.querySelector('.edit-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        const appointmentId = e.target.dataset.id;
        openEditModal(appointmentId);
    });

    stickyNote.querySelector('.delete-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        const appointmentId = e.target.dataset.id;
        deleteAppointment(appointmentId);
    });

    $(stickyNote).draggable({
        containment: "body",
        scroll: false,
        snap: ".calendar td",
        snapMode: "inner",
        stop: function(event, ui) {
            // Ensure the sticky note sits correctly when dropped
            $(this).css({
                top: 0,
                left: 0
            });
        }
    });

    return stickyNote;
}

function updateCalendar() {
    const calendarYear = document.getElementById("calendarYear");
    const calendarMonth = document.getElementById("calendarMonth");
    const calendarBody = document.getElementById("calendarBody");
    
    calendarYear.textContent = currentYear;
    calendarMonth.textContent = new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long' });
    calendarBody.innerHTML = "";

    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const lastDate = new Date(currentYear, currentMonth + 1, 0).getDate();
    const today = new Date();

    let dayCounter = 1;

    for (let i = 0; i < 6; i++) {
        const row = document.createElement("tr");
        for (let j = 0; j < 7; j++) {
            const cell = document.createElement("td");
            if (i === 0 && j < firstDay) {
                cell.textContent = "";
            } else if (dayCounter <= lastDate) {
                const cellDate = new Date(currentYear, currentMonth, dayCounter);
                const dayAppointments = appointments.filter(a => a.date === `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(dayCounter).padStart(2, '0')}`);
                cell.textContent = dayCounter;

                if (cellDate < today) {
                    cell.classList.add('past-date');
                } else {
                    if (dayAppointments.length > 0) {
                        dayAppointments.forEach(appointment => {
                            const stickyNote = createStickyNote(appointment);
                            cell.appendChild(stickyNote);
                        });
                    }

                    cell.addEventListener("click", function () {
                        openModal(dayCounter, dayAppointments);
                    });
                }

                $(cell).droppable({
                    accept: ".sticky-note",
                    drop: function(event, ui) {
                        const droppedNote = ui.helper[0];
                        $(this).append(droppedNote);
                        $(droppedNote).css({
                            top: 0,
                            left: 0
                        });
                        adjustCellHeight($(this));
                    }
                });

                dayCounter++;
            } else {
                cell.classList.add('empty-cell');
            }
            row.appendChild(cell);
        }
        calendarBody.appendChild(row);
    }
}

function adjustCellHeight(cell) {
    const notes = cell.find('.sticky-note');
    let totalHeight = 0;
    notes.each(function() {
        totalHeight += $(this).outerHeight(true);
    });
    cell.css('height', totalHeight + 20); // Add some padding
}

function openEditModal(appointmentId) {
    const appointment = appointments.find(a => a.id == appointmentId);
    if (appointment) {
        document.getElementById('appointmentDate').value = appointment.date;
        document.getElementById('appointmentTime').value = appointment.time;
        document.getElementById('patientName').value = appointment.patientName;
        document.getElementById('appointmentStatus').value = appointment.status;
        document.getElementById('appointmentForm').dataset.id = appointment.id;
        document.getElementById('appointmentModal').style.display = 'block';
    }
}

function deleteAppointment(appointmentId) {
    const index = appointments.findIndex(a => a.id == appointmentId);
    if (index !== -1) {
        appointments.splice(index, 1);
        updateCalendar();
        updateUpcomingAppointments();
    }
}

document.getElementById('appointmentForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const appointmentId = this.dataset.id;
    const appointment = appointments.find(a => a.id == appointmentId);
    if (appointment) {
        appointment.date = document.getElementById('appointmentDate').value;
        appointment.time = document.getElementById('appointmentTime').value;
        appointment.patientName = document.getElementById('patientName').value;
        appointment.status = document.getElementById('appointmentStatus').value;
        updateCalendar();
        updateUpcomingAppointments();
        document.getElementById('appointmentModal').style.display = 'none';
    }
});

document.querySelector('.close-btn').addEventListener('click', function () {
    document.getElementById('appointmentModal').style.display = 'none';
});

function updateUpcomingAppointments() {
    const upcomingPatients = document.getElementById('upcomingPatients');
    upcomingPatients.innerHTML = '';

    const scheduledAppointments = appointments.filter(a => a.status === 'Scheduled');
    scheduledAppointments.forEach(appointment => {
        const appointmentDiv = document.createElement('div');
        appointmentDiv.classList.add('appointment');
        appointmentDiv.innerHTML = `
            <p><strong>${appointment.patientName}</strong></p>
            <p>${appointment.date} at ${appointment.time}</p>
            <button class="open-btn">Open</button>
            <div class="patient-description">
                <p><strong>Age:</strong> ${appointment.age}</p>
                <p><strong>Contact:</strong> ${appointment.contact}</p>
                <p><strong>Medical History:</strong> ${appointment.medicalHistory}</p>
                <p>${appointment.description}</p>
            </div>
        `;
        appointmentDiv.querySelector('.open-btn').addEventListener('click', () => {
            toggleDescription(appointmentDiv);
        });
        upcomingPatients.appendChild(appointmentDiv);
    });
}

function toggleDescription(appointmentDiv) {
    const descriptionDiv = appointmentDiv.querySelector('.patient-description');
    if (descriptionDiv.style.display === 'none' || descriptionDiv.style.display === '') {
        descriptionDiv.style.display = 'block';
    } else {
        descriptionDiv.style.display = 'none';
    }
}

document.getElementById('prevYearBtn').addEventListener('click', () => {
    currentYear--;
    updateCalendar();
});

document.getElementById('nextYearBtn').addEventListener('click', () => {
    currentYear++;
    updateCalendar();
});

document.getElementById('prevMonthBtn').addEventListener('click', () => {
    if (currentMonth === 0) {
        currentMonth = 11;
        currentYear--;
    } else {
        currentMonth--;
    }
    updateCalendar();
});

document.getElementById('nextMonthBtn').addEventListener('click', () => {
    if (currentMonth === 11) {
        currentMonth = 0;
        currentYear++;
    } else {
        currentMonth++;
    }
    updateCalendar();
});
document.addEventListener("DOMContentLoaded", function () {
    updateCalendar();
    updateUpcomingAppointments();
});