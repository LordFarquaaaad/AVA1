import { createContext, useContext, useEffect, useState } from "react";

// Available themes
const themes = {
  cozy: {
    bg: "bg-[#f5ebe0]", // Warm beige background
    text: "text-[#3e3e3e]",
    sidebar: "bg-[#d8c3a5] text-[#5e4937]",
    cardColor: "#f8f4e1", // ✅ Normal card color for components
    lighterCardColor: "#faf3e7", // ✅ Slightly lighter than the main card
    button: "bg-[#8b5e3b] text-white hover:bg-[#a97c50]"
  },
  candlelight: {
    bg: "bg-[#2c2a2a]", // Dimmed warm dark
    text: "text-[#e8cba4]",
    sidebar: "bg-[#3e322c] text-[#e8cba4]",
    cardColor: "#44372e", // ✅ Normal card background
    lighterCardColor: "#57483e", // ✅ Lighter than the background
    button: "bg-[#a97c50] text-white hover:bg-[#8b5e3b]"
  },
  dark: {
    bg: "bg-[#1a1a1a]", // Dark theme
    text: "text-[#f5f5f5]",
    sidebar: "bg-[#2a2a2a] text-[#f5f5f5]",
    cardColor: "#333", // ✅ Normal card color
    lighterCardColor: "#444", // ✅ Slightly lighter for contrast
    button: "bg-[#444] text-white hover:bg-[#666]"
  }
};

// Context setup
const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(localStorage.getItem("theme") || "cozy");

  // Apply theme changes and save to localStorage
  useEffect(() => {
    localStorage.setItem("theme", theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, themes }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);



