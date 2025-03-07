// src/App.js
import React, { Suspense } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { ErrorBoundary } from "react-error-boundary";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { ReportProvider } from "./context/ReportContext";
import LoadingSpinner from "./components/common/LoadingSpinner";
import { routes } from "./constants/routes";

// 🔹 Top-Level Error Boundary
function AppErrorBoundary({ children }) {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => {
        window.location.reload(); // Reset by reloading the page
      }}
    >
      {children}
    </ErrorBoundary>
  );
}

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

// 🔹 **PrivateRoute Component**
function PrivateRoute({ isProtected, children }) {
  const { user, loading } = useAuth();

  // Show loading spinner while authentication status is being checked
  if (loading) {
    return <LoadingSpinner />;
  }

  // Redirect unauthenticated users from protected routes to the login page
  if (isProtected && !user) {
    return <Navigate to="/login" replace />;
  }

  // Redirect authenticated users away from non-protected routes (e.g., login page)
  if (!isProtected && user) {
    return <Navigate to="/" replace />;
  }

  // Render children if authenticated or if the route is not protected
  return children;
}

// 🔹 **App Component**
function App() {
  return (
    <Router>
      <AuthProvider>
        <ReportProvider>
          <Suspense fallback={<LoadingSpinner />}>
            <AppErrorBoundary>
              <Routes>
                {/* Map over the routes configuration */}
                {routes.map((route, index) => {
                  const { path, element, protected: isProtected, children } = route;

                  return (
                    <Route
                      key={index}
                      path={path}
                      element={
                        isProtected ? (
                          <PrivateRoute isProtected={isProtected}>
                            {element}
                          </PrivateRoute>
                        ) : (
                          element
                        )
                      }
                    >
                      {/* Render nested routes */}
                      {children &&
                        children.map((child, childIndex) => {
                          const { path: childPath, element: childElement } = child;
                          return (
                            <Route
                              key={childIndex}
                              path={childPath}
                              element={
                                <PrivateRoute isProtected={isProtected}>
                                  {childElement}
                                </PrivateRoute>
                              }
                            />
                          );
                        })}
                    </Route>
                  );
                })}
              </Routes>
            </AppErrorBoundary>
          </Suspense>
        </ReportProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;