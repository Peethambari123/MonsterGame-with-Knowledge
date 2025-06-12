import streamlit as st
import random

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

# Title
st.title("🧠 Monster Quiz Battle Game")

# Subject and level selection
subject = st.selectbox("Select Subject", ["DBMS"])  # Extendable
level = st.selectbox("Choose Difficulty", ["beginner", "intermediate", "advanced"])

quiz = questions[level]

# Monster visual
st.markdown("### Monster Status:")
st.image("https://cdn-icons-png.flaticon.com/512/1162/1162636.png", width=st.session_state.monster_size)

# Show quiz question
if st.session_state.current_q < len(quiz):
    q = quiz[st.session_state.current_q]
    st.subheader(f"Q{st.session_state.current_q+1}: {q['question']}")
    option = st.radio("Choose your answer:", q["options"], key=f"q{st.session_state.current_q}")
    
    if st.button("Submit Answer"):
        if option == q["answer"]:
            st.success("Correct! The monster shrinks.")
            st.session_state.monster_size = max(100, st.session_state.monster_size - 50)
            st.session_state.score += 1
        else:
            st.error("Wrong! The monster grows.")
            st.session_state.monster_size += 50

        st.session_state.current_q += 1
        st.experimental_rerun()
else:
    st.success(f"🎉 Game Over! You scored {st.session_state.score} out of {len(quiz)}")
    if st.button("Play Again"):
        st.session_state.monster_size = 300
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.experimental_rerun()
