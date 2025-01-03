import openai
import streamlit as st
import random

st.title("Echo Bot")

# Initialize the OpenAI client with the API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# List of fallback responses
fallback_responses = [
    "Hi,how can i help you",
    "I'm sorry, I'm currently unable to respond. Please try again later.",
    "It seems I'm having trouble connecting to the server. Can I help you with something else?",
    "Apologies, but I'm not able to provide a response right now. Please try again in a bit.",
    "My connection to the server is down. How can I assist you otherwise?",
    "I'm currently facing technical difficulties. Please check back soon."
]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Generate assistant response using OpenAI API
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        # Extract the assistant's message from the response
        assistant_message = response["choices"][0]["message"]["content"]

    except Exception as e:
        # Use a fallback response if OpenAI API call fails
        assistant_message = random.choice(fallback_responses)
        st.error(f"An error occurred: {str(e)}")

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_message)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

