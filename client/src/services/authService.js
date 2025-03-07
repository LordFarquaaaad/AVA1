// src/services/authService.js
import apiClient from "./apiClient";

// Helper function to check if a token is expired
const isTokenExpired = (token) => {
  if (!token) return true;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.exp * 1000 < Date.now(); // Check if token expiration time is in the past
  } catch (e) {
    console.error("Invalid JWT format:", e);
    return true;
  }
};

const authService = {
  login: async (identifier, password) => {
    try {
      const response = await apiClient.post("/auth/login", { identifier, password });
      console.log("📌 Login response:", response.data, "Cookies:", document.cookie);

      if (response.data.access_token) {
        localStorage.setItem("access_token", response.data.access_token);
        apiClient.defaults.headers.common["Authorization"] = `Bearer ${response.data.access_token}`;
      }

      if (response.data.refresh_token) {
        localStorage.setItem("refresh_token", response.data.refresh_token);
      }

      return response.data;
    } catch (error) {
      console.error("❌ Login failed:", error.response?.data?.message || error.message);
      throw new Error(error.response?.data?.message || "Login failed. Please try again.");
    }
  },

  getCurrentUser: async () => {
    try {
      const accessToken = localStorage.getItem("access_token");

      // Check if the access token is expired
      if (!accessToken || isTokenExpired(accessToken)) {
        console.warn("🔄 Access token expired or missing, attempting refresh...");
        const newAccessToken = await authService.refreshToken();
        if (!newAccessToken) {
          throw new Error("Failed to refresh access token");
        }
      }

      const response = await apiClient.get("/auth/me");
      console.log("📌 Current user response:", response.data);
      return response.data;
    } catch (error) {
      console.error("❌ Failed to fetch current user:", error.response?.data?.message || error.message);
      throw new Error(error.response?.data?.message || "Failed to fetch user data. Please try again.");
    }
  },

  refreshToken: async () => {
    try {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
        console.warn("🚨 No refresh token found!");
        throw new Error("No refresh token available");
      }

      const response = await apiClient.post("/auth/refresh", {}, {
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      });

      if (response.data.access_token) {
        console.log("🔄 New Access Token Received:", response.data.access_token);
        localStorage.setItem("access_token", response.data.access_token);
        apiClient.defaults.headers.common["Authorization"] = `Bearer ${response.data.access_token}`;
        return response.data.access_token;
      } else {
        throw new Error("No new access token received");
      }
    } catch (error) {
      console.error("❌ Refresh Token Failed:", error.response?.data?.message || error.message);
      throw new Error(error.response?.data?.message || "Failed to refresh token. Please log in again.");
    }
  },

  logout: async () => {
    try {
      await apiClient.post("/auth/logout");
    } catch (error) {
      console.warn("⚠️ Logout request failed, forcing token reset.");
    } finally {
      // Clear tokens from localStorage
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");

      // Clear tokens from cookies
      document.cookie = "access_token_cookie=; max-age=0; path=/";
      document.cookie = "refresh_token_cookie=; max-age=0; path=/";

      // Redirect to login page
      window.location.href = "/auth/login";
    }
  },
};

export default authService;
