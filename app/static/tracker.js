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

// Get tenant ID from the page (this would be set server-side in a real implementation)
async function getTenantId() {
    const domainName = window.location.hostname;

    try {
        const response = await fetch(`/api/get-tenant-id?domain=${domainName}`);
        const data = await response.json();

        if (data.tenant_id && data.is_active) {
            const titleTag = document.getElementById('page-title');
            if (titleTag) {
                titleTag.textContent = data.tenant;
            }
            document.title = data.tenant;

            const blogTitle = `Welcome to Our ${data.tenant}`;
            const h1 = document.getElementById('blog-title');
            if (h1) {
                h1.textContent = blogTitle;
            }

            return data.tenant_id;
        } 
        else if(data.tenant_id) {
            console.log('Tenant is not active');
            return null;
        }
        else {
            console.log('Tenant not found');
            return null;
        }
    } 
    catch (err) {
        console.error('Error fetching tenant info:', err);
        return null;
    }
}

// Function to track page view
async function trackPageView(tenantId) {
    // Returns when tenantId is null or invalid
    if (!tenantId || isNaN(tenantId)) {
        console.error("Invalid tenantId:", tenantId);
        return;
    }

    const identityId = getCookie('identityId');
    const sessionId = getCookie('session_id');
    const pageUrl = window.location.href;

    // Prepare data for API call
    const data = {
        meta_data: {
            identityid: identityId
        },
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
document.addEventListener('DOMContentLoaded', async () => {
    const tenantId = await getTenantId();
    if (tenantId) {
        trackPageView(tenantId);
    }
});
