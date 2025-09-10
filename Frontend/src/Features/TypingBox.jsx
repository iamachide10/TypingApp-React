
import './TypingBox.css'; // Import CSS

function TypingBox({ text, userInput }) {
  return (
    <div className="typing-box">
      {text.split('').map((char, index) => {
        let className = '';
        if (index < userInput.length) {
          className = char === userInput[index] ? 'correct' : 'incorrect';
        }
        return (
          <span key={index} className={className}>
            {char}
          </span>
        );
      })}
    </div>
  );
}

export default TypingBox;
