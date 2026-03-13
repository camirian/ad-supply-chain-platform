import React, { useState, useEffect, useRef } from 'react';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import { Shield, Database, FileText, Upload, Play, Server, Beaker, Network } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import './App.css';

const API_BASE = "http://localhost:8000";

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { label: 'Mission Control', icon: <Shield size={18} />, path: '/' },
    { label: 'Agent Chat', icon: <Network size={18} />, path: '/agent' },
    { label: 'Validation Matrix', icon: <Database size={18} />, path: '/database' },
    { label: 'Documentation', icon: <FileText size={18} />, path: '/docs' }
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <Server size={24} className="brand-icon" />
        <div>
          <h2 className="brand-title">A&D Supply</h2>
          <span className="brand-subtitle">Project Workspace</span>
        </div>
      </div>
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.path}
            className={`nav-btn ${location.pathname === item.path ? 'active' : ''}`}
            onClick={() => navigate(item.path)}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </nav>
    </aside>
  );
};

const LandingPage = ({ apiKey, setApiKey }) => {
  const [tempKey, setTempKey] = useState(apiKey || '');
  const navigate = useNavigate();

  const handleSaveToken = () => {
    setApiKey(tempKey);
    // Once they hit save, if there's a key, naturally guide to Agent Chat
    if (tempKey) {
      navigate('/agent');
    }
  };

  return (
    <div className="page-container landing">
      <div className="hero-section">
        <h1 className="hero-title">A&D Supply Chain Verifier</h1>
        <p className="hero-description">
          Your AI-Powered Systems Engineering Co-Pilot. Automate the interrogation of your supply chain database using native, zero-billing Gemini LangChain reasoning blocks.
        </p>
      </div>

      <div className="feature-cards">
        <div className="card">
          <div className="card-icon-wrapper"><Database size={24} /></div>
          <h3>1. Interrogate Schema</h3>
          <p>Review the localized SQLite database containing normalized schemas for Parts, Suppliers, and Work Orders.</p>
        </div>
        <div className="card">
          <div className="card-icon-wrapper"><Beaker size={24} /></div>
          <h3>2. AI SQL Synthesis</h3>
          <p>The Gemini-backed LangChain agent autonomously drafts SELECT statements compliant with the schema.</p>
        </div>
        <div className="card">
          <div className="card-icon-wrapper"><Play size={24} /></div>
          <h3>3. Execute & Verify</h3>
          <p>Securely run the generated Pytest-equivalent scripts and conversational abstractions against the backend.</p>
        </div>
      </div>

      <div className="api-key-section">
        <div className="api-key-card">
          <label className="key-label">
            <Shield size={16} /> Google Gemini API Key
          </label>
          <input 
            type="password" 
            value={tempKey} 
            onChange={(e) => setTempKey(e.target.value)} 
            placeholder="sk-..." 
            className="key-input"
          />
          <button onClick={handleSaveToken} className="btn-primary">
            <Upload size={18} /> Configure Cortex
          </button>
        </div>
      </div>
    </div>
  );
};

const AgentPage = ({ apiKey }) => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am your A&D supply chain tracking agent. Ensure you have provided your Gemini API Key in the Mission Control center. How can I assist you today?' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userQuery = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userQuery }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userQuery, api_key: apiKey })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response || `Error: ${data.detail}` }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: `Network Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container chat-layout">
        <header className="page-header">
          <h1>Semantic Logic Interface</h1>
          <p>Probe the intelligence matrix via conversational abstraction logic.</p>
        </header>
        <div className="chat-window">
          <div className="messages">
            {messages.map((m, idx) => (
              <div key={idx} className={`message-row ${m.role}`}>
                <div className={`message-bubble ${m.role}`}>
                  {m.role === 'assistant' && <span className="avatar">🤖</span>}
                  {m.role === 'user' && <span className="avatar">👤</span>}
                  <div className="markdown"><ReactMarkdown>{m.content}</ReactMarkdown></div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="message-row assistant">
                <div className="message-bubble assistant loading">
                  <span className="avatar">🤖</span>
                  <div className="typing-indicator"><span></span><span></span><span></span></div>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
          <form onSubmit={handleSend} className="input-form">
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Query supply chain requirements..." />
            <button type="submit" disabled={!input.trim() || loading} className="btn-primary square-btn">Synthesize Action</button>
          </form>
        </div>
    </div>
  );
};

const DatabasePage = () => {
  const [schema, setSchema] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/schema`)
      .then(res => res.json())
      .then(data => setSchema(data.schema))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="page-container schema-layout">
      <header className="page-header">
        <h1>Ephemeral State Matrix</h1>
        <p>Live memory block of the Cloud Run verification database.</p>
      </header>
      <div className="schema-container">
        {schema ? Object.keys(schema).map(table => (
          <div key={table} className="table-card">
            <h3>📦 {table}</h3>
            <div className="table-preview">
              <table>
                <thead>
                  <tr>{schema[table].length > 0 && Object.keys(schema[table][0]).map(k => <th key={k}>{k}</th>)}</tr>
                </thead>
                <tbody>
                  {schema[table].slice(0, 3).map((row, idx) => (
                    <tr key={idx}>{Object.values(row).map((val, i) => <td key={i}>{String(val)}</td>)}</tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )) : <div className="loading-state">Syncing logic blocks from backend...</div>}
      </div>
    </div>
  );
};

const DocsPage = () => {
  const [docs, setDocs] = useState([]);
  const [activeDoc, setActiveDoc] = useState('');
  const [content, setContent] = useState('');

  useEffect(() => {
    fetch(`${API_BASE}/api/docs`)
      .then(res => res.json())
      .then(data => {
        setDocs(data.docs);
        if (data.docs.length > 0) loadDoc(data.docs[0]);
      });
  }, []);

  const loadDoc = async (docId) => {
    setActiveDoc(docId);
    setContent('Syncing Document Context...');
    try {
      const res = await fetch(`${API_BASE}/api/docs/${encodeURIComponent(docId)}`);
      const data = await res.json();
      setContent(data.content);
    } catch(err) {
      setContent('Failed to authenticate remote doc logic.');
    }
  };

  return (
    <div className="page-container docs-layout">
      <header className="page-header">
        <h1>Project Knowledge Base</h1>
        <p>Access the complete repository of technical documentation, architectural guides, and system manuals.</p>
      </header>
      <div className="docs-content-wrapper">
        <aside className="docs-sidebar">
          <h4>AVAILABLE DOCUMENTS</h4>
          {docs.map(doc => (
            <button key={doc} className={`doc-link ${activeDoc === doc ? 'active' : ''}`} onClick={() => loadDoc(doc)}>
              <FileText size={16}/> {doc}
            </button>
          ))}
        </aside>
        <section className="docs-viewer">
          <h3>{activeDoc}</h3>
          <div className="markdown-body">
            <ReactMarkdown>{content}</ReactMarkdown>
          </div>
        </section>
      </div>
    </div>
  );
};

function App() {
  const [apiKey, setApiKey] = useState('');

  return (
    <div className="app-layout">
      <Sidebar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<LandingPage apiKey={apiKey} setApiKey={setApiKey} />} />
          <Route path="/agent" element={<AgentPage apiKey={apiKey} />} />
          <Route path="/database" element={<DatabasePage />} />
          <Route path="/docs" element={<DocsPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
