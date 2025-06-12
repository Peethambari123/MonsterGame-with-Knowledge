import streamlit as st
import google.generativeai as genai

# Setup Gemini API
API_KEY = "AIzaSyAPlD-AdySRdcbtYZYmDV4v_spoAfYVm4A"  # Replace with your own key if needed
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session states
if "monster_size" not in st.session_state:
    st.session_state.monster_size = 300
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question = None
if "answer_options" not in st.session_state:
    st.session_state.answer_options = []
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = ""
if "answer_submitted" not in st.session_state:
    st.session_state.answer_submitted = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "subject" not in st.session_state:
    st.session_state.subject = "DBMS"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "beginner"

# Function to fetch a question from Gemini
def fetch_question(subject, difficulty):
    prompt = f"""
    Generate one multiple-choice question for the subject '{subject}' at {difficulty} level. 
    Format the response as:
    Question: <text>
    Options: [A. ..., B. ..., C. ..., D. ...]
    Answer: <exact correct option letter and text>
    """
    response = model.generate_content(prompt).text
    lines = response.strip().splitlines()

    # Extract question
    question_text = [line for line in lines if line.startswith("Question:")][0].replace("Question:", "").strip()

    # Extract options
    options = [line.strip() for line in lines if line.strip().startswith(("A.", "B.", "C.", "D."))]

    # Extract answer
    answer_line = [line for line in lines if "Answer:" in line][0]
    correct_answer = answer_line.replace("Answer:", "").strip()

    return question_text, options, correct_answer

# UI
st.title("🎮 AI-Powered Monster Quiz Game")
st.markdown("Answer questions correctly to shrink the monster. If you're wrong, it grows!")

# Subject and difficulty selection
col1, col2 = st.columns(2)
subject_list = ["DBMS", "Python", "AI", "Networks", "OS", "ML", "Cybersecurity", "Data Science"]
with col1:
    subject = st.selectbox("Select Subject", subject_list, key="subject")
with col2:
    difficulty = st.selectbox("Select Difficulty", ["beginner", "intermediate", "advanced"], key="difficulty")

# Monster Image
st.image("https://cdn-icons-png.flaticon.com/512/1162/1162636.png", width=st.session_state.monster_size)

# Fetch new question
if st.button("🔄 Get New Question") or st.session_state.question is None:
    q, opts, ans = fetch_question(subject, difficulty)
    st.session_state.question = q
    st.session_state.answer_options = opts
    st.session_state.correct_answer = ans
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None

# Show question and options
if st.session_state.question:
    st.subheader("📘 " + st.session_state.question)
    selected = st.radio("Your answer:", st.session_state.answer_options, key="selected_option")

    if st.button("✅ Submit Answer") and not st.session_state.answer_submitted:
        st.session_state.answer_submitted = True
        correct_letter = st.session_state.correct_answer.strip()[0]
        selected_letter = selected.strip()[0]
        if selected_letter == correct_letter:
            st.success("Correct! Monster shrinks.")
            st.session_state.monster_size = max(100, st.session_state.monster_size - 50)
            st.session_state.score += 1
        else:
            st.error(f"Wrong! Correct answer was: {st.session_state.correct_answer}")
            st.session_state.monster_size += 50

# Display score and monster status
st.markdown(f"**Score:** {st.session_state.score}")
health = max(0, 1000 - st.session_state.monster_size * 2)
st.progress(health, text=f"Monster Weakness Level: {health}/1000")

# Reset Game Button
if st.button("🔁 Reset Game"):
    st.session_state.monster_size = 300
    st.session_state.score = 0
    st.session_state.question = None
