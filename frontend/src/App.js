import React, { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const sendQuery = async () => {
    if (!query) return;
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/chat", { query });
      setResponse(res.data.response);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <h1 className="text-2xl font-bold mb-4">Aura - AI Assistant</h1>
      <input
        type="text"
        className="p-2 border rounded w-1/2"
        placeholder="Ask Aura anything..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        className="mt-3 p-2 bg-blue-500 text-white rounded"
        onClick={sendQuery}
      >
        Send
      </button>
      {response && (
        <div className="mt-4 p-3 bg-white shadow-md w-1/2 rounded">
          <strong>Response:</strong> {response}
        </div>
      )}
    </div>
  );
}

export default App;
