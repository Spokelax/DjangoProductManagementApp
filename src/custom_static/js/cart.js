// Cart management
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function updateCartDisplay() {

    const cartItemsDiv = document.getElementById('cart-items');
    const cartCount = document.getElementById('cart-count');
    const cartTotalDiv = document.getElementById('cart-total');
    cartItemsDiv.innerHTML = '';
    let total = 0;
    const uniqueProducts = new Set(cart.map(item => item.productId)).size;
    cartCount.textContent = uniqueProducts;

    if (cart.length === 0) {
        cartItemsDiv.innerHTML = '<p class="text-gray-500">Cart is empty</p>';
        cartTotalDiv.textContent = '';
        document.getElementById('cart-actions').classList.add('hidden');
        return;
    }

    document.getElementById('cart-actions').classList.remove('hidden');
    cart.forEach((item, index) => {

        let expirationText = 'N/A';
        let expirationColor = 'text-gray-500';

        if (item.batchExpiration) {
            const today = new Date();
            const expDate = new Date(item.batchExpiration);
            const daysDiff = Math.ceil((expDate - today) / (1000 * 60 * 60 * 24));
            if (daysDiff <= 0) {
                expirationText = `Expired (since ${item.batchExpiration})`;
                expirationColor = 'text-red-500';
            }
            else {
                expirationText = `Expires in ${daysDiff} days (${item.batchExpiration})`;
                expirationColor = daysDiff < 5 ? 'text-red-400' :
                    daysDiff < 14 ? 'text-orange-400' : 'text-green-400';
            }
        }

        const itemDiv = document.createElement('div');
        itemDiv.className = 'flex justify-between items-center';
        itemDiv.innerHTML = `
            <div>
        
            <p class="text-sm text-gray-500">Batch #${item.batchId}</p>
            <p class="font-semibold">${item.productName} (${item.quantity}/${item.availableStock})</p>
            <p class="text-sm ${expirationColor}">${expirationText}</p>
                <input type="number" min="1" max="${item.availableStock}" value="${item.quantity}" 
                    class="input input-bordered w-20" onchange="updateQuantity(${index}, this.value)">
            </div>
            <div>
                <p>€${(item.price * item.quantity).toFixed(2)}</p>

                <button type="button" class="btn btn-sm btn-error"
                    onmousedown="event.preventDefault()"
                    onclick="removeFromCart(${index})">Remove
                </button>

            </div>
        `;
        cartItemsDiv.appendChild(itemDiv);
        total += item.price * item.quantity;
    });
    cartTotalDiv.textContent = `Total: €${total.toFixed(2)}`;
}

function addToCart(productId, productName, batchId, batchExpiration, quantity, price, availableStock) {
    const roundedPrice = parseFloat(price.toFixed(2));
    const existingItem = cart.find(item => item.productId === productId && item.batchId === batchId);
    if (existingItem) {
        const newQuantity = existingItem.quantity + parseInt(quantity);
        if (newQuantity > availableStock) {
            alert(`Cannot add ${newQuantity} items; only ${availableStock} available in this batch.`);
            return;
        }
        existingItem.quantity = newQuantity;
    } else {
        if (parseInt(quantity) > availableStock) {
            alert(`Cannot add ${quantity} items; only ${availableStock} available in this batch.`);
            return;
        }
        cart.push({
            productId,
            productName,
            batchId,
            batchExpiration,
            quantity: parseInt(quantity),
            price: roundedPrice,
            availableStock
        });
    }
    saveCart();
    updateCartDisplay();
}

function updateQuantity(index, quantity) {
    quantity = parseInt(quantity);
    if (quantity < 1) {
        removeFromCart(index);
        return;
    }
    if (quantity > cart[index].availableStock) {
        alert(`Cannot set ${quantity} items; only ${cart[index].availableStock} available in this batch.`);
        return;
    }
    cart[index].quantity = quantity;
    saveCart();
    updateCartDisplay();
}

function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    updateCartDisplay();
}

function clearCart() {
    cart = [];
    saveCart();
    updateCartDisplay();
    document.getElementById('checkout-form').classList.add('hidden');
}

async function showBatchModal(productId) {
    const response = await fetch(`/api/product/${productId}/batches/`);
    const batches = await response.json();
    const modal = document.getElementById('batch-modal');
    const batchOptions = document.getElementById('batch-options');
    const productNameSpan = document.getElementById('modal-product-name');
    batchOptions.innerHTML = '';
    productNameSpan.textContent = batches.product_name;

    // Calculate quantities already in cart for this product
    const cartQuantities = {};
    cart.forEach(item => {
        if (item.productId === productId) {
            cartQuantities[item.batchId] = (cartQuantities[item.batchId] || 0) + item.quantity;
        }
    });

    if (batches.batches.length === 0 || batches.batches.every(batch => batch.available_stock <= (cartQuantities[batch.id] || 0))) {
        batchOptions.innerHTML = '<p class="text-red-500">No batches available</p>';
    } else {
        batches.batches.forEach(batch => {
            const cartQuantity = cartQuantities[batch.id] || 0;
            const effectiveStock = batch.available_stock - cartQuantity;
            if (effectiveStock <= 0) return; // Skip batches with no remaining stock

            let expirationText = 'N/A';
            let expirationColor = 'text-gray-500';
            if (batch.expiration_date) {
                const today = new Date();
                const expDate = new Date(batch.expiration_date);
                const daysDiff = Math.ceil((expDate - today) / (1000 * 60 * 60 * 24));

                if (daysDiff <= 0) {
                    expirationText = `Expired (since ${batch.expiration_date})`;
                    expirationColor = 'text-red-500';
                } else {
                    expirationText = `Expires in ${daysDiff} days (${batch.expiration_date})`;
                    expirationColor = daysDiff < 5 ? 'text-red-400' :
                        daysDiff < 14 ? 'text-orange-400' : 'text-green-400';
                }
            }

            const div = document.createElement('div');
            div.className = 'flex justify-between items-center';
            div.innerHTML = `
                <div>
                    <p class="${expirationColor}">${expirationText}</p>
                    <p>Available: ${effectiveStock}</p>
                </div>
                <div class="flex items-center space-x-2">
                
                    <input type="number" min="1" max="${effectiveStock}" value="1" 
                        class="input input-bordered w-20" id="quantity-${batch.id}">

                    <button class="btn btn-primary" 
                        onclick="addToCart(${productId}, '${batches.product_name}', ${batch.id}, 
                        '${batch.expiration_date || ''}', document.getElementById('quantity-${batch.id}').value, 
                        ${batches.price}, ${batch.available_stock}); closeBatchModal()">Add</button>
                </div>
            `;
            batchOptions.appendChild(div);
        });
    }
    modal.classList.add('modal-open');
}

function closeBatchModal() {
    document.getElementById('batch-modal').classList.remove('modal-open');
}

document.getElementById('checkout-cart').addEventListener('click', () => {
    document.getElementById('checkout-form').classList.remove('hidden');
});

document.getElementById('cancel-checkout').addEventListener('click', () => {
    document.getElementById('checkout-form').classList.add('hidden');
});

document.getElementById('confirm-checkout').addEventListener('click', async () => {
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenElement) {
        alert('Error: CSRF token not found. Please refresh the page and try again.');
        return;
    }
    const response = await fetch('/api/checkout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfTokenElement.value
        },
        body: JSON.stringify({ items: cart })
    });
    const result = await response.json();
    if (result.success) {
        document.getElementById('checkout-form').classList.add('hidden');
        cart = [];
        saveCart();
        updateCartDisplay();
        location.reload();
    } else {
        alert(result.error);
    }
});

document.getElementById('clear-cart').addEventListener('click', clearCart);

updateCartDisplay();

document.querySelectorAll('.dropdown').forEach(dropdown => {
    dropdown.addEventListener('focusout', () => {
        setTimeout(() => {
            if (!dropdown.contains(document.activeElement)) {
                document.getElementById('checkout-form').classList.add('hidden');
            }
        }, 100); // Slight delay to allow DOM updates
    });
});