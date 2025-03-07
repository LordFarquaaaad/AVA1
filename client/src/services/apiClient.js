// src/services/apiClient.js
import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

const apiClient = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
  timeout: parseInt(process.env.REACT_APP_API_TIMEOUT, 10) || 30000,
});

let isRefreshing = false;
let failedQueue = [];
let refreshRetryCount = 0;
const MAX_REFRESH_RETRIES = 2;

// 🔹 **Helper Function: Decode JWT & Check Expiration**
const isTokenExpired = (token) => {
  if (!token) return true;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.exp * 1000 < Date.now();
  } catch (e) {
    console.error("Invalid JWT format:", e);
    return true;
  }
};

// 🔹 **Helper to Get Cookie**
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

// 🔹 **Helper to Clear Cookies**
const clearCookies = () => {
  document.cookie.split(";").forEach((cookie) => {
    const eqPos = cookie.indexOf("=");
    const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
    document.cookie = `${name}=; max-age=0; path=/; domain=${window.location.hostname}`;
  });
};

// 🔹 **Process Failed Requests Queue**
const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) prom.reject(error);
    else prom.resolve(token);
  });
  failedQueue = [];
};

// 🔹 **Queue with Timeout**
const queueWithTimeout = (promise, timeoutMs = 5000) =>
  Promise.race([
    promise,
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Request timeout during token refresh")), timeoutMs)
    ),
  ]);

// 🔹 **Refresh Token Function with Redirect Callback**
let redirectCallback = null;
let isPublicRoute = false; // Flag to indicate if the current route is public
export const setRedirectCallback = (callback) => (redirectCallback = callback);
export const setIsPublicRoute = (value) => (isPublicRoute = value); // New method to set public route status

const refreshToken = async () => {
  if (refreshRetryCount >= MAX_REFRESH_RETRIES) {
    console.error(`❌ Max refresh retries (${MAX_REFRESH_RETRIES}) exceeded`);
    clearCookies();
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    if (redirectCallback) {
      redirectCallback("Max refresh retries exceeded");
    } else {
      setTimeout(() => {
        alert("Session expired. Redirecting to login...");
        window.location.href = "/auth/login";
      }, 1000);
    }
    processQueue(new Error("Max refresh retries exceeded"), null);
    return null;
  }

  try {
    console.log(`🔄 Attempting to refresh token (Attempt ${refreshRetryCount + 1})...`);
    const response = await apiClient.post("/auth/refresh", {}, { withCredentials: true });
    const newAccessToken = response.data.access_token;
    const newRefreshToken = response.data.refresh_token;

    if (!newAccessToken) throw new Error("No new access token received");

    refreshRetryCount = 0;
    localStorage.setItem("access_token", newAccessToken);
    if (newRefreshToken) localStorage.setItem("refresh_token", newRefreshToken);
    apiClient.defaults.headers.common["Authorization"] = `Bearer ${newAccessToken}`;
    processQueue(null, newAccessToken);
    return newAccessToken;
  } catch (error) {
    console.error("❌ Refresh Token Failed:", error.response?.status, error.response?.data || error.message);
    refreshRetryCount++;
    processQueue(error, null);
    if (refreshRetryCount >= MAX_REFRESH_RETRIES && redirectCallback) {
      redirectCallback("Token refresh failed after max retries");
    }
    return null;
  } finally {
    isRefreshing = false;
  }
};

// 🔹 **Request Interceptor**
apiClient.interceptors.request.use(
  async (config) => {
    const accessToken = localStorage.getItem("access_token") || getCookie("access_token_cookie");
    const refreshToken = localStorage.getItem("refresh_token") || getCookie("refresh_token_cookie");

    // Skip token refresh logic on public routes
    if (isPublicRoute) {
      delete config.headers.Authorization;
      return config;
    }

    if (!accessToken || isTokenExpired(accessToken)) {
      console.warn("🔄 Access token expired or missing, attempting refresh...");
      if (!isRefreshing && refreshToken) {
        isRefreshing = true;
        const newToken = await refreshToken();
        if (newToken) {
          config.headers.Authorization = `Bearer ${newToken}`;
        } else {
          return Promise.reject(new Error("Failed to refresh token"));
        }
      } else {
        return Promise.reject(new Error("No refresh token available"));
      }
    } else {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// 🔹 **Response Interceptor** (unchanged)
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      console.error("❌ Unauthorized request, attempting token refresh...");
      originalRequest._retry = true;

      if (!isRefreshing) {
        isRefreshing = true;
        const newAccessToken = await refreshToken();
        if (newAccessToken) {
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return apiClient(originalRequest);
        }
      }

      return queueWithTimeout(
        new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
      ).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`;
        return apiClient(originalRequest);
      }).catch((err) => Promise.reject(err));
    }

    if (error.response?.status === 403) {
      console.error("❌ Forbidden: You do not have permission to access this resource.");
    } else if (error.response?.status === 500) {
      console.error("❌ Internal Server Error: Please try again later.");
    }

    return Promise.reject(error);
  }
);

export default apiClient;

