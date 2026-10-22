
                    # Validate the AI-generated quiz.
                    if len(questions) != num_questions:
                        raise ValueError(
                            "The AI returned the wrong number "
                            "of questions. Please generate again."
                        )

                    for q in questions:
                        if not all(
                            key in q
                            for key in [
                                "question", "options",
                                "answer", "explanation"
                            ]
                        ):
                            raise ValueError(
                                "A question is missing required fields."
                            )

                        if (
                            set(q["options"].keys())
                            != {"A", "B", "C", "D"}
                            or q["answer"] not in {"A", "B", "C", "D"}
                        ):
                            raise ValueError(
                                "A question has invalid options or answer."
                            )

                    st.session_state.quiz_data = questions
                    st.session_state.quiz_topic = topic.strip()

                except (json.JSONDecodeError, ValueError) as e:
                    st.error(f"Could not prepare the quiz: {e}")
                    st.session_state.quiz_data = None

    # Display the generated quiz and calculate the score.
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
                    options=["A", "B", "C", "D"],
                    format_func=lambda key, opts=options: (
                        f"{key}. {opts[key]}"
                    ),
                    index=None,
                    key=f"quiz_answer_{i}"
                )
                answers.append(selected)

            submitted_quiz = st.form_submit_button(
                "✅ Submit Answers",
                use_container_width=True
            )

        if submitted_quiz:
            score = sum(
                1 for selected, q in zip(answers, questions)
                if selected == q["answer"]
            )

            percentage = score / len(questions) * 100

            st.markdown("## 📊 Your Results")
            st.metric(
                "Your Score",
                f"{score} / {len(questions)}",
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
                zip(answers, questions)
            ):
                correct = q["answer"]

                if selected == correct:
                    st.success(f"Question {i + 1}: Correct")
                else:
                    st.error(
                        f"Question {i + 1}: Incorrect. "
                        f"Correct answer: {correct}. "
                        f"{q['options'][correct]}"
                    )

                st.write(q["explanation"])

        if st.button("🔄 Generate Another Quiz"):
            st.session_state.quiz_data = None
            st.session_state.quiz_topic = ""
            st.rerun()


# ---------- FOOTER ----------
st.divider()
st.caption(
    "StudyMate AI • Built with Python, Streamlit, and Groq. "
    "Always verify important academic information."
)
