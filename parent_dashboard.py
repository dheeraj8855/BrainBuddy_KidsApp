import streamlit as st
import pandas as pd


def show_parent_dashboard():
    st.title("👩‍👦 Parent Dashboard - BrainBuddy Kids App")

    # Initialize quiz history if not present
    if 'quiz_history' not in st.session_state:
        st.session_state.quiz_history = []

    st.subheader("📊 Quiz Attempt History")

    if st.session_state.quiz_history:
        # Build DataFrame from quiz history
        data = {
            "Attempt No.": [],
            "Quiz Type": [],
            "Score": [],
            "Total Questions": [],
            "Time": []
        }

        for idx, entry in enumerate(st.session_state.quiz_history):
            data["Attempt No."].append(idx + 1)
            data["Quiz Type"].append(entry['quiz'])
            data["Score"].append(entry['score'])
            data["Total Questions"].append(entry['total'])
            data["Time"].append(entry['time'])

        df = pd.DataFrame(data)

        st.table(df)

        # Clear history button
        if st.button("🗑️ Clear Entire History"):
            st.session_state.quiz_history = []
            st.success("✅ Quiz history cleared successfully!")
            st.rerun()

    else:
        st.info(
            "ℹ️ No quiz history available yet. Encourage your child to try some quizzes!")
