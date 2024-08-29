import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_response(question):
    response = chat.send_message(question, stream=True)
    return response


st.title("Q/A App")
st.header("Gemini Chat Bot")


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


user_input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")


if submit and user_input:
    response = get_response(user_input)
    st.session_state['chat_history'].append(("You", user_input))
    st.subheader("Response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))


st.subheader("Chat History:")
for role, text in st.session_state["chat_history"]:
    st.write(f"{role}: {text}")
