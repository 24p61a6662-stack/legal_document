import { useState } from "react";
import axios from "axios";

function Chat() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        query: query,
      });

      setResponse(res.data.answer);   // 🔥 This displays answer
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>AI Legal Assistant</h2>

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button onClick={sendMessage}>Send</button>

      <p>{response}</p>  {/* 🔥 This shows chatbot answer */}
    </div>
  );
}

export default Chat;