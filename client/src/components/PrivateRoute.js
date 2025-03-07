// src/components/PrivateRoute.js
import React, { useEffect } from "react";
import { useLocation, Outlet, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import LoadingSpinner from "./common/LoadingSpinner";

function PrivateRoute({ isProtected, children }) {
  const { user, loading, checkAuthStatus } = useAuth();
  const location = useLocation();

  // Debugging: Log route protection and user status
  console.log("PrivateRoute - isProtected:", isProtected, "user:", user, "loading:", loading);

  // Trigger auth check only for protected routes when not loading
  useEffect(() => {
    if (isProtected && !loading) {
      checkAuthStatus(true);
    }
  }, [isProtected, loading, checkAuthStatus]);

  // Show loading spinner while authentication status is being checked
  if (loading) {
    return <LoadingSpinner />;
  }

  // Redirect unauthenticated users from protected routes to the login page
  if (isProtected && !user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Redirect authenticated users away from non-protected routes (e.g., login page)
  if (!isProtected && user) {
    return <Navigate to="/" replace />;
  }

  // Render children if provided, otherwise render nested routes using Outlet
  return children ? children : <Outlet />;
}

export default PrivateRoute;