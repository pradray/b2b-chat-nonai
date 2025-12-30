import { useState, useEffect, useRef } from 'react';

const ChatWidget = ({ onNavigate }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! I can help with MOQ, Pricing, or Navigation.", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (textOverride = null) => {
    const textToSend = textOverride || input;
    if (!textToSend.trim()) return;

    const newMessages = [...messages, { text: textToSend, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    try {
      // Connect to Python Backend (Flask)
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: textToSend })
      });
      
      const data = await response.json();

      setMessages(prev => [...prev, { text: data.message, sender: "bot" }]);

      if (data.action) {
        onNavigate(data.action);
      }

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { text: "Error: Backend not reachable.", sender: "bot" }]);
    }
  };

  return (
    <div className="chat-widget">
      <button className="chat-toggle" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? "✖" : "💬 Support"}
      </button>

      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">B2B Assistant</div>
          <div className="chat-body">
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
            
            <div className="chips">
              <button onClick={() => handleSend("Check MOQ")}>MOQ</button>
              <button onClick={() => handleSend("Go to Marketplace")}>Marketplace</button>
              <button onClick={() => handleSend("Suppliers")}>Suppliers</button>
            </div>
          </div>
          <div className="chat-input-area">
            <input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type here..."
            />
            <button onClick={() => handleSend()}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;