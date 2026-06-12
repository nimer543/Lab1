// app/views/static/js/main.js

document.addEventListener("DOMContentLoaded", function() {
    
    // Date validation
    const tripForm = document.getElementById("trip-form");
    if (tripForm) {
        const startDateInput = document.getElementById("start_date");
        const endDateInput = document.getElementById("end_date");
        
        tripForm.addEventListener("submit", function(event) {
            const startDate = new Date(startDateInput.value);
            const endDate = new Date(endDateInput.value);
            
            if (endDate < startDate) {
                event.preventDefault(); 
                alert("Błąd: Data zakończenia podróży nie może być wcześniejsza niż data jej rozpoczęcia!");
                endDateInput.focus();
            }
        });
        
        startDateInput.addEventListener("change", function() {
            endDateInput.min = startDateInput.value;
        });
    }

    // Delete confirmation
    const deleteForms = document.querySelectorAll(".delete-confirm-form");
    deleteForms.forEach(form => {
        form.addEventListener("submit", function(event) {
            const message = form.getAttribute("data-confirm-message") || "Czy na pewno chcesz usunąć ten element?";
            const confirmed = confirm(message);
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

});

