/**
 * InventoryOS — Shared JavaScript
 * Handles: delete confirmation modal, flash message auto-dismiss
 */

// ── Delete Confirmation Modal ─────────────────────────────────────────────────

/**
 * Open the delete confirmation modal.
 * @param {string} productName - Human-readable product name shown in the modal.
 * @param {string} deleteUrl   - The POST action URL for the delete form.
 */
function openDeleteModal(productName, deleteUrl) {
  document.getElementById('delete-product-name').textContent = productName;
  document.getElementById('delete-form').action = deleteUrl;
  document.getElementById('delete-modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden'; // prevent scroll behind modal
}

/** Close the delete confirmation modal. */
function closeDeleteModal() {
  document.getElementById('delete-modal').classList.add('hidden');
  document.body.style.overflow = '';
}

// Close modal when clicking outside the dialog box
document.getElementById('delete-modal')?.addEventListener('click', function(e) {
  if (e.target === this) closeDeleteModal();
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeDeleteModal();
});

// ── Flash Message Auto-Dismiss ────────────────────────────────────────────────

// Auto-dismiss flash messages after 5 seconds
setTimeout(function () {
  const flash = document.getElementById('flash-msg');
  if (flash) {
    flash.style.transition = 'opacity 0.5s ease';
    flash.style.opacity = '0';
    setTimeout(() => flash.remove(), 500);
  }
}, 5000);
