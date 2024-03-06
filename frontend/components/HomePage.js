import React from 'react';
import SunTrendChart from './SunTrendChart';  // Assuming you have this component 
import ClothingRecommendations from './ClothingRecommendations';
import SunscreenTracker from './SunscreenTracker';

function HomePage({ isLoggedIn, user }) {
  return (
    <div>
      <h1>Welcome to Sun360!</h1>
      {isLoggedIn ? (
        <div>
          <h2>Your Personalized Dashboard, {user.user_name}</h2>
          <SunTrendChart locationId={user.location_id} /> 
          <ClothingRecommendations uvIndex={/* ... */} location={/* ... */} />
          <SunscreenTracker userId={user.user_id} />
        </div>
      ) : (
        <div>
          <p>Get started with personalized sun protection recommendations.</p>
          <button onClick={() => navigate('/login')}>Login</button> 
          <button onClick={() => navigate('/register')}>Register</button>
        </div>
      )}
    </div>
  );
}

export default HomePage;