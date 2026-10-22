
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

                   
