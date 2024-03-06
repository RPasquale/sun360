import React, { useContext, useEffect } from 'react'; // Include useEffect in the import
import { useNavigate } from 'react-router-dom';
import ClothingRecommendations from './ClothingProtection/ClothingRecommendation';
import SunscreenTracker from './SunscreenUsage/SunscreenTracker';
import UserContext from './UserContext';

function HomePage() {
  const navigate = useNavigate();
  navigate('/path');  
  const { user } = useContext(UserContext);
  const isLoggedIn = Boolean(user);

  // Correctly use useEffect for conditional navigation
  useEffect(() => {
    // This example assumes you want to redirect if not logged in, adjust as necessary
    if (!isLoggedIn) {
      navigate('/login'); // Adjust the path as needed
    }
    // The empty array means this effect runs once on mount. Add dependencies if needed.
  }, [isLoggedIn, navigate]); // Make sure to include navigate in the dependency array if you use it inside useEffect

  return (
    <div>
      <h1>Welcome to Sun360!</h1>
      {isLoggedIn ? (
        <div>
          <h2>Your Personalized Dashboard, {user.user_name}</h2>
          <ClothingRecommendations uvIndex={user.ClothingRecommendations} location={user.location} />
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
