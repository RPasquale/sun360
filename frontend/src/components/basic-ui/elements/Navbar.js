// Navbar.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";

import useAuth from "../../../hooks/useAuth";
import MenuIcon from "../icons/MenuIcon";

import "./Navbar.css";

const LOGOUT_URL = "http://127.0.0.1:5000/logout";

function Navbar() {
  // Check auth and display different elements in nav bar based on whether user is logged in or not
  const { auth, setAuth } = useAuth();
  const navigate = useNavigate();

  const [showDropdown, setShowDropdown] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleLogout = async () => {
    try {
      // Get request to backend server for logout
      // await axios.post(
      //   LOGOUT_URL,
      //   {},
      //   {
      //     headers: {
      //       "Content-Type": "application/json",
      //       "Authorization": auth.accessToken,
      //       "Access-ID": auth.accessID,
      //     },
      //     withCredentials: true,
      //   }
      // );
      setTimeout(() => {
        // Reset the auth on logout
        setAuth({});
        // Navigate back to home
        navigate("/", { replace: true });
      }, 5000);
    } catch (error) {
      console.log(error);
    }
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
        {auth?.accessID && auth?.accessToken && (
          <>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        )}
        {(!auth?.accessID || !auth?.accessToken) && (
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
