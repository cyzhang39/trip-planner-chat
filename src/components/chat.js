import React, { useState, useRef, useEffect } from 'react';
import '../styles/main.css';

export default function Chat() {
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'Hi! To start, what’s your trip start date (YYYY-MM-DD)?' }
  ]);
  const [step, setStep] = useState('start-date');
  const [answers, setAnswers] = useState({});
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = (content) => {
    setMessages(msgs => [...msgs, { from: 'user', text: content }]);
    setInput('');
    handleNextStep(content);
  };

  const handleNextStep = (answer) => {
    let nextBotText = '';
    let nextStep = '';

    switch (step) {
      case 'start-date':
        setAnswers(a => ({ ...a, start_date: answer }));
        nextBotText = 'Great—what’s your end date?';
        nextStep = 'end-date';
        break;

      case 'end-date':
        setAnswers(a => ({ ...a, end_date: answer }));
        nextBotText = 'How many people are traveling?';
        nextStep = 'party-size';
        break;

      case 'party-size':
        setAnswers(a => ({ ...a, party_size: answer }));
        nextBotText = 'What’s your budget per day? (<100, 100-200, 200-300, >300)';
        nextStep = 'budget';
        break;

      case 'budget':
        setAnswers(a => ({ ...a, budget: answer }));
        nextBotText = 'Which region/country are you visiting?';
        nextStep = 'region';
        break;

      case 'region':
        setAnswers(a => ({ ...a, region: answer }));
        nextBotText = 'Any top activity categories? (e.g. beach, food. Comma-separated.)';
        nextStep = 'activities';
        break;

      case 'activities':
        setAnswers(a => ({ ...a, activities: answer.split(',').map(s => s.trim()) }));
        nextBotText = 'Anything else we should know?';
        nextStep = 'extras';
        break;

      case 'extras':
        setAnswers(a => ({ ...a, extras: answer }));
        nextBotText = 'All set! Shall I generate your itinerary now? (yes/no)';
        nextStep = 'confirm';
        break;

      case 'confirm':
        if (/^y(es)?$/i.test(answer)) {
          setMessages(msgs => [
            ...msgs,
            { from: 'bot', text: 'Generating your itinerary… 🎉' }
          ]);
          setStep('loading');

          fetch("http://localhost:8000/api/plan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(answers),
          })
            .then(res => res.json())
            .then(data => {
              const itinerary = data.itinerary || data;
              // const lines = itinerary.split('\n').filter(line => line.trim());
              const days = itinerary.split(/\n?Day\s+/).filter(s => s.trim()).map(s => 'Day ' + s.trim())
              const m = days.join('\n\n')

              setMessages(msgs => [
                ...msgs,
                { from: 'bot', text: "Here’s your itinerary" },
                { from: 'bot', text: m },
                // ...lines.map((line, i) => ({ from: 'bot', text: line }))
              ]);
              setStep('done');
            })
            .catch(err => {
              console.error(err);
              setMessages(msgs => [
                ...msgs,
                { from: 'bot', text: '😞 Oops, something went wrong.' }
              ]);
              setStep('done');
            });
        } else {
          setMessages(msgs => [
            ...msgs,
            { from: 'bot', text: 'Okay, let me know what to change.' }
          ]);
          setStep('done');
        }
      break;

      default:
        return;
    }

    setMessages(msgs => [...msgs, { from: 'bot', text: nextBotText }]);
    setStep(nextStep);
  };

  return (
    <div className="chat-container">
      {}
      <div className="chat-window">
        {messages.map((m, i) => (
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
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && input.trim()) {
              sendMessage(input.trim());
            }
          }}
          placeholder="Type your answer…"
        />
        <button
          onClick={() => input.trim() && sendMessage(input.trim())}
          disabled={!input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
}
