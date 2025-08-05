import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("AI Chatbot Agents")
st.write("create and interact with the AI agents!")

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

st.session_state.system_prompt = st.text_area(
    "define your AI Agent:", 
    height=70, 
    placeholder="type your system prompt here...",
    value=st.session_state.system_prompt
)

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o"]

provider = st.radio("Select Provider:", ("Groq", "OpenAI"))
selected_model = st.selectbox("Select Model:", MODEL_NAMES_GROQ if provider == "Groq" else MODEL_NAMES_OPENAI)


allow_web_search = st.checkbox("Allow Web Search")

st.session_state.user_query = st.text_area(
    "Enter your query:", 
    height=150, 
    placeholder="Ask your AI agent...",
    value=st.session_state.user_query
)

API_URL = "http://127.0.0.1:9999/chat"


if st.button("Ask Agent!"):
    if st.session_state.user_query.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "model_prompt": st.session_state.system_prompt or "You are a helpful AI agent.",
            "messages": [st.session_state.user_query],
            "allow_search": allow_web_search
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data["error"])
                elif "response" in response_data:
                    st.subheader("agent Response")
                    response_text = response_data["response"]
                    if isinstance(response_text, dict):
                        response_text = response_text.get("content", str(response_text))
                    st.markdown(response_text.replace("\n", "<br>"), unsafe_allow_html=True)
                else:
                    st.warning("no 'response' key found in backend response.")
            else:
                st.error(f"backend error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"request failed: {e}")
    else:
        st.warning("please enter a query to ask the agent.")