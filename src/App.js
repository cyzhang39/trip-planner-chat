import React, { useContext } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { AuthContext } from './auth';
import Login from './login';
import Register from './register';
import Conversation from './conversation';

export default function App() {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();
  return (
    <Routes>
      <Route path="/login" element={token ? <Navigate to="/" /> : <Login onSwitch={() => navigate('/register')} />}/>
      <Route path="/register" element={token ? <Navigate to="/" /> : <Register onSwitch={() => navigate('/login')} />}/>
      <Route path="/" element={token ? <Conversation /> : <Navigate to="/login" />}/>
      <Route path="*" element={<Navigate to={token ? "/" : "/login"} />}/>
    </Routes>
  );
}
