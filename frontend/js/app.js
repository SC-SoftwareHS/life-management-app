// UI Utilities
const UI = {
    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
    },

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    },

    showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.classList.remove('hidden');
        setTimeout(() => toast.classList.add('hidden'), 3000);
    },

    showError(message, elementId) {
        const errorEl = document.getElementById(elementId);
        errorEl.textContent = message;
        errorEl.classList.remove('hidden');
    },

    showModal(title, content) {
        const modal = document.getElementById('modal');
        const modalBody = document.getElementById('modal-body');
        modalBody.innerHTML = `<h2>${title}</h2>${content}`;
        modal.classList.remove('hidden');
    },

    hideModal() {
        document.getElementById('modal').classList.add('hidden');
    }
};

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Auth event listeners
    document.getElementById('login').addEventListener('submit', (e) => Auth.handleLogin(e));
    document.getElementById('register').addEventListener('submit', (e) => Auth.handleRegister(e));
    document.getElementById('show-register').addEventListener('click', (e) => {
        e.preventDefault();
        Auth.toggleForms();
    });
    document.getElementById('show-login').addEventListener('click', (e) => {
        e.preventDefault();
        Auth.toggleForms();
    });
    document.getElementById('logout-btn').addEventListener('click', () => Auth.handleLogout());

    // Modal close
    document.querySelector('.modal-close').addEventListener('click', () => UI.hideModal());
    document.getElementById('modal').addEventListener('click', (e) => {
        if (e.target.id === 'modal') UI.hideModal();
    });

    // Initialize authentication
    Auth.init();
});
