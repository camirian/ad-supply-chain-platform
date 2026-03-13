import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const API_BASE = "http://localhost:8000";

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am your A&D supply chain tracking agent. How can I assist you with Parts, Suppliers, or Work Orders today?' }
  ]);
  const [schema, setSchema] = useState(null);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const bottomRef = useRef(null);

  useEffect(() => {
    fetchSchema();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchSchema = async () => {
    try {
      // Allow it to fetch from wherever the backend is running
      // If deployed, we'll want dynamic API routes or an env var
      const res = await fetch(`${API_BASE}/api/schema`);
      const data = await res.json();
      if(data.schema) setSchema(data.schema);
    } catch (err) {
      console.error("Failed to fetch schema", err);
      // Don't crash, just let the UI know schema isn't available
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userQuery = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userQuery }]);
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userQuery })
      });
      
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.detail || "Error from server");
      }
      
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (err) {
      console.error(err);
      setError(err.message);
      setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="layout">
      {/* Sidebar - Database Explorer */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <h2>🏢 System Schema</h2>
          <p>Local SQLite Definition</p>
        </div>
        
        <div className="schema-container">
          {schema ? (
            Object.keys(schema).map((table) => (
              <div key={table} className="table-card">
                <h3>📦 {table}</h3>
                <div className="table-preview">
                  <table>
                    <thead>
                      <tr>
                        {schema[table].length > 0 && Object.keys(schema[table][0]).map(k => (
                          <th key={k}>{k}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {schema[table].slice(0, 3).map((row, idx) => (
                        <tr key={idx}>
                          {Object.values(row).map((val, i) => (
                            <td key={i}>{String(val)}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  {schema[table].length > 0 && <p className="caption">Sample of {schema[table].length} rows...</p>}
                </div>
              </div>
            ))
          ) : (
             <div className="blueprint-loading">Waiting for backend connection...</div>
          )}
        </div>
      </aside>

      {/* Main Chat Interface */}
      <main className="main-content">
        <header className="chat-header">
          <h1>✈️ A&D Supply Chain Intelligence</h1>
          <p className="subtitle">Zero-Billing Cloud Architecture • Gemini Powered</p>
        </header>
        
        <div className="chat-window">
          <div className="messages">
            {messages.map((m, idx) => (
              <div key={idx} className={`message-row ${m.role}`}>
                <div className={`message-bubble ${m.role}`}>
                  {m.role === 'assistant' && <span className="avatar">🤖</span>}
                  {m.role === 'user' && <span className="avatar">👤</span>}
                  <div className="markdown" dangerouslySetInnerHTML={{__html: m.content.replace(/\n/g, '<br/>')}} />
                </div>
              </div>
            ))}
            {loading && (
              <div className="message-row assistant">
                <div className="message-bubble assistant loading">
                  <span className="avatar">🤖</span>
                  <div className="typing-indicator">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="suggestions">
            <button onClick={() => setInput("Which supplier has the highest rating?")}>Top Suppliers</button>
            <button onClick={() => setInput("Show me all blocked work orders.")}>Blocked WO</button>
            <button onClick={() => setInput("What part does Quantum Electronics supply?")}>Quantum Electronics</button>
          </div>

          <form onSubmit={handleSend} className="input-form">
            <input 
              type="text" 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              placeholder="Ask about parts, suppliers, or lead times..." 
              autoFocus
            />
            <button type="submit" disabled={!input.trim() || loading} className="send-btn">
              Send
            </button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default App;
