document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("reservation-form");
  const formCheck = document.getElementById("reservation-check-form");
  const popup = document.getElementById("reservation-popup");
  const details = document.getElementById("reservation-details");
  const closeBtn = document.getElementById("close-reservation-popup");
  const reservationStatus = document.getElementById("reservation-status");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);

    fetch("/api/reservations/", {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      },
      body: formData
    })
      .then(response => {
        if (!response.ok) throw new Error("Failed");
        return response.json();
      })
      .then(data => {
        // Fill popup with reservation details
        details.innerHTML = `
          <p><strong>Name:</strong> ${data.name}</p>
          <p><strong>Email:</strong> ${data.email}</p>
          <p><strong>Date:</strong> ${new Date(data.reservation_date).toLocaleString()}</p>
          <p><strong>Guests:</strong> ${data.number_of_guests}</p>
          <p><strong>ID:</strong> ${data.id}</p>
            <p><strong>Status:</strong> Please Take a note !!</p>
        `;

        popup.classList.remove("hidden");
        popup.classList.add("show");
        form.reset();
      })
      .catch(err => {
        alert("Error occurred.");
        console.error(err);
      });

    // Close popup
    closeBtn.addEventListener("click", () => {
      popup.classList.remove("show");
      popup.classList.add("hidden");
    });
  });

  formCheck.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(formCheck);

    fetch("/api/reservations/check/", {
        method: "POST",  // ❗ Important
        headers: {
        "X-Requested-With": "XMLHttpRequest"
        },
        body: formData
    })
        .then(response => {
        if (!response.ok) throw new Error("Failed");
        return response.json();
        })
        .then(data => {
        // Fill popup or status element with reservation details
        reservationStatus.innerHTML = `
            <p><strong>Name:</strong> ${data.name}</p>
            <p><strong>Email:</strong> ${data.email}</p>
            <p><strong>Date:</strong> ${new Date(data.reservation_date).toLocaleString()}</p>
            <p><strong>Guests:</strong> ${data.number_of_guests}</p>
            <p><strong>ID:</strong> ${data.id}</p>
            <p>Please be here 15 mins earlier for the best experience. <br> Hope to see you soon ! </p>
        `;
        reservationStatus.classList.remove("hidden");
        reservationStatus.classList.add("show");
        })
        .catch(err => {
        reservationStatus.innerHTML = `<p style="color:red;"><strong>No reservations found. <br> Please check your email and reservation number.</strong></p>`;
        reservationStatus.classList.remove("hidden");
        reservationStatus.classList.add("show");
        console.error(err);
        });
  });
});

  flatpickr("#reservation_date", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    time_24hr: true,
    minuteIncrement: 30
  });