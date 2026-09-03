import streamlit as st
import requests

st.set_page_config(
    page_title="AI Career Counselor & Roadmap Assistant",
    page_icon="💬",
    layout="centered"
)

st.title("💬 AI Career Counselor & Roadmap Assistant")
st.write("Have a natural conversation about your career goals, pivot strategies, and step-by-step milestones.")

# Point to your live backend endpoint
API_URL = "https://career-roadmap-backend-7e6h.onrender.com/chat/"

# Initialize chat history in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Career Counselor. What is your background, and what career path or tech domain are you looking to explore?"}
    ]

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask about your career path, skills, or roadmap phases..."):
    # Append user message
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
                response = requests.post(API_URL, json=payload)
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