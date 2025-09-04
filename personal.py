# First, we get the special tools we need from their boxes.
import streamlit as st # This tool helps us make a simple website for our chatbot.
from transformers import pipeline # This tool helps us use the big AI brain.

# This is like giving our chatbot a special name and showing a picture.
st.title("My Fun Money Friend! 💰")
st.image("https://i.imgur.com/gK9x86U.png", width=150) # You can replace this with your own piggy bank image.

# This tells the computer to remember the AI brain so it doesn't have to think hard every time.
# We call our AI brain "pipe".
@st.cache_resource
def load_ai_brain():
    # We tell the brain what it's for (making text) and which brain to use (IBM's Granite).
    ai_pipe = pipeline("text-generation", model="gpt2"),
    return ai_pipe

# We get our AI brain ready.
ai_brain = load_ai_brain()

# This is like a special diary for our chatbot to remember what we talked about.
if "messages" not in st.session_state:
    st.session_state.messages = []

# We show all the old pages from our diary on the screen.
for chat_message in st.session_state.messages:
    with st.chat_message(chat_message["role"]):
        st.markdown(chat_message["content"])

# This is a little box where the user can type their question.
user_question = st.chat_input("Ask me a question about money!")

# If the user types something, we do the magic!
if user_question:
    # We show the user's question on the screen.
    with st.chat_message("user"):
        st.markdown(user_question)
    
    # We write the user's question in our diary.
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Now we ask our AI brain to think and give us an answer.
    # We give it a little nudge to make sure the answer is not too long.
    ai_response = ai_brain(user_question, max_length=150)[0]["generated_text"]
    
    # We show the AI's answer on the screen.
    with st.chat_message("assistant"):
        st.markdown(ai_response)
        
    # We write the AI's answer in our diary.
    st.session_state.messages.append({"role": "assistant", "content": ai_response})