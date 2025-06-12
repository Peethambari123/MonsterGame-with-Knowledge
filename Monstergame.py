import streamlit as st
import google.generativeai as genai
import random
import time

# Configure Gemini API
API_KEY = "AIzaSyAPlD-AdySRdcbtYZYmDV4v_spoAfYVm4A"  # Replace with your actual key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Page setup
st.set_page_config(page_title="Monster Quiz Game", page_icon="👾")

# Monster image from user
monster_url = "https://tse2.mm.bing.net/th?id=OIP.0Z_qvxfmya6sNzHZN_XtkgHaHa&pid=Api&P=0&h=180"

# Session states
if "monster_size" not in st.session_state:
    st.session_state.monster_size = 300
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question = None
if "options" not in st.session_state:
    st.session_state.options = []
if "correct" not in st.session_state:
    st.session_state.correct = ""
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False

# Function to fetch a unique question
def fetch_question(subject, difficulty):
    seed_emoji = random.choice(["🐍", "🧠", "📘", "🛡️", "⚙️", "💻", "🧮"])
    seed = int(time.time())
    prompt = f"""
{seed_emoji} Generate a completely new and creative multiple-choice question for the subject '{subject}' at '{difficulty}' level.
Format:
Question: <your question>
A. <option>
B. <option>
C. <option>
D. <option>
Answer: <Correct letter and full option text>
Seed: {seed}
"""
    response = model.generate_content(prompt).text.strip().splitlines()

    question = ""
    options = []
    answer = ""

    for line in response:
        if line.startswith("Question:"):
            question = line.replace("Question:", "").strip()
        elif line.startswith(("A.", "B.", "C.", "D.")):
            options.append(line.strip())
        elif line.startswith("Answer:"):
            answer = line.replace("Answer:", "").strip()

    return question, options, answer

# App UI
st.title("👾 Monster Quiz Game")
st.markdown("Defeat the monster by answering questions correctly. It shrinks when you're right, grows when you're wrong!")

# Display monster
st.image(monster_url, width=st.session_state.monster_size)

# Subject and difficulty selection
subject = st.selectbox("📘 Select Subject", ["DBMS", "Python", "AI", "Networks", "OS", "Cybersecurity", "ML"])
difficulty = st.selectbox("🎯 Select Difficulty", ["beginner", "intermediate", "advanced"])

# Get new question
if st.button("🔄 Get New Question"):
    q, opts, ans = fetch_question(subject, difficulty)
    st.session_state.question = q
    st.session_state.options = opts
    st.session_state.correct = ans
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None

# Show question and answer options
if st.session_state.question:
    st.subheader("🧠 " + st.session_state.question)
    st.session_state.selected_option = st.radio("Choose your answer:", st.session_state.options)

    if st.button("✅ Submit Answer") and not st.session_state.answer_submitted:
        st.session_state.answer_submitted = True
        selected_letter = st.session_state.selected_option[0]
        correct_letter = st.session_state.correct[0]

        if selected_letter == correct_letter:
            st.success("✅ Correct! Monster shrinks.")
            st.session_state.monster_size = max(100, st.session_state.monster_size - 50)
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer was: {st.session_state.correct}")
            st.session_state.monster_size = min(500, st.session_state.monster_size + 50)

# Show score and monster weakness level
st.markdown(f"**🏆 Score:** {st.session_state.score}")
progress = max(0, min(100, 100 - (st.session_state.monster_size - 100) * 100 // 400))
st.progress(progress, text="Monster Weakness Level")

# Reset game button
if st.button("🔁 Reset Game"):
    st.session_state.monster_size = 300
    st.session_state.score = 0
    st.session_state.question = None
    st.session_state.options = []
    st.session_state.correct = ""
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None
