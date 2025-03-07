// src/context/AuthContext.js (unchanged core logic, ensure token usage)
import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { useLocation } from "react-router-dom";
import authService from "../services/authService";
import { setIsPublicRoute } from "../services/apiClient";

const AuthContext = createContext();

export function AuthProvider({ children, onRedirect }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false); // Start false
  const [error, setError] = useState(null);
  const location = useLocation();

  const publicRoutes = ["/login", "/auth/register", "/"]; // Match your routes.js

  const redirectToLogin = useCallback(
    (reason) => {
      console.log(`🔄 Redirecting to /login due to: ${reason}`);
      setUser(null);
      setError(`Authentication failed: ${reason}. Redirecting to login...`);
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      if (onRedirect) onRedirect("/login");
    },
    [onRedirect]
  );

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

  const checkAuthStatus = useCallback(
    async (isProtectedRoute = false) => {
      if (!isProtectedRoute) {
        setLoading(false);
        return;
      }
      console.log("Checking auth status...");
      try {
        setLoading(true);
        setError(null);

        const accessToken = localStorage.getItem("access_token");
        const refreshToken = localStorage.getItem("refresh_token");

        if (!accessToken || isTokenExpired(accessToken)) {
          if (refreshToken) {
            const newAccessToken = await authService.refreshToken();
            if (newAccessToken) {
              localStorage.setItem("access_token", newAccessToken);
            } else {
              throw new Error("Failed to refresh access token");
            }
          } else {
            throw new Error("No refresh token available");
          }
        }

        const userData = await authService.getCurrentUser();
        setUser(userData?.user || null);
      } catch (error) {
        console.error("Auth check failed:", error.message, error.response?.status);
        setUser(null);
        if (error.response?.status === 401 || !localStorage.getItem("access_token")) {
          redirectToLogin(error.response?.status === 401 ? "Unauthorized" : error.message);
        } else {
          setError(error.message || "Failed to fetch user.");
        }
      } finally {
        setLoading(false);
      }
    },
    [redirectToLogin]
  );

  useEffect(() => {
    console.log("AuthProvider useEffect triggered, pathname:", location.pathname); // Debug
    if (!location) {
      console.warn("Location is undefined, skipping auth check");
      setLoading(false);
      return;
    }

    const isPublicRoute = publicRoutes.includes(location.pathname);
    console.log("Current pathname:", location.pathname, "Is public route?", isPublicRoute); // Debug
    setIsPublicRoute(isPublicRoute);
    // Do not call checkAuthStatus here; let PrivateRoute trigger it
  }, [location.pathname]); // Only react to route changes

  const login = async (identifier, password) => {
    try {
      setLoading(true);
      setError(null);
      const userData = await authService.login(identifier, password);
      console.log("Login successful, user:", userData.user);
      setUser(userData.user);
      await checkAuthStatus(true);
      const next = new URLSearchParams(window.location.search).get("next") || "/";
      if (onRedirect) onRedirect(next);
    } catch (error) {
      setError(error.message || "Login failed.");
      console.error("Login error:", error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      setLoading(true);
      setError(null);
      await authService.logout();
      redirectToLogin("User logged out");
    } catch (error) {
      setError("Logout failed.");
      console.error("Logout error:", error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    checkAuthStatus,
    redirectToLogin,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}

export default AuthContext;