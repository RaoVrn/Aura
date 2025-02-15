//// filepath: /d:/Aura/frontend/src/components/InputField.js
import React, { useState } from "react";
import { IoSend } from "react-icons/io5"; 

function InputField({ sendQuery }) {
  const [query, setQuery] = useState("");

  const handleSend = () => {
    sendQuery(query);
    setQuery("");
  };

  return (
    <div className="input-container">
      <input
        type="text"
        className="input-field"
        placeholder="Ask Aura anything..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <button className="send-button" onClick={handleSend}>
        <IoSend size={20} />
      </button>
    </div>
  );
}

export default InputField;