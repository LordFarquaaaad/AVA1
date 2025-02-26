import apiClient from "./apiClient";

const authService = {
  // Log in with username & password
  login: async (username, password) => {
    try {
      const response = await apiClient.post("/auth/login", { username, password });
      return response.data.user; // Return the user object from the response
    } catch (error) {
      throw error;
    }
  },

  // Log out (server might remove session, or you might remove local token)
  logout: async () => {
    try {
      await apiClient.post("/auth/logout");
    } catch (error) {
      throw error;
    }
  },

  // Fetch currently logged-in user
  getCurrentUser: async () => {
    try {
      const response = await apiClient.get("/auth/me");
      return response.data.user; // Return the user object from the response
    } catch (error) {
      throw error;
    }
  },
};

export default authService;




