import streamlit as st
from rag import get_response

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.markdown( """ <style> .stMain { text-align: center; } </style> """, unsafe_allow_html=True)

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("namak.png", width=250)
st.title("NAMAK Medicine AI Assistant")
st.write("NAMAK Assistant can help you with your quaries!")



# Function to handle user input and generate response
def handle_input():
    user_input = st.session_state.user_input_input
    if user_input:
        # Append user message to chat history
        st.session_state['messages'].append({"user": user_input})
        
        # Get response from the chatbot
        response = get_response(user_input)
        
        # Append bot response to chat history
        st.session_state['messages'].append({"bot": response})
        
        # Clear the input field by resetting the session state variable
        st.session_state.user_input_input = ""



# Display chat history
for message in st.session_state['messages']:
    if "user" in message:
        st.markdown(f'<p style="color:red ;text-align: right;"><b><u>You:</u></b> {message["user"]}</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p style="color:white;text-align: left;"><b><u>Bot:</u></b> {message["bot"]}</p>', unsafe_allow_html=True)

# Chat input
st.text_input("You: ", key="user_input_input", on_change=handle_input)