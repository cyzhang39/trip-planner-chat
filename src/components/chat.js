// src/components/Chat.jsx
import React, { useState, useRef, useEffect } from 'react';
import '../styles/main.css';

export default function Chat({messages, step, answers, onSessionChange}) {
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const update = (fields) => {
    onSessionChange(fields);
  };
  const setMessages = (msgs) => update({ messages: msgs });
  const setStep = (s) => update({ step: s });
  const setAnswers = (ans) => update({ answers: ans });

  const download = () => {
    const txt = messages.map(m => `${m.from === 'user' ? 'You' : 'Assistant'}: ${m.text}`).join('\n\n');
    const blob = new Blob([txt], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'trip_planner_conversation.txt';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };



  const sendMessage = (content) => {
    const userMsg = { from: 'user', text: content };
    const updated = [...messages, userMsg];
    setMessages(updated);
    setInput('');

    if (step === 'listening') {
      handleFollowUp(content, updated);
    } else {
      handleNextStep(content, updated);
    }
  };

  const handleFollowUp = (question, history) => {
    setStep('loading');
    fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, chat_history: history }),
    })
      .then(res => res.json())
      .then(data => {
        setMessages([...history, { from: 'bot', text: data.answer }]);
        setStep('listening');
      })
      .catch(() => {
        setMessages([...history, { from: 'bot', text: '😞 Something went wrong.' }]);
        setStep('listening');
      });
  };

  const handleNextStep = (answer, history) => {
    let nextBotText = '';
    let nextStep    = '';

    switch (step) {
      case 'start-date':
        setAnswers({ ...answers, start_date: answer });
        nextBotText = 'Great — and what\'s your end date?';
        nextStep    = 'end-date';
        break;
      case 'end-date':
        setAnswers({ ...answers, end_date: answer });
        nextBotText = 'How many people are there in total traveling?';
        nextStep    = 'party-size';
        break;
      case 'party-size':
        setAnswers({ ...answers, party_size: answer });
        nextBotText = 'What\'s your estimated average budget per day per traveler? (<100, 100-200, 200-300, >300)';
        nextStep    = 'budget';
        break;
      case 'budget':
        setAnswers({ ...answers, budget: answer });
        nextBotText = 'Which region/country are you visiting?';
        nextStep    = 'region';
        break;
      case 'region':
        setAnswers({ ...answers, region: answer });
        nextBotText = 'Any top activity categories? (e.g. beach, food. Comma-separated!)';
        nextStep    = 'activities';
        break;
      case 'activities':
        setAnswers({ ...answers, activities: answer.split(',').map(s => s.trim()) });
        nextBotText = 'Anything else I should know?';
        nextStep    = 'extras';
        break;
      case 'extras':
        setAnswers({ ...answers, extras: answer });
        nextBotText = 'All set! Shall I generate your itinerary now? (yes/no)';
        nextStep    = 'confirm';
        break;
      case 'confirm':
        if (/^y(es)?$/i.test(answer)) {
          setMessages([...history, { from: 'bot', text: 'Generating your itinerary… 🎉' }]);
          setStep('loading');

          fetch("http://localhost:8000/api/plan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(answers),
          })
            .then(res => res.json())
            .then(data => {
              const itinerary = data.itinerary || '';
              setMessages([
                ...history,
                { from: 'bot', text: "Here\'s your itinerary:" },
                { from: 'bot', text: itinerary }
              ]);
              setStep('listening');
            })
            .catch(() => {
              setMessages([...history, { from: 'bot', text: '😞 Oops, something went wrong.' }]);
              setStep('listening');
            });
          return;
        } else {
          setMessages([...history, { from: 'bot', text: 'Okay, let me know what to change.' }]);
          setStep('listening');
        }
        break;

      default:
        return;
    }

    if (nextBotText) {
      setMessages([...history, { from: 'bot', text: nextBotText }]);
      setStep(nextStep);
    }
  };

  return (
    <div className="chat-container">
      <div className='chat-head'>
        <button className='download-btn' onClick={download}> Download conversation (txt)</button>
      </div>
      <div className="chat-window">
        {messages.map((m,i) => (
          <div key={i} className={`message ${m.from}`}>
            <div className="bubble">{m.text}</div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="input-container">
        <input
          type="text"
          value={input}
          disabled={step === 'loading'}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && input.trim() && sendMessage(input.trim())}
          placeholder="Type your answer…"
        />
        <button
          onClick={() => input.trim() && sendMessage(input.trim())}
          disabled={!input.trim() || step === 'loading'}
        >
          {step === 'loading' ? '…' : 'Send'}
        </button>
      </div>
    </div>
  );
}
