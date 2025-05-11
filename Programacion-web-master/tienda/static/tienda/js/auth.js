// Auth utilities for JWT handling
const auth = {
    // Store tokens in localStorage
    setTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    },

    // Get access token
    getAccessToken() {
        return localStorage.getItem('access_token');
    },

    // Get refresh token
    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    },

    // Remove tokens on logout
    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    },

    // Check if user is authenticated
    isAuthenticated() {
        return !!this.getAccessToken();
    },

    // Login function
    async login(username, password) {
        try {
            const response = await fetch('/api/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            this.setTokens(data.access, data.refresh);
            return true;
        } catch (error) {
            console.error('Login error:', error);
            return false;
        }
    },

    // Refresh token function
    async refreshToken() {
        try {
            const response = await fetch('/api/token/refresh/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    refresh: this.getRefreshToken()
                })
            });

            if (!response.ok) {
                throw new Error('Token refresh failed');
            }

            const data = await response.json();
            this.setTokens(data.access, this.getRefreshToken());
            return true;
        } catch (error) {
            console.error('Token refresh error:', error);
            this.clearTokens();
            return false;
        }
    },

    // Logout function
    logout() {
        this.clearTokens();
        window.location.href = '/login/';
    }
};

// API request utility with automatic token handling
const api = {
    async request(url, options = {}) {
        // Add authorization header if token exists
        const token = auth.getAccessToken();
        if (token) {
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${token}`
            };
        }

        try {
            let response = await fetch(url, options);

            // If token expired, try to refresh and retry
            if (response.status === 401) {
                const refreshSuccess = await auth.refreshToken();
                if (refreshSuccess) {
                    // Retry the request with new token
                    options.headers['Authorization'] = `Bearer ${auth.getAccessToken()}`;
                    response = await fetch(url, options);
                } else {
                    // If refresh failed, redirect to login
                    auth.logout();
                    return null;
                }
            }

            return response;
        } catch (error) {
            console.error('API request error:', error);
            return null;
        }
    },

    // GET request
    async get(url) {
        return this.request(url);
    },

    // POST request
    async post(url, data) {
        return this.request(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
    },

    // PUT request
    async put(url, data) {
        return this.request(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
    },

    // DELETE request
    async delete(url) {
        return this.request(url, {
            method: 'DELETE'
        });
    }
}; 