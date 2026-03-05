import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("chatHistory")) || [];
    setHistory(saved);
  }, []);

  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(history));
  }, [history]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // 🎤 Voice Input
  const startVoiceInput = () => {
    if (!window.webkitSpeechRecognition) {
      alert("Voice recognition not supported in this browser");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
      const voiceText = event.results[0][0].transcript;
      setInput(voiceText);
    };
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    const updatedMessages = [...messages, userMessage];

    setMessages(updatedMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        question: userMessage.content,
      });

      const botMessage = {
        role: "bot",
        content: res.data.answer,
      };

      const finalMessages = [...updatedMessages, botMessage];
      setMessages(finalMessages);

      if (currentChatId === null) {
        const newChat = {
          id: Date.now(),
          title: userMessage.content.slice(0, 30),
          messages: finalMessages,
        };
        setHistory((prev) => [...prev, newChat]);
        setCurrentChatId(newChat.id);
      } else {
        setHistory((prev) =>
          prev.map((chat) =>
            chat.id === currentChatId
              ? { ...chat, messages: finalMessages }
              : chat
          )
        );
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // 📎 Upload Handler
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      const botMessage = {
        role: "bot",
        content: res.data.answer,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const loadChat = (chat) => {
    setMessages(chat.messages);
    setCurrentChatId(chat.id);
  };

  const newChat = () => {
    setMessages([]);
    setCurrentChatId(null);
  };

  const deleteChat = (id) => {
    const updated = history.filter((chat) => chat.id !== id);
    setHistory(updated);
    if (id === currentChatId) {
      setMessages([]);
      setCurrentChatId(null);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", background: "#343541", color: "white" }}>

      {/* Sidebar */}
      <div style={{ width: "260px", background: "#202123", padding: "15px", overflowY: "auto" }}>
        <button onClick={newChat}
          style={{
            width: "100%",
            padding: "10px",
            marginBottom: "15px",
            background: "#444654",
            color: "white",
            border: "none",
            borderRadius: "5px"
          }}>
          + New Chat
        </button>

        {history.map((chat) => (
          <div key={chat.id}
            style={{
              display: "flex",
              alignItems: "center",
              padding: "10px",
              marginBottom: "10px",
              background: "#2a2b32",
              borderRadius: "5px",
              fontSize: "14px"
            }}>
            <div onClick={() => loadChat(chat)} style={{ flex: 1, cursor: "pointer" }}>
              {chat.title}
            </div>
            <button onClick={() => deleteChat(chat.id)}
              style={{ background: "transparent", border: "none", color: "#888" }}>
              ✕
            </button>
          </div>
        ))}
      </div>

      {/* Chat Area */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>

        {/* Messages */}
        <div style={{ flex: 1, padding: "20px", overflowY: "auto" }}>
          {messages.map((msg, index) => (
            <div key={index}
              style={{
                marginBottom: "15px",
                display: "flex",
                justifyContent: msg.role === "user" ? "flex-end" : "flex-start"
              }}>
              <div style={{
                maxWidth: "70%",
                padding: "12px",
                borderRadius: "8px",
                background: msg.role === "user" ? "#10a37f" : "#444654",
                whiteSpace: "pre-wrap"
              }}>
                {msg.content}
              </div>
            </div>
          ))}
          {loading && <div style={{ color: "#aaa" }}>Typing...</div>}
          <div ref={chatEndRef} />
        </div>

        {/* ✅ ChatGPT Style Input */}
        <div style={{ padding: "15px", background: "#343541", display: "flex", justifyContent: "center" }}>
          <div style={{
            width: "100%",
            maxWidth: "800px",
            background: "#40414f",
            borderRadius: "25px",
            display: "flex",
            alignItems: "center",
            padding: "8px 15px",
            gap: "10px",
          }}>

            {/* 📎 Upload */}
            <label style={{ cursor: "pointer", fontSize: "18px" }}>
              📎
              <input type="file" hidden onChange={handleFileUpload} />
            </label>

            {/* Text Area */}
            <textarea
              style={{
                flex: 1,
                background: "transparent",
                border: "none",
                outline: "none",
                color: "white",
                resize: "none",
                fontSize: "14px",
              }}
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Message Legal AI..."
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendMessage();
                }
              }}
            />

            {/* 🎤 Voice */}
            <button
              onClick={startVoiceInput}
              style={{
                background: "transparent",
                border: "none",
                color: "white",
                fontSize: "18px",
                cursor: "pointer",
              }}>
              🎤
            </button>

          </div>
        </div>

      </div>
    </div>
  );
}

export default App;