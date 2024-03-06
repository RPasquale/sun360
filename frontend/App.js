import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { UserProvider } from './UserContext';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import HomePage from './components/HomePage'; // Adjust the path as needed
import LoginPage from './components/LoginPage'; // Adjust the path as needed
import RegisterPage from './components/RegisterPage';
import Navbar from './components/Navbar';
import { UserProvider } from './UserContext';

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
          <Switch>
            <Route path="/" exact component={HomePage} />
            <Route path="/login" component={LoginPage} />
            <Route path="/register" component={RegisterPage} />
            {/* Define other routes as needed */}
          </Switch>
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;