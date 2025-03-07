import React from "react";
import { useTheme } from "../../context/theme/ThemeContext";

const Header = () => {
  const { theme, setTheme, themes } = useTheme();

  // Fallback to 'scholar' if theme is undefined or invalid
  const currentTheme = theme && Object.keys(themes).includes(theme) ? theme : "scholar";
  console.log("Theme in Header:", currentTheme, themes); // Debugging log

  return (
    <div className={`w-full p-4 shadow-md flex items-center justify-between rounded-b-xl ${themes[currentTheme].bg}`}>
      <h1 className={`text-2xl font-semibold flex items-center ${themes[currentTheme].text}`}>🏡 Welcome Home</h1>

      {/* Theme Toggle Dropdown */}
      <div className="relative">
        <select
          className={`px-3 py-2 rounded-lg ${themes[currentTheme].button}`}
          value={currentTheme}
          onChange={(e) => setTheme(e.target.value)}
        >
          <option value="scholar">📚 Scholar</option>
          <option value="sage">🌿 Sage</option>
          <option value="slate">📉 Slate</option>
        </select>
      </div>
    </div>
  );
};

export default Header;




  