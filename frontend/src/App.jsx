import { useState } from 'react';
import './App.css';
import ChatWidget from './ChatWidget';

function App() {
  const [activeTab, setActiveTab] = useState('marketplace');

  // --- MOCK DATA ---
  const products = [
    { id: 1, name: "Industrial Servo Motor", price: "$450.00", moq: "10 Units" },
    { id: 2, name: "500m Fiber Optic Cable", price: "$120.00", moq: "20 Rolls" },
    { id: 3, name: "Heavy Duty Actuator", price: "$85.00", moq: "50 Units" },
  ];

  const suppliers = [
    { name: "Global Steel Works", region: "Germany", rating: "★★★★★" },
    { name: "Shenzhen Electronics", region: "China", rating: "★★★★☆" },
  ];

  // Callback for Chatbot Navigation
  const handleBotNavigation = (page) => {
    if (page && ['marketplace', 'suppliers', 'rfq', 'login'].includes(page)) {
      setActiveTab(page);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Global B2B Hub</h1>
        <nav>
          <button className={activeTab === 'marketplace' ? 'active' : ''} onClick={() => setActiveTab('marketplace')}>Marketplace</button>
          <button className={activeTab === 'suppliers' ? 'active' : ''} onClick={() => setActiveTab('suppliers')}>Suppliers</button>
          <button className={activeTab === 'rfq' ? 'active' : ''} onClick={() => setActiveTab('rfq')}>Bulk RFQ</button>
          <button className={activeTab === 'login' ? 'active' : ''} onClick={() => setActiveTab('login')}>Login</button>
        </nav>
      </header>

      <main className="main-content">
        {activeTab === 'marketplace' && (
          <div className="fade-in">
            <h2>Wholesale Marketplace</h2>
            <div className="grid">
              {products.map(p => (
                <div key={p.id} className="card">
                  <h3>{p.name}</h3>
                  <p>Price: {p.price}</p>
                  <span className="badge">MOQ: {p.moq}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'suppliers' && (
          <div className="fade-in">
            <h2>Verified Suppliers</h2>
            <ul>
              {suppliers.map((s, idx) => (
                <li key={idx} className="list-item">
                  <strong>{s.name}</strong> ({s.region}) - {s.rating}
                </li>
              ))}
            </ul>
          </div>
        )}

        {activeTab === 'rfq' && (
          <div className="fade-in">
            <h2>Request for Quotation</h2>
            <form className="rfq-form" onSubmit={(e) => e.preventDefault()}>
              <input placeholder="Company Name" className="input-field" />
              <input placeholder="Target Price" type="number" className="input-field" />
              <button className="btn-primary">Submit RFQ</button>
            </form>
          </div>
        )}

        {activeTab === 'login' && (
          <div className="fade-in">
            <h2>Partner Login</h2>
            <input placeholder="Email" className="input-field" />
            <button className="btn-primary">Login</button>
          </div>
        )}
      </main>

      {/* Pass navigation handler to ChatWidget */}
      <ChatWidget onNavigate={handleBotNavigation} />
    </div>
  );
}

export default App;