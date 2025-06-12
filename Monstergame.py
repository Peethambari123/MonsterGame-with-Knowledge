import streamlit as st
import google.generativeai as genai

# Setup Gemini API
API_KEY = "AIzaSyAPlD-AdySRdcbtYZYmDV4v_spoAfYVm4A"  # Replace with your own API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Page config
st.set_page_config(page_title="Monster Quiz Game", page_icon="👾")

# Initial state
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

# Function to fetch a question
def fetch_question(subject, difficulty):
    prompt = f"""
    Generate ONE multiple choice question for the subject '{subject}' at '{difficulty}' level.
    Format exactly like this:
    Question: <your question>
    A. <option>
    B. <option>
    C. <option>
    D. <option>
    Answer: <correct letter and option text>
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

# Header
st.title("👾 Monster Quiz Game")
st.markdown("Defeat the monster by answering questions right. It shrinks when you're correct, and grows if you're wrong!")

# Monster Image
monster_url = "https://tse2.mm.bing.net/th?id=OIP.0Z_qvxfmya6sNzHZN_XtkgHaHa&pid=Api&P=0&h=180"
st.image(monster_url, width=st.session_state.monster_size)

# Subject and difficulty selectors
subject = st.selectbox("📘 Select Subject", ["DBMS", "Python", "AI", "Networks", "OS", "Cybersecurity"])
difficulty = st.selectbox("🎯 Select Difficulty", ["beginner", "intermediate", "advanced"])

# Get new question
if st.button("🔄 Get New Question"):
    st.session_state.question, st.session_state.options, st.session_state.correct = fetch_question(subject, difficulty)
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
            st.success("✅ Correct! The monster shrinks.")
            st.session_state.monster_size = max(100, st.session_state.monster_size - 50)
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer was: {st.session_state.correct}")
            st.session_state.monster_size = min(500, st.session_state.monster_size + 50)

# Score
st.markdown(f"**🏆 Score:** {st.session_state.score}")

# Progress bar
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
