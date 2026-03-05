import React from "react";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

function Home() {
  return (
    <div className="app-container">
      <Sidebar />
      <ChatWindow />
    </div>
  );
}

export default Home;