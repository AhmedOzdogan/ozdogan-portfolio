document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("menu-container");
  if (!container) return;

  // tiny slugify helper for names like "Red Velvet"
  const slugify = (s) =>
    String(s || "")
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "");

  // normalize category -> { key: "cakes", label: "Cakes" }
  const getCategory = (item) => {
    const c = item.category;
    if (!c) return { key: "uncategorized", label: "Uncategorized" };

    if (typeof c === "string") {
      const key = slugify(c);
      return { key, label: c.charAt(0).toUpperCase() + c.slice(1) };
    }
    // object case
    const key = c.slug ? String(c.slug).toLowerCase() : slugify(c.name);
    const label = c.name || c.slug || "Uncategorized";
    return { key, label };
  };

  const urlParams = new URLSearchParams(window.location.search);
  const selected = (urlParams.get("category") || "").toLowerCase(); // e.g. "cakes"

  fetch("/api/products/")
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    })
    .then((data) => {
      container.innerHTML = "";

      if (!Array.isArray(data) || data.length === 0) {
        container.innerHTML = "<p>No menu items available.</p>";
        return;
      }

      // Group by normalized category key
      const groups = {};
      for (const item of data) {
        const { key, label } = getCategory(item);
        if (!groups[key]) groups[key] = { label, items: [] };
        groups[key].items.push(item);
      }

      // Filter by ?category= if present
      const entries = Object.entries(groups)
        .filter(([key]) => !selected || key === selected)
        // optional: sort by label
        .sort((a, b) => a[1].label.localeCompare(b[1].label));

      if (entries.length === 0) {
        container.innerHTML = "<p>No items in this category.</p>";
        return;
      }

      for (const [key, group] of entries) {
        const section = document.createElement("section");
        section.className = "menu-category";

        const heading = document.createElement("h2");
        heading.textContent = group.label.toUpperCase();
        section.appendChild(heading);

        const grid = document.createElement("div");
        grid.className = "menu-grid";

        for (const item of group.items) {
          // prefer image field if your serializer exposes it
          const imgField = item.image || item.thumbnail || null;
          const fallback = `/static/main/img/menu/${slugify(item.name)}.png`;
          const imgSrc = imgField || fallback;

          // price can be string or number
          const rawPrice = item.price;
          const price =
            typeof rawPrice === "number"
              ? rawPrice.toFixed(2)
              : !isNaN(rawPrice)
              ? Number(rawPrice).toFixed(2)
              : rawPrice;

          const card = document.createElement("div");
          card.className = "menu-item";
          card.innerHTML = `
            <img src="${imgSrc}" alt="${item.name}"
                 onerror="this.onerror=null;this.src='/static/main/img/menu/placeholder.png';">
            <a href="/menu/products/${item.id}/">
              <h3>${item.name}</h3>
            </a>
            <h3><span>$${price}</span></h3>
            <p>${item.description || ""}</p>
          `;
          grid.appendChild(card);
        }

        section.appendChild(grid);
        container.appendChild(section);
      }
    })
    .catch((err) => {
      console.error("Error fetching menu:", err);
      container.innerHTML = "<p>Error loading menu.</p>";
    });
});