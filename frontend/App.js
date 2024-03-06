import React, { useState, useEffect } from 'react';
import axios from 'axios';
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
      <div className="app-container"> 
      {appState.loading ? 
        <p>Loading...</p> : 
        <p>{appState.data.message}</p> // Display the message from API 
      }
      </div>

    </UserProvider>

  );
}

export default App;
