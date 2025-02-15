import React from "react";
import ReactMarkdown from "react-markdown";
import PropTypes from "prop-types";

function Message({ text, sender }) {
  return (
    <div className={`message ${sender === "user" ? "user" : "ai"}`}>
      <ReactMarkdown>{text || "No message available."}</ReactMarkdown>
    </div>
  );
}

Message.propTypes = {
  text: PropTypes.string.isRequired,
  sender: PropTypes.oneOf(["user", "ai"]).isRequired,
};

export default Message;
