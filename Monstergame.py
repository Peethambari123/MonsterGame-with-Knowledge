import streamlit as st
import random

# Set page config
st.set_page_config(page_title="Monster Quiz Battle", layout="centered")

# Sample DBMS questions
questions = {
    "beginner": [
        {"question": "What does DBMS stand for?", "options": ["Data Backup Management System", "Database Management System", "Data Based Managing System"], "answer": "Database Management System"},
        {"question": "Which of these is a primary key?", "options": ["Unique value", "Duplicate", "Null"], "answer": "Unique value"},
    ],
    "intermediate": [
        {"question": "Which SQL clause is used to filter records?", "options": ["WHERE", "SELECT", "ORDER BY"], "answer": "WHERE"},
        {"question": "What is normalization?", "options": ["Adding redundancy", "Removing redundancy", "Adding columns"], "answer": "Removing redundancy"},
    ],
    "advanced": [
        {"question": "Which normal form removes transitive dependency?", "options": ["1NF", "2NF", "3NF"], "answer": "3NF"},
        {"question": "Which SQL command is used to remove a table?", "options": ["DELETE", "REMOVE", "DROP"], "answer": "DROP"},
    ]
}

# Initialize session state
if "monster_size" not in st.session_state:
    st.session_state.monster_size = 300
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

def reset_game():
    st.session_state.monster_size = 300
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None

def main():
    st.title("🧟 Monster Quiz Battle Game")

    subject = st.selectbox("Select Subject", ["DBMS"])
    level = st.selectbox("Choose Difficulty Level", ["beginner", "intermediate", "advanced"])

    quiz = questions[level]

    st.markdown("### 👾 Monster Status")
    st.image("https://cdn-icons-png.flaticon.com/512/1162/1162636.png", width=st.session_state.monster_size)

    if st.session_state.current_q < len(quiz):
        q = quiz[st.session_state.current_q]
        st.subheader(f"Q{st.session_state.current_q + 1}: {q['question']}")
        st.session_state.selected_option = st.radio("Choose your answer:", q["options"], key=f"q{st.session_state.current_q}")

        if not st.session_state.answer_submitted:
            if st.button("Submit Answer"):
                if st.session_state.selected_option == q["answer"]:
                    st.success("✅ Correct! The monster shrinks.")
                    st.session_state.monster_size = max(100, st.session_state.monster_size - 50)
                    st.session_state.score += 1
                else:
                    st.error("❌ Wrong! The monster grows.")
                    st.session_state.monster_size += 50

                st.session_state.answer_submitted = True
        else:
            if st.button("Next Question"):
                st.session_state.current_q += 1
                st.session_state.answer_submitted = False
                st.session_state.selected_option = None

    else:
        st.balloons()
        st.success(f"🎉 Game Over! You scored {st.session_state.score} out of {len(quiz)}")
        if st.button("Play Again"):
            reset_game()

main()
