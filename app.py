import streamlit as st

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚"
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
