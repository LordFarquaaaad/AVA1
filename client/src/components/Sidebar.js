import { Link } from "react-router-dom";
import { FaHome, FaFileAlt, FaCog } from "react-icons/fa";

const Sidebar = () => {
  return (
    <div className="w-64 h-screen bg-gray-900 text-white p-4">
      <h2 className="text-xl font-bold">Teacher AI</h2>
      <ul>
        <li className="p-2 hover:bg-gray-700">
          <Link to="/" className="flex items-center space-x-2">
            <FaHome /> <span>Dashboard</span>
          </Link>
        </li>
        <li className="p-2 hover:bg-gray-700">
          <Link to="/reports" className="flex items-center space-x-2">
            <FaFileAlt /> <span>Reports</span>
          </Link>
        </li>
        <li className="p-2 hover:bg-gray-700">
          <Link to="/settings" className="flex items-center space-x-2">
            <FaCog /> <span>Settings</span>
          </Link>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;



