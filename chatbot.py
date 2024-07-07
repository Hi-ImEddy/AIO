import streamlit as st # type: ignore
from hugchat import hugchat # type: ignore
from hugchat.login import Login # type: ignore


def generate_response(prompt_input, hf_email, hf_password):
    # Login to Hugging Face
    sign = Login(hf_email, hf_password)  # Create a Login object with provided email and password
    cookies = sign.login()  # Perform login and obtain cookies

    # Create Chatbot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # Initialize ChatBot with cookies
    return chatbot.chat(prompt_input)  # Generate and return the chatbot's response


def main():
    # App title
    st.title("Simple Chatbot")  # Set the title of the Streamlit app

    # Login UI
    # Hugging Face credentials
    with st.sidebar:  # Create a sidebar for user login
        st.title("Login HugChat")  # Sidebar title
        hf_email = st.text_input("Enter Email:")  # Input field for email
        hf_password = st.text_input("Enter password:", type="password")  # Input field for password
        if not (hf_email and hf_password):  # Check if both email and password are entered
            st.warning("Please enter your email and password")  # Show warning if not entered
        else:
            st.success("Proceed to simple chatbot")  # Show success message if entered

    # Simple Chatbot UI
    # Store LLM response in session
    if "messages" not in st.session_state.keys():  # Check if 'messages' key is in session state
        st.session_state.messages = [{  # Initialize 'messages' in session state
            "role": "assistant",
            "content": "May I help you?"
        }]

    # Display chat messages
    for message in st.session_state.messages:  # Loop through all messages in session state
        with st.chat_message(message["role"]):  # Display each message based on its role
            st.write(message["content"])  # Write the message content

    # User-provided prompt
    if user_prompt := st.chat_input(disabled=not (hf_email and hf_password)):  # Input field for user's chat prompt
        st.session_state.messages.append({  # Append user's message to session state
            "role": "user",
            "content": user_prompt
        })
        with st.chat_message("user"):  # Display user's message
            st.write(user_prompt)

    # Generate new response if last response wasn't from "role": "assistant"
    if st.session_state.messages[-1]["role"] != "assistant":  # Check if the last message is not

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(
                    user_prompt, hf_email, hf_password)
                st.write(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })


if __name__ == '__main__':
    main()
