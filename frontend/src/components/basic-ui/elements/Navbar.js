// Navbar.js
import React, { useState, useContext, useEffect } from "react";
import { Link } from "react-router-dom";
import useAuth from "../../../hooks/useAuth";
import "./Navbar.css";
import MenuIcon from "../icons/MenuIcon";

function Navbar() {
  // Check auth and display different elements in nav bar based on whether user is logged in or not
  const { auth } = useAuth();

  const [showDropdown, setShowDropdown] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleLogout = () => {
    // setIsLoggedIn(false);
  };

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
    setIsDropdownOpen(!isDropdownOpen);
  };

  useEffect(() => {
    const dropdownContent = document.querySelector(".dropdown-content");
    if (dropdownContent) {
      dropdownContent.style.display = showDropdown ? "block" : "none";
    }
  }, [showDropdown]);

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button onClick={toggleDropdown} className="dropdown-btn">
          <div className="menu-icon">
            <MenuIcon />
          </div>
        </button>
        <div className={`dropdown-content ${isDropdownOpen ? "open" : ""}`}>
          <Link to="/uv-impact">UV Impact</Link>
          <Link to="/reminders">Reminders</Link>
        </div>
      </div>
      <div className="navbar-center">
        <Link to="/" className="brand-logo">
          Sun360
        </Link>
      </div>
      <div className="navbar-right">
        {auth?.email && auth?.accessToken && (
          <>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
        {(!auth?.email || !auth?.accessToken) && (
          <>
            <Link to="/login" className="nav-link login-link">
              Login
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
