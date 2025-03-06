document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    let recordsPerPage = 8;
    let totalPages = 1;
    let patients = [];
    let sortColumn = null;
    let sortAscending = true;

    function fetchRecords() {
        fetch("/records")
            .then(response => response.json())
            .then(data => {
                patients = data;
                totalPages = Math.ceil(patients.length / recordsPerPage);
                renderTable();
                updatePagination();
            })
            .catch(error => console.error("⚠️ Error fetching patient records:", error));
    }

    function renderTable() {
        let table = document.getElementById("patientTable");
        table.innerHTML = `
            <tr>
                <th data-column="id">ID 🔽</th>
                <th data-column="firstname">First Name 🔽</th>
                <th data-column="lastname">Last Name 🔽</th>
                <th data-column="age">Age 🔽</th>
                <th data-column="sex">Sex 🔽</th>
                <th data-column="room">Room 🔽</th>
                <th data-column="admission">Admission Date 🔽</th>
                <th data-column="discharge">Discharge Date 🔽</th>
                <th data-column="assist">Assist By 🔽</th>
            </tr>`;

        let sortedPatients = [...patients];

        if (sortColumn) {
            sortedPatients.sort((a, b) => {
                let valA = a[sortColumn];
                let valB = b[sortColumn];

                // Convert to numbers if sorting ID or Age
                if (sortColumn === "id" || sortColumn === "age") {
                    valA = parseInt(valA, 10);
                    valB = parseInt(valB, 10);
                }

                if (valA < valB) return sortAscending ? -1 : 1;
                if (valA > valB) return sortAscending ? 1 : -1;
                return 0;
            });
        }

        let start = (currentPage - 1) * recordsPerPage;
        let end = start + recordsPerPage;
        let paginatedPatients = sortedPatients.slice(start, end);

        paginatedPatients.forEach(patient => {
            let row = table.insertRow();
            row.innerHTML = `
                <td>${patient.id}</td>
                <td>${patient.firstname}</td>
                <td>${patient.lastname}</td>
                <td>${patient.age}</td>
                <td>${patient.sex}</td>
                <td>${patient.room}</td>
                <td>${patient.admission}</td>
                <td>${patient.discharge}</td>
                <td>${patient.assist}</td>
            `;
        });

        addSortingEventListeners();
    }

    function updatePagination() {
        document.getElementById("currentPage").value = currentPage;
        document.getElementById("totalPages").textContent = totalPages;
        document.getElementById("prevPage").disabled = currentPage === 1;
        document.getElementById("nextPage").disabled = currentPage === totalPages;
    }

    function addSortingEventListeners() {
        document.querySelectorAll("#patientTable th").forEach(header => {
            header.addEventListener("click", function () {
                let column = this.getAttribute("data-column");

                if (sortColumn === column) {
                    sortAscending = !sortAscending; // Toggle sorting order
                } else {
                    sortColumn = column;
                    sortAscending = true;
                }

                renderTable();
            });
        });
    }

    document.getElementById("prevPage").addEventListener("click", function () {
        if (currentPage > 1) {
            currentPage--;
            renderTable();
            updatePagination();
        }
    });

    document.getElementById("nextPage").addEventListener("click", function () {
        if (currentPage < totalPages) {
            currentPage++;
            renderTable();
            updatePagination();
        }
    });

    document.getElementById("currentPage").addEventListener("change", function () {
        let page = parseInt(this.value);
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
            renderTable();
            updatePagination();
        } else {
            this.value = currentPage;
        }
    });

    fetchRecords();


    document.getElementById("p_save").addEventListener("click", function(event) {
        event.preventDefault(); // Prevent form from reloading the page
    
        let patientData = {
            firstname: document.getElementById("p_firstname").value,
            lastname: document.getElementById("p_lastname").value,
            age: document.getElementById("p_age").value,
            sex: document.getElementById("p_sex").value,
            room: document.getElementById("p_room").value,
            admission_date: document.getElementById("p_admissiondate").value,
            discharge_date: document.getElementById("dischargedate").value
        };
    
        fetch("/InsertPatientInfo", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(patientData)
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Show success or error message
            if (data.status === "success") {
                document.getElementById("form_patientinfo").reset(); // Clear form fields
            }
        })
        .catch(error => console.error("Error:", error));
    });        
       
});





       