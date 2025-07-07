import React, { useState, useContext } from 'react';
import { AuthContext } from './auth';

export default function Login({ onSwitch }) {
  const {login} = useContext(AuthContext);
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [error, setError] = useState('');

  const submit = async e => {
    e.preventDefault();
    try {
      await login(user, pass);
    }catch (e){
      setError(e.message);
    }
  };

  return (
    <form onSubmit={submit} className="auth-form">
      <h2>Log In</h2>
      {error && <div className="error">{error}</div>}
      <input placeholder="Username" value={user} onChange={e => setUser(e.target.value)}/>
      <input placeholder="Password" type="password" value={pass} onChange={e => setPass(e.target.value)}/>
      <button type="submit">Log In</button>
      <p>
        New here?{' '}
        <button type="button" onClick={() => onSwitch('register')}> Register </button>
      </p>
    </form>
  );
}
