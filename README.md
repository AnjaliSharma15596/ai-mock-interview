# 🎯 InterviewAI — AI Mock Interview System

An AI-powered mock interview platform built with Python, Streamlit, and Google Gemini.

## Features
- 🔐 User Register & Login system
- 💼 10+ Job Roles with 3 difficulty levels
- 🤖 AI-generated role-specific questions
- 💬 Instant AI feedback per answer (what was good, missing, ideal hint)
- 📊 Final performance report with improvement tips
- 📂 Interview history saved per user

## Tech Stack
- **Python** — Core language
- **Streamlit** — UI Framework
- **Google Gemini API** — LLM for questions & feedback
- **SQLite** — Local database for users & history
- **python-dotenv** — Secure API key management

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/ai-mock-interview
cd ai-mock-interview
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
Create a `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get your free key at: https://aistudio.google.com

### 4. Run the app
```bash
streamlit run app.py
```

## Project Structure
```
ai-mock-interview/
├── app.py            # Main application (all pages)
├── database.py       # SQLite database logic
├── ai_helper.py      # Gemini AI integration
├── requirements.txt  # Dependencies
└── .env              # API key (never commit this)
```

## .gitignore
Make sure to add `.env` and `interview_app.db` to your `.gitignore`!
