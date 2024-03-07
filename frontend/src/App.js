import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Updated import
import HomePage from './components/HomePage';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import Navbar from './components/Navbar';
import Reminders from './components/Reminders';
import { UserProvider } from './components/UserContext';

const API_BASE_URL = 'http://localhost:5000'; // Replace with your Flask app's URL

function App() {
  const [appState, setAppState] = useState({ loading: true, data: null });

  useEffect(() => {
    axios.get(`${API_BASE_URL}/`)  // Make an initial request to API
      .then(response => {
        setAppState({ loading: false, data: response.data });
      })
      .catch(error => { 
        console.error('Error fetching data:', error);
        setAppState({ loading: false, data: null }); // Adjust as needed for errors
      });
  }, []); 

  return (
    <UserProvider>
      <Router>
        <div className="app-container">
          <Navbar />
          <Routes> 
            <Route path="/home" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/reminders" element={<Reminders />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;
