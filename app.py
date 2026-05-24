import streamlit as st
from dotenv import load_dotenv
import os
from database import init_db, register_user, login_user, save_interview, get_user_interviews, get_interview_details
from ai_helper import generate_questions, evaluate_answer, generate_final_report

load_dotenv()
init_db()

st.set_page_config(
    page_title="InterviewAI",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── GLOBAL STYLES ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #0d0d0d;
    --surface: #161616;
    --surface2: #1f1f1f;
    --border: #2a2a2a;
    --accent: #c8f04a;
    --accent2: #4af0c8;
    --text: #f0f0f0;
    --muted: #888;
    --danger: #ff5c5c;
    --gold: #f5c842;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.block-container { padding: 2rem 1.5rem !important; max-width: 720px !important; }

h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(200,240,74,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #d9ff55 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(200,240,74,0.3) !important;
}
.stButton > button:disabled {
    background: var(--border) !important;
    color: var(--muted) !important;
    transform: none !important;
}

/* Secondary button style */
.sec-btn > button {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}
.sec-btn > button:hover {
    background: var(--border) !important;
    transform: translateY(-1px) !important;
    box-shadow: none !important;
}

/* Slider */
.stSlider { color: var(--accent) !important; }

/* Progress */
.stProgress > div > div { background: var(--accent) !important; border-radius: 99px !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Custom components */
.logo { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 900; color: var(--accent); letter-spacing: -1px; margin-bottom: 0; }
.logo span { color: var(--text); }

.hero-title { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; line-height: 1.1; color: var(--text); margin: 1.5rem 0 0.5rem; }
.hero-title .highlight { color: var(--accent); }

.hero-sub { font-size: 1.05rem; color: var(--muted); margin-bottom: 2.5rem; font-weight: 300; line-height: 1.6; }

.card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 2rem; margin: 1rem 0; }

.badge { display: inline-block; background: rgba(200,240,74,0.1); color: var(--accent); border: 1px solid rgba(200,240,74,0.3); border-radius: 99px; padding: 3px 12px; font-size: 0.8rem; font-weight: 500; margin-right: 6px; }

.badge-blue { background: rgba(74,240,200,0.1); color: var(--accent2); border-color: rgba(74,240,200,0.3); }

.question-card { background: var(--surface); border-left: 4px solid var(--accent); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; font-size: 1.05rem; line-height: 1.7; color: var(--text); }

.score-circle { display: inline-block; width: 56px; height: 56px; border-radius: 50%; background: rgba(200,240,74,0.1); border: 2px solid var(--accent); color: var(--accent); font-size: 1.2rem; font-weight: 700; text-align: center; line-height: 52px; }

.feedback-good { background: rgba(74,240,200,0.08); border: 1px solid rgba(74,240,200,0.2); border-radius: 10px; padding: 0.8rem 1rem; margin: 0.5rem 0; font-size: 0.9rem; color: #e0e0e0 !important; }
.feedback-miss { background: rgba(255,92,92,0.08); border: 1px solid rgba(255,92,92,0.2); border-radius: 10px; padding: 0.8rem 1rem; margin: 0.5rem 0; font-size: 0.9rem; color: #e0e0e0 !important; }
.feedback-hint { background: rgba(245,200,66,0.08); border: 1px solid rgba(245,200,66,0.2); border-radius: 10px; padding: 0.8rem 1rem; margin: 0.5rem 0; font-size: 0.9rem; color: #e0e0e0 !important; }

.stat-box { background: var(--surface2); border: 1px solid var(--border); border-radius: 12px; padding: 1.2rem; text-align: center; }
.stat-box .num { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700; color: var(--accent); }
.stat-box .label { font-size: 0.8rem; color: var(--muted); margin-top: 2px; }

.history-item { background: var(--surface2); border: 1px solid var(--border); border-radius: 12px; padding: 1rem 1.2rem; margin: 0.6rem 0; display: flex; justify-content: space-between; align-items: center; color: #f0f0f0 !important; }
.history-item strong { color: #f0f0f0 !important; }

.divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

.tip-item { background: var(--surface2); border-radius: 10px; padding: 0.8rem 1rem; margin: 0.4rem 0; font-size: 0.9rem; display: flex; gap: 0.6rem; align-items: flex-start; color: #f0f0f0 !important; }

.card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 2rem; margin: 1rem 0; color: #f0f0f0 !important; }

.perf-excellent { color: var(--accent); }
.perf-good { color: var(--accent2); }
.perf-average { color: var(--gold); }
.perf-needs { color: var(--danger); }
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE INIT ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "landing",
        "user": None,
        "questions": [],
        "answers": [],
        "feedbacks": [],
        "scores": [],
        "current_q": 0,
        "job_role": "",
        "difficulty": "",
        "num_questions": 5,
        "final_report": None,
        "interview_id": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


def go(page):
    st.session_state.page = page
    st.rerun()


def logo():
    st.markdown('<div class="logo">Interview<span>AI</span></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "landing":

    st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d !important; }
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0 2rem 0;
        border-bottom: 1px solid var(--border);
        margin-bottom: 3rem;
    }
    .nav-logo {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        font-weight: 900;
        color: var(--accent);
        letter-spacing: -0.5px;
    }
    .nav-logo span { color: var(--text); }
    .nav-tag {
        background: rgba(200,240,74,0.1);
        color: var(--accent);
        border: 1px solid rgba(200,240,74,0.25);
        border-radius: 99px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    .hero-eyebrow {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 2px;
        color: var(--accent);
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .hero-heading {
        font-family: 'Playfair Display', serif;
        font-size: 3.2rem;
        font-weight: 900;
        line-height: 1.1;
        color: var(--text);
        margin-bottom: 1.2rem;
    }
    .hero-heading .hl { color: var(--accent); }
    .hero-desc {
        font-size: 1rem;
        color: var(--muted);
        line-height: 1.8;
        margin-bottom: 2.5rem;
        max-width: 520px;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 2.5rem 0;
    }
    .feature-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.4rem;
        transition: border-color 0.2s;
    }
    .feature-card:hover { border-color: rgba(200,240,74,0.4); }
    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.6rem;
    }
    .feature-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: var(--text);
        margin-bottom: 0.3rem;
    }
    .feature-desc {
        font-size: 0.82rem;
        color: var(--muted);
        line-height: 1.5;
    }
    .metrics-row {
        display: flex;
        gap: 2rem;
        margin: 2rem 0;
        padding: 1.5rem;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
    }
    .metric-item { text-align: center; flex: 1; }
    .metric-num {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 900;
        color: var(--accent);
    }
    .metric-label {
        font-size: 0.78rem;
        color: var(--muted);
        margin-top: 2px;
        letter-spacing: 0.3px;
    }
    .metric-divider {
        width: 1px;
        background: var(--border);
        align-self: stretch;
    }
    .testimonial {
        background: var(--surface);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 2rem 0;
        font-size: 0.9rem;
        color: var(--muted);
        font-style: italic;
        line-height: 1.7;
    }
    .testimonial strong { color: var(--text); font-style: normal; }
    .footer-line {
        text-align: center;
        font-size: 0.78rem;
        color: var(--muted);
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border);
    }
    </style>

    <div class="nav-bar">
        <div class="nav-logo">Interview<span>AI</span></div>
        <div class="nav-tag">✦ AI POWERED</div>
    </div>

    <div class="hero-eyebrow">Your Personal Interview Coach</div>
    <div class="hero-heading">
        Land your dream job<br>with <span class="hl">AI-powered</span><br>mock interviews.
    </div>
    <div class="hero-desc">
        Practice with real interview questions tailored to your role.
        Get instant AI feedback on every answer. Track your growth.
        Walk into every interview with confidence.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Get Started — Free", use_container_width=True):
            go("register")
    with col2:
        st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
        if st.button("🔐 Login to Account", use_container_width=True):
            go("login")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="metrics-row">
        <div class="metric-item">
            <div class="metric-num">10+</div>
            <div class="metric-label">JOB ROLES</div>
        </div>
        <div class="metric-divider"></div>
        <div class="metric-item">
            <div class="metric-num">3</div>
            <div class="metric-label">DIFFICULTY LEVELS</div>
        </div>
        <div class="metric-divider"></div>
        <div class="metric-item">
            <div class="metric-num">AI</div>
            <div class="metric-label">POWERED FEEDBACK</div>
        </div>
        <div class="metric-divider"></div>
        <div class="metric-item">
            <div class="metric-num">∞</div>
            <div class="metric-label">PRACTICE SESSIONS</div>
        </div>
    </div>

    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Role-Specific Questions</div>
            <div class="feature-desc">AI generates tailored questions for your exact job role and experience level.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Instant AI Feedback</div>
            <div class="feature-desc">Get detailed feedback on every answer — what was good and what to improve.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Performance Report</div>
            <div class="feature-desc">Full report with scores, strengths, weaknesses and improvement tips.</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📂</div>
            <div class="feature-title">Interview History</div>
            <div class="feature-desc">Track your progress over time with saved interview history and scores.</div>
        </div>
    </div>

    <div class="testimonial">
        💡 <strong>Why this works:</strong> Research shows that deliberate practice with feedback is the fastest way to improve interview performance. InterviewAI gives you unlimited practice with the quality of a real interviewer.
    </div>

    <div class="footer-line">
        Built with AI · Free to use · No credit card required
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REGISTER
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "register":
    logo()
    st.markdown("### Create your account")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    name = st.text_input("👤 Full Name", placeholder="Rahul Sharma")
    email = st.text_input("📧 Email Address", placeholder="rahul@email.com")
    password = st.text_input("🔒 Password", type="password", placeholder="Min. 6 characters")
    confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Repeat your password")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✅ Create Account", use_container_width=True):
        if not name or not email or not password:
            st.error("Please fill in all fields.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            success, msg = register_user(name, email, password)
            if success:
                st.success("Account created! Please login.")
                import time; time.sleep(1)
                go("login")
            else:
                st.error(msg)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
    if st.button("← Already have an account? Login", use_container_width=True):
        go("login")
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "login":
    logo()
    st.markdown("### Welcome back 👋")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    email = st.text_input("📧 Email Address", placeholder="rahul@email.com")
    password = st.text_input("🔒 Password", type="password", placeholder="Your password")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔐 Login", use_container_width=True):
        if not email or not password:
            st.error("Please fill in all fields.")
        else:
            success, result = login_user(email, password)
            if success:
                st.session_state.user = result
                go("dashboard")
            else:
                st.error(result)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
    if st.button("← New here? Create an account", use_container_width=True):
        go("register")
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    if not st.session_state.user:
        go("login")

    user = st.session_state.user
    logo()
    st.markdown(f"### Hey, {user['name'].split()[0]} 👋")
    st.markdown("Ready to practice today?")

    interviews = get_user_interviews(user["id"])

    # Stats row
    total = len(interviews)
    avg_score = round(sum(i["overall_score"] for i in interviews if i["overall_score"]) / total, 1) if total else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-box"><div class="num">{total}</div><div class="label">Interviews Done</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-box"><div class="num">{avg_score}</div><div class="label">Avg Score /10</div></div>', unsafe_allow_html=True)
    with c3:
        last_role = interviews[0]["job_role"] if interviews else "—"
        st.markdown(f'<div class="stat-box"><div class="num" style="font-size:1rem;line-height:2.5">{last_role[:10]}</div><div class="label">Last Role</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if st.button("🚀 Start New Interview", use_container_width=True):
        go("setup")

    if interviews:
        st.markdown("#### 📁 Recent Interviews")
        for iv in interviews[:5]:
            score = iv["overall_score"] or 0
            st.markdown(f"""
            <div class="history-item">
                <div>
                    <strong>{iv['job_role']}</strong>
                    <span class="badge">{iv['difficulty']}</span><br>
                    <span style="font-size:0.8rem;color:var(--muted)">{iv['completed_at'][:10]}</span>
                </div>
                <div style="text-align:right">
                    <div class="score-circle">{score}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
        if st.button("📂 View Full History", use_container_width=True):
            go("history")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        go("landing")
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: INTERVIEW SETUP
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "setup":
    logo()
    st.markdown("### Set up your interview")
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        job_role = st.selectbox("💼 Job Role", [
            "Software Developer", "Data Analyst", "Data Scientist",
            "Frontend Developer", "Backend Developer", "Machine Learning Engineer",
            "Product Manager", "HR / People Operations", "Marketing Analyst", "Business Analyst"
        ])
    with col2:
        difficulty = st.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard"])

    num_questions = st.slider("🔢 Number of Questions", 3, 10, 5)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Interview", use_container_width=True):
        with st.spinner("🤖 AI is generating your questions..."):
            questions = generate_questions(job_role, difficulty, num_questions)
        if questions:
            st.session_state.questions = questions
            st.session_state.answers = []
            st.session_state.feedbacks = []
            st.session_state.scores = []
            st.session_state.current_q = 0
            st.session_state.job_role = job_role
            st.session_state.difficulty = difficulty
            st.session_state.num_questions = num_questions
            go("interview")
        else:
            st.error("Could not generate questions. Check your API key.")

    st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
    if st.button("← Back to Dashboard", use_container_width=True):
        go("dashboard")
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: INTERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "interview":
    questions = st.session_state.questions
    current = st.session_state.current_q
    total = len(questions)

    logo()
    st.markdown(f'<span class="badge">💼 {st.session_state.job_role}</span>'
                f'<span class="badge badge-blue">📊 {st.session_state.difficulty}</span>',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress((current) / total)
    st.markdown(f'<p style="color:var(--muted);font-size:0.85rem">Question {current+1} of {total}</p>',
                unsafe_allow_html=True)

    st.markdown(f'<div class="question-card">❓ {questions[current]}</div>', unsafe_allow_html=True)

    # Pre-fill if user came back to this question
    prev_answer = ""
    if len(st.session_state.answers) > current:
        prev_answer = st.session_state.answers[current]

    answer = st.text_area("✍️ Your Answer",
        value=prev_answer,
        placeholder="Type your answer clearly and confidently...",
        height=200, key=f"ans_{current}")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
        if st.button("⬅️ Previous", use_container_width=True, disabled=(current == 0)):
            if len(st.session_state.answers) > current:
                st.session_state.answers[current] = answer
            else:
                st.session_state.answers.append(answer)
            st.session_state.current_q -= 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        label = "Next ➡️" if current < total - 1 else "Submit ✅"
        if st.button(label, use_container_width=True):
            if not answer.strip():
                st.warning("⚠️ Please write an answer before continuing.")
            else:
                if len(st.session_state.answers) > current:
                    st.session_state.answers[current] = answer
                else:
                    st.session_state.answers.append(answer)

                if current < total - 1:
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    go("feedback")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FEEDBACK (evaluates all answers)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "feedback":
    logo()
    st.markdown("### 💬 AI Feedback on Your Answers")

    questions = st.session_state.questions
    answers = st.session_state.answers

    if not st.session_state.feedbacks:
        with st.spinner("🤖 AI is evaluating your answers... please wait"):
            feedbacks = []
            scores = []
            for q, a in zip(questions, answers):
                result = evaluate_answer(q, a, st.session_state.job_role)
                feedbacks.append(result)
                scores.append(result.get("score", 5))
            st.session_state.feedbacks = feedbacks
            st.session_state.scores = scores

    feedbacks = st.session_state.feedbacks
    scores = st.session_state.scores

    for i, (q, a, f) in enumerate(zip(questions, answers, feedbacks)):
        score = f.get("score", 5)
        with st.expander(f"Q{i+1}: {q[:65]}...  —  Score: {score}/10"):
            st.markdown(f'<div class="question-card" style="font-size:0.95rem">❓ {q}</div>', unsafe_allow_html=True)
            st.markdown(f"**Your Answer:** {a}")
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            st.markdown(f'<div class="feedback-good">✅ <strong>What was good:</strong> {f.get("what_was_good", "")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="feedback-miss">❌ <strong>What was missing:</strong> {f.get("what_was_missing", "")}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="feedback-hint">💡 <strong>Ideal answer hint:</strong> {f.get("ideal_answer_hint", "")}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 View Final Report", use_container_width=True):
        go("report")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FINAL REPORT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "report":
    logo()
    st.markdown("### 📊 Your Performance Report")

    if not st.session_state.final_report:
        with st.spinner("🤖 Generating your final report..."):
            report = generate_final_report(
                st.session_state.job_role,
                st.session_state.difficulty,
                st.session_state.questions,
                st.session_state.answers,
                st.session_state.feedbacks,
                st.session_state.scores
            )
            st.session_state.final_report = report

            # Save to database
            if st.session_state.user:
                feedbacks_text = [
                    f"Good: {f.get('what_was_good','')} | Missing: {f.get('what_was_missing','')}"
                    for f in st.session_state.feedbacks
                ]
                save_interview(
                    st.session_state.user["id"],
                    st.session_state.job_role,
                    st.session_state.difficulty,
                    report.get("overall_score", 0),
                    st.session_state.questions,
                    st.session_state.answers,
                    feedbacks_text,
                    st.session_state.scores
                )

    report = st.session_state.final_report
    perf = report.get("performance_level", "Average")
    perf_class = {"Excellent": "perf-excellent", "Good": "perf-good",
                  "Average": "perf-average", "Needs Improvement": "perf-needs"}.get(perf, "perf-average")

    # Overall score
    st.markdown(f"""
    <div class="card" style="text-align:center">
        <div style="font-size:3.5rem;font-family:'Playfair Display',serif;font-weight:900;color:var(--accent)">
            {report.get('overall_score', 0)}<span style="font-size:1.5rem;color:var(--muted)">/10</span>
        </div>
        <div class="{perf_class}" style="font-size:1.1rem;font-weight:600;margin-top:0.3rem">{perf}</div>
        <div style="color:var(--muted);font-size:0.9rem;margin-top:0.3rem">
            {st.session_state.job_role} · {st.session_state.difficulty}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.8rem;color:var(--muted);margin-bottom:0.4rem">🏆 STRONGEST ANSWER</div>
            <div style="font-size:0.9rem">{report.get('strongest_answer', '')}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.8rem;color:var(--muted);margin-bottom:0.4rem">⚠️ WEAKEST AREA</div>
            <div style="font-size:0.9rem">{report.get('weakest_area', '')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 🎯 Top Improvement Tips")
    for i, tip in enumerate(report.get("improvement_tips", []), 1):
        st.markdown(f'<div class="tip-item"><span style="color:var(--accent);font-weight:700">{i}.</span> {tip}</div>',
                    unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="border-color:rgba(200,240,74,0.3);margin-top:1rem">
        <span style="font-size:1.2rem">💬</span> <em>{report.get('encouragement', '')}</em>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 New Interview", use_container_width=True):
            st.session_state.questions = []
            st.session_state.answers = []
            st.session_state.feedbacks = []
            st.session_state.scores = []
            st.session_state.final_report = None
            st.session_state.current_q = 0
            go("setup")
    with col2:
        st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.final_report = None
            go("dashboard")
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HISTORY
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "history":
    if not st.session_state.user:
        go("login")

    logo()
    st.markdown("### 📂 Interview History")

    interviews = get_user_interviews(st.session_state.user["id"])

    if not interviews:
        st.info("You haven't completed any interviews yet. Start one from the dashboard!")
    else:
        for iv in interviews:
            score = iv["overall_score"] or 0
            with st.expander(f"💼 {iv['job_role']} — {iv['difficulty']} — Score: {score}/10 — {iv['completed_at'][:10]}"):
                details = get_interview_details(iv["id"])
                for i, d in enumerate(details):
                    st.markdown(f"**Q{i+1}:** {d['question']}")
                    st.markdown(f"*Your Answer:* {d['answer']}")
                    if d["feedback"]:
                        st.markdown(f'<div class="feedback-good" style="font-size:0.85rem">💬 {d["feedback"]}</div>',
                                    unsafe_allow_html=True)
                    st.markdown(f"Score: **{d['score']}/10**")
                    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="sec-btn">', unsafe_allow_html=True)
    if st.button("← Back to Dashboard", use_container_width=True):
        go("dashboard")
    st.markdown('</div>', unsafe_allow_html=True)