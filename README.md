# AI Scam Bot Simulator
### A Cybersecurity Research & Training Tool for IT Support Phishing Detection

## Overview

This project provides a controlled environment for simulating AI-powered phishing attacks that impersonate IT support personnel. The system uses state-of-the-art language models through Ollama to create realistic social engineering scenarios for cybersecurity education and training. It is **exclusively designed for cybersecurity coursework, research, and educational purposes** to help security professionals and students identify, analyze, and develop defenses against AI-generated phishing attacks that pose as legitimate IT support.

### Technical Stack

**Backend:**
- **FastAPI 0.115.12** - Modern, high-performance API framework with automatic documentation
- **Ollama 0.5.1** - Local LLM inference server for model hosting and management
- **MySQL 8.0** - Robust relational database for persistent conversation storage
- **aiomysql 0.2.0** - Asynchronous MySQL client for optimal database performance
- **Uvicorn 0.34.2** - ASGI server with standard extensions for production deployment

**Frontend:**
- **React 19.1.1** - Modern UI framework with latest features and TypeScript support
- **Vite 7.0.6** - Lightning-fast build tool and development server
- **Tailwind CSS 3.4.3** - Utility-first CSS framework for professional UI design
- **TypeScript 5.8.4** - Type-safe development with advanced language features
- **Axios 1.11.0** - Promise-based https client for API communication
- **Heroicons** - Beautiful hand-crafted SVG icons for enhanced UX

**AI/ML:**
- **Ollama Compatible Models** - Support for any model from the Ollama library
- **Custom Prompt Engineering** - Specialized prompts for IT support impersonation scenarios
- **Llama 3.2** - Recommended default model for average PCs (configurable via environment)

**Security & Infrastructure:**
- **Docker & Docker Compose** - Containerized deployment with service orchestration
- **Cryptography 45.0.5** - Advanced cryptographic operations for secure data handling
- **CORS Security** - Configurable cross-origin resource sharing policies
- **Health Monitoring** - Comprehensive service health checks and status monitoring

## Research Objectives

This tool enables researchers and security professionals to:

- Generate and analyze AI-powered social engineering patterns and escalation tactics
- Study the progression from helpful IT support to malicious data collection requests
- Benchmark detection systems against evolving threats that use trust-building techniques
- Analyze linguistic markers of AI-generated deceptive content and payment solicitation
- Examine sensitive data extraction patterns through automated credit card information detection
- Develop more robust prevention and defense mechanisms against progressive phishing attacks
- Conduct ethical security training in safe environments with realistic escalation scenarios

## ⚠️ Important Legal & Ethical Notice ⚠️

> **DISCLAIMER:** This software is provided strictly for academic research, authorized penetration testing, and defensive security training. **Under no circumstances should this tool be deployed to deceive, manipulate, or harm individuals, organizations, or systems.**

Key restrictions:
- All generated content includes mandatory disclaimers
- Usage restricted to controlled research environments only
- Not to be deployed in production environments or public-facing applications
- Not for commercial exploitation of vulnerabilities

Unauthorized deployment or misuse may violate multiple laws including computer fraud statutes, privacy regulations, and telecommunications acts.

## Features

- **AI-Powered IT Support Simulation** - Realistic chatbot impersonating IT helpdesk personnel
- **Professional User Interface** - Modern, responsive design with professional IT support appearance
- **Real-time Typing Indicators** - Visual feedback showing when the AI is "typing" responses
- **Conversation Management** - Persistent conversation storage with message history
- **Session Management** - Automatic session creation and tracking with unique identifiers
- **Enhanced User Experience** - Auto-focus input field, responsive design, and smooth interactions
- **Progressive Phishing Simulation** - Message limits trigger escalation to payment requests after fixed number of messages
- **Sensitive Data Extraction** - Automated detection and logging of credit card information, expiry dates, and CVV codes
- **Comprehensive API** - RESTful endpoints for chat, conversation management, analytics, and sensitive data monitoring
- **Real-time Model Information** - Health checks and model status monitoring
- **Database Analytics** - Interaction statistics, conversation tracking, and sensitive data analysis
- **Docker Containerization** - Easy deployment with full service orchestration
- **GPU Acceleration** - NVIDIA GPU support for faster model inference
- **CORS Security** - Configurable cross-origin resource sharing
- **Research-Focused Logging** - Detailed logs for cybersecurity analysis
- **Centralized Configuration** - Single environment file for all service configuration

## Installation

### Prerequisites

**Required:**
- **Docker** (version 20.10+ recommended)
- **Docker Compose** (version 2.0+ recommended)
- **4GB+ RAM** (minimum for basic models like llama3.2:1b)
- **10GB+ free disk space** (for models and data storage)

**Recommended:**
- **8GB+ RAM** (for llama3.2:3b and better performance)
- **16GB+ RAM** (for larger models like llama3.2-vision:11b)
- **NVIDIA GPU** with CUDA support (for accelerated model inference)
- **SSD storage** (faster model loading and better performance)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/RL199/AI-Scam-Bot.git
cd AI-Scam-Bot

# Create and configure environment file
cp .env.example .env
# Edit .env with your secure database credentials (see Environment Configuration below)

# Start all services (database, backend, frontend, AI model)
docker-compose up -d

# Verify services are running
docker-compose ps

# View logs (optional)
docker-compose logs -f

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
# Model API: http://localhost:11434
```


### Environment Configuration

Create a `.env` file in the root directory with the following configuration:

```env
# Database Credentials (REQUIRED - Change these!)
MYSQL_ROOT_PASSWORD=your_secure_root_password_here
MYSQL_PASSWORD=your_secure_user_password_here

# Database Configuration (Optional - defaults provided)
MYSQL_DATABASE=scambot_db
MYSQL_USER=scambot_user

# AI Model Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Model Selection Guide:
# - llama3.2:1b    (Recommended for 4-8GB RAM, fastest)
# - llama3.2:3b    (Recommended for 8GB RAM, balanced)
# See https://ollama.ai/library for full model list
```

**⚠️ Security Note:** Always use strong, unique passwords for database credentials. Never commit the `.env` file to version control.


### Performance Tips

- **CPU-only systems**: Use smaller models (1b-3b) for acceptable performance
- **GPU acceleration**: Install NVIDIA Container Toolkit for faster inference
- **Memory optimization**: Close other applications when running larger models
- **Storage**: Models are cached locally, requiring 2GB+ per model

## API Endpoints

### Core Endpoints

| Method | Endpoint      | Description                   | Parameters                              |
| ------ | ------------- | ----------------------------- | --------------------------------------- |
| `GET`  | `/health`     | Health check and model status | None                                    |
| `POST` | `/chat`       | Chat with the AI model        | `message`, `conversation_id`, `user_id` |
| `GET`  | `/model/info` | Model information and status  | None                                    |

### Conversation Management

| Method | Endpoint                            | Description                        | Parameters        |
| ------ | ----------------------------------- | ---------------------------------- | ----------------- |
| `POST` | `/conversations`                    | Create new conversation            | `user_id`         |
| `GET`  | `/conversations/{id}/history`       | Get conversation history           | `conversation_id` |
| `GET`  | `/conversations/{id}/message-count` | Get message count for conversation | `conversation_id` |
| `GET`  | `/users/{id}/conversations`         | Get all conversations for user     | `user_id`         |

### Admin & Research Endpoints

| Method | Endpoint                                         | Description                                    | Parameters                      |
| ------ | ------------------------------------------------ | ---------------------------------------------- | ------------------------------- |
| `GET`  | `/admin/sensitive-data`                          | Get all captured sensitive data for analysis   | `limit`, `format` (optional)    |
| `GET`  | `/admin/sensitive-data/conversation/{id}`        | Get sensitive data for specific conversation   | `conversation_id`               |

**📚 Interactive Documentation:** Visit `https://localhost:8000/docs` for complete API documentation with interactive testing interface.

## Usage

### Getting Started

1. **Start the services** using Docker Compose
2. **Access the frontend** at `http://localhost:3000`
3. **Begin a conversation** with the AI IT support simulator
4. **Analyze interaction patterns** for research purposes

### Security Controls

The system implements several ethical safeguards and research features:

- **Progressive Escalation Simulation**: After fixed number of messages, the system demonstrates typical phishing escalation by requesting credit card information for "premium support"
- **Automated Data Extraction**: Real-time detection and logging of credit card numbers, expiry dates, and CVV codes using pattern recognition
- **Sensitive Data Isolation**: Captured sensitive information is stored in separate database tables for security research analysis
- **Session Tracking**: Monitors and logs all interactions for accountability and research purposes

**Note:** The progressive escalation feature simulates real-world phishing tactics where attackers build trust through initial helpful interactions before requesting sensitive information. All captured data is used exclusively for cybersecurity research and training purposes.


## Architecture

### System Overview
```

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │    │                 │
│    Frontend     │◄──►│     Backend     │◄──►│   Ollama API    │◄──►│     Models      │
│   (React/TS)    │    │    (FastAPI)    │    │   (LLM Server)  │    │   (LLaMA 3.2)   │
│                 │    │                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │                 │
                       │   MySQL DB      │
                       │  (Persistence)  │
                       │                 │
                       └─────────────────┘
```

### Data Flow

1. **User Input**: User sends message through React frontend
2. **API Processing**: FastAPI backend processes request and validates input
3. **Model Inference**: Backend sends prompt to Ollama for AI response generation
4. **Escalation Logic**: After fixed number of messages, system triggers payment request simulation
5. **Data Extraction**: Automated detection of credit card information in user responses
6. **Database Storage**: Conversation data and sensitive information stored separately in MySQL
7. **Response Delivery**: AI response is sent back through the API to frontend
8. **UI Update**: Frontend displays the response with typing indicators and formatting

### Security Architecture

- **Network Isolation**: Services run in isolated Docker networks
- **Credential Management**: Environment-based secret management
- **Input Validation**: Comprehensive request validation and sanitization
- **Rate Limiting**: Protection against abuse and resource exhaustion
- **Audit Logging**: Detailed logging for security monitoring and research

## Troubleshooting

### Performance Optimization

- Use NVIDIA GPU with CUDA support
- Increase Docker memory allocation (8GB+ recommended)
- Use faster storage (SSD recommended)
- Monitor system resources during operation

### Getting Help

- **Documentation**: Visit `http://localhost:8000/docs` for API documentation
- **Issues**: Report bugs on [GitHub Issues](https://github.com/RL199/AI-Scam-Bot/issues)
- **Discussions**: Join discussions on [GitHub Discussions](https://github.com/RL199/AI-Scam-Bot/discussions)

## License & Legal

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.

**Full License**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

**⚠️ Ethical Use Reminder**: This tool is designed exclusively for cybersecurity research, education, and defensive training. Use responsibly and in accordance with all applicable laws and regulations.

© 2025 Roy Levi. Content available under CC BY-NC 4.0 License.
