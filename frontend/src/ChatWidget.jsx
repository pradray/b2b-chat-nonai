/**
 * B2B Chat Widget - Updated with Security & Accessibility Fixes
 * ==============================================================
 * Changes made:
 * 1. Input sanitization (Security)
 * 2. Request timeout with AbortController (Security)
 * 3. aria-live region for screen readers (Accessibility - WCAG 4.1.3)
 * 4. Escape key to close (Accessibility - WCAG 2.1.1)
 * 5. Proper ARIA labels (Accessibility - WCAG 4.1.2)
 * 6. Focus management (Accessibility - WCAG 2.4.3)
 * 7. Loading state improvements (UX)
 */

import { useState, useEffect, useRef } from 'react';

// Configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/chat';
const MAX_MESSAGE_LENGTH = 500;
const REQUEST_TIMEOUT_MS = 10000; // 10 seconds

/**
 * Security: Sanitize user input
 */
const sanitizeInput = (text) => {
  if (typeof text !== 'string') return '';
  return text
    .replace(/[<>]/g, '') // Remove potential HTML tags
    .slice(0, MAX_MESSAGE_LENGTH)
    .trim();
};

const ChatWidget = ({ onNavigate }) => {
  // State
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: "Hello! I can help with MOQ, Pricing, Shipping, or Navigation. What do you need?", sender: "bot" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Refs
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const chatWindowRef = useRef(null);

  /**
   * Auto-scroll to bottom when messages change
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  /**
   * Accessibility: Focus input when chat opens
   */
  useEffect(() => {
    if (isOpen && inputRef.current) {
      // Small delay to ensure DOM is ready
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  }, [isOpen]);

  /**
   * Accessibility: Handle Escape key to close chat (WCAG 2.1.1)
   */
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen]);

  /**
   * Send message to backend
   */
  const handleSend = async (textOverride = null) => {
    const rawText = textOverride || input;
    const textToSend = sanitizeInput(rawText);
    
    // Validation
    if (!textToSend || isLoading) return;

    // Add user message immediately
    setMessages(prev => [...prev, { text: textToSend, sender: "user" }]);
    setInput("");
    setIsLoading(true);

    // Security: Request timeout with AbortController
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: textToSend }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
      }

      const data = await response.json();

      // Add bot response
      setMessages(prev => [...prev, { text: data.message, sender: "bot" }]);

      // Handle navigation action
      if (data.action) {
        onNavigate(data.action);
      }

    } catch (error) {
      clearTimeout(timeoutId);
      
      let errorMessage = "Network error. Please try again.";
      
      if (error.name === 'AbortError') {
        errorMessage = "Request timed out. Please try again.";
      } else if (error.message.includes('429')) {
        errorMessage = "Too many requests. Please wait a moment.";
      }

      setMessages(prev => [...prev, { text: errorMessage, sender: "bot" }]);
      console.error('Chat error:', error);
      
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handle keyboard events
   */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  /**
   * Toggle chat open/closed
   */
  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  /**
   * Quick action chips
   */
  const quickActions = [
    { label: "MOQ", message: "What is the minimum order quantity?" },
    { label: "Marketplace", message: "Show me the marketplace" },
    { label: "Suppliers", message: "Show me the suppliers" },
    { label: "Shipping", message: "What are the shipping options?" },
    { label: "Help", message: "What can you help me with?" }
  ];

  return (
    <div className="chat-widget">
      {/* Toggle Button */}
      <button 
        className="chat-toggle" 
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat support" : "Open chat support"}
        aria-expanded={isOpen}
        aria-controls="chat-dialog"
      >
        {isOpen ? "✖" : "💬 Support"}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div 
          id="chat-dialog"
          className="chat-window" 
          role="dialog"
          aria-modal="true"
          aria-label="B2B Support Chat"
          aria-describedby="chat-description"
          ref={chatWindowRef}
        >
          {/* Header */}
          <div className="chat-header">
            <span id="chat-description">B2B Assistant</span>
            <button 
              onClick={() => setIsOpen(false)} 
              aria-label="Close chat"
              className="chat-close-btn"
            >
              ✖
            </button>
          </div>

          {/* Message Area - Accessibility: aria-live for screen readers */}
          <div 
            className="chat-body"
            role="log"
            aria-live="polite"
            aria-label="Chat messages"
            aria-relevant="additions"
          >
            {messages.map((msg, i) => (
              <div 
                key={i} 
                className={`message ${msg.sender}`}
                role="article"
                aria-label={`${msg.sender === 'bot' ? 'Assistant' : 'You'}: ${msg.text}`}
              >
                {msg.text}
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="message bot typing" aria-live="polite">
                <span className="typing-indicator">
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                  <span className="typing-dot"></span>
                </span>
                <span className="visually-hidden">Assistant is typing</span>
              </div>
            )}

            <div ref={messagesEndRef} />

            {/* Quick Action Chips */}
            <div className="chips" role="group" aria-label="Quick actions">
              {quickActions.map((action, index) => (
                <button 
                  key={index}
                  onClick={() => handleSend(action.message)}
                  aria-label={`Quick action: ${action.label}`}
                  disabled={isLoading}
                >
                  {action.label}
                </button>
              ))}
            </div>
          </div>

          {/* Input Area */}
          <div className="chat-input-area">
            <label htmlFor="chat-input" className="visually-hidden">
              Type your message
            </label>
            <input
              id="chat-input"
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              aria-describedby="chat-input-hint"
              maxLength={MAX_MESSAGE_LENGTH}
              disabled={isLoading}
              autoComplete="off"
            />
            <span id="chat-input-hint" className="visually-hidden">
              Press Enter to send or click the Send button
            </span>
            <button 
              onClick={() => handleSend()}
              aria-label="Send message"
              disabled={isLoading || !input.trim()}
            >
              {isLoading ? "..." : "Send"}
            </button>
          </div>

          {/* Character Counter */}
          {input.length > 0 && (
            <div className="char-counter" aria-live="polite">
              {input.length}/{MAX_MESSAGE_LENGTH}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ChatWidget;
