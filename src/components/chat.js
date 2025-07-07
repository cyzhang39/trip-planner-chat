import React, {useState, useRef, useEffect} from 'react';
import '../styles/main.css';
import {API_BASE} from '../api';

export default function Chat({messages = [], step, answers, onSessionChange, sessionId, token}){
  const [input, setInput] = useState('');
  const msgInput = useRef(null);

  useEffect(() => {msgInput.current?.scrollIntoView({behavior: 'smooth'})}, [messages]);

  const setMessages= msgs => onSessionChange({messages: msgs});
  const setStep = s => onSessionChange({step: s});
  const setAnswers = a => onSessionChange({answers: a});

  const persist = async (from_user, text) => {
    try{
      await fetch(`${API_BASE}/api/sessions/${sessionId}/messages`, 
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({from_user, text})
      });
    }catch (e){
      console.error('Persist error:', e);
    }
  };

  const sendMessage = async content => {
    const userMsg = {from: 'user', text: content};
    const nxt = [...messages, userMsg];
    setMessages(nxt);
    setInput('');
    await persist('user', content);

    if (step === 'listening') {
      await handleFollowUp(content, nxt);
    } else {
      await handleNextStep(content, nxt);
    }
  };

  const handleFollowUp = async (question, history) => {
    setStep('loading');
    let response = 'Something went wrong...Perhaps model ran out of tokens.';
    try {
      const res = await fetch(`${API_BASE}/api/chat`, 
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          session_id: sessionId,
          question,
          chat_history: history
        })
      });
      response = (await res.json()).answer;
    }catch (e){
      console.error('Chat API error:', e);
    }

    const bot = {from: 'bot', text: response};
    const nxt = [...history, bot]
    setMessages(nxt);
    await persist('bot', response);
    setStep('listening');
  };

  const handleNextStep = async (answer, history) => {
    let question = '';
    let stp = '';

    switch (step) {
      case 'start-date':
        setAnswers({...answers, start_date: answer});
        question = "Great — and what's your end date?";
        stp = 'end-date';
        break;
      case 'end-date':
        setAnswers({...answers, end_date: answer});
        question = 'How many people are traveling?';
        stp = 'party-size';
        break;
      case 'party-size':
        setAnswers({...answers, party_size: answer});
        question = "What's your per person budget per day in terms of US Dollar? (<100, 100-200, 200-300, 300-400, 400-500, >500)";
        stp = 'budget';
        break;
      case 'budget':
        setAnswers({...answers, budget: answer});
        question = 'Which region/country are you visiting?';
        stp = 'region';
        break;
      case 'region':
        setAnswers({...answers, region: answer});
        question = 'What activities are you interested in? (e.g. beach, food — COMMA SEPERATED)';
        stp = 'activities';
        break;
      case 'activities':
        setAnswers({...answers, activities: answer.split(',').map(s => s.trim())});
        question = 'Anything else I should know?';
        stp = 'extras';
        break;
      case 'extras':
        setAnswers({...answers, extras: answer});
        question = 'All set! Generate itinerary now? (yes/no)';
        stp = 'confirm';
        break;
      case 'confirm':
        setStep('loading');
        if (/^y(es)?$/i.test(answer)) {
          // const summaryLines = [
          //   `Start Date: ${answers.start_date}`,
          //   `End Date: ${answers.end_date}`,
          //   `Party Size: ${answers.party_size}`,
          //   `Budget: ${answers.budget}`,
          //   `Region: ${answers.region}`,
          //   `Activities: ${answers.activities.join(', ')}`,
          //   `Extras: ${answers.extras || 'None'}`
          // ];
          // const summaryText = summaryLines.join('\n');
          // const recapMsg = { from: 'bot', text: "Here’s what I received:\n" + summaryText };

          const genMsg = {from: 'bot', text: 'Generating your itinerary...'};
          const after = [...history, genMsg]
          setMessages(after);
          await persist('bot', genMsg.text);

          let itin = 'Could not generate itinerary...';
          try{
            const res = await fetch(`${API_BASE}/api/plan`, 
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`
              },
              body: JSON.stringify({session_id: sessionId, ...answers})
            });
            itin = (await res.json()).itinerary;
          }catch (e){
            console.error('Plan error:', e);
          }
          const response = {from: 'bot', text: itin};
          const final = [...after, response]
          setMessages(final);
          await persist('bot', response.text);
        }else{
          const no = {from: 'bot', text: 'Okay, let me know what to change.'};
          const cancel = [...history, no]
          setMessages(cancel);
          await persist('bot', no.text);
        }
        setStep('listening');
        return;
      default:
        return;
    }

    if (question) {
      setMessages([...history, {from: 'bot', text: question}]);
      await persist('bot', question);
      setStep(stp);
    }
  };

  const download = () => {
    const txt = messages.map(m => `${m.from}: ${m.text}`).join('\n\n');
    const blob = new Blob([txt], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'chat.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="chat-container">
      <div className="chat-head">
        <button onClick={download}>Download</button>
      </div>
      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.from}`}>
            <div className="bubble">{m.text}</div>
          </div>
        ))}
        <div ref={msgInput} />
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          disabled={step === 'loading'}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && input.trim() && sendMessage(input.trim())}
          placeholder="Type your answer..."
        />
        <button
          onClick={() => input.trim() && sendMessage(input.trim())}
          disabled={!input.trim() || step === 'loading'}
        >
          {step === 'loading' ? '...' : 'Send'}
        </button>
      </div>
    </div>
  );
}
