---
title: Celestial Red Teamer
emoji: 🛡️
colorFrom: indigo
colorTo: indigo
sdk: docker
pinned: false
app_port: 8000
tags:
  - openenv
---

# 🛡️ Celestial Red Teamer
**Autonomous AI Security Agent Evaluation Framework**

Built for the **Meta PyTorch Hackathon 2026**, Celestial Red Teamer is a high-fidelity, safe, and reproducible environment designed to evaluate the offensive reasoning and cyber-security capabilities of Large Language Models (LLMs).

---

## 👥 Team CELESTIAL
* **S B Rohit Bapu** – Lead Architect & Environment Design
* **Vikrant** – Security Research & Challenge Development
* **Ayyappan** – Infrastructure & DevOps Integration

---

## 📖 Project Overview

### **The Problem**
Traditional AI benchmarks rely on static code snippets or multiple-choice questions that fail to capture the multi-step reasoning required for real-world penetration testing. Furthermore, testing autonomous agents on live infrastructure poses significant safety risks.

### **The Solution**
Celestial Red Teamer provides a **Dynamic Sandbox** where agents interact with real Linux services (Apache, FTP, PHP) inside isolated Docker containers. By using the **OpenEnv** framework, we provide a standardized "Action-Observation" loop that measures agent success via objective rewards.

---

## 🛠️ Technical Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestration** | **OpenEnv (Meta)** | Standardized RL environment API for agent evaluation. |
| **Intelligence** | **Llama 3 / OpenAI SDK** | Cognitive engine for command generation and reasoning. |
| **Sandbox** | **Docker** | High-fidelity isolation for secure "Live-Fire" testing. |
| **Safety** | **Guardrails.py** | Real-time command filtering and observation truncation. |
| **Runtime** | **Astral `uv`** | High-performance Python dependency management. |

### **💻 Development & Performance Note**
This environment was developed and stress-tested on a **Core Ultra 7** workstation equipped with **32GB DDR5 RAM** and an **RTX 5060 Ti (16GB VRAM)**. This local "Frontier-grade" setup allowed for rapid iteration of Llama 3 agents using **Ollama**, ensuring the sandbox remains stable under heavy inference loads.

---

## 🚀 System Architecture

1.  **Environment Service**: A FastAPI server exposing `/reset`, `/step`, and `/state` endpoints.
2.  **Action-Observation Loop**:
    * **Action**: The AI sends a structured bash command (e.g., `nmap` or `curl`).
    * **Observation**: The sandbox executes the command and returns the raw terminal output.
3.  **Security Guardrails**: All commands are sanitized via `parser.py` and checked against a safety blacklist in `guardrails.py` before execution.

---

## 🤖 Submission & Evaluation

This project is optimized for the Meta grading bot with the following constraints:
* **Memory**: Limited to 8GB RAM per session.
* **Runtime**: Inference script completes in under 20 minutes.
* **Logging**: Emits mandatory structured logs (`[START]`, `[STEP]`, `[END]`) for automated scoring.

### **Running Inference**
To test the environment as the grader would:
```bash
export API_BASE_URL="[https://huggingface.co/spaces/your-username/celestial-red-teamer](https://huggingface.co/spaces/your-username/celestial-red-teamer)"
export MODEL_NAME="llama3"
export HF_TOKEN="your_token"

python inference.py
