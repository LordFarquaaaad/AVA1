import { lazy } from "react";

const Dashboard = lazy(() => import("../pages/Dashboard"));
const ReportsPage = lazy(() => import("../pages/ReportsPage"));
const SettingsPage = lazy(() => import("../pages/SettingsPage"));
const LoginPage = lazy(() => import("../pages/LoginPage"));
const NotFoundPage = lazy(() => import("../pages/NotFoundPage"));

export const routes = [
  { path: "/", element: <Dashboard />, protected: true },
  { path: "/reports", element: <ReportsPage />, protected: true },
  { path: "/settings", element: <SettingsPage />, protected: true },
  { path: "/login", element: <LoginPage />, protected: false },
  { path: "*", element: <NotFoundPage />, protected: false },
];