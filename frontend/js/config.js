// API Configuration
// This will be updated with production URL after backend deployment
const CONFIG = {
    // For local development
    API_URL_LOCAL: 'http://localhost:8000',

    // For production - UPDATE THIS after deploying backend to Railway/Render
    API_URL_PRODUCTION: 'https://your-backend-app.railway.app', // CHANGE THIS

    // Auto-detect environment
    get API_BASE_URL() {
        // If running on localhost, use local API
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return this.API_URL_LOCAL;
        }
        // Otherwise use production API
        return this.API_URL_PRODUCTION;
    }
};

// Export for use in api.js
window.CONFIG = CONFIG;
