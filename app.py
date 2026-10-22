
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="StudyMate AI",
    page_icon="📚",
    layout="wide"
)

# ---------- PROFESSIONAL UI ----------
st.markdown("""
<style>
    .stApp {
        background-color: #F5F7FC;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: #172554;
    }

    .hero {
        background: linear-gradient(120deg, #102A56, #2563EB);
        padding: 30px;
        border-radius: 18px;
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 2.3rem;
        margin-bottom: 8px;
    }

    .hero p {
        color: #E0EAFF;
        font-size: 1.05rem;
    }

    div.stButton > button {
        background: #2563EB;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background: #1D4ED8;
        color: white;
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
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
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        st.error(
            "Unable to get an AI response. Check your API key, "
        "Groq usage limits, model availability, and app logs." 
        )
        return None

    try:
        client = Groq(api_key=api_key)

        with st.spinner("StudyMate AI is thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
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
    [
        "Ask a Question",
        "Summarize Notes",
        "Generate Quiz"
    ]
)

st.divider()

# ---------- 1. ASK A QUESTION ----------
if task == "Ask a Question":
    st.subheader("💬 Ask StudyMate AI")
    st.write("Get clear, student-friendly explanations.")

    with st.form("question_form"):
        question = st.text_area(
            "Enter your question",
            placeholder="Example: Explain artificial intelligence in simple words.",
            height=130
        )

        submitted = st.form_submit_button(
            "✨ Get Answer",
            use_container_width=True
        )

    if submitted:
        if question.strip():
            answer = get_ai_response(
                system_prompt=(
                    "You are StudyMate AI, a helpful study assistant. "
                    "Explain concepts clearly for college students. "
                    "Use headings, examples, and simple language where "
                    "appropriate. If you are unsure of a fact, say so."
                ),
                user_prompt=question.strip(),
                max_tokens=1200
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
            [
                "Short summary",
                "Detailed summary",
                "Exam revision notes",
                "Key points only"
            ]
        )

        submitted = st.form_submit_button(
            "✨ Summarize Notes",
            use_container_width=True
        )

    if submitted:
        if notes.strip():
            summary = get_ai_response(
                system_prompt=(
                    "You are StudyMate AI, an academic note summarizer. "
                    "Use only the supplied notes as the source for "
                    "source-specific facts. Do not invent details. "
                    "If something is unclear or missing, say so. "
                    "Format the result in readable Markdown."
                ),
                user_prompt=(
                    f"Create a {summary_style.lower()} from these notes. "
                    "Preserve important terminology, definitions, "
                    "formulas, and examples.\n\n"
                    f"STUDY NOTES:\n{notes}"
                ),
                max_tokens=1800
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

# ---------- 3. GENERATE QUIZ ----------
else:
    st.subheader("🧠 Generate a Practice Quiz")
    st.write("Test your understanding with multiple-choice questions.")

    with st.form("quiz_form"):
        topic = st.text_input(
            "Quiz topic",
            placeholder="Example: Python functions"
        )

        num_questions = st.selectbox(
            "Number of questions",
            [5, 10, 15]
        )

        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"]
        )

        submitted = st.form_submit_button(
            "✨ Generate Quiz",
            use_container_width=True
        )

    if submitted:
        if topic.strip():
            quiz = get_ai_response(
                system_prompt=(
                    "You are StudyMate AI, an educational quiz creator. "
                    "Create accurate multiple-choice questions. "
                    "Give four options labelled A, B, C, and D for "
                    "each question. After all questions, provide an "
                    "answer key with a brief explanation for each "
                    "correct answer. Make sure the answer key matches "
                    "the options. Use clear Markdown formatting."
                ),
                user_prompt=(
                    f"Create {num_questions} multiple-choice questions "
                    f"about: {topic.strip()}\n"
                    f"Difficulty: {difficulty}\n\n"
                    "Number each question. Include four options per "
                    "question. Put the complete answer key and brief "
                    "explanations at the end, after all questions."
                ),
                max_tokens=2500
            )

            if quiz:
                st.markdown("### 📝 Your Practice Quiz")
                st.markdown(quiz)

                st.download_button(
                    "⬇️ Download Quiz",
                    data=quiz,
                    file_name="studymate_quiz.md",
                    mime="text/markdown"
                )
        else:
            st.warning("Please enter a quiz topic.")

# ---------- FOOTER ----------
st.divider()
st.caption(
    "StudyMate AI • Built with Python, Streamlit, and Groq. "
    "Always verify important academic information."
)
