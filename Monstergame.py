import streamlit as st
import google.generativeai as genai

# Set up Gemini API
API_KEY = "AIzaSyAPlD-AdySRdcbtYZYmDV4v_spoAfYVm4A"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# App title
st.set_page_config(page_title="Mega GPT Quiz Generator", page_icon="🧠")
st.title("🧠 GPT Mega Quiz & Chat")
st.write("Ask questions, chat with the bot, or generate unlimited quiz questions from any subject!")

# Sidebar to choose mode
mode = st.sidebar.radio("Choose Mode", ["💬 Chat Mode", "📚 Quiz Generator"])

# Common setup for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# === CHAT MODE ===
if mode == "💬 Chat Mode":
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

    subject = st.text_input("Enter any subject (e.g., Quantum Computing, History, Python, etc.)", value="Python")
    difficulty = st.selectbox("Select Difficulty", ["beginner", "intermediate", "advanced"])
    if st.button("🎯 Generate Question"):
        with st.spinner("Generating a new question..."):
            prompt = f"""
Generate a creative and non-repeated multiple-choice question from the subject: "{subject}" at {difficulty} level.

Use this exact format:
Question: <question>
A. <option>
B. <option>
C. <option>
D. <option>
Answer: <correct letter and full answer>

Make it challenging but understandable.
"""
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

            st.markdown(f"**🧠 Question:** {question}")
            for opt in options:
                st.markdown(f"- {opt}")
            st.markdown(f"**✅ Correct Answer:** {answer}")
