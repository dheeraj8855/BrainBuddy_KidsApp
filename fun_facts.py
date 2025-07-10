import streamlit as st
import random
import rewards
from datetime import datetime

# Function to fully clear Fun Facts session state


def clear_fun_facts_session():
    keys_to_clear = [key for key in st.session_state.keys(
    ) if key.startswith('fun_') or key.startswith('fun_answer_')]
    for key in keys_to_clear:
        del st.session_state[key]
    st.session_state.fun_facts_answers = []
    st.session_state.fun_facts_submitted = False
    st.session_state.fun_facts_shuffled_questions = []
    st.query_params.clear()
    st.rerun()  # Instantly restart the app to refresh everything


def run_fun_facts_quiz():
    st.header("🤓 Fun Facts Quiz")

    # Define questions
    fun_facts_questions = [
        {"question": "What planet is known as the Red Planet?", "answer": "Mars"},
        {"question": "What is the tallest animal in the world?", "answer": "Giraffe"},
        {"question": "How many legs does a spider have?", "answer": "8"},
        {"question": "What is the fastest land animal?", "answer": "Cheetah"},
        {"question": "Which is the largest mammal?", "answer": "Blue Whale"},
        {"question": "Which bird is known for mimicking sounds?", "answer": "Parrot"},
        {"question": "Which planet has rings around it?", "answer": "Saturn"},
        {"question": "Which animal is known as the King of the Jungle?", "answer": "Lion"},
        {"question": "What is the smallest planet in our solar system?",
            "answer": "Mercury"},
        {"question": "What gas do plants absorb?", "answer": "Carbon dioxide"},
    ]

    # Shuffle questions once per session
    if 'fun_facts_shuffled_questions' not in st.session_state:
        st.session_state.fun_facts_shuffled_questions = random.sample(
            fun_facts_questions, len(fun_facts_questions))
        st.session_state.fun_facts_answers = [
            ""] * len(st.session_state.fun_facts_shuffled_questions)
        st.session_state.fun_facts_submitted = False

    questions = st.session_state.fun_facts_shuffled_questions
    total_questions = len(questions)

    # Display all questions with text inputs
    for idx, q in enumerate(questions):
        st.write(f"**Q{idx + 1}: {q['question']}**")
        st.session_state.fun_facts_answers[idx] = st.text_input(
            f"Your Answer for Q{idx + 1}:",
            key=f"fun_answer_{idx}",
            value=st.session_state.fun_facts_answers[idx]
        )

    # Submit button
    if not st.session_state.fun_facts_submitted:
        if st.button("✅ Submit Fun Facts Quiz"):
            st.session_state.fun_facts_submitted = True
            st.rerun()

    # Show results
    if st.session_state.fun_facts_submitted:
        score = 0
        for idx, q in enumerate(questions):
            user_answer = st.session_state.fun_facts_answers[idx].strip(
            ).lower()
            correct_answer = q['answer'].lower()
            st.write(f"Q{idx + 1}: {q['question']}")
            st.write(
                f"👉 Your Answer: {st.session_state.fun_facts_answers[idx]}")
            st.write(f"✅ Correct Answer: {q['answer']}")
            if user_answer == correct_answer:
                score += 1

        st.success(f"🏆 Your Fun Facts Score: {score}/{total_questions}")
        rewards.show_reward(score, total_questions)

        # Save to quiz history
        if 'quiz_history' not in st.session_state:
            st.session_state.quiz_history = []
        st.session_state.quiz_history.append({
            "quiz": "Fun Facts Quiz",
            "score": score,
            "total": total_questions,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Restart button
        if st.button("🔄 Restart Fun Facts Quiz"):
            clear_fun_facts_session()
