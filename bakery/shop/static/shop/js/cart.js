document.addEventListener("DOMContentLoaded", () => {
  const qtyInputs = document.querySelectorAll(".qty-input");

  qtyInputs.forEach(input => {
    const form = input.closest("form");
    const button = form.querySelector("button[type=submit]");
    const originalValue = input.value;

    input.addEventListener("input", () => {
      if (input.value !== originalValue) {
        button.classList.remove("btn-outline-secondary");
        button.classList.add("btn-danger");
      } else {
        button.classList.remove("btn-danger");
        button.classList.add("btn-outline-secondary");
      }
    });
  });
});
