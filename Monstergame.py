import streamlit as st
import google.generativeai as genai
import random
import time

# Configure Gemini API
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Page setup
st.set_page_config(page_title="Monster Quiz Game", page_icon="👾")

# Session state
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

# Monster images based on size
def get_monster_image(size):
    if size <= 150:
        return "https://cdn.pixabay.com/photo/2013/07/13/13/37/monster-161004_960_720.png"  # Weak monster
    elif size <= 300:
        return "https://cdn.pixabay.com/photo/2016/03/31/19/58/monster-1295124_960_720.png"  # Medium monster
    else:
        return "https://cdn.pixabay.com/photo/2016/03/31/19/58/monster-1295125_960_720.png"  # Strong monster

# CSS for size transition animation
st.markdown("""
    <style>
        .monster-image {
            transition: transform 0.5s ease-in-out;
        }
        .monster-image:hover {
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# Function to fetch unique questions
def fetch_question(subject, difficulty):
    seed_emoji = random.choice(["🐍", "🧠", "📘", "🛡️", "⚙️", "💻", "🧮"])
    seed = int(time.time())
    prompt = f"""
{seed_emoji} Generate a completely new and creative multiple-choice question for the subject '{subject}' at '{difficulty}' level.
Do NOT repeat previous formats or content.

Format like this:
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

# App title
st.title("👾 Monster Quiz Game")
st.markdown("Defeat the monster by answering questions correctly. It shrinks when you're right, grows when you're wrong!")

# Monster display with animation
monster_url = get_monster_image(st.session_state.monster_size)
st.markdown(f'<img src="{monster_url}" class="monster-image" width="{st.session_state.monster_size}">', unsafe_allow_html=True)

# Monster status message
if st.session_state.monster_size <= 150:
    st.markdown("**The monster is nearly defeated!**")
elif st.session_state.monster_size >= 400:
    st.markdown("**The monster is growing stronger!**")
else:
    st.markdown("**Keep fighting the monster!**")

# Select subject and difficulty
subject = st.selectbox("📘 Select Subject", ["DBMS", "Python", "AI", "Networks", "OS", "Cybersecurity", "ML"])
difficulty = st.selectbox("🎯 Select Difficulty", ["beginner", "intermediate", "advanced"])

# Get question
if st.button("🔄 Get New Question"):
    q, opts, ans = fetch_question(subject, difficulty)
    st.session_state.question = q
    st.session_state.options = opts
    st.session_state.correct = ans
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None

# Show question and options
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

# Score and progress
st.markdown(f"**🏆 Score:** {st.session_state.score}")
progress = max(0, min(100, 100 - (st.session_state.monster_size - 100) * 100 // 400))
st.progress(progress, text="Monster Weakness Level")

# Reset game
if st.button("🔁 Reset Game"):
    st.session_state.monster_size = 300
    st.session_state.score = 0
    st.session_state.question = None
    st.session_state.options = []
    st.session_state.correct = ""
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None
