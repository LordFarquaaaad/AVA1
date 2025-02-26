import React from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext"; // Use useAuth instead of AuthContext

function PrivateRoute({ children }) {
  const { user, loading } = useAuth(); // Use loading state
  const location = useLocation();

  if (loading) {
    return <div>Loading...</div>; // Show loading spinner while checking authentication
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

export default PrivateRoute;