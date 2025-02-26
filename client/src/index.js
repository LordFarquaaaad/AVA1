import React from "react";
import ReactDOM from "react-dom/client"; // <-- Use the new React 18 API
import App from "./App";
import { ThemeProvider } from "./context/theme/ThemeContext"; // Ensure ThemeContext is correct
import "./styles/index.css";

// Get the root element
const root = ReactDOM.createRoot(document.getElementById("root"));

// Render the app using createRoot
root.render(
  <ThemeProvider>
    <App />
  </ThemeProvider>
);
