// Navbar.js
import React, { useState, useContext, useEffect } from 'react';
import { Link } from 'react-router-dom'; // Assuming you're using React Router
import UserContext from './UserContext';
import './Navbar.css';

function Navbar() {
  const [showDropdown, setShowDropdown] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const { isLoggedIn, setIsLoggedIn } = useContext(UserContext);

  const handleLogout = () => {
    setIsLoggedIn(false); // Update context to reflect user has logged out
  };

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };
  
  // When the showDropdown state changes, you may use useEffect to perform DOM updates.
  useEffect(() => {
    const dropdownContent = document.querySelector('.dropdown-content');
    if (dropdownContent) {
      dropdownContent.style.display = showDropdown ? 'block' : 'none';
    }
  }, [showDropdown]); // Only re-run the effect if showDropdown changes
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button onClick={toggleDropdown} className="dropdown-btn">
          <div>😎</div>

        </button>
        {isDropdownOpen && (
          <div className={`dropdown-content ${isDropdownOpen ? 'open' : ''}`}>
          </div>
        )}
        {showDropdown && (
          <div className="dropdown-content">
            <Link to="/uv-impact">UV Impact</Link>
            <Link to="/reminders">Reminders</Link>
          </div>
        )}
      </div>
      <div className="navbar-center">
        <Link to="/home" className="brand-logo">Sun360</Link>
      </div>
      <div className="navbar-right">
        {isLoggedIn ? (
          <>
            <span style={{ marginRight: '20px' }}><Link to="/register">Register</Link></span>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <span style={{ marginRight: '20px' }}><Link to="/register">Register</Link></span>
            <Link to="/login">Login</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
