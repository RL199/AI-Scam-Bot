import React from "react";

interface HeaderProps {
  isConnected: boolean;
}

const Header: React.FC<HeaderProps> = ({ isConnected }) => {
  return (
    <header className="chat-header">
      <div className="max-w-6xl mx-auto px-3 sm:px-6 py-2 sm:py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 sm:space-x-4 min-w-0 flex-1">
            <div className="company-logo flex-shrink-0">
              <svg
                className="w-3 h-3 sm:w-5 sm:h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
            </div>
            <div className="min-w-0 flex-1">
              <h1 className="text-sm sm:text-2xl font-bold text-secondary-900 truncate">
                TechSupport Pro
              </h1>
              <p className="text-secondary-600 text-xs sm:text-sm font-medium hidden sm:block">
                Enterprise IT Support • 24/7 Technical Assistance
              </p>
              <p className="text-secondary-600 text-xs font-medium sm:hidden">
                24/7 IT Support
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-1 sm:space-x-4 flex-shrink-0">
            <div
              className={`status-badge text-xs sm:text-sm ${
                isConnected ? "status-online" : "status-connecting"
              }`}
            >
              <div
                className={`w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full mr-1 sm:mr-2 ${
                  isConnected
                    ? "bg-success-500 animate-pulse-slow"
                    : "bg-warning-500 animate-bounce-slow"
                }`}
              ></div>
              <span className="font-medium text-xs sm:text-sm">
                {isConnected ? "Support Online" : "Connecting..."}
              </span>
            </div>
          </div>
        </div>

        {/* Hide support indicators on mobile to save space, show on desktop */}
        <div className="hidden sm:block mt-6 grid grid-cols-3 gap-4 text-sm">
          <div className="support-indicator">
            <svg
              className="w-4 h-4 text-primary-600 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <span className="truncate">Certified Technicians</span>
          </div>
          <div className="support-indicator">
            <svg
              className="w-4 h-4 text-primary-600 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                clipRule="evenodd"
              />
            </svg>
            <span className="truncate">Avg Response: &lt; 30s</span>
          </div>
          <div className="support-indicator">
            <svg
              className="w-4 h-4 text-primary-600 flex-shrink-0"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
              <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
            </svg>
            <span className="truncate">Remote & On-site</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
