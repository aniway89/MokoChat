from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
import json

# Configure Generative AI
genai.configure(api_key=os.getenv("API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def load_chat_history(filename="chat_history.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                data = file.read().strip()  # Read and strip any leading/trailing whitespace
                if not data:
                    return []  # If the file is empty, return an empty list
                return json.loads(data)  # Use json.loads instead of json.load to handle the string directly
            except json.JSONDecodeError:
                # If there is an error decoding JSON, return an empty list
                return []
    return []  # If the file doesn't exist, return an empty list

def save_chat_history(history, filename="chat_history.json"):
    with open(filename, "w") as file:
        json.dump(history, file, indent=4)  # Pretty-print JSON for better readability

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = load_chat_history()

# Input box for user query
input_query = st.text_area("Input your question:", key="input_query")

# Enter button to submit the query
if st.button("Enter"):
    if input_query:
        response = get_gemini_response(input_query)
        response_text = ""
        for chunk in response:
            response_text += chunk.text
        # Display the response in a text area for better readability
        st.text_area("The Response is", response_text, height=200)

        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input_query))
        st.session_state['chat_history'].append(("Bot", response_text))
        # Save the updated chat history to file
        save_chat_history(st.session_state['chat_history'])

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
