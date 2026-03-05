import React, { useState } from "react";
import axios from "axios";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const register = async () => {
    try {
      await axios.post("http://localhost:8000/register", {
        username,
        password,
      });

      alert("Registered successfully!");
    } catch (error) {
      alert("Registration failed");
    }
  };

  return (
    <div className="auth-box">
      <h2>Register</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={register}>Register</button>
    </div>
  );
}

export default Register;