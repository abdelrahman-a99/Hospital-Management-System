document.addEventListener("DOMContentLoaded", function () {
    document.querySelector('.sidebar a[href="#reports"]').addEventListener('click', function (event) {
        event.preventDefault();
        fetchPatientReports();
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch patient reports
    function fetchPatientReports() {
        fetch('/api/patient-reports/', { method: 'GET' })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                const reportTableBody = document.getElementById('reportBody');
                reportTableBody.innerHTML = ''; 

                data.forEach(patient => {
                    const row = `
                        <tr>
                            <td>${patient.name}</td>
                            <td>${patient.age}</td>
                            <td>${patient.gender}</td>
                            <td>${patient.lastVisit}</td>
                            <td>${patient.medicalRecords}</td>
                            <td>${patient.nextVisit}</td>
                        </tr>
                    `;
                    reportTableBody.insertAdjacentHTML('beforeend', row);
                });
            })
            .catch(error => {
                console.error('Error fetching patient reports:', error);
            });
    }

    fetchPatientReports();
});
