import React, { useState, useRef, useEffect } from "react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = "Type your IT support question...",
}) => {
  const [message, setMessage] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = Math.min(textarea.scrollHeight, 120) + "px";
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [message]);

  // Focus the textarea after sending a message or when becoming enabled
  useEffect(() => {
    if (!disabled && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [disabled, message]);

  // Focus on component mount
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage("");
      // Focus will be handled by the useEffect above
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
  };

  return (
    <div className="chat-input-container">
      <div className="chat-input-wrapper">
        <form
          onSubmit={handleSubmit}
          className="flex items-end space-x-2 sm:space-x-4"
        >
          <div className="flex-1">
            <div className="relative">
              <textarea
                ref={textareaRef}
                value={message}
                onChange={handleInputChange}
                onKeyPress={handleKeyPress}
                placeholder={placeholder}
                disabled={disabled}
                rows={1}
                className="input-field resize-none min-h-[44px] sm:min-h-[48px] pr-10 sm:pr-12 text-sm sm:text-base"
                style={{ paddingRight: "2.5rem" }}
              />
              {message.length > 0 && (
                <div className="absolute right-2 sm:right-3 bottom-2 sm:bottom-3 text-xs text-secondary-400">
                  {message.length}/500
                </div>
              )}
            </div>
            <div className="flex items-center justify-between mt-2 text-xs text-secondary-500">
              <span className="hidden sm:block">
                Press Enter to send, Shift+Enter for new line
              </span>
              <span className="sm:hidden">Tap send or press Enter</span>
              {disabled && (
                <span className="text-warning-600 font-medium">
                  Please wait...
                </span>
              )}
            </div>
          </div>
          <button
            type="submit"
            disabled={disabled || !message.trim() || message.length > 500}
            className="btn-primary flex items-center justify-center min-w-[44px] h-[44px] sm:min-w-[48px] sm:h-[48px] touch-manipulation"
            title="Send message"
          >
            <svg
              className="w-4 h-4 sm:w-5 sm:h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          </button>
        </form>

        <div className="flex items-center justify-between mt-2 sm:mt-3 text-xs text-secondary-500">
          <div className="flex items-center space-x-2 sm:space-x-4">
            <span className="flex items-center space-x-1">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="hidden sm:inline">Secure chat</span>
              <span className="sm:hidden">Secure</span>
            </span>
            <span className="flex items-center space-x-1">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="hidden sm:inline">End-to-end encrypted</span>
              <span className="sm:hidden">Encrypted</span>
            </span>
          </div>
          <span className="hidden sm:inline">TechSupport Pro v2.1</span>
          <span className="sm:hidden">v2.1</span>
        </div>
      </div>
    </div>
  );
};

export default ChatInput;
