import streamlit as st
import google.generativeai as genai

# Setup Gemini API
API_KEY = "AIzaSyAPlD-AdySRdcbtYZYmDV4v_spoAfYVm4A"  # Replace with your API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Set page config
st.set_page_config(page_title="Monster Quiz", page_icon="👾")

# Initialize states
if "monster_size" not in st.session_state:
    st.session_state.monster_size = 300
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_data" not in st.session_state:
    st.session_state.question_data = None
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# Function to fetch a question from Gemini
def fetch_question(subject, difficulty):
    prompt = f"""
    Generate ONE multiple-choice question for the subject '{subject}' at '{difficulty}' level.
    Format:
    Question: <text>
    A. <option1>
    B. <option2>
    C. <option3>
    D. <option4>
    Answer: <Correct Option Letter and Text>
    """
    response = model.generate_content(prompt).text
    lines = response.strip().splitlines()

    question = [l for l in lines if l.startswith("Question:")][0].replace("Question:", "").strip()
    options = [l.strip() for l in lines if l.startswith(("A.", "B.", "C.", "D."))]
    answer_line = [l for l in lines if l.startswith("Answer:")][0]
    correct_answer = answer_line.replace("Answer:", "").strip()

    return question, options, correct_answer

# Monster Quiz UI
st.title("👾 AI-Powered Monster Quiz Game")
st.markdown("Answer right to **shrink** the monster. Answer wrong... it **grows**!")

# Select subject & difficulty
subject = st.selectbox("📚 Select Subject", ["DBMS", "Python", "AI", "Networks", "OS", "ML", "Cybersecurity"])
difficulty = st.selectbox("🎯 Select Difficulty", ["beginner", "intermediate", "advanced"])

# Show monster image (real monster!)
st.image("https://cdn.pixabay.com/photo/2013/07/13/13/37/monster-161004_960_720.png", width=st.session_state.monster_size)

# Get New Question
if st.button("🔄 Get New Question"):
    question, options, correct = fetch_question(subject, difficulty)
    st.session_state.question_data = {"question": question, "options": options, "correct": correct}
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None

# Show question
if st.session_state.question_data:
    st.subheader("🧠 " + st.session_state.question_data["question"])
    selected = st.radio("Choose your answer:", st.session_state.question_data["options"], key="answer_radio")

    # Submit answer
    if st.button("✅ Submit Answer") and not st.session_state.answer_submitted:
        st.session_state.answer_submitted = True
        st.session_state.selected_option = selected
        correct_letter = st.session_state.question_data["correct"].strip()[0]
        selected_letter = selected.strip()[0]

        if selected_letter == correct_letter:
            st.success("🎉 Correct! Monster shrinks!")
            st.session_state.monster_size = max(100, st.session_state.monster_size - 50)
            st.session_state.score += 1
        else:
            st.error(f"💀 Wrong! Correct answer was: {st.session_state.question_data['correct']}")
            st.session_state.monster_size = min(500, st.session_state.monster_size + 50)

# Score and monster health
st.markdown(f"**🏆 Score:** {st.session_state.score}")
st.progress(max(0, 1000 - st.session_state.monster_size * 2), text="Monster Weakness Level")

# Reset Game
if st.button("🔁 Reset Game"):
    st.session_state.monster_size = 300
    st.session_state.score = 0
    st.session_state.question_data = None
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None
