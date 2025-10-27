// API Configuration
const CONFIG = {
    // For local development - use same origin as frontend
    get API_URL_LOCAL() {
        // If accessing via 127.0.0.1, use that; if via localhost, use localhost
        return window.location.origin;
    },

    // For production - auto-detect based on current domain
    get API_URL_PRODUCTION() {
        // Use the same origin as the frontend (Railway serves both on same domain)
        return window.location.origin;
    },

    // Auto-detect environment
    get API_BASE_URL() {
        // Always use the same origin as the frontend
        return window.location.origin;
    }
};

// Export for use in api.js
window.CONFIG = CONFIG;
