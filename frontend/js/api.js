// API Base URL - use CONFIG if available, otherwise auto-detect
const API_BASE_URL = window.CONFIG?.API_BASE_URL || (
    window.location.hostname === 'localhost'
        ? 'http://localhost:8000'  // Local development
        : window.location.origin   // Production (same domain as frontend)
);

// API Client
class API {
    // Auth endpoints
    static async register(username, email, password, fullName) {
        const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                username,
                email,
                password,
                full_name: fullName
            })
        });
        return this.handleResponse(response);
    }

    static async login(username, password) {
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });
        return this.handleResponse(response);
    }

    static async logout() {
        const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        return this.handleResponse(response);
    }

    static async getCurrentUser() {
        const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
            credentials: 'include'
        });
        return this.handleResponse(response);
    }

    // Life Areas
    static async getLifeAreas() {
        const response = await fetch(`${API_BASE_URL}/api/areas/`, {
            credentials: 'include'
        });
        return this.handleResponse(response);
    }

    // Goals
    static async getGoals(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE_URL}/api/goals/?${params}`, {
            credentials: 'include'
        });
        return this.handleResponse(response);
    }

    static async createGoal(data) {
        const response = await fetch(`${API_BASE_URL}/api/goals/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    static async updateGoal(id, data) {
        const response = await fetch(`${API_BASE_URL}/api/goals/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    static async deleteGoal(id) {
        const response = await fetch(`${API_BASE_URL}/api/goals/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        if (response.status === 204) return true;
        return this.handleResponse(response);
    }

    // Habits
    static async getHabits(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE_URL}/api/habits/?${params}`, {
            credentials: 'include'
        });
        return this.handleResponse(response);
    }

    static async createHabit(data) {
        const response = await fetch(`${API_BASE_URL}/api/habits/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    static async checkinHabit(id, data = {}) {
        const response = await fetch(`${API_BASE_URL}/api/habits/${id}/checkin`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    static async deleteHabit(id) {
        const response = await fetch(`${API_BASE_URL}/api/habits/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        if (response.status === 204) return true;
        return this.handleResponse(response);
    }

    // Tasks
    static async getTasks(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE_URL}/api/tasks/?${params}`, {
            credentials: 'include'
        });
        return this.handleResponse(response);
    }

    static async createTask(data) {
        const response = await fetch(`${API_BASE_URL}/api/tasks/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    static async updateTask(id, data) {
        const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    static async deleteTask(id) {
        const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        if (response.status === 204) return true;
        return this.handleResponse(response);
    }

    // Contacts
    static async getContacts(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${API_BASE_URL}/api/contacts/?${params}`, {
            credentials: 'include'
        });
        return this.handleResponse(response);
    }

    static async createContact(data) {
        const response = await fetch(`${API_BASE_URL}/api/contacts/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    static async deleteContact(id) {
        const response = await fetch(`${API_BASE_URL}/api/contacts/${id}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        if (response.status === 204) return true;
        return this.handleResponse(response);
    }

    static async getContactBirthday(id) {
        const response = await fetch(`${API_BASE_URL}/api/contacts/${id}/birthday`, {
            credentials: 'include'
        });
        return this.handleResponse(response);
    }

    // Helper method to handle responses
    static async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
            throw new Error(error.detail || error.message || 'An error occurred');
        }
        return response.json();
    }
}
