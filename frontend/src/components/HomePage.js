import React, { useContext, useEffect } from "react"; // Include useEffect in the import
import { useNavigate } from "react-router-dom";
import ClothingRecommendations from "./clothing/ClothingRecommendation";
import SunscreenTracker from "./ssusage/SunscreenTracker";
import useAuth from "../hooks/useAuth";

function HomePage() {
  const navigate = useNavigate();
  const { auth } = useAuth();

  // // Correctly use useEffect for conditional navigation
  // useEffect(() => {
  //   // This example assumes you want to redirect if not logged in, adjust as necessary
  //   if (!isLoggedIn) {
  //     navigate('/login'); // Adjust the path as needed
  //   }
  //   // The empty array means this effect runs once on mount. Add dependencies if needed.
  // }, [isLoggedIn, navigate]); // Make sure to include navigate in the dependency array if you use it inside useEffect

  return (
    <div>
      <h1>Welcome to Sun360!</h1>
      {auth?.email && auth?.accessToken && (
        <div>
          {/* <h2>Your Personalized Dashboard, {user.user_name}</h2> */}
          {/* <ClothingRecommendations
            uvIndex={user.ClothingRecommendations}
            location={user.location}
          /> */}
          {/* <SunscreenTracker userId={user.user_id} /> */}
        </div>
      )}
      {(!auth?.email || !auth?.accessToken) && (
        <div>
          <p>Get started with personalized sun protection recommendations.</p>
          <button onClick={() => navigate("/login")}>Login</button>
          <button onClick={() => navigate("/register")}>Register</button>
        </div>
      )}
    </div>
  );
}

export default HomePage;
