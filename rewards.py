import streamlit as st


def show_reward(score, total):
    if score == total:
        st.success("🎈 Wow! Perfect Score! 🎉")
    elif score >= total * 0.7:
        st.success("👏 Great Job! You're doing awesome!")
    elif score >= total * 0.5:
        st.info("😊 Good Try! Keep practicing!")
    else:
        st.warning("🙃 Don't worry! Try again and improve!")
