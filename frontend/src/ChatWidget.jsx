import { useState, useEffect, useRef } from 'react';

// Use environment variable for URL
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/chat';

const ChatWidget = ({ onNavigate }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! I can help with MOQ, Pricing, or Navigation.", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false); // New: Typing State
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = async (textOverride = null) => {
    const textToSend = textOverride || input;
    if (!textToSend.trim()) return;

    // 1. Add User Message immediately
    const newMessages = [...messages, { text: textToSend, sender: "user" }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true); // Start loading

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: textToSend })
      });
      
      const data = await response.json();

      // 2. Add Bot Response after delay (simulates thinking)
      setMessages(prev => [...prev, { text: data.message, sender: "bot" }]);

      if (data.action) {
        onNavigate(data.action);
      }

    } catch (error) {
      setMessages(prev => [...prev, { text: "Network error. Please try again.", sender: "bot" }]);
    } finally {
      setIsLoading(false); // Stop loading
    }
  };

  // Accessibility: Handle 'Enter' key
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  return (
    <div className="chat-widget">
      <button 
        className="chat-toggle" 
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle Chat Support" // A11y
      >
        {isOpen ? "✖" : "💬 Support"}
      </button>

      {isOpen && (
        <div 
          className="chat-window" 
          role="dialog" // A11y
          aria-label="B2B Support Assistant" // A11y
        >
          <div className="chat-header">
            B2B Assistant
            <button onClick={() => setIsOpen(false)} aria-label="Close Chat" style={{background:'none', border:'none', color:'white', cursor:'pointer'}}>✖</button>
          </div>
          
          <div className="chat-body">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
            
            {/* Loading Indicator */}
            {isLoading && <div className="message bot typing">Bot is typing...</div>}
            
            <div ref={messagesEndRef} />
            
            <div className="chips">
              {/* Added tabIndex for keyboard navigation */}
              <button onClick={() => handleSend("Check MOQ")} tabIndex="0">MOQ</button>
              <button onClick={() => handleSend("Go to Marketplace")} tabIndex="0">Marketplace</button>
              <button onClick={() => handleSend("Suppliers")} tabIndex="0">Suppliers</button>
            </div>
          </div>

          <div className="chat-input-area">
            <input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown} // Replaced onKeyPress
              placeholder="Type here..."
              aria-label="Type your message" // A11y
            />
            <button onClick={() => handleSend()}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;