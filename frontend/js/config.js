// API Configuration
const CONFIG = {
    // For local development
    API_URL_LOCAL: 'http://localhost:8000',

    // For production - auto-detect based on current domain
    get API_URL_PRODUCTION() {
        // Use the same origin as the frontend (Railway serves both on same domain)
        return window.location.origin;
    },

    // Auto-detect environment
    get API_BASE_URL() {
        // If running on localhost, use local API
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return this.API_URL_LOCAL;
        }
        // Otherwise use production API (same domain as frontend)
        return this.API_URL_PRODUCTION;
    }
};

// Export for use in api.js
window.CONFIG = CONFIG;
