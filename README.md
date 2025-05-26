# AI Scam Bot Simulator
## A Cybersecurity Research & Training Tool

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview

This project provides a controlled environment for simulating scam-like chatbot behavior using state-of-the-art LLaMA-based language models. It is **exclusively designed for cybersecurity research, training, and educational purposes** to help security professionals identify, analyze, and develop defenses against AI-generated social engineering attacks.

### Technical Stack

- `transformers` (Hugging Face) - For model interaction and inference
- `torch` (PyTorch) - For tensor operations and model execution
- `FastAPI` - For lightweight API endpoints
- LLaMA or similar foundation models - For text generation

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

- Configurable simulation of various social engineering tactics
- Customizable response templates and interaction flows
- Comprehensive logging for research analysis
- FastAPI server for integration with testing frameworks
- Support for multiple open-source LLMs (LLaMA 2, GPT-J, etc.)
- Sandboxed execution environment

## Installation

```bash
# Clone the repository
git clone https://github.com/username/AI-Scam-Bot.git
cd AI-Scam-Bot

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Citation

If you use this tool in your research, please cite it as:

```
Roy, L. (2025). AI Scam Bot Simulator: A Tool for Cybersecurity Research.
GitHub Repository: https://github.com/RL199/AI-Scam-Bot
```

© 2025 Roy Levi. Content available under CC BY-NC 4.0 License.
