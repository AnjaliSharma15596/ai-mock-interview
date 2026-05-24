import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_questions(job_role, difficulty, num_questions):
    prompt = f"""You are a senior technical interviewer at a top company.
Generate exactly {num_questions} interview questions for a {job_role} position at {difficulty} difficulty.

Rules:
- Mix technical and behavioral questions realistically
- Make questions specific to the {job_role} role
- Number each question: 1. Question here
- Only output the numbered questions, nothing else



Generate now:"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    raw = response.choices[0].message.content.strip()
    questions = []
    for line in raw.split("\n"):
        line = line.strip()
        if line and line[0].isdigit() and "." in line:
            q = line.split(".", 1)[1].strip()
            if q:
                questions.append(q)
    return questions


def evaluate_answer(question, answer, job_role):
    prompt = f"""You are an expert interviewer evaluating a candidate for a {job_role} position.

Question: {question}
Candidate's Answer: {answer}

STRICT RULES:
- If answer is blank, gibberish or irrelevant like 'xyz', 'abc', 'test' — give score 0
- If answer is too short or vague — maximum score is 4
- Only give 8-10 for genuinely detailed correct answers
- Be honest, do not be generous

Evaluate the answer and respond in this exact JSON format:
{{
  "score": <integer from 1 to 10>,
  "what_was_good": "<one sentence about what was good>",
  "what_was_missing": "<one sentence about what was missing or could be better>",
  "ideal_answer_hint": "<one sentence hint about what a great answer would include>"
}}

Only respond with the JSON. No extra text."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        return {
            "score": 5,
            "what_was_good": "You attempted the question.",
            "what_was_missing": "Could not parse detailed feedback.",
            "ideal_answer_hint": "Try to be more specific and structured."
        }


def generate_final_report(job_role, difficulty, questions, answers, feedbacks, scores):
    qa_summary = ""
    for i, (q, a, s) in enumerate(zip(questions, answers, scores)):
        qa_summary += f"Q{i+1}: {q}\nAnswer: {a}\nScore: {s}/10\n\n"

    prompt = f"""You are a career coach reviewing a mock interview for a {job_role} position ({difficulty} difficulty).

Here is the full interview summary:
{qa_summary}

Generate a final performance report in this exact JSON format:
{{
  "overall_score": <average score as float>,
  "performance_level": "<one of: Excellent / Good / Average / Needs Improvement>",
  "strongest_answer": "<which question number had the best answer and why, one sentence>",
  "weakest_area": "<what topic or skill needs most improvement, one sentence>",
  "improvement_tips": [
    "<tip 1>",
    "<tip 2>",
    "<tip 3>"
  ],
  "encouragement": "<one motivating sentence for the candidate>"
}}

Only respond with the JSON. No extra text."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        avg = sum(scores) / len(scores) if scores else 0
        return {
            "overall_score": round(avg, 1),
            "performance_level": "Average",
            "strongest_answer": "You showed effort throughout the interview.",
            "weakest_area": "Focus on structuring your answers better.",
            "improvement_tips": [
                "Practice the STAR method for behavioral questions.",
                "Review core technical concepts for your role.",
                "Work on giving concise, structured answers."
            ],
            "encouragement": "Keep practicing — every interview makes you better!"
        }
