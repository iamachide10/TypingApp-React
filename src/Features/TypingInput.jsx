import React from "react";
import './TypingInput.css'; // Import CSS

function TypingInput({ userInput, setUserInput }) {
  return (
    <div className="typing-input-container">
      <input
        className="typing-input"
        type="text"
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Start typing..."
      />
    </div>
  );
}

export default TypingInput;
