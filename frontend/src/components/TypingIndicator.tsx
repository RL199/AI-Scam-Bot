import React from 'react';

interface TypingIndicatorProps {
  text?: string;
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({ text = 'Support agent is typing' }) => {
  return (
    <div className="message-container">
      <div className="message-assistant">
        <div className="typing-indicator">
          <span className="text-sm italic text-secondary-600 font-medium">{text}</span>
          <div className="flex space-x-1 ml-2">
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
            <div className="typing-dot"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
