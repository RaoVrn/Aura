import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import InputField from "../components/InputField";
import Message from "../components/Message";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const chatBoxRef = useRef(null);

  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  const sendQuery = async (query) => {
    if (!query.trim()) return;

    // Add the user message
    const userMessage = { text: query, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    // Show the loading indicator
    setIsLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:5000/ask", { query });
      const aiMessage = { text: res.data.response, sender: "ai" };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { text: "Error fetching response.", sender: "ai" },
      ]);
    } finally {
      // Hide the loading indicator
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      {/* Title moved to App.js */}
      <div className="chat-box" ref={chatBoxRef}>
        {messages.map((msg, index) => (
          <Message key={index} text={msg.text} sender={msg.sender} />
        ))}
        {isLoading && (
          <div className="message ai">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
      </div>
      <InputField sendQuery={sendQuery} />
    </div>
  );
}

export default Chat;
