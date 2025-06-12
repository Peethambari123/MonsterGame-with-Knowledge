import streamlit as st
import google.generativeai as genai

# Set up the Gemini API
API_KEY = "AIzaSyAPlD-AdySRdcbtYZYmDV4v_spoAfYVm4A"  # Use your key here
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit page setup
st.set_page_config(page_title="Monster Quiz Game", page_icon="👾")

# Initialize session states
if "monster_size" not in st.session_state:
    st.session_state.monster_size = 300  # size between 100 and 500
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_data" not in st.session_state:
    st.session_state.question_data = None
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# Function to fetch question from Gemini
def fetch_question(subject, difficulty):
    prompt = f"""
    Generate one multiple-choice question for the subject '{subject}' at '{difficulty}' level.
    Format:
    Question: <question>
    A. <option1>
    B. <option2>
    C. <option3>
    D. <option4>
    Answer: <Correct Option Letter and Text>
    """
    response = model.generate_content(prompt).text
    lines = response.strip().splitlines()

    question = [line for line in lines if line.startswith("Question:")][0].replace("Question:", "").strip()
    options = [line.strip() for line in lines if line.strip().startswith(("A.", "B.", "C.", "D."))]
    answer = [line for line in lines if "Answer:" in line][0].replace("Answer:", "").strip()
    return question, options, answer

# Title
st.title("👾 Monster Quiz Game")
st.markdown("Answer correctly to **shrink** the monster. Wrong answers make it **grow**!")

# Select subject and difficulty
subject = st.selectbox("📘 Select Subject", ["DBMS", "Python", "AI", "Networks", "OS", "ML", "Cybersecurity"])
difficulty = st.selectbox("🎯 Select Difficulty", ["beginner", "intermediate", "advanced"])

# Monster image
st.image("https://cdn.pixabay.com/photo/2013/07/13/13/37/monster-161004_960_720.png", width=st.session_state.monster_size)

# Get new question
if st.button("🔄 Get New Question"):
    q, opts, ans = fetch_question(subject, difficulty)
    st.session_state.question_data = {"question": q, "options": opts, "correct": ans}
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None

# Display question and options
if st.session_state.question_data:
    st.subheader("🧠 " + st.session_state.question_data["question"])
    selected = st.radio("Choose your answer:", st.session_state.question_data["options"], key="selected_option")

    # Submit answer
    if st.button("✅ Submit Answer") and not st.session_state.answer_submitted:
        st.session_state.answer_submitted = True
        correct_letter = st.session_state.question_data["correct"].strip()[0]
        selected_letter = selected.strip()[0]

        if selected_letter == correct_letter:
            st.success("✅ Correct! Monster shrinks.")
            st.session_state.monster_size = max(100, st.session_state.monster_size - 50)
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong! Correct answer was: {st.session_state.question_data['correct']}")
            st.session_state.monster_size = min(500, st.session_state.monster_size + 50)

# Show score and monster weakness as progress bar (0–100)
monster_percent = max(0, min(100, 100 - (st.session_state.monster_size - 100) * 100 // 400))
st.markdown(f"**🏆 Score:** {st.session_state.score}")
st.progress(monster_percent, text="Monster Weakness Level")

# Reset Game
if st.button("🔁 Reset Game"):
    st.session_state.monster_size = 300
    st.session_state.score = 0
    st.session_state.question_data = None
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None
