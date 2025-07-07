// src/App.js
import React, { useContext } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthContext } from './auth';
import Login from './login';
import Register from './register';
import Conversation from './conversation';

export default function App() {
  const { token } = useContext(AuthContext);
  return (
    <Routes>
      <Route path="/login" element={token ? <Navigate to="/" /> : <Login onSwitch={() => {}} />}/>
      <Route path="/register" element={token ? <Navigate to="/" /> : <Register onSwitch={() => {}} />}/>
      <Route path="/" element={token ? <Conversation /> : <Navigate to="/login" />}/>
      <Route path="*" element={<Navigate to={token ? "/" : "/login"} />}/>
    </Routes>
  );
}
