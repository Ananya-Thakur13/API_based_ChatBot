import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# Ensure API key is available
# your .env file should have this content :- GOOGLE_API_KEY= XXXX........... (your api key here)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY is missing. Check your .env file.") # Create .env and paste your own API_KEY, i have not pasted mine here, 
    st.stop()

# Initialize Google Gemini Model
model = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

# Streamlit UI 
st.title("🤖 Chatbot with Gemini API") # you can change style by changing config.toml file
st.markdown("A simple chatbot interface using **Google Gemini AI** and Streamlit.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = model.invoke([HumanMessage(user_input)])
        bot_reply = response.content

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        with st.chat_message("assistant"):
            st.markdown(bot_reply)
    
    except Exception as e:
        st.error(f"Error: {e}")
