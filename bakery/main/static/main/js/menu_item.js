document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("item-container");
  if (!container) return;

  // /menu/<id>
  const match = window.location.pathname.match(/\/menu\/(\d+)/);
  const itemId = match ? match[1] : null;

  const money = (n) => Number(n || 0).toFixed(2);
  const slugify = (t) => String(t||"").toLowerCase().replace(/\s+/g,"-")
    .replace(/[^\w-]+/g,"").replace(/--+/g,"-").replace(/^-+/, "").replace(/-+$/,"");

  function renderProduct(product) {
    const imgSrc = product.picture || `/static/main/img/menu_items/${slugify(product.name)}.png`;
    const base = Number(product.price);

    // ✅ add an outer wrapper with product id (optional but handy)
    container.innerHTML = `
      <div id="product" data-product-id="${product.id}">
        <div class="item">
          <div class="item-picture">
            <img src="${imgSrc}" alt="${product.name}" width="320" height="240"
                 loading="lazy" decoding="async" style="object-fit:cover">
          </div>
          <div class="item-content">
            <h3>${product.name}</h3>
            <h3><span>$<span id="base-price">${money(base)}</span></span></h3>
            <p>${product.description || ""}</p>
          </div>
        </div>

        <div class="addons-section">
          <h3>Available Add-ons</h3>
          <div id="addons-wrap"><p>Loading add-ons…</p></div>

          <div class="quantity-control">
            <label for="item-qty">Quantity:</label>
            <button type="button" id="qty-decrease">-</button>
            <input type="number" id="item-qty" value="1" min="1" style="width:3em;">
            <button type="button" id="qty-increase">+</button>
          </div>

          <div class="total">Total: $<span id="total-price">${money(base)}</span></div>
          <button id="add-to-cart" type="button" class="btn btn-primary">Add to cart</button>
        </div>
      </div>
    `;

    // Quantity counter logic
    const qtyInput = document.getElementById("item-qty");
    document.getElementById("qty-decrease").addEventListener("click", () => {
      qtyInput.value = Math.max(1, Number(qtyInput.value) - 1);
      qtyInput.dispatchEvent(new Event("change"));
    });
    document.getElementById("qty-increase").addEventListener("click", () => {
      qtyInput.value = Number(qtyInput.value) + 1;
      qtyInput.dispatchEvent(new Event("change"));
    });
  }

  function renderAddonsFlat(addons, basePrice) {
    const wrap = document.getElementById("addons-wrap");
    const active = addons.filter(a => a.is_active);

    if (active.length === 0) {
      wrap.innerHTML = "<p>No add-ons for this category.</p>";
      return;
    }

    let html = `<fieldset class="addon-group"><legend>Extras</legend>`;
    for (const a of active) {
      const priceNum = Number(a.price);
      html += `
        <label class="addon-option" style="display:flex;align-items:center;justify-content:space-between;gap:1em;margin-bottom:0.5em;">
          <span style="display:flex;align-items:center;gap:0.5em;">
        <input type="checkbox" class="addon-option" name="addon" value="${a.id}" data-price="${priceNum}">
        ${a.name}
          </span>
          <span class="addon-price">+$${priceNum.toFixed(2)}</span>
        </label>`;
    }
    html += `</fieldset>`;
    wrap.innerHTML = html;

    const totalEl = document.getElementById("total-price");
    const qtyEl   = document.getElementById("item-qty");

    const getQty = () => {
      const n = Number(qtyEl?.value);
      return Number.isFinite(n) && n > 0 ? n : 1;
    };

    const updateTotal = () => {
      let extra = 0;
      wrap.querySelectorAll('input.addon-option[type="checkbox"]:checked')
          .forEach(el => { extra += Number(el.dataset.price || 0); });
      const base = Number(basePrice) || 0;
      totalEl.textContent = ((base + extra) * getQty()).toFixed(2);
    };

    wrap.addEventListener("change", updateTotal);
    qtyEl?.addEventListener("input", updateTotal);
    qtyEl?.addEventListener("change", updateTotal);
    updateTotal();
  }

  // ---- Flow: product → addons(category) ----
  fetch(`/api/products/${itemId}/`)
    .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
    .then(product => {
      renderProduct(product);
      const categoryId = product?.category?.id;
      if (!categoryId) {
        document.getElementById("addons-wrap").innerHTML = "<p>No category; no add-ons.</p>";
        return;
      }
      return fetch(`/api/addons/category/${categoryId}/`)
        .then(r => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
        .then(addons => renderAddonsFlat(addons, Number(product.price)));
    })
    .catch(err => {
      console.error("Error:", err);
      container.innerHTML = "<p>Error loading item or add-ons.</p>";
    });

  // --- Add to cart ---
  function getCsrfToken() {
    const m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : null;
  }
  async function addToCart(productId) {
    const qty = Math.max(1, parseInt(document.getElementById('item-qty').value || '1', 10));
    const addons = Array.from(document.querySelectorAll('input.addon-option:checked')).map(el => el.value);

    const body = new URLSearchParams();
    body.append('qty', String(qty));
    addons.forEach(id => body.append('addons[]', id));

    const res = await fetch(`/shop/cart/add/${productId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body,
      credentials: 'same-origin',
    });

    if (!res.ok) {
      const text = await res.text();
      console.error('Add to cart failed:', res.status, text.slice(0, 500));
      alert(`Add to cart failed (${res.status}). Check console.`);
      return;
    }

    try {
      const data = await res.json();
    } catch {
    }
    alert('Added to cart!');
    document.dispatchEvent(new CustomEvent('cart:updated'));
  }

  document.addEventListener('click', (e) => {
    if (e.target && e.target.id === 'add-to-cart') {
      addToCart(Number(itemId));
    }
  });
});
