import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import ChatInterface from './components/Chat/ChatInterface';
import LatestUpdates from './components/Updates/LatestUpdates';
import Navbar from './components/Layout/Navbar';
import './styles/App.css';

const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="loading-screen">Loading...</div>;
  }

  return isAuthenticated ? (
    <>
      <Navbar />
      {children}
    </>
  ) : (
    <Navigate to="/login" />
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/chat"
              element={
                <PrivateRoute>
                  <ChatInterface />
                </PrivateRoute>
              }
            />
            <Route
              path="/updates"
              element={
                <PrivateRoute>
                  <LatestUpdates />
                </PrivateRoute>
              }
            />
            <Route path="/" element={<Navigate to="/chat" />} />
          </Routes>
          <ToastContainer
            position="top-right"
            autoClose={3000}
            hideProgressBar={false}
            newestOnTop
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
          />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
