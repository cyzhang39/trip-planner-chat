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
    <div className='auth-pages'>
      <form onSubmit={submit} className="auth-form">
        <h2>Register</h2>
        {error && <div className="error">{error}</div>}
        <input placeholder="Username" value={user} onChange={e => setUser(e.target.value)} minLength={3} maxLength={20} pattern="^[A-Za-z0-9]+$" title="3–20 letters or numbers only" required/>
        <input placeholder="Password" type="password" value={pass} onChange={e => setPass(e.target.value)} minLength={4} maxLength={20} title="4-20 characters" required/>
        <button type="submit">Sign Up</button>
        <p>
          Already have an account?{' '}
          <button type="button" onClick={() => onSwitch('login')}> Log In </button>
        </p>
      </form>
    </div>
    
  );
}
