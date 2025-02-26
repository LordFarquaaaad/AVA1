import React from "react";
import { useTheme } from "../../context/theme/ThemeContext";

const Header = () => {
  const { theme, setTheme, themes } = useTheme();

  return (
    <div className={`w-full ${themes[theme].sidebar} p-4 shadow-md flex items-center justify-between rounded-b-xl`}>
      <h1 className="text-2xl font-semibold flex items-center">🏡 Welcome Home</h1>

      {/* Theme Toggle Dropdown */}
      <div className="relative">
        <select
          className={`px-3 py-2 rounded-lg ${themes[theme].button}`}
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
        >
          <option value="cozy">🏡 Cozy</option>
          <option value="candlelight">🕯️ Candlelight</option>
          <option value="dark">🌙 Dark Mode</option>
        </select>
      </div>
    </div>
  );
};

export default Header;




  