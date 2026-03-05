import axios from "axios";
import { useState } from "react";

function Dashboard({ setToken }) {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    const token = localStorage.getItem("token");

    try {
      const res = await axios.post(
        "http://localhost:8000/chat",
        { text: input },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setResponse(res.data.reply);
    } catch (error) {
      alert("Unauthorized or backend error. Please login again.");
      localStorage.removeItem("token");
      setToken(null);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <div>
      <h2>AI Legal Assistant</h2>
      <button onClick={logout}>Logout</button>

      <input
        placeholder="Ask something..."
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>

      <p>{response}</p>
    </div>
  );
}

export default Dashboard;