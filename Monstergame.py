import streamlit as st
import google.generativeai as genai

# Set up Gemini API
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Initialize messages and question history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_history" not in st.session_state:
    st.session_state.question_history = []

# App configuration
st.set_page_config(page_title="Mega GPT Quiz & Chat", page_icon="🧠")
st.title("🧠 Mega GPT Quiz & Chat")
st.write("Chat with the AI or generate unlimited quiz questions from any subject!")

# Sidebar to choose mode
mode = st.sidebar.radio("Choose Mode", ["💬 Chat Mode", "📚 Quiz Generator"])

# === CHAT MODE ===
if mode == "💬 Chat Mode":
    st.subheader("🤖 Chatbot - Your AI Assistant")
    st.write("Welcome to the Chatbot! How can I help you?")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Say something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = st.session_state.chat.send_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"):
            st.markdown(response.text)

# === QUIZ GENERATOR MODE ===
else:
    st.subheader("📚 Quiz Question Generator")

    # Sample subjects for dropdown (extendable, but custom input allowed)
    sample_subjects = [
        "Python", "Quantum Computing", "World History", "Mathematics", "Biology",
        "Machine Learning", "Literature", "Physics", "Chemistry", "Economics", "Other"
    ]
    subject = st.selectbox("Select or Enter a Subject", sample_subjects, index=len(sample_subjects)-1)
    if subject == "Other":
        subject = st.text_input("Enter any subject (e.g., Astrophysics, Medieval Art, etc.)", value="Python")

    difficulty = st.selectbox("Select Difficulty", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("🎯 Generate Question"):
        with st.spinner("Generating a new question..."):
            # Enhanced prompt to ensure variety and non-repetition
            prompt = f"""
Generate a creative, unique, and non-repetitive multiple-choice question from the subject: "{subject}" at {difficulty} level.
The question should be challenging but understandable, tailored to the specified difficulty.
Avoid repeating these questions: {st.session_state.question_history[-5:]} (last 5 questions for context).

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
                st.markdown(f"**🧠 Question:** {question}")
                for opt in options:
                    st.markdown(f"- {opt}")
                st.markdown(f"**✅ Correct Answer:** {answer}")

            except Exception as e:
                st.error(f"Error generating question: {str(e)}. Please try again.")
