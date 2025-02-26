import React from "react";
import { Link } from "react-router-dom";
import { useTheme } from "../../context/theme/ThemeContext"; // Import ThemeContext

const Sidebar = () => {
  const { theme, themes } = useTheme(); // Get the current theme styles

  return (
    <div className={`w-64 h-full p-6 shadow-lg rounded-r-xl ${themes[theme].sidebar}`}>
      <h2 className="text-2xl font-bold mb-6">🏡 Teacher AI</h2>
      <nav>
        <ul>
          <li className="mb-3">
            <Link 
              to="/" 
              className={`block p-3 rounded-lg transition duration-300 ${themes[theme].button}`}
            >
              📋 Dashboard
            </Link>
          </li>
          <li className="mb-3">
            <Link 
              to="/reports" 
              className={`block p-3 rounded-lg transition duration-300 ${themes[theme].button}`}
            >
              📄 Reports
            </Link>
          </li>
          <li>
            <Link 
              to="/settings" 
              className={`block p-3 rounded-lg transition duration-300 ${themes[theme].button}`}
            >
              ⚙️ Settings
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;



