import React from 'react';
import { useHistory } from 'react-router-dom';  // Import useHistory
import SunTrendChart from './SunTrendChart';
import ClothingRecommendations from './ClothingRecommendations';
import SunscreenTracker from './SunscreenTracker';
import { useUser } from './UserContext'; // Import useUser if using Context for user state

function HomePage() {
  const history = useHistory();
  const { user } = useUser(); // Access user and potentially isLoggedIn state
  const isLoggedIn = Boolean(user);

  return (
    <div>
      <h1>Welcome to Sun360!</h1>
      {isLoggedIn ? (
        <div>
          <h2>Your Personalized Dashboard, {user.user_name}</h2>
          <SunTrendChart locationId={user.location_id} /> 
          <ClothingRecommendations uvIndex={user.ClothingRecommendations} location= {user.location} />
          <SunscreenTracker userId={user.user_id} />
        </div>
      ) : (
        <div>
          <p>Get started with personalized sun protection recommendations.</p>
          <button onClick={() => history.push('/login')}>Login</button>
          <button onClick={() => history.push('/register')}>Register</button>
        </div>
      )}
    </div>
  );
}

export default HomePage;
