import React, {createContext, useState, useEffect} from 'react';

export const AuthContext = createContext();

export function AuthProvider({children}) {
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState(null);

  useEffect(() => {
    const t = localStorage.getItem('token');
    const u = localStorage.getItem('username');
    if (t) {
      setToken(t);
      setUsername(u);
    }
  }, []);

  const login = async (username, password) => {
    const res = await fetch('http://localhost:8000/auth/login', 
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) throw new Error('Login failed');
    const { access_token } = await res.json();
    setToken(access_token);
    setUsername(username);
    localStorage.setItem('token', access_token);
    localStorage.setItem('username', username);
  };

  const register = async (username, password) => {
    const res = await fetch('http://localhost:8000/auth/register', 
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Registration failed');
    }
    return login(username, password);
  };

  const logout = () => {
    setToken(null);
    setUsername(null);
    localStorage.removeItem('token');
    localStorage.removeItem('username');
  };

  return <AuthContext.Provider value={{token, username, login, register, logout}}> {children} </AuthContext.Provider>;
}
