import React, {useState} from 'react';
import Chat from './components/chat.js';
import {v4 as uuidv4} from 'uuid'
import './styles/main.css'


export default function App() {
  const [sessions, setSessions] = useState([])
  const [id, setId] = useState(null)
  // const [nextNum, setNum] = useState(1)

  const getNext = () => {
    const used = sessions
      .map(s => {
        const m = s.name.match(/^Chat (\d+)$/);
        return m ? parseInt(m[1], 10) : NaN;
      })
      .filter(n => !isNaN(n));
    let n = 1;
    while (used.includes(n)) n++;
    return n;
  };


  const createSession = () => {
    const sid = uuidv4();
    const num = getNext();
    const newSession = {
      sid, 
      name: `Chat ${num}`,
      messages: [{ from: 'bot', text: 'Hi! I am your trip planner assistant. Before generating your itinerary, please answer a few questions first. \n First, when do you plan to start this trip (YYYY-MM-DD)?' }],
      step: 'start-date',
      answers: {}
    }
    // setNum(num => num + 1);
    setSessions(s => [...s, newSession])
    setId(sid)
    
  };
  const deleteSession = (sid) => {
    setSessions(s => s.filter(ss => ss.sid !== sid));
    if(sid === id){
      const remain = sessions.filter(ss => ss.sid !== sid);
      setId(remain.length ? remain[0].sid : null);
    }
  };
  const updateSession = (sid, updates) => {
    setSessions(s => s.map(ss => ss.sid === sid ? {...ss, ...updates} : ss));
  };
  const activeSession = sessions.find(ss => ss.sid === id);

  return (
    <div className="app-container">
      <aside className="sidebar">
        <button className="new-chat-btn" onClick={createSession}>
          + New Chat
        </button>
        <ul className="session-list">
          {sessions.map(sess => (
            <li
              key={sess.sid}
              className={sess.sid === id ? 'active' : ''}
              onClick={() => setId(sess.sid)}
            >
              {sess.name}
              <button
                className="delete-btn"
                onClick={() => deleteSession(sess.sid)}
              >×</button>
            </li>
          ))}
        </ul>
      </aside>
      <main className="chat-panel">
        {activeSession
          ? <Chat
              messages={activeSession.messages}
              step={activeSession.step}
              answers={activeSession.answers}
              onSessionChange={updates => updateSession(id, updates)}
            />
          : <div className="no-chat">No chat selected. Create one to start!</div>
        }
      </main>
    </div>
  )
}