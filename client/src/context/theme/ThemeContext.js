import { createContext, useContext, useEffect, useState } from "react";

// Available themes optimized for teachers
const themes = {
  scholar: {
    bg: "bg-[#f9fafb]", // Light, clean off-white background for a professional look
    text: "text-[#333333]", // Dark gray for readability
    sidebar: "bg-[#e5e7eb] text-[#333333]", // Light gray sidebar with dark text for contrast
    cardColor: "#ffffff", // Pure white cards for a crisp, professional appearance
    lighterCardColor: "#f3f4f6", // Slightly off-white for subtle contrast in cards
    button: "bg-[#4a90e2] text-white hover:bg-[#357ab8]", // Professional blue button, easy on the eyes
    errorColor: "#e74c3c", // Red for errors, visible but not overwhelming
    successColor: "#2ecc71", // Green for success messages, teacher-friendly
  },
  sage: {
    bg: "bg-[#f0f7f4]", // Soft mint green background, calm and earthy
    text: "text-[#2c3e50]", // Dark navy for readability
    sidebar: "bg-[#d1e7dd] text-[#2c3e50]", // Light green sidebar with dark text
    cardColor: "#ffffff", // White cards for contrast
    lighterCardColor: "#e8f5e9", // Very light green for subtle card highlight
    button: "bg-[#27ae60] text-white hover:bg-[#219653]", // Earthy green button, teacher-friendly
    errorColor: "#e74c3c", // Red for errors
    successColor: "#2ecc71", // Green for success
  },
  slate: {
    bg: "bg-[#f5f7fa]", // Light gray-blue background, modern and minimal
    text: "text-[#2c3e50]", // Dark navy for readability
    sidebar: "bg-[#e2e8f0] text-[#2c3e50]", // Medium gray sidebar with dark text
    cardColor: "#ffffff", // White cards for clarity
    lighterCardColor: "#edf2f7", // Very light gray for card highlight
    button: "bg-[#4682b4] text-white hover:bg-[#3a6ea0]", // Steel blue button, professional and modern
    errorColor: "#e74c3c", // Red for errors
    successColor: "#2ecc71", // Green for success
  },
};

// Context setup
const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "scholar"); // Default to 'scholar' for professional look

  // Apply theme changes and save to localStorage
  useEffect(() => {
    localStorage.setItem("theme", theme);
    // Optionally update the document class for global CSS application
    document.documentElement.className = `theme-${theme}`;
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, themes }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);



