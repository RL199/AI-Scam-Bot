import React from "react";

interface TypingIndicatorProps {
  text?: string;
}

const TypingIndicator: React.FC<TypingIndicatorProps> = ({
  text = "Support agent is typing",
}) => {
  return (
    <div className="message-container">
      <div className="message-assistant">
        <div className="typing-indicator">
          <span className="text-sm italic text-secondary-600 font-medium">
            {text}
          </span>
          <div className="flex space-x-1 ml-2">
            <div 
              className="w-2 h-2 bg-secondary-400 rounded-full"
              style={{ 
                animation: 'typing-bounce 1.4s infinite ease-in-out',
                animationDelay: '-0.32s' 
              }}
            ></div>
            <div 
              className="w-2 h-2 bg-secondary-400 rounded-full"
              style={{ 
                animation: 'typing-bounce 1.4s infinite ease-in-out',
                animationDelay: '-0.16s' 
              }}
            ></div>
            <div 
              className="w-2 h-2 bg-secondary-400 rounded-full"
              style={{ 
                animation: 'typing-bounce 1.4s infinite ease-in-out',
                animationDelay: '0s' 
              }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
