// src/constants/routes.js
import { lazy } from "react";

const Dashboard = lazy(() => import("../pages/Dashboard"));
const ReportsPage = lazy(() => import("../pages/ReportsPage"));
const SettingsPage = lazy(() => import("../pages/SettingsPage"));
const LoginPage = lazy(() => import("../pages/LoginPage"));
const NotFoundPage = lazy(() => import("../pages/NotFoundPage"));
const MainLayout = lazy(() => import("../components/layout/MainLayout")); // Import MainLayout

export const routes = [
  {
    path: "/",
    element: <MainLayout />, // Wrap Dashboard with MainLayout
    protected: true,
    children: [
      { index: true, element: <Dashboard /> }, // Dashboard is the index route
      { path: "dashboard", element: <Dashboard /> },
      { path: "reports", element: <ReportsPage /> },
      { path: "settings", element: <SettingsPage /> },
    ],
  },
  { path: "/login", element: <LoginPage />, protected: false },
  { path: "*", element: <NotFoundPage />, protected: false },
];