import streamlit as st

st.set_page_config( page_title="AI Study Assistant",
    page_icon="📚"
)

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
        border: none;
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        border-radius: 10px;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True )
st.markdown("""
<div class="hero">
    <h1>📚 AI Study Assistant</h1>
    <p>Your personal learning companion — study smarter,
    stay organized, and keep learning.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("What would you like to study today?")
st.caption("Choose a tool below to get started.")

    
)

st.title("📚 AI Study Assistant")
st.write("Your personal learning companion!")

task = st.selectbox(
    "Choose a study tool",
    ["Ask a Question", "Summarize Notes", "Generate Quiz"]
)

if task == "Ask a Question":
    question = st.text_area("Enter your question")
    if st.button("Submit Question"):
        if question.strip():
            st.info(
                "Your question: " + question +
                "\n\nAI answering will be added next!"
            )
        else:
            st.warning("Please enter a question.")

elif task == "Summarize Notes":
    notes = st.text_area("Paste your study notes")
    if st.button("Summarize"):
        if notes.strip():
            st.write("Your notes:")
            st.write(notes)
            st.info("AI summarization will be added next!")
        else:
            st.warning("Please enter your notes.")

else:
    topic = st.text_input("Enter a quiz topic")
    if st.button("Generate Quiz"):
        if topic.strip():
            st.write("Quiz topic:", topic)
            st.info("AI quiz generation will be added next!")
        else:
            st.warning("Please enter a topic.")
