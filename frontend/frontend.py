import streamlit as st
import requests

st.set_page_config(
    page_title="AI Career Counselor & Roadmap Assistant",
    page_icon="💬",
    layout="centered"
)

st.title("💬 AI Career Counselor & Roadmap Assistant")
st.markdown("🎯 **Welcome to the Tech Career Pathway Assessment!** Have a natural conversation about your career goals, pivot strategies, and step-by-step milestones.")

# Set your backend URL: Use local endpoint for testing, or your live Render URL when deployed
# BACKEND_URL = "https://tech-career-backend.onrender.com/chat/"
BACKEND_URL = "http://127.0.0.1:8000/chat/"

# Initialize chat history in session state to match the classic welcome prompt flow
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's identify your ideal technical career track across 8 specialized domains. There are 10 questions. For each question, simply reply with your choice (A, B, C, D, E, F, G, or H). Respond OK and let's get started!"}
    ]

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input via chat box
if prompt := st.chat_input("Ask about your career path, skills, or roadmap phases..."):
    # Append user message to session state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare payload for FastAPI /chat/ endpoint
    payload = {
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(BACKEND_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("reply", "I'm here to help!")
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    error_msg = f"Error from backend: {response.status_code} - {response.text}"
                    st.error(error_msg)
            except Exception as e:
                st.error(f"Could not connect to backend server: {e}")