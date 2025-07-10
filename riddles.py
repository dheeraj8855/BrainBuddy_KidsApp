import streamlit as st
import random
import rewards
from datetime import datetime

# Function to clear Riddles session state completely


def clear_riddles_session():
    keys_to_clear = [key for key in st.session_state.keys()
                     if key.startswith('riddle_')]
    for key in keys_to_clear:
        del st.session_state[key]
    st.session_state.riddle_answers = []
    st.session_state.riddle_submitted = False
    st.session_state.riddle_shuffled_questions = []
    st.query_params.clear()
    st.rerun()  # Instant refresh


def run_riddles():
    st.header("🧠 Riddles Quiz")

    riddles_questions = [
        {"question": "I’m tall when I’m young, and short when I’m old. What am I?",
            "answer": "A candle"},
        {"question": "What has keys but can't open doors?", "answer": "A piano"},
        {"question": "I speak without a mouth and hear without ears. What am I?",
            "answer": "An echo"},
        {"question": "What can travel around the world while staying in the same spot?",
            "answer": "A stamp"},
        {"question": "What has hands but can’t clap?", "answer": "A clock"},
        {"question": "What comes down but never goes up?", "answer": "Rain"},
        {"question": "What has to be broken before you can use it?", "answer": "An egg"},
        {"question": "What gets wetter the more it dries?", "answer": "A towel"},
        {"question": "What has a head and a tail but no body?", "answer": "A coin"},
        {"question": "What has one eye but cannot see?", "answer": "A needle"},
    ]

    # Shuffle once per session
    if 'riddle_shuffled_questions' not in st.session_state:
        st.session_state.riddle_shuffled_questions = random.sample(
            riddles_questions, len(riddles_questions))
        st.session_state.riddle_answers = [
            ""] * len(st.session_state.riddle_shuffled_questions)
        st.session_state.riddle_submitted = False

    questions = st.session_state.riddle_shuffled_questions
    total_questions = len(questions)

    # Display all riddles with text inputs
    for idx, q in enumerate(questions):
        st.write(f"**Q{idx + 1}: {q['question']}**")
        st.session_state.riddle_answers[idx] = st.text_input(
            f"Your Answer for Q{idx + 1}:",
            key=f"riddle_answer_{idx}",
            value=st.session_state.riddle_answers[idx]
        )

    # Submit button
    if not st.session_state.riddle_submitted:
        if st.button("✅ Submit Riddles Quiz"):
            st.session_state.riddle_submitted = True
            st.rerun()

    # Show results
    if st.session_state.riddle_submitted:
        score = 0
        for idx, q in enumerate(questions):
            user_answer = st.session_state.riddle_answers[idx].strip().lower()
            correct_answer = q['answer'].lower()
            st.write(f"Q{idx + 1}: {q['question']}")
            st.write(f"👉 Your Answer: {st.session_state.riddle_answers[idx]}")
            st.write(f"✅ Correct Answer: {q['answer']}")
            if user_answer == correct_answer:
                score += 1

        st.success(f"🏆 Your Riddles Score: {score}/{total_questions}")
        rewards.show_reward(score, total_questions)

        # Save for Parent Dashboard
        if 'quiz_history' not in st.session_state:
            st.session_state.quiz_history = []
        st.session_state.quiz_history.append({
            "quiz": "Riddles Quiz",
            "score": score,
            "total": total_questions,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Restart button
        if st.button("🔄 Restart Riddles Quiz"):
            clear_riddles_session()
