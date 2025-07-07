import React, {useState, useContext} from 'react';
import { AuthContext } from './auth';

export default function Register({ onSwitch }) {
  const {register} = useContext(AuthContext);
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [error, setError] = useState('');

  const submit = async e => {
    e.preventDefault();
    try {
      await register(user, pass);
    }catch (e) {
      setError(e.message);
    }
  };

  return (
    <form onSubmit={submit} className="auth-form">
      <h2>Register</h2>
      {error && <div className="error">{error}</div>}
      <input placeholder="Username" value={user} onChange={e => setUser(e.target.value)}/>
      <input placeholder="Password" type="password" value={pass} onChange={e => setPass(e.target.value)}/>
      <button type="submit">Sign Up</button>
      <p>
        Already have an account?{' '}
        <button type="button" onClick={() => onSwitch('login')}> Log In </button>
      </p>
    </form>
  );
}
