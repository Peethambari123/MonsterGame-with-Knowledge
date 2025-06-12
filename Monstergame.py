import streamlit as st
import google.generativeai as genai

# Setup Gemini API
API_KEY = "AIzaSyAPlD-AdySRdcbtYZYmDV4v_spoAfYVm4A"
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

    question_text = lines[0].replace("Question: ", "").strip()
    options_line = [line for line in lines if "Options" in line or line.strip().startswith(("A.", "B.", "C.", "D."))]
    if options_line[0].startswith("Options:"):
        options_line = options_line[0].replace("Options:", "").strip()
        options = [opt.strip() for opt in options_line.split(",")]
    else:
        options = [line.strip() for line in options_line]

    answer_line = [line for line in lines if "Answer:" in line][0]
    correct_answer = answer_line.replace("Answer:", "").strip()

    return question_text, options, correct_answer

# UI
st.title("🎮 AI-Powered Monster Quiz Game")
st.markdown("Answer questions correctly to shrink the monster. If you're wrong, it grows!")

col1, col2 = st.columns(2)
with col1:
    subject = st.selectbox("Select Subject", ["DBMS", "Python", "AI", "Networks"], key="subject")
with col2:
    difficulty = st.selectbox("Select Difficulty", ["beginner", "intermediate", "advanced"], key="difficulty")

st.image("https://cdn-icons-png.flaticon.com/512/1162/1162636.png", width=st.session_state.monster_size)

# Get new question if not already fetched or reset
if st.button("🔄 Get New Question") or st.session_state.question is None:
    q, opts, ans = fetch_question(subject, difficulty)
    st.session_state.question = q
    st.session_state.answer_options = opts
    st.session_state.correct_answer = ans
    st.session_state.answer_submitted = False
    st.session_state.selected_option = None

# Show question
if st.session_state.question:
    st.subheader("📘 " + st.session_state.question)
    selected = st.radio("Your answer:", st.session_state.answer_options, key="selected_option")

    if st.button("✅ Submit Answer") and not st.session_state.answer_submitted:
        st.session_state.answer_submitted = True
        if selected in st.session_state.correct_answer:
            st.success("Correct! Monster shrinks.")
            st.session_state.monster_size = max(100, st.session_state.monster_size - 50)
            st.session_state.score += 1
        else:
            st.error(f"Wrong! Correct answer was: {st.session_state.correct_answer}")
            st.session_state.monster_size += 50

# Score display
st.markdown(f"**Score:** {st.session_state.score}")
