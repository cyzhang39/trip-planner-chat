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
    <div className='app-root'>
      <header className='app-header'><a href='https://github.com/cyzhang39/trip-planner-chat' className='github' title='https://github.com/cyzhang39/trip-planner-chat'>View source or report issue on github</a></header>
      <Routes>
        <Route path="/login" element={token ? <Navigate to="/" /> : <Login onSwitch={() => navigate('/register')} />}/>
        <Route path="/register" element={token ? <Navigate to="/" /> : <Register onSwitch={() => navigate('/login')} />}/>
        <Route path="/" element={token ? <Conversation /> : <Navigate to="/login" />}/>
        <Route path="*" element={<Navigate to={token ? "/" : "/login"} />}/>
      </Routes>
    </div>
    
  );
}
