import React from 'react';
import { ChatMessage } from '../types/api';

interface MessageProps {
  message: ChatMessage;
  timestamp?: Date;
}

const Message: React.FC<MessageProps> = ({ message, timestamp }) => {
  const isUser = message.role === 'user';
  const timeString = timestamp ? timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
  
  return (
    <div className={`message-container flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex max-w-sm lg:max-w-md ${isUser ? 'flex-row-reverse' : 'flex-row'} items-end space-x-2`}>
        {!isUser && (
          <div className="flex-shrink-0 mb-1">
            <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <svg className="w-4 h-4 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
              </svg>
            </div>
          </div>
        )}
        
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`${isUser ? 'message-user' : 'message-assistant'}`}>
            <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
          </div>
          
          {timeString && (
            <div className={`text-xs text-secondary-500 mt-1 px-2 ${isUser ? 'text-right' : 'text-left'}`}>
              {timeString}
            </div>
          )}
        </div>
        
        {isUser && (
          <div className="flex-shrink-0 mb-1">
            <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-xs font-semibold">
              U
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Message;
