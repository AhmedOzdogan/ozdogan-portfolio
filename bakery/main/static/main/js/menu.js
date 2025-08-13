document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("menu-container");
  if (!container) return;

  const slugify = (s) =>
    String(s || "")
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "");

  const getCategory = (item) => {
    const c = item.category;
    if (!c) return { key: "uncategorized", label: "Uncategorized" };
    if (typeof c === "string") {
      const key = slugify(c);
      return { key, label: c.charAt(0).toUpperCase() + c.slice(1) };
    }
    const key = c.slug ? String(c.slug).toLowerCase() : slugify(c.name);
    const label = c.name || c.slug || "Uncategorized";
    return { key, label };
  };

  const urlParams = new URLSearchParams(window.location.search);
  const selected = (urlParams.get("category") || "").toLowerCase();

  fetch("/api/products/")
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then((data) => {
      if (!Array.isArray(data) || data.length === 0) {
        container.innerHTML = "<p>No menu items available.</p>";
        return;
      }

      const groups = {};
      for (const item of data) {
        const { key, label } = getCategory(item);
        if (!groups[key]) groups[key] = { label, items: [] };
        groups[key].items.push(item);
      }

      const entries = Object.entries(groups)
        .filter(([key]) => !selected || key === selected)
        .sort((a, b) => a[1].label.localeCompare(b[1].label));

      if (entries.length === 0) {
        container.innerHTML = "<p>No items in this category.</p>";
        return;
      }

      // Build all HTML first to minimize DOM updates
      let html = "";
      for (const [key, group] of entries) {
        html += `<section class="menu-category">`;
        html += `<h2>${group.label.toUpperCase()}</h2>`;
        html += `<div class="menu-grid">`;

        for (const item of group.items) {
          const imgSrc = item.picture || `/static/main/img/menu_items/${slugify(item.name)}.png`;
          const rawPrice = item.price;
          const price =
            typeof rawPrice === "number"
              ? rawPrice.toFixed(2)
              : !isNaN(rawPrice)
              ? Number(rawPrice).toFixed(2)
              : rawPrice;

          html += `
            <div class="menu-item">
              <img src="${imgSrc}" alt="${item.name}" 
              width="320" height="240"
              loading="lazy" decoding="async"
              style="object-fit:cover">
              <a href="/menu/${item.id}/">
                <h3>${item.name}</h3>
              </a>
              <h3><span>$${price}</span></h3>
              <p>${item.description || ""}</p>

              <a href='/menu/${item.id}/' id="add-to-cart" type="button">Add to cart</a>
            </div>
          `;
        }

        html += `</div></section>`;
      }

      // Inject into DOM once
      container.innerHTML = html;
    })
    .catch((err) => {
      console.error("Error fetching menu:", err);
      container.innerHTML = "<p>Error loading menu.</p>";
    });
});
