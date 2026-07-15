// JavaScript for Kerala Street index page
// Handles cart, menu filtering, and checkout

const deliveryFee = 2;
const currencySymbol = "£";
const cart = new Map();

window.addEventListener('DOMContentLoaded', function() {
    const cartItemsEl = document.getElementById("cartItems");
    const cartSubtotalEl = document.getElementById("cartSubtotal");
    const cartDeliveryEl = document.getElementById("cartDelivery");
    const cartTotalEl = document.getElementById("cartTotal");
    const menuHeading = document.getElementById("menuHeading");
    const menuGrid = document.getElementById("menuGrid");
    const menuEmpty = document.getElementById("menuEmpty");
    const subCategoryTabs = document.getElementById("subCategoryTabs");
    const searchInput = document.getElementById("menuSearch");
    const vegOnlyToggle = document.getElementById("vegOnly");
    const offerOnlyToggle = document.getElementById("offerOnly");
    const categoryButtons = document.querySelectorAll(".category-btn");
    const menuItems = Array.from(document.querySelectorAll(".menu-item-card"));
    let activeCategory = "Combo Offers";
    let activeSub = "All";

    const updateTotals = () => {
        let subtotal = 0;
        cart.forEach((item) => {
            subtotal += item.price * item.qty;
        });
        cartSubtotalEl.textContent = `${currencySymbol}${subtotal.toFixed(2)}`;
        cartDeliveryEl.textContent = `${currencySymbol}${deliveryFee.toFixed(2)}`;
        cartTotalEl.textContent = `${currencySymbol}${(subtotal + deliveryFee).toFixed(2)}`;
    };

    const updateSubTabs = () => {
        const subs = new Set([
            "All",
            ...menuItems
                .filter((item) => item.dataset.category === activeCategory)
                .map((item) => item.dataset.sub || "Other")
        ]);

        subCategoryTabs.innerHTML = Array.from(subs)
            .map((sub) => `<button class="sub-tab${sub === activeSub ? " active" : ""}" data-sub="${sub}">${sub}</button>`)
            .join("");

        subCategoryTabs.querySelectorAll(".sub-tab").forEach((tab) => {
            tab.addEventListener("click", () => {
                activeSub = tab.dataset.sub;
                updateSubTabs();
                filterMenu();
            });
        });
    };

    const filterMenu = () => {
        const query = searchInput.value.toLowerCase();
        const vegOnly = vegOnlyToggle.checked;
        const offerOnly = offerOnlyToggle.checked;
        let visibleCount = 0;

        menuItems.forEach((item) => {
            const categoryMatch = item.dataset.category === activeCategory;
            const subMatch = activeSub === "All" || (item.dataset.sub || "Other") === activeSub;
            const text = `${item.dataset.name} ${item.querySelector("p").textContent}`.toLowerCase();
            const searchMatch = text.includes(query);
            const vegMatch = !vegOnly || item.dataset.veg === "true";
            const offerMatch = !offerOnly || item.dataset.offer === "true";

            if (categoryMatch && subMatch && searchMatch && vegMatch && offerMatch) {
                item.style.display = "flex";
                visibleCount += 1;
            } else {
                item.style.display = "none";
            }
        });

        menuEmpty.style.display = visibleCount === 0 ? "block" : "none";
    };

    categoryButtons.forEach((button) => {
        button.addEventListener("click", () => {
            categoryButtons.forEach((btn) => btn.classList.remove("active"));
            button.classList.add("active");
            activeCategory = button.dataset.category;
            activeSub = "All";
            menuHeading.textContent = activeCategory;
            updateSubTabs();
            filterMenu();
        });
    });

    [searchInput, vegOnlyToggle, offerOnlyToggle].forEach((el) => {
        el.addEventListener("input", filterMenu);
        el.addEventListener("change", filterMenu);
    });

    const renderCart = () => {
        if (cart.size === 0) {
            cartItemsEl.innerHTML = '<p class="order-hint">Your cart is empty. Add items to get started.</p>';
            updateTotals();
            return;
        }

        const itemsHtml = Array.from(cart.values()).map((item) => `
            <div class="cart-item">
                <div class="cart-item-info">
                    <h4>${item.name}</h4>
                    <span>${currencySymbol}${item.price.toFixed(2)}</span>
                </div>
                <div class="qty-controls">
                    <button type="button" class="qty-btn" data-action="decrease" data-name="${item.name}">-</button>
                    <span>${item.qty}</span>
                    <button type="button" class="qty-btn" data-action="increase" data-name="${item.name}">+</button>
                    <button type="button" class="remove-btn" data-action="remove" data-name="${item.name}">Remove</button>
                </div>
            </div>
        `).join("");

        cartItemsEl.innerHTML = itemsHtml;
        updateTotals();
    };

    document.querySelectorAll(".add-to-cart").forEach((button) => {
        button.addEventListener("click", () => {
            const card = button.closest(".menu-item-card");
            const name = card.dataset.name;
            const price = Number(card.dataset.price);
            if (cart.has(name)) {
                cart.get(name).qty += 1;
            } else {
                cart.set(name, { name, price, qty: 1 });
            }
            renderCart();
        });
    });

    cartItemsEl.addEventListener("click", (event) => {
        const target = event.target;
        const action = target.dataset.action;
        const name = target.dataset.name;
        if (!action || !name || !cart.has(name)) return;

        const item = cart.get(name);
        if (action === "increase") item.qty += 1;
        if (action === "decrease") item.qty = Math.max(1, item.qty - 1);
        if (action === "remove") cart.delete(name);
        renderCart();
    });

    document.getElementById("checkoutForm").addEventListener("submit", (event) => {
        event.preventDefault();
        if (cart.size === 0) {
            alert("Please add items to your cart.");
            return;
        }

        const name = document.getElementById("orderName").value.trim();
        const phone = document.getElementById("orderPhone").value.trim();
        const address = document.getElementById("orderAddress").value.trim();
        const payment = document.getElementById("orderPayment").value.trim();

        if (!name || !phone || !address || !payment) {
            alert("Please complete all checkout fields.");
            return;
        }

        alert("Order received! We will confirm your order shortly.");
        cart.clear();
        event.target.reset();
        renderCart();
    });

    updateSubTabs();
    filterMenu();
    renderCart();

    // Gallery animation on scroll (fix: run on load and scroll, and on resize)
    function galleryReveal() {
        const images = document.querySelectorAll('.gallery-section .gallery-animate');
        const trigger = window.innerHeight * 0.92;
        images.forEach(img => {
            const rect = img.getBoundingClientRect();
            if (rect.top < trigger) {
                img.classList.add('visible');
            } else {
                img.classList.remove('visible');
            }
        });
    }

    galleryReveal();
    window.addEventListener('scroll', galleryReveal);
    window.addEventListener('resize', galleryReveal);

    // Remove any previous popup modal code if present
    (function removeOldPopup() {
        const old = document.getElementById('popupModalBackdrop');
        if (old) old.remove();
    })();

    // Popup modal for order/reserve
    function showPopupModal() {
        if (document.getElementById('popupModalBackdrop')) return;
        const backdrop = document.createElement('div');
        backdrop.className = 'popup-modal-backdrop';
        backdrop.id = 'popupModalBackdrop';
        backdrop.innerHTML = `
          <div class="popup-modal">
            <button class="popup-close" aria-label="Close">&times;</button>
            <h3>Welcome to Kerala Street</h3>
            <p style="margin-bottom:22px;">What would you like to do?</p>
            <button class="popup-btn" onclick="window.location.href='/menu/'">Order Online</button>
            <button class="popup-btn reserve" onclick="window.location.href='index.html#reservation'">Reserve a Table</button>
          </div>
        `;
        document.body.appendChild(backdrop);
        backdrop.querySelector('.popup-close').onclick = function() {
            backdrop.remove();
        };
        backdrop.onclick = function(e) {
            if (e.target === backdrop) backdrop.remove();
        };
        document.body.style.overflow = 'hidden';
        backdrop.addEventListener('transitionend', function() {
            if (!document.body.contains(backdrop)) document.body.style.overflow = '';
        });
        backdrop.querySelector('.popup-close').addEventListener('click', function() {
            document.body.style.overflow = '';
        });
        backdrop.addEventListener('click', function(e) {
            if (e.target === backdrop) document.body.style.overflow = '';
        });
    }
    window.addEventListener('DOMContentLoaded', function() {
        setTimeout(showPopupModal, 400);
    });
});
