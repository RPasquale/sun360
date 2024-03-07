import React, { createContext, useState } from 'react';

const UserContext = createContext({
  isLoggedIn: false,
  user: null,
  setIsLoggedIn: () => {},
});

export const UserProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  const login = async (username, password) => {
    // TODO: 1. Send login request to the backend endpoint 
    //       2. If successful, set isLoggedIn to true and store user data

    // Simulation:
    if (username === 'testuser' && password === 'password') { 
      setIsLoggedIn(true);
      setUser({ user_name: username });
    } else {
      throw new Error('Invalid credentials');
    }
  };

  const logout = () => {
    setIsLoggedIn(false);
    setUser(null);
  };

  return (
    <UserContext.Provider value={{ isLoggedIn, user, login, logout }}> 
      {children}
    </UserContext.Provider>
  );
};

export default UserContext;
