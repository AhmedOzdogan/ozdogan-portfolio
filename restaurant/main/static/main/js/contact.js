console.log("js is ready")
function handleSubmit(event) {
  event.preventDefault();

  const form = document.getElementById('contact-form');
  const popup = document.getElementById('success-popup');
  const button = form.querySelector('button[type="submit"]');

  // Change button text
    button.textContent = 'Sending...';
    button.disabled = true;

    // Delay the fetch submission by 2 seconds
    setTimeout(() => {
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
        'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => {
        if (!response.ok) throw new Error('Submission failed');
        return response.text();
        })
        .then(() => {
        form.reset();
        popup.classList.add('show');
        button.textContent = 'Send Message';
        button.disabled = false;
        })
        .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
        button.textContent = 'Send Message';
        button.disabled = false;
        });

    }, 2000);
}

document.addEventListener("DOMContentLoaded", () => {
  const closeBtn = document.getElementById("close-popup");
  const popup = document.getElementById("success-popup");

  if (closeBtn && popup) {
    closeBtn.addEventListener("click", () => {
      popup.classList.remove("show");
      location.reload(); // ✅ Optional: refresh page to reset state
    });
  }
});