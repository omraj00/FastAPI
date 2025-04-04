/**
 * Blog Page Tracker
 * 
 * This script captures page load events and sends tracking data to the backend.
 * It collects:
 * - Identity ID from cookies (if available)
 * - Current page URL
 * - Session ID (generated if not exists)
 */

// Helper function to get a cookie value by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Helper function to set a cookie
function setCookie(name, value, days) {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = `; expires=${date.toUTCString()}`;
    }
    document.cookie = `${name}=${value}${expires}; path=/`;
}

// Generate a random session ID if not exists
function getOrCreateSessionId() {
    let sessionId = getCookie('sessionId');
    if (!sessionId) {
        sessionId = 'sess_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        setCookie('sessionId', sessionId, 1); // Session cookie expires in 1 day
    }
    return sessionId;
}

// Get tenant ID from the page (this would be set server-side in a real implementation)
// For demonstration, we'll default to 1 if not found
function getTenantId() {
    // In a real implementation, this would be injected by the server
    // based on the current domain/tenant
    return 1; 
}

// Function to track page view
function trackPageView() {
    const identityId = getCookie('identityId');
    const sessionId = getOrCreateSessionId();
    const pageUrl = window.location.href;
    const tenantId = getTenantId();

    // Prepare data for API call
    const data = {
        identity_id: identityId,
        session_id: sessionId,
        page_url: pageUrl,
        tenant_id: tenantId
    };

    // Send tracking data to the backend
    fetch('/api/track-pageview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            console.error('Error tracking page view:', response.statusText);
        }
        return response.json();
    })
    .then(data => console.log('Page view tracked successfully'))
    .catch(error => console.error('Error tracking page view:', error));
}

// Track page view on page load
document.addEventListener('DOMContentLoaded', trackPageView);
