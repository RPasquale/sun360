
// Navbar.js
import React, { useContext } from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router
import UserContext from './UserContext';

function Navbar() {
  const { isLoggedIn, setIsLoggedIn } = useContext(UserContext);

  const handleLogout = () => {
    // Logout logic, update context
    setIsLoggedIn(false);
  };

  return (
    <nav>
      {/* Your app name/logo */}
      <div style={{ float: 'right' }}>
        {isLoggedIn ? (
          <button onClick={handleLogout}>Logout</button>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </nav>
  );
}

export default Navbar;