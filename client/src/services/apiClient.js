import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000"; // Local Flask server (adjust as needed)

const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // Added timeout for better error handling (10 seconds)
});

// Helper function to set the token in localStorage and apiClient headers
export const setToken = (token) => {
  localStorage.setItem("token", token);
  apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  console.log("📌 Token set:", token.slice(0, 10) + "...");
};

// Helper function to clear the token from localStorage and apiClient headers
export const clearToken = () => {
  localStorage.removeItem("token");
  delete apiClient.defaults.headers.common["Authorization"];
  console.log("📌 Token cleared");
};

// Request Interceptor: Attach Authorization Token Dynamically
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log("📌 Token attached to request:", token.slice(0, 10) + "...");
    } else {
      console.log("📌 No token found in localStorage");
    }
    return config;
  },
  (error) => {
    console.error("❌ Request interceptor error:", error);
    return Promise.reject(error);
  }
);

// Response Interceptor: Global Error Handling
apiClient.interceptors.response.use(
  (response) => response, // Pass successful responses through
  (error) => {
    console.error("❌ API request failed:", {
      status: error.response?.status,
      message: error.message,
      data: error.response?.data,
    });

    // Handle specific status codes
    if (error.response) {
      switch (error.response.status) {
        case 401:
          console.warn("⚠️ Unauthorized (401): Redirecting to login...");
          clearToken(); // Clear the token on 401 errors
          // window.location.href = "/login"; // Uncomment if routing is set up
          break;
        case 403:
          console.warn("⚠️ Forbidden (403): Insufficient permissions");
          break;
        case 500:
          console.warn("⚠️ Server Error (500): Something went wrong on the backend");
          break;
        default:
          console.warn(`⚠️ Unexpected error (${error.response.status})`);
      }
    } else if (error.request) {
      console.error("❌ Network error: No response received");
    }

    return Promise.reject(error); // Propagate error for downstream handling
  }
);

export default apiClient;
