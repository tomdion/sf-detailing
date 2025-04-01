// src/api/client.ts
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// Function to get CSRF token from cookies
const getCsrfToken = () => {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
};

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Essential for cross-domain cookies
});

// Add CSRF token to every request
apiClient.interceptors.request.use(
  config => {
    const token = getCsrfToken();
    if (token) {
      config.headers['X-CSRFToken'] = token;
    }
    return config;
  },
  error => Promise.reject(error)
);

export default apiClient;