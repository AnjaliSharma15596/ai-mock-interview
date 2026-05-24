# 🎯 InterviewAI — AI-Powered Mock Interview System

> Practice smarter. Get hired faster.

A full-stack AI-powered mock interview platform that generates role-specific interview questions, evaluates answers in real-time using LLaMA AI, and provides detailed performance reports with improvement tips.

---

## 🚀 Live Demo
> Coming soon — deploying on Hugging Face Spaces

---

## 📸 Features

- 🔐 **User Authentication** — Register & Login with secure password hashing
- 💼 **10+ Job Roles** — Software Developer, Data Analyst, ML Engineer and more
- 📊 **3 Difficulty Levels** — Easy, Medium, Hard
- 🤖 **AI-Generated Questions** — Role-specific questions powered by LLaMA via Groq API
- 💬 **Real-time AI Feedback** — Per-answer evaluation with score, strengths and improvement hints
- 📈 **Performance Report** — Overall score, strongest answer, weakest area and top 3 improvement tips
- 📂 **Interview History** — All past interviews saved and accessible anytime

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Core language |
| Streamlit | Frontend UI |
| Groq API + LLaMA 3.1 | LLM for question generation & feedback |
| SQLite | Database for users & interview history |
| python-dotenv | Secure API key management |

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/AnjaliSharma15596/ai-mock-interview.git
cd ai-mock-interview
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your free Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up for free
- Create an API key

### 4. Create `.env` file
```
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
ai-mock-interview/
├── app.py            # Main application — all 8 pages
├── ai_helper.py      # Groq LLaMA AI integration
├── database.py       # SQLite database logic
├── requirements.txt  # Dependencies
└── README.md         # Project documentation
```

---

## 💡 How It Works

```
Register / Login
      ↓
Select Job Role + Difficulty
      ↓
AI Generates Interview Questions (LLaMA via Groq)
      ↓
User Types Answers
      ↓
AI Evaluates Each Answer (Score + Feedback)
      ↓
Final Performance Report Generated
      ↓
Interview Saved to History
```

---

## 🎯 Use Cases

- **Freshers** preparing for campus placements
- **Job seekers** practicing before interviews
- **Students** improving communication and technical skills

---

## 👩‍💻 Author

**Anjali Sharma**
- GitHub: [@AnjaliSharma15596](https://github.com/AnjaliSharma15596)

---



