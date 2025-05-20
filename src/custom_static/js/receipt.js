function openReceiptModal(receiptId) {
    document.getElementById(`receipt-modal-${receiptId}`).classList.remove('hidden');
    document.getElementById(`receipt-modal-${receiptId}`).classList.add('modal-open');
}

function closeReceiptModal(receiptId) {
    document.getElementById(`receipt-modal-${receiptId}`).classList.add('hidden');
    document.getElementById(`receipt-modal-${receiptId}`).classList.remove('modal-open');
}

// Auto-open if receipt ID passed in URL
document.addEventListener("DOMContentLoaded", () => {
    const openId = new URLSearchParams(window.location.search).get("open");
    if (openId) openReceiptModal(openId);
});
