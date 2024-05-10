document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('insertButton').addEventListener('click', addCustomer);
    document.getElementById('searchBox').addEventListener('input', function() {
        performSearch(this.value, 1); // Search by customer name in the second column (index 1)
    });
    document.getElementById('timesheetSearchBox').addEventListener('input', function() {
        performSearch(this.value, 3); // Search by timesheet in the fourth column (index 3)
    });
});

let nextCustomerId = 1; // Global variable to track the next customer ID
let currentCustomer = {}; // Global object to store current customer details

function addCustomer() {
    var isValid = true;

    var transportHours = document.getElementById('transportHours').value || '0';
    var transportMinutes = document.getElementById('transportMinutes').value || '0';
    var hideTransport = document.getElementById('hideTransportCheckbox').checked;
    var hasContract = document.getElementById('contractCheckbox').checked;

    var customerName = document.getElementById('customerName').value.trim();
    var address = document.getElementById('address').value.trim();
    var contact = document.getElementById('contact').value.trim();
    var email = document.getElementById('email').value.trim();
    var phone = document.getElementById('phone').value.trim();
    var notes = document.getElementById('customerNotes').value.trim();

    if (!customerName || !address || !contact || !email || !phone) {
        alert('All fields except notes are required.');
        isValid = false;
    }

    if (!isValid) {
        return;
    }

    var techLevel1 = getTechLevelData(1);
    var techLevel2 = getTechLevelData(2);
    var techLevel3 = getTechLevelData(3);

    // Store customer details in global variable
    currentCustomer = {
        name: customerName,
        address: address,
        contact: contact,
        email: email,
        phone: phone,
        notes: notes,
        techLevel1: techLevel1,
        techLevel2: techLevel2,
        techLevel3: techLevel3
    };

    var table = document.querySelector('.files-display table tbody');
    var newRow = table.insertRow();
    newRow.innerHTML = `

        <td>${nextCustomerId}</td>
        <td><a href="modify-customer.html?id=${nextCustomerId}" class="customer-name-link">${customerName}</a></td>
        <td>
            Transportation: ${transportHours} hour/s ${transportMinutes} min <br>
            Hide transportation charges: ${hideTransport ? 'Yes' : 'No'}<br>
            Contract: ${hasContract ? 'Yes' : 'No'}<br>
            R1: $${parseFloat(techLevel1.regular).toFixed(2)} TH1: $${parseFloat(techLevel1.timeAndHalf).toFixed(2)} DT1: $${parseFloat(techLevel1.doubleTime).toFixed(2)}<br>
            R2: $${parseFloat(techLevel2.regular).toFixed(2)} TH2: $${parseFloat(techLevel2.timeAndHalf).toFixed(2)} DT2: $${parseFloat(techLevel2.doubleTime).toFixed(2)}<br>
            R3: $${parseFloat(techLevel3.regular).toFixed(2)} TH3: $${parseFloat(techLevel3.timeAndHalf).toFixed(2)} DT3: $${parseFloat(techLevel3.doubleTime).toFixed(2)}
        </td>
        <td>
            <button onclick="viewTimesheets(currentCustomer)">Show all</button><br><br>
            <button onclick="createNewTimesheet(currentCustomer)">New Timesheet</button>
        </td>
        <td>
            Address: ${address || 'N/A'}<br>
            Contact: ${contact || 'N/A'}<br>
            E-mail: ${email || 'N/A'}<br>
            Phone Number: ${phone || 'N/A'}
        </td>
        <td>${notes || ''}</td>
        <td><button onclick="confirmDelete(this)">Delete</button></td>
    `;

    nextCustomerId++; // Increment the ID for the next customer

    // Clear form fields after adding a customer
    document.getElementById('customerName').value = '';
    document.getElementById('address').value = '';
    document.getElementById('contact').value = '';
    document.getElementById('email').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('customerNotes').value = '';
}

function getTechLevelData(level) {
    return {
        regular: document.querySelector(`input[name='tech${level}-regular']`).value || '0',
        timeAndHalf: document.querySelector(`input[name='tech${level}-time-half']`).value || '0',
        doubleTime: document.querySelector(`input[name='tech${level}-double-time']`).value || '0'
    };
}

function confirmDelete(btn) {
    if (confirm('Are you sure you want to delete this customer?')) {
        var row = btn.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }
}

function performSearch(searchTerm, columnIndex) {
    var table = document.querySelector('.files-display table tbody');
    Array.from(table.rows).forEach(row => {
        let cellText = row.cells[columnIndex].textContent.toLowerCase();
        row.style.display = cellText.includes(searchTerm.toLowerCase()) ? '' : 'none';
    });
}

document.getElementById('timesheetForm').addEventListener('submit', function(e) {
    e.preventDefault();
    // Handle form data here
    this.reset();
});

function viewTimesheets(customer) { 
    window.location.href = `timesheets.html?customerName=${encodeURIComponent(customer.name)}`;
}

function createNewTimesheet(customer) {
    window.location.href = `timesheet-creation.html?customerName=${encodeURIComponent(customer.name)}`;
}

function searchTimesheets() {
    console.log('Searching for timesheets...');
}

function modifyTimesheet(timesheetId) {
    window.location.href = `update-timesheet.html?timesheetId=${timesheetId}`;
}

// FILE UPLOAD FOR TIMESHEET CREATION
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        console.log('Form submitted with:', new FormData(form));
        // Uncomment the next line to see if the form has the file before submission
        // event.preventDefault(); // Prevent the form from submitting
    });
});
