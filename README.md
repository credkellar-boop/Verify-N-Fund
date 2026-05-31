# 🏦 Verify-N-Fund 

![Build Status](https://img.shields.io/github/actions/workflow/status/credkellar-boop/Verify-N-Fund/ci.yml?branch=main&label=CI/CD%20Build)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Gemini%202.5%20Flash-8E75B2?logo=google&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Verify-N-Fund** is an AI-powered automation blueprint designed for currency exchanges, check-cashing services, and financial institutions. By combining automated verification databases, optical character recognition (OCR), and a highly specialized Gemini AI Agent, this tool drastically cuts down the time compliance officers spend manually reviewing checks.

## ✨ Key Features

* **High-Speed Vision Scanner:** Upload check images for instant OCR extraction of routing numbers, account numbers, and amounts using Gemini's multimodal capabilities.
* **Automated Risk Matrix:** Programmatic risk scoring engine categorizes checks into instant routing tiers (Approved, Flagged for Review, Rejected).
* **Guarded AI Knowledge Base:** An in-app assistant explicitly programmed *strictly* to answer questions regarding the verification process and fraud prevention. 
* **Management Analytics:** Role-based access granting executives real-time visualization of business performance, transaction volumes, and audit logs.
* **Enterprise Ready:** Fully containerized with Docker and continuously tested via GitHub Actions CI pipelines.

---

## 📂 Project Structure

```text
Verify-N-Fund/
│
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions automated testing pipeline
│
├── src/
│   ├── __init__.py
│   ├── app.py                 # Main Streamlit dashboard interface
│   ├── gemini_agent.py        # Guardrailed AI & Vision extraction logic
│   ├── verifier.py            # Automated routing and risk calculation engine
│   ├── database.py            # Local CSV ledger management for audits
│   └── analytics.py           # Pandas data transformation for management view
│
├── tests/
│   ├── __init__.py
│   └── test_verifier.py       # Pytest unit tests for the risk engine
│
├── config/                    
│   └── audit_log.csv          # Local tracking ledger (Generated at runtime)
│
├── .env                       # Environment variables (API Keys - DO NOT COMMIT)
├── .dockerignore              # Excludes unnecessary files from container builds
├── .gitignore                 # Excludes cache, logs, and sensitive data from Git
├── docker-compose.yml         # Multi-container orchestration blueprint
├── Dockerfile                 # Production container build instructions
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
