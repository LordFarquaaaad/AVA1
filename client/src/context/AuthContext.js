import React, { createContext, useContext, useState, useEffect } from "react";
import authService from "../services/authService"; // Import authService

// Create the context
const AuthContext = createContext();

// AuthProvider component
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true); // Add loading state

  // Fetch the current user on initial load
  useEffect(() => {
    const fetchCurrentUser = async () => {
      try {
        const userData = await authService.getCurrentUser();
        setUser(userData);
      } catch (error) {
        setUser(null); // No user is logged in
      } finally {
        setLoading(false); // Stop loading
      }
    };

    fetchCurrentUser();
  }, []);

  const login = async (username, password) => {
    try {
      const userData = await authService.login(username, password);
      setUser(userData); // Set the user data returned from the backend
    } catch (error) {
      throw error; // Propagate the error
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
      setUser(null); // Clear the user data
    } catch (error) {
      throw error; // Propagate the error
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook to use the AuthContext
export function useAuth() {
  return useContext(AuthContext);
}

