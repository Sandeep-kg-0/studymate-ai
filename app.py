
import json
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color: #F5F7FC; }
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 { color: #172554; }
.hero {
    background: linear-gradient(120deg, #102A56, #2563EB);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 24px;
}
.hero h1 { color: white; font-size: 2.3rem; }
.hero p { color: #E0EAFF; font-size: 1.05rem; }
div.stButton > button {
    background: #2563EB;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📚 StudyMate AI</h1>
    <p>Your personal learning companion — study smarter,
    stay organized, and keep learning.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("What would you like to study today?")
st.caption("Choose a tool below to get started.")


# ---------- GROQ AI FUNCTION ----------
def get_ai_response(system_prompt, user_prompt, max_tokens=1200):
    try:
        api_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        api_key = ""

    if not api_key:
        st.error("GROQ_API_KEY is missing from Streamlit Secrets.")
        return None

    try:
        client = Groq(api_key=api_key)
        with st.spinner("StudyMate AI is thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.4
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Groq error: {type(e).__name__}: {e}")
        return None


# ---------- TOOL SELECTOR ----------
task = st.selectbox(
    "Choose a study tool",
    ["Ask a Question", "Summarize Notes", "Generate Quiz"]
)
st.divider()


# ---------- 1. ASK A QUESTION ----------
if task == "Ask a Question":
    st.subheader("💬 Ask StudyMate AI")
    st.write("Get clear, student-friendly explanations.")

    with st.form("question_form"):
        question = st.text_area(
            "Enter your question",
            placeholder="Example: Explain Python in simple words.",
            height=130
        )
        submitted = st.form_submit_button(
            "✨ Get Answer", use_container_width=True
        )

    if submitted:
        if question.strip():
            answer = get_ai_response(
                "You are StudyMate AI, a helpful study assistant. "
                "Explain concepts clearly for college students using "
                "simple language, headings and examples where useful.",
                question.strip(),
                1200
            )
            if answer:
                st.markdown("### 📖 Answer")
                st.markdown(answer)
        else:
            st.warning("Please enter a question.")


# ---------- 2. SUMMARIZE NOTES ----------
elif task == "Summarize Notes":
    st.subheader("📚 Summarize Your Notes")
    st.write("Turn lengthy study material into revision-friendly notes.")

    with st.form("summary_form"):
        notes = st.text_area(
            "Paste your study notes",
            placeholder="Paste your textbook notes or class notes here...",
            height=250
        )
        summary_style = st.selectbox(
            "Summary style",
            ["Short summary", "Detailed summary",
             "Exam revision notes", "Key points only"]
        )
        submitted = st.form_submit_button(
            "✨ Summarize Notes", use_container_width=True
        )

    if submitted:
        if notes.strip():
            summary = get_ai_response(
                "You are an academic note summarizer. Use the supplied "
                "notes as the source for source-specific facts. Do not "
                "invent details. Format the result in readable Markdown.",
                f"Create a {summary_style.lower()} from these notes. "
                "Preserve important terminology, definitions, formulas "
                "and examples.\n\nSTUDY NOTES:\n" + notes,
                1800
            )
            if summary:
                st.markdown("### 📝 Your Summary")
                st.markdown(summary)
                st.download_button(
                    "⬇️ Download Summary",
                    data=summary,
                    file_name="studymate_summary.md",
                    mime="text/markdown"
                )
        else:
            st.warning("Please paste your study notes.")


# ---------- 3. GENERATE INTERACTIVE QUIZ ----------
else:
    st.subheader("🧠 Interactive Practice Quiz")
    st.write("Answer the questions and check your score.")

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "quiz_topic" not in st.session_state:
        st.session_state.quiz_topic = ""
    if "quiz_result" not in st.session_state:
        st.session_state.quiz_result = None

    with st.form("quiz_form"):
        topic = st.text_input(
            "Quiz topic", placeholder="Example: Python functions"
        )
        num_questions = st.selectbox(
            "Number of questions", [5, 10, 15]
        )
        difficulty = st.selectbox(
            "Difficulty", ["Easy", "Medium", "Hard"]
        )
        generate = st.form_submit_button(
            "✨ Generate Quiz", use_container_width=True
        )

    if generate:
        if not topic.strip():
            st.warning("Please enter a quiz topic.")
        else:
            raw_quiz = get_ai_response(
                "You are an educational quiz generator. Return ONLY valid "
                "JSON without Markdown fences, using this structure: "
                '{"questions":[{"question":"Question text",'
                '"options":{"A":"Option A","B":"Option B",'
                '"C":"Option C","D":"Option D"},'
                '"answer":"A","explanation":"Why A is correct"}]}. '
                "Each question needs four options and one correct answer. "
                "The answer must be A, B, C or D.",
                f"Create exactly {num_questions} multiple-choice "
                f"questions about {topic.strip()}. Difficulty: {difficulty}. "
                "Return valid JSON only.",
                3500
            )

            if raw_quiz:
                try:
                    cleaned = raw_quiz.strip()
                    if cleaned.startswith("```"):
                        cleaned = cleaned.split("\n", 1)[1]
                        cleaned = cleaned.rsplit("```", 1)[0].strip()

                    quiz_data = json.loads(cleaned)
                    questions = quiz_data.get("questions", [])

                    # Validate quiz data inside the try block.
                    if len(questions) != num_questions:
                        raise ValueError(
                            "Wrong number of questions. Please generate again."
                        )

                    for q in questions:
                        if not all(
                            key in q for key in
                            ["question", "options", "answer", "explanation"]
                        ):
                            raise ValueError(
                                "A question is missing required fields."
                            )

                        if (
                            not isinstance(q["options"], dict)
                            or set(q["options"]) != {"A", "B", "C", "D"}
                            or q["answer"] not in {"A", "B", "C", "D"}
                        ):
                            raise ValueError(
                                "A question has invalid options or answer."
                            )

                    st.session_state.quiz_data = questions
                    st.session_state.quiz_topic = topic.strip()
                    st.session_state.quiz_result = None

                except (json.JSONDecodeError, ValueError, TypeError) as e:
                    st.error(f"Could not prepare the quiz: {e}")
                    st.session_state.quiz_data = None
                    st.session_state.quiz_result = None

    questions = st.session_state.quiz_data

    if questions:
        st.markdown(f"### 📝 Quiz: {st.session_state.quiz_topic}")

        with st.form("answer_quiz_form"):
            answers = []
            for i, q in enumerate(questions):
                st.markdown(f"**Question {i + 1}. {q['question']}**")
                options = q["options"]
                selected = st.radio(
                    f"Choose your answer for question {i + 1}",
                    ["A", "B", "C", "D"],
                    format_func=lambda key, opts=options:
                        f"{key}. {opts[key]}",
                    index=None,
                    key=f"quiz_answer_{i}"
                )
                answers.append(selected)

            submitted_quiz = st.form_submit_button(
                "✅ Submit Answers", use_container_width=True
            )

        if submitted_quiz:
            if any(answer is None for answer in answers):
                st.warning("Please answer every question before submitting.")
            else:
                st.session_state.quiz_result = answers

        if st.session_state.quiz_result is not None:
            submitted_answers = st.session_state.quiz_result
            score = sum(
                1 for selected, q in zip(submitted_answers, questions)
                if selected == q["answer"]
            )
            percentage = score / len(questions) * 100

            st.markdown("## 📊 Your Results")
            st.metric(
                "Your Score", f"{score} / {len(questions)}",
                f"{percentage:.0f}%"
            )
            st.progress(percentage / 100)

            if percentage >= 80:
                st.success("Excellent work! You understand this topic well.")
            elif percentage >= 50:
                st.info("Good effort! Review the explanations below.")
            else:
                st.warning("Keep practising. Review each explanation.")

            st.markdown("### 📖 Answer Review")
            for i, (selected, q) in enumerate(
                zip(submitted_answers, questions)
            ):
                correct = q["answer"]
                if selected == correct:
                    st.success(f"Question {i + 1}: Correct")
                else:
                    st.error(
                        f"Question {i + 1}: Incorrect. Correct answer: "
                        f"{correct}. {q['options'][correct]}"
                    )
                st.write(q["explanation"])

        if st.button("🔄 Generate Another Quiz"):
            st.session_state.quiz_data = None
            st.session_state.quiz_topic = ""
            st.session_state.quiz_result = None
            st.rerun()


# ---------- FOOTER ----------
st.divider()
st.caption(
    "StudyMate AI • Built with Python, Streamlit, and Groq. "
    "Always verify important academic information."
)
