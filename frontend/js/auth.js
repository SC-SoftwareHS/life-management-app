// Authentication module
const Auth = {
    currentUser: null,

    async init() {
        // Check if user is already logged in
        try {
            this.currentUser = await API.getCurrentUser();
            this.showApp();
        } catch (error) {
            this.showAuth();
        }
    },

    async handleLogin(e) {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;

        try {
            UI.showLoading();
            const response = await API.login(username, password);
            this.currentUser = response.user;
            this.showApp();
            UI.showToast('Welcome back!', 'success');
        } catch (error) {
            UI.showError(error.message, 'auth-error');
        } finally {
            UI.hideLoading();
        }
    },

    async handleRegister(e) {
        e.preventDefault();
        const username = document.getElementById('register-username').value;
        const email = document.getElementById('register-email').value;
        const fullName = document.getElementById('register-fullname').value;
        const password = document.getElementById('register-password').value;

        try {
            UI.showLoading();
            await API.register(username, email, password, fullName);
            // Auto-login after registration
            const response = await API.login(username, password);
            this.currentUser = response.user;
            this.showApp();
            UI.showToast('Account created successfully!', 'success');
        } catch (error) {
            UI.showError(error.message, 'auth-error');
        } finally {
            UI.hideLoading();
        }
    },

    async handleLogout() {
        try {
            await API.logout();
            this.currentUser = null;
            this.showAuth();
            UI.showToast('Logged out successfully', 'success');
        } catch (error) {
            UI.showToast('Error logging out', 'error');
        }
    },

    showAuth() {
        document.getElementById('auth-screen').classList.remove('hidden');
        document.getElementById('app-screen').classList.add('hidden');
    },

    showApp() {
        document.getElementById('auth-screen').classList.add('hidden');
        document.getElementById('app-screen').classList.remove('hidden');
        document.getElementById('user-name').textContent = this.currentUser.full_name || this.currentUser.username;

        // Load dashboard
        Dashboard.load();
    },

    toggleForms() {
        document.getElementById('login-form').classList.toggle('hidden');
        document.getElementById('register-form').classList.toggle('hidden');
        document.getElementById('auth-error').classList.add('hidden');
    }
};
