import streamlit as st
import google.generativeai as genai
import random

# Set up Gemini API
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state for question history
if "question_history" not in st.session_state:
    st.session_state.question_history = []

# App configuration
st.set_page_config(page_title="Mega Quiz Generator", page_icon="🧠")
st.title("🧠 Mega Quiz Generator")
st.write("Generate unlimited quiz questions from any subject imaginable!")

# Quiz Generator Interface
st.subheader("📚 Quiz Question Generator")

# Sample subjects for dropdown (extendable, but custom input allowed)
sample_subjects = [
    "Python", "Quantum Computing", "World History", "Mathematics", "Biology",
    "Machine Learning", "Literature", "Physics", "Chemistry", "Economics", "Other"
]
subject = st.selectbox("Select or Enter a Subject", sample_subjects, index=len(sample_subjects)-1)
if subject == "Other":
    subject = st.text_input("Enter any subject (e.g., Astrophysics, Medieval Poetry, Blockchain, etc.)", value="Python")

difficulty = st.selectbox("Select Difficulty", ["Beginner", "Intermediate", "Advanced"])

# Question style for variety
question_styles = [
    "conceptual", "scenario-based", "problem-solving", "fact-based", "application-based"
]
selected_style = random.choice(question_styles)  # Randomize style for variety

if st.button("🎯 Generate Question"):
    with st.spinner("Generating a new question..."):
        # Enhanced prompt for diverse, non-repetitive questions
        prompt = f"""
Generate a unique, creative multiple-choice question from the subject: "{subject}" at {difficulty} level.
The question should be {selected_style}, challenging but understandable, and avoid repetition.
Avoid repeating these questions: {st.session_state.question_history[-10:]} (last 10 questions for context).

Use this exact format:
Question: <question>
A. <option>
B. <option>
C. <option>
D. <option>
Answer: <correct letter and full answer>
"""
        try:
            result = model.generate_content(prompt).text.strip().splitlines()

            # Parse the output
            question, options, answer = "", [], ""
            for line in result:
                if line.startswith("Question:"):
                    question = line.replace("Question:", "").strip()
                elif line.startswith(("A.", "B.", "C.", "D.")):
                    options.append(line.strip())
                elif line.startswith("Answer:"):
                    answer = line.replace("Answer:", "").strip()

            # Store question in history to avoid repetition
            st.session_state.question_history.append(question)

            # Display the question
            st.markdown(f"**🧠 Question (Style: {selected_style}):** {question}")
            for opt in options:
                st.markdown(f"- {opt}")
            
            # Show answer only when requested
            if st.button("Show Answer"):
                st.markdown(f"**✅ Correct Answer:** {answer}")

        except Exception as e:
            st.error(f"Error generating question: {str(e)}. Please try again.")

# Option to clear question history
if st.button("Clear Question History"):
    st.session_state.question_history = []
    st.success("Question history cleared!")
