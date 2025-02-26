import React, { Suspense } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ErrorBoundary } from "react-error-boundary";
import { AuthProvider } from "./context/AuthContext";
import { ReportProvider } from "./context/ReportContext";
import { routes } from "./constants/routes"; // Import centralized routes
import LoadingSpinner from "./components/common/LoadingSpinner"; // Reusable loading spinner
import PrivateRoute from "./components/PrivateRoute"; // Private route component
import Sidebar from "./components/layout/Sidebar"; // Sidebar component
import Header from "./components/layout/Header"; // Header component
import LoginPage from "./pages/LoginPage"; // Import LoginPage

// 🔹 Error Fallback Component
function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert" className="p-4 text-red-700">
      <h2 className="font-bold">Something went wrong:</h2>
      <p>{error.message}</p>
      <button onClick={resetErrorBoundary} className="bg-blue-500 text-white px-4 py-2 mt-2">
        Retry
      </button>
    </div>
  );
}

// 🔹 MainLayout - Structure with Sidebar, Header & Content
function MainLayout() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-grow flex flex-col overflow-auto">
        <Header />
        <div className="p-6">
          <ErrorBoundary FallbackComponent={ErrorFallback}>
            <Suspense fallback={<LoadingSpinner />}>
              <Routes>
                {routes.map((route) => (
                  <Route
                    key={route.path}
                    path={route.path}
                    element={
                      route.protected ? (
                        <PrivateRoute>{route.element}</PrivateRoute>
                      ) : (
                        route.element
                      )
                    }
                  />
                ))}
              </Routes>
            </Suspense>
          </ErrorBoundary>
        </div>
      </div>
    </div>
  );
}

// 🔹 App Component - Wrap with Providers
function App() {
  return (
    <AuthProvider>
      <ReportProvider>
        <Router>
          <Suspense fallback={<LoadingSpinner />}>
            <Routes>
              <Route path="/login" element={<LoginPage />} /> {/* Use LoginPage here */}
              <Route path="*" element={<MainLayout />} />
            </Routes>
          </Suspense>
        </Router>
      </ReportProvider>
    </AuthProvider>
  );
}

export default App;