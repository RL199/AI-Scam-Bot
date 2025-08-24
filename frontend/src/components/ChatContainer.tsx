import React, { useState, useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import { ChatMessage } from "../types/api";
import { apiService } from "../services/api";
import Header from "./Header";
import Message from "./Message";
import ChatInput from "./ChatInput";
import TypingIndicator from "./TypingIndicator";

const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [userId] = useState<string>(() => uuidv4());
  const [isConnected, setIsConnected] = useState(false);
  const [messageCount, setMessageCount] = useState(0);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const typingTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Check API health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await apiService.healthCheck();
        setIsConnected(true);
      } catch (error) {
        console.error("Health check failed:", error);
        setIsConnected(false);
      }
    };

    checkHealth();
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Add welcome message when connected
  useEffect(() => {
    if (isConnected && messages.length === 0) {
      const welcomeMessage: ChatMessage = {
        role: "assistant",
        content: `Welcome to TechSupport Pro! 👋

I'm your dedicated IT Support specialist, ready to help you resolve any technical challenges you're facing.

**What I can assist you with:**
• Computer performance issues and troubleshooting
• Software installation and configuration problems
• Network connectivity and Wi-Fi issues
• Email setup and synchronization
• Security concerns and virus removal
• Hardware diagnostics and recommendations
• Printer and peripheral device setup
• Password resets and account recovery

**Quick Tips:**
- Be as specific as possible when describing your issue
- Include error messages or codes if you see any
- Let me know what device and operating system you're using

How can I help you today? Please describe your technical issue in detail.`,
      };
      setMessages([welcomeMessage]);
    }
  }, [isConnected, messages.length]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (typingTimeoutRef.current) {
        clearTimeout(typingTimeoutRef.current);
      }
    };
  }, []);

  const handleSendMessage = async (messageContent: string) => {
    if (!isConnected) {
      alert(
        "Connection to IT support is currently unavailable. Please try again later."
      );
      return;
    }

    // Disable input immediately when message is sent
    setIsProcessing(true);

    const userMessage: ChatMessage = {
      role: "user",
      content: messageContent,
    };

    // Add user message to chat
    setMessages((prev) => [...prev, userMessage]);
    setMessageCount((prev) => prev + 1);

    // Clear any existing typing timeout
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }

    // Start the API call immediately but don't show results until minimum delay
    const startTime = Date.now();
    const minimumDelay = 10000; // 10 seconds minimum for human-like timing

    // Show typing indicator after a short delay
    typingTimeoutRef.current = setTimeout(() => {
      setIsTyping(true);
    }, 2000); // Show typing after 2 seconds

    let response: any;
    let error: any;

    try {
      // Create conversation if it doesn't exist
      if (!conversationId) {
        const conversationResponse = await apiService.createConversation({
          user_id: userId,
          title: "IT Support Session - " + new Date().toLocaleDateString(),
        });
        setConversationId(conversationResponse.conversation_id);
      }

      // Send chat request
      response = await apiService.chat({
        messages: [userMessage],
        conversation_id: conversationId || undefined,
        user_id: userId,
      });
    } catch (err) {
      console.error("Error sending message:", err);
      error = err;
    }

    // Calculate how much time has passed and wait for minimum delay
    const elapsed = Date.now() - startTime;
    const remainingDelay = Math.max(0, minimumDelay - elapsed);
    await new Promise((resolve) => setTimeout(resolve, remainingDelay));

    // Handle response or error after the minimum delay
    if (error) {
      const errorMessage: ChatMessage = {
        role: "assistant",
        content: `I apologize, but I'm experiencing technical difficulties at the moment. This could be due to:

• High server load
• Network connectivity issues
• Temporary service maintenance

**What you can do:**
1. Please try sending your message again in a few moments
2. Check your internet connection
3. If the issue persists, you can contact our emergency support line at: **1-800-TECH-911**

Our human support team is standing by to assist you. Thank you for your patience! 🔧`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } else {
      // Add assistant response
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.response,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Update conversation ID if it was created during this request
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }
    }

    // Clear timeout and hide typing indicator
    if (typingTimeoutRef.current) {
      clearTimeout(typingTimeoutRef.current);
    }
    setIsTyping(false);
    setIsProcessing(false);
  };

  return (
    <div className="chat-container">
      <Header isConnected={isConnected} />

      {/* Connection Status Banner */}
      {!isConnected && (
        <div className="bg-warning-50 border-l-4 border-warning-500 text-warning-800 p-3 sm:p-4">
          <div className="flex items-center">
            <svg
              className="w-4 h-4 sm:w-5 sm:h-5 mr-2 sm:mr-3 animate-spin flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
                clipRule="evenodd"
              />
            </svg>
            <div className="min-w-0 flex-1">
              <p className="font-medium text-sm sm:text-base">
                Establishing secure connection to IT support...
              </p>
              <p className="text-xs sm:text-sm mt-1">
                Please wait while we connect you to our support team.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Chat Messages */}
      <div className="chat-messages scrollbar-thin">
        <div className="max-w-4xl mx-auto">
          {messages.map((message, index) => (
            <Message
              key={index}
              message={message}
              timestamp={
                new Date(Date.now() - (messages.length - index - 1) * 60000)
              }
            />
          ))}
          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Session Info - More compact on mobile */}
      <div className="bg-secondary-50 border-t border-secondary-200 px-2 sm:px-6 py-1 sm:py-2">
        <div className="max-w-4xl mx-auto flex items-center justify-between text-xs text-secondary-600">
          <div className="flex items-center space-x-2 sm:space-x-4 min-w-0 flex-1">
            <span className="truncate">
              ID: {conversationId?.slice(-8) || "Send message first"}
            </span>
            <span className="hidden sm:inline">Messages: {messageCount}</span>
            <span className="sm:hidden">Msgs: {messageCount}</span>
            <span className="sm:hidden truncate">AI Tech</span>
          </div>
          <div className="flex items-center space-x-1 sm:space-x-4 flex-shrink-0">
            <span className="hidden sm:inline">Response Time: Excellent</span>
            <span className="sm:hidden">Fast</span>
            <span className="flex items-center space-x-1">
              <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 bg-success-500 rounded-full"></div>
              <span className="hidden sm:inline">Secure Connection</span>
              <span className="sm:hidden">Secure</span>
            </span>
          </div>
        </div>
      </div>

      {/* Chat Input */}
      <ChatInput
        onSendMessage={handleSendMessage}
        disabled={!isConnected || isTyping || isProcessing}
        placeholder={
          !isConnected
            ? "Establishing connection to IT support..."
            : isTyping || isProcessing
            ? "Please wait for technician response..."
            : "Describe your issue in detail..."
        }
      />
    </div>
  );
};

export default ChatContainer;
