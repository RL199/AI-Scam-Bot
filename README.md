# AI Scam Bot Simulator
## A Cybersecurity Research & Training Tool for IT Support Phishing Detection

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-19.1.1-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://docker.com/)

## Overview

This project provides a controlled environment for simulating AI-powered phishing attacks that impersonate IT support personnel. The system uses state-of-the-art language models through Ollama to create realistic social engineering scenarios for cybersecurity education and training. It is **exclusively designed for cybersecurity coursework, research, and educational purposes** to help security professionals and students identify, analyze, and develop defenses against AI-generated phishing attacks that pose as legitimate IT support.

### Technical Stack

**Backend:**
- **FastAPI** - Lightweight, high-performance API framework
- **Ollama** - Local LLM inference server for model hosting
- **MySQL** - Persistent database for conversation storage

**Frontend:**
- **React 19.1.1** - Modern UI framework with TypeScript support
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework

**AI/ML:**
- **LLaMA** - Foundation language model for text generation
- **Ollama API** - Model inference and management
- **Custom prompt engineering** - Specialized for IT support impersonation

**Infrastructure:**
- **Docker & Docker Compose** - Containerized deployment
- **NGINX** (optional) - Reverse proxy and load balancing
- **GPU Support** - NVIDIA GPU acceleration for model inference

## Research Objectives

This tool enables researchers and security professionals to:

- Generate and analyze AI-powered social engineering patterns
- Benchmark detection systems against evolving threats
- Study linguistic markers of AI-generated deceptive content
- Develop more robust prevention and defense mechanisms
- Conduct ethical security training in safe environments

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
- **Conversation Management** - Persistent conversation storage with message history
- **Rate Limiting & Security Controls** - Built-in message limits and ethical safeguards
- **Comprehensive API** - RESTful endpoints for chat, conversation management, and analytics
- **Real-time Model Information** - Health checks and model status monitoring
- **Database Analytics** - Interaction statistics and conversation tracking
- **Docker Containerization** - Easy deployment with full service orchestration
- **GPU Acceleration** - NVIDIA GPU support for faster model inference
- **CORS Security** - Configurable cross-origin resource sharing
- **Research-Focused Logging** - Detailed logs for cybersecurity analysis

## Installation

### Prerequisites

- Docker and Docker Compose
- NVIDIA GPU (optional, for accelerated inference)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/RL199/AI-Scam-Bot.git
cd AI-Scam-Bot

# Create environment file
cp .env.example .env
# Edit .env with your database credentials

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```


### Environment Configuration

Create a `.env` file in the root directory with:

```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=scambot_db
MYSQL_USER=scambot_user
OLLAMA_HOST=http://localhost:11434
```

## API Endpoints

- `GET /health` - Health check and model status
- `POST /chat` - Chat with the AI model
- `POST /conversations` - Create new conversation
- `GET /conversations/{id}/history` - Get conversation history
- `GET /conversations/{id}/message-count` - Get message count
- `GET /users/{id}/conversations` - Get user conversations
- `GET /model/info` - Model information

## Usage

1. Start the services using Docker Compose
2. Access the frontend at `http://localhost:3000`
3. Begin a conversation with the AI IT support simulator
4. Analyze the interaction patterns for research purposes

**Note:** The system implements message limits to demonstrate common phishing tactics where attackers escalate requests for sensitive information after establishing trust.

## Citation

If you use this tool in your research, please cite it as:

```
Roy, L. (2025). AI Scam Bot Simulator: A Tool for Cybersecurity Research.
GitHub Repository: https://github.com/RL199/AI-Scam-Bot
```

© 2025 Roy Levi. Content available under CC BY-NC 4.0 License.
