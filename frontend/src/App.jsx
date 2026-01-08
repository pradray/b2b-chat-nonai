/**
 * B2B Hub Main Application - Updated with Accessibility Fixes
 * ============================================================
 * Changes made:
 * 1. Form labels added (Accessibility - WCAG 1.3.1)
 * 2. Proper form structure (Accessibility)
 * 3. aria-current for navigation (Accessibility)
 * 4. Skip link for keyboard users (Accessibility)
 */

import { useState } from 'react';
import './App.css';
import ChatWidget from './ChatWidget';

function App() {
  const [activeTab, setActiveTab] = useState('marketplace');

  // Form state
  const [rfqForm, setRfqForm] = useState({ companyName: '', targetPrice: '' });
  const [loginForm, setLoginForm] = useState({ email: '' });

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

  // Form handlers
  const handleRfqSubmit = (e) => {
    e.preventDefault();
    alert(`RFQ Submitted!\nCompany: ${rfqForm.companyName}\nTarget Price: $${rfqForm.targetPrice}`);
    setRfqForm({ companyName: '', targetPrice: '' });
  };

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    alert(`Login attempted with: ${loginForm.email}`);
    setLoginForm({ email: '' });
  };

  return (
    <div className="app-container">
      {/* Accessibility: Skip link for keyboard users */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <header className="header">
        <h1>Global B2B Hub</h1>
        <nav aria-label="Main navigation">
          <button 
            className={activeTab === 'marketplace' ? 'active' : ''} 
            onClick={() => setActiveTab('marketplace')}
            aria-current={activeTab === 'marketplace' ? 'page' : undefined}
          >
            Marketplace
          </button>
          <button 
            className={activeTab === 'suppliers' ? 'active' : ''} 
            onClick={() => setActiveTab('suppliers')}
            aria-current={activeTab === 'suppliers' ? 'page' : undefined}
          >
            Suppliers
          </button>
          <button 
            className={activeTab === 'rfq' ? 'active' : ''} 
            onClick={() => setActiveTab('rfq')}
            aria-current={activeTab === 'rfq' ? 'page' : undefined}
          >
            Bulk RFQ
          </button>
          <button 
            className={activeTab === 'login' ? 'active' : ''} 
            onClick={() => setActiveTab('login')}
            aria-current={activeTab === 'login' ? 'page' : undefined}
          >
            Login
          </button>
        </nav>
      </header>

      <main id="main-content" className="main-content">
        {/* Marketplace Tab */}
        {activeTab === 'marketplace' && (
          <div className="fade-in">
            <h2>Wholesale Marketplace</h2>
            <div className="grid" role="list" aria-label="Product listings">
              {products.map(p => (
                <div key={p.id} className="card" role="listitem">
                  <h3>{p.name}</h3>
                  <p>Price: {p.price}</p>
                  <span className="badge">MOQ: {p.moq}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Suppliers Tab */}
        {activeTab === 'suppliers' && (
          <div className="fade-in">
            <h2>Verified Suppliers</h2>
            <ul aria-label="Supplier list">
              {suppliers.map((s, idx) => (
                <li key={idx} className="list-item">
                  <strong>{s.name}</strong> ({s.region}) - 
                  <span aria-label={`Rating: ${s.rating.length} out of 5 stars`}>
                    {s.rating}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* RFQ Tab - Accessibility: Proper form labels */}
        {activeTab === 'rfq' && (
          <div className="fade-in">
            <h2>Request for Quotation</h2>
            <form 
              className="rfq-form" 
              onSubmit={handleRfqSubmit}
              aria-label="Request for quotation form"
            >
              <div className="form-group">
                <label htmlFor="company-name">Company Name</label>
                <input 
                  id="company-name"
                  type="text"
                  placeholder="Enter your company name" 
                  className="input-field"
                  value={rfqForm.companyName}
                  onChange={(e) => setRfqForm({...rfqForm, companyName: e.target.value})}
                  required
                  aria-required="true"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="target-price">Target Price (USD)</label>
                <input 
                  id="target-price"
                  type="number"
                  placeholder="Enter target price" 
                  className="input-field"
                  value={rfqForm.targetPrice}
                  onChange={(e) => setRfqForm({...rfqForm, targetPrice: e.target.value})}
                  min="0"
                  step="0.01"
                  required
                  aria-required="true"
                />
              </div>
              
              <button type="submit" className="btn-primary">
                Submit RFQ
              </button>
            </form>
          </div>
        )}

        {/* Login Tab - Accessibility: Proper form labels */}
        {activeTab === 'login' && (
          <div className="fade-in">
            <h2>Partner Login</h2>
            <form 
              className="login-form"
              onSubmit={handleLoginSubmit}
              aria-label="Partner login form"
            >
              <div className="form-group">
                <label htmlFor="login-email">Email Address</label>
                <input 
                  id="login-email"
                  type="email"
                  placeholder="Enter your email" 
                  className="input-field"
                  value={loginForm.email}
                  onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                  required
                  aria-required="true"
                  autoComplete="email"
                />
              </div>
              
              <button type="submit" className="btn-primary">
                Login
              </button>
              
              <p className="form-hint">
                New partner? Contact sales@b2bhub.com to register.
              </p>
            </form>
          </div>
        )}
      </main>

      {/* Chat Widget */}
      <ChatWidget onNavigate={handleBotNavigation} />
    </div>
  );
}

export default App;
