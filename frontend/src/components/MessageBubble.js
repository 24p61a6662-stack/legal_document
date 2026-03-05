import React from "react";

function MessageBubble({ message, sender }) {
  return (
    <div className={`message ${sender}`}>
      {message}
    </div>
  );
}

export default MessageBubble;