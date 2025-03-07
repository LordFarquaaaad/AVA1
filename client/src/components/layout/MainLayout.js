// src/components/layout/MainLayout.js
import React from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Header from "./Header";

function MainLayout() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-grow flex flex-col overflow-auto">
        <Header />
        <div className="p-6">
          <Outlet /> {/* Render nested routes here */}
        </div>
      </div>
    </div>
  );
}

export default MainLayout;