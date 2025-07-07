import React, { useState, useEffect, useContext } from 'react';
import Chat from './components/chat';
import './styles/main.css';
import {listSessions, createSession as apiCreateSession, deleteSession as apiDeleteSession, getSession as apiGetSession} from './api';
import {AuthContext} from './auth';

const QUESTION_STEPS = ['start-date', 'end-date', 'party-size', 'budget', 'region', 'activities', 'extras', 'confirm'];

export default function Conversation() {
  const {token, logout} = useContext(AuthContext);
  const [sessions, setSessions] = useState([]);
  const [activeId, setActiveId] = useState(null);

  useEffect(() => {
    if (!token) return;
    listSessions(token).then(data => {
      const mapped = data.map(ss => {
        const uiMessages = ss.messages.map(m => ({from: m.from_user === 'user' ? 'user' : 'bot', text: m.text}));
        const numUser = ss.messages.filter(m => m.from_user === 'user').length;
        const step = numUser >= QUESTION_STEPS.length ? 'listening' : QUESTION_STEPS[numUser];

        const userTexts = ss.messages.filter(m => m.from_user === 'user').map(m => m.text);
        const answers = {
          start_date: userTexts[0] || '',
          end_date: userTexts[1] || '',
          party_size: userTexts[2] || '',
          budget: userTexts[3] || '',
          region: userTexts[4] || '',
          activities: (userTexts[5] || '').split(',').map(s => s.trim()),
          extras: userTexts[6] || ''
        };
        return {
          id: ss.id,
          title: ss.title,
          messages: uiMessages,
          step,
          answers
        };
      });
      setSessions(mapped);
      if (mapped.length) setActiveId(mapped[0].id);
    });
  }, [token]);

  const createSession = () => {
    apiCreateSession(token).then(created => {
      apiGetSession(token, created.id).then(full => {
        const uiMessages = full.messages.map(m => ({from: m.from_user === 'user' ? 'user' : 'bot', text: m.text}));
        const numUser = full.messages.filter(m => m.from_user === 'user').length;
        const step = numUser >= QUESTION_STEPS.length ? 'listening' : QUESTION_STEPS[numUser];
        const userTexts = full.messages.filter(m => m.from_user === 'user').map(m => m.text);
        const answers = {
          start_date: userTexts[0] || '',
          end_date: userTexts[1] || '',
          party_size: userTexts[2] || '',
          budget: userTexts[3] || '',
          region: userTexts[4] || '',
          activities: (userTexts[5] || '').split(',').map(s => s.trim()),
          extras: userTexts[6] || ''
        };
        const newSess = {
          id: full.id,
          title: full.title,
          messages: uiMessages,
          step,
          answers
        };
        setSessions(s => [...s, newSess]);
        setActiveId(full.id);
      });
    });
  };

  const deleteSession = sid => {
    apiDeleteSession(token, sid).then(() => {
        setSessions(s => s.filter(ss => ss.id !== sid));
        if (sid === activeId) {
          const rem = sessions.filter(ss => ss.id !== sid);
          setActiveId(rem.length ? rem[0].id : null);
        }
      }).catch(err => console.error('Delete failed:', err));
  };

  const selectSession = sid => {setActiveId(sid);};

  const updateSession = (sid, updates) => {setSessions(s => s.map(ss => (ss.id === sid ? { ...ss, ...updates } : ss)));};

  const activeSession = sessions.find(ss => ss.id === activeId);

  return (
    <>
      <header className="app-header">
        <button onClick={logout}>Log Out</button>
      </header>
      <div className="app-container">
        <aside className="sidebar">
          <button className="new-chat-btn" onClick={createSession}> + New Chat </button>
          <ul className="session-list">
            {sessions.map(ss => (
              <li key={ss.id} className={ss.id === activeId ? 'active' : ''} onClick={() => selectSession(ss.id)}>
                {ss.title}
                <button className="delete-btn" onClick={e => {
                    e.stopPropagation();
                    deleteSession(ss.id);
                  }}
                > x </button>
              </li>
            ))}
          </ul>
        </aside>
        <main className="chat-panel">
          {activeSession ? (
            <Chat messages={activeSession.messages}
              step={activeSession.step}
              answers={activeSession.answers}
              onSessionChange={updates => updateSession(activeId, updates)}
              sessionId={activeSession.id}
              token={token} />) : (<div className="no-chat">No chat selected. Create one to start!</div>)}
        </main>
      </div>
    </>
  );
}
