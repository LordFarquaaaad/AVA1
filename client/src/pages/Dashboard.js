import React from "react";
import { useAuth } from "../context/AuthContext"; // Use useAuth instead of AuthContext

function Dashboard() {
  const { user } = useAuth(); // Use the useAuth hook

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {user ? user.username : "Guest"}!</p>
    </div>
  );
}

export default Dashboard;

  