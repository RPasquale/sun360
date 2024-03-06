
// Navbar.js
import React, { useContext } from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router
import UserContext from './UserContext';
import './Navbar.css';

function Navbar() {
  const { isLoggedIn, setIsLoggedIn } = useContext(UserContext);

  const handleLogout = () => {
    // Logout logic, update context
    setIsLoggedIn(false);
  };

  return (
    <nav className="navbar">  {/* Apply 'navbar' class here */}
        <div className="navbar-center">
            <Link to="/" className="brand-logo">SUN360</Link>
        </div>
        <div className="navbar-right">
            {isLoggedIn ? (
                <button onClick={handleLogout}>Logout</button>
            ) : (
                <>
                    <Link to="/register">Register</Link>
                    <Link to="/login">Login</Link>
                </>
            )}
        </div>
    </nav>
  );
}

export default Navbar;