import streamlit as st
import random
import rewards
from datetime import datetime

# Function to clear Vocabulary Quiz session state


def clear_vocabulary_session():
    keys_to_clear = [key for key in st.session_state.keys()
                     if key.startswith('vocab_')]
    for key in keys_to_clear:
        del st.session_state[key]
    st.session_state.vocab_answers = []
    st.session_state.vocab_submitted = False
    st.session_state.vocab_shuffled_questions = []
    st.query_params.clear()
    st.rerun()  # Instant refresh


def run_vocabulary_quiz():
    st.header("📚 Vocabulary Quiz")

    vocab_questions = [
        {"word": "Enormous", "meaning": "Very big"},
        {"word": "Tiny", "meaning": "Very small"},
        {"word": "Brave", "meaning": "Showing courage"},
        {"word": "Beautiful", "meaning": "Very pretty"},
        {"word": "Fast", "meaning": "Moving quickly"},
        {"word": "Happy", "meaning": "Feeling joy"},
        {"word": "Cold", "meaning": "Low temperature"},
        {"word": "Kind", "meaning": "Nice to others"},
        {"word": "Jump", "meaning": "To leap up"},
        {"word": "Smart", "meaning": "Very intelligent"},
    ]

    # Shuffle once per session
    if 'vocab_shuffled_questions' not in st.session_state:
        st.session_state.vocab_shuffled_questions = random.sample(
            vocab_questions, len(vocab_questions))
        st.session_state.vocab_answers = [
            ""] * len(st.session_state.vocab_shuffled_questions)
        st.session_state.vocab_submitted = False

    questions = st.session_state.vocab_shuffled_questions
    total_questions = len(questions)

    # Display all vocabulary questions
    for idx, q in enumerate(questions):
        st.write(f"**Q{idx + 1}: What is the meaning of '{q['word']}'?**")
        st.session_state.vocab_answers[idx] = st.text_input(
            f"Your Answer for Q{idx + 1}:",
            key=f"vocab_answer_{idx}",
            value=st.session_state.vocab_answers[idx]
        )

    # Submit button
    if not st.session_state.vocab_submitted:
        if st.button("✅ Submit Vocabulary Quiz"):
            st.session_state.vocab_submitted = True
            st.rerun()

    # Show results after submission
    if st.session_state.vocab_submitted:
        score = 0
        for idx, q in enumerate(questions):
            user_answer = st.session_state.vocab_answers[idx].strip().lower()
            correct_answer = q['meaning'].lower()
            st.write(f"Q{idx + 1}: Meaning of **{q['word']}**")
            st.write(f"👉 Your Answer: {st.session_state.vocab_answers[idx]}")
            st.write(f"✅ Correct Answer: {q['meaning']}")
            if user_answer == correct_answer:
                score += 1

        st.success(f"🏆 Your Vocabulary Score: {score}/{total_questions}")
        rewards.show_reward(score, total_questions)

        # Save to quiz history for Parent Dashboard
        if 'quiz_history' not in st.session_state:
            st.session_state.quiz_history = []
        st.session_state.quiz_history.append({
            "quiz": "Vocabulary Quiz",
            "score": score,
            "total": total_questions,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Restart button
        if st.button("🔄 Restart Vocabulary Quiz"):
            clear_vocabulary_session()
