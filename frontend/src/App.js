import React from "react";

import { Routes, Route } from "react-router-dom"; // Updated import
import Layout from "./components/basic-ui/elements/layout";
import HomePage from "./components/HomePage";
import LoginPage from "./components/user/LoginPage";
import RegisterPage from "./components/user/RegisterPage";
import Reminders from "./components/Reminders";
import useAuth from "./hooks/useAuth";
import PersistLogin from "./components/user/PersistLogin";
import RequireAuth from "./components/user/RequireAuth";
import Page404 from "./page404";

function App() {
  // For validating whether user is logged in or not
  const { auth } = useAuth();

  return (
    <main className="app">
      {/* Layout component for attaching navigation bar to the remaining app */}
      <Layout>
        <Routes>
          {/* For home (/) route, if user is logged in, then navigated to search app and if not logged in, then navigated to login page */}
          <Route exact path="/" element={<HomePage />} />

          {/* Global paths - login and signup */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected Routes */}
          <Route element={<PersistLogin />}>
            <Route element={<RequireAuth />}>
              <Route path="/reminders" element={<Reminders />} />
            </Route>
          </Route>

          {/* Invalid Paths */}
          <Route path="*" element={<Page404 />} />
        </Routes>
      </Layout>
    </main>
  );
}

export default App;
