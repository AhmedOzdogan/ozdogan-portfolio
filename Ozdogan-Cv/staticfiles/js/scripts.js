(function () {
  const header = document.querySelector(".header");
  const btn = document.querySelector(".menu-btn");
  const nav = document.querySelector(".nav-list");

  function sync() {
    if (!header || !nav) return;
    nav.style.top = header.offsetHeight + "px";
    document.body.style.paddingTop = header.offsetHeight + "px";
  }

  // toggle open/close
  if (btn && header) {
    btn.addEventListener("click", () => {
      const open = header.classList.toggle("is-open");
      btn.setAttribute("aria-expanded", String(open));
      sync();
    });
  }

  window.addEventListener("load", sync);
  window.addEventListener("resize", sync);
})();
