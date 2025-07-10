import streamlit as st
import math_quiz
import vocabulary
import riddles
import fun_facts
import animal_quiz
import parent_dashboard
import os

# Set page config
st.set_page_config(page_title="BrainBuddy Kids App 🎈", layout="centered")

# Title
st.title("BrainBuddy Kids App 🎈")

# Load Premium Status from File


def load_premium_status():
    if os.path.exists("premium_status.txt"):
        with open("premium_status.txt", "r") as f:
            status = f.read().strip()
            return status == "unlocked"
    return False

# Save Premium Status


def save_premium_status():
    with open("premium_status.txt", "w") as f:
        f.write("unlocked")


# Initialize Premium State
if "is_premium" not in st.session_state:
    st.session_state.is_premium = load_premium_status()

# Sidebar Navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.selectbox("Select Activity", [
    "Home",
    "Math Quiz",
    "Vocabulary Quiz",
    "Riddles",
    "Fun Facts",
    "Animal Quiz",
    "Parent Dashboard"
])

# Home Page
if page == "Home":
    st.header("Welcome to BrainBuddy Kids App!")
    st.markdown("""
    👉 Choose an activity from the left sidebar:

    - Math Quiz
    - Vocabulary Quiz 🔒 (Premium)
    - Riddles 🔒 (Premium)
    - Fun Facts
    - Animal Quiz
    - Parent Dashboard

    ✅ Have fun learning!
    """)

    if not st.session_state.is_premium:
        st.markdown("### Unlock Premium 🔓")
        st.info("Get access to Vocabulary Quiz & Riddles for just ₹149 (one-time).")
        if st.button("Unlock Now ₹149"):
            # In real app: Here you would handle payment (UPI, etc.)
            save_premium_status()
            st.session_state.is_premium = True
            st.success("Premium Unlocked! Enjoy all features.")
            st.rerun()

# Math Quiz
elif page == "Math Quiz":
    math_quiz.run_math_quiz()

# Vocabulary Quiz (Premium Lock)
elif page == "Vocabulary Quiz":
    if st.session_state.is_premium:
        vocabulary.run_vocabulary_quiz()
    else:
        st.warning("🔒 This feature is for Premium users only.")
        if st.button("Unlock Premium ₹149"):
            save_premium_status()
            st.session_state.is_premium = True
            st.success("Premium Unlocked!")
            st.rerun()

# Riddles (Premium Lock)
elif page == "Riddles":
    if st.session_state.is_premium:
        riddles.run_riddles()
    else:
        st.warning("🔒 This feature is for Premium users only.")
        if st.button("Unlock Premium ₹149"):
            save_premium_status()
            st.session_state.is_premium = True
            st.success("Premium Unlocked!")
            st.rerun()

# Fun Facts (Free)
elif page == "Fun Facts":
    fun_facts.run_fun_facts_quiz()

# Animal Quiz (Free)
elif page == "Animal Quiz":
    animal_quiz.run_animal_quiz()

# Parent Dashboard
elif page == "Parent Dashboard":
    parent_dashboard.show_parent_dashboard()
