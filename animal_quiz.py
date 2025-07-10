import streamlit as st
import random
import rewards
from datetime import datetime

# Function to clear session state for Animal Quiz


def clear_animal_quiz_session():
    keys_to_clear = [key for key in st.session_state.keys() if key.startswith(
        'animal_') or key.startswith('animal_answer_')]
    for key in keys_to_clear:
        del st.session_state[key]
    st.session_state.animal_answers = []
    st.session_state.animal_submitted = False
    st.query_params.clear()
    st.rerun()  # Ensure clean restart immediately


def run_animal_quiz():
    st.header("🐾 Animal Quiz")

    # Define the questions
    animal_questions = [
        {"question": "Which animal is known as the King of the Jungle?", "answer": "Lion"},
        {"question": "Which animal is the largest mammal?", "answer": "Blue Whale"},
        {"question": "Which bird is known for its beautiful tail?", "answer": "Peacock"},
        {"question": "Which animal is known for building dams?", "answer": "Beaver"},
        {"question": "Which insect makes honey?", "answer": "Bee"},
        {"question": "Which animal has a long trunk?", "answer": "Elephant"},
        {"question": "Which bird cannot fly?", "answer": "Ostrich"},
        {"question": "Which animal has black and white stripes?", "answer": "Zebra"},
        {"question": "Which marine animal has eight legs?", "answer": "Octopus"},
        {"question": "Which animal is known for hopping?", "answer": "Kangaroo"},
    ]

    # Shuffle once per new session
    if 'animal_shuffled_questions' not in st.session_state:
        st.session_state.animal_shuffled_questions = random.sample(
            animal_questions, len(animal_questions))
        st.session_state.animal_answers = [
            ""] * len(st.session_state.animal_shuffled_questions)
        st.session_state.animal_submitted = False

    questions = st.session_state.animal_shuffled_questions
    total_questions = len(questions)

    # Display questions
    for idx, q in enumerate(questions):
        st.write(f"**Q{idx + 1}: {q['question']}**")
        st.session_state.animal_answers[idx] = st.text_input(
            f"Your Answer for Q{idx + 1}:",
            key=f"animal_answer_{idx}",
            value=st.session_state.animal_answers[idx]
        )

    # Submit button
    if not st.session_state.animal_submitted:
        if st.button("✅ Submit Animal Quiz"):
            st.session_state.animal_submitted = True
            st.rerun()

    # Results after submission
    if st.session_state.animal_submitted:
        score = 0
        for idx, q in enumerate(questions):
            user_answer = st.session_state.animal_answers[idx].strip().lower()
            correct_answer = q['answer'].lower()
            st.write(f"Q{idx + 1}: {q['question']}")
            st.write(f"👉 Your Answer: {st.session_state.animal_answers[idx]}")
            st.write(f"✅ Correct Answer: {q['answer']}")
            if user_answer == correct_answer:
                score += 1

        st.success(f"🏆 Your Animal Quiz Score: {score}/{total_questions}")
        rewards.show_reward(score, total_questions)

        # Save quiz history
        if 'quiz_history' not in st.session_state:
            st.session_state.quiz_history = []
        st.session_state.quiz_history.append({
            "quiz": "Animal Quiz",
            "score": score,
            "total": total_questions,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Restart button
        if st.button("🔄 Restart Animal Quiz"):
            clear_animal_quiz_session()
