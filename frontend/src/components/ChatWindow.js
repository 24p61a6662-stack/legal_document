import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import MessageBubble from "./MessageBubble";

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    try {
      // ✅ Get token from localStorage
      const token = localStorage.getItem("token");

      const res = await axios.post(
        "http://localhost:8000/chat",
        { query: input },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const botMessage = {
        text: res.data.response,
        sender: "bot",
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          text: "Unauthorized or backend error. Please login again.",
          sender: "bot",
        },
      ]);
    }

    setInput("");
  };

  return (
    <div className="chat-area">
      <div className="chat-header">Legal Contract Assistant</div>

      <div className="messages">
        {messages.map((msg, index) => (
          <MessageBubble
            key={index}
            message={msg.text}
            sender={msg.sender}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <textarea
          rows="2"
          placeholder="Ask about clauses, risks, compliance..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default ChatWindow;