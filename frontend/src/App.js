import React from "react";
import Chat from "./pages/Chat";
import "./styles/global.css";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Aura - AI Assistant</h1>
      </header>
      <Chat />
    </div>
  );
}

export default App;
