

1. Introduction

The streamlit_app.py script is a self-contained web application built with Streamlit. It creates a user-friendly chat interface that connects to Google's Gemini API for generating AI responses and uses MongoDB to log the conversation history.

2. File Structure

The project relies on a few key files to function correctly:

streamlit_app.py: The main application script containing all the logic.

requirements.txt: Lists all the necessary Python libraries for the project.

.env: A local file (not uploaded to GitHub) that securely stores the API keys and database connection string.

3. Core Dependencies

streamlit: The main framework for building the web application's user interface.

requests: Used to make HTTP POST requests to the Gemini API endpoint.

pymongo: The official Python driver for interacting with the MongoDB database.

python-dotenv: Loads the environment variables from the .env file for local development.

certifi: Provides SSL certificates to ensure a secure connection to MongoDB, which is crucial for deployment.

4. Code Breakdown

The script is organized into several logical sections, from configuration to execution.

4.1. Initial Setup and Imports

import os
import requests
import streamlit as st
# ... other imports
from dotenv import load_dotenv

load_dotenv()


The script begins by importing all required libraries.

load_dotenv() is called immediately to load the GEMINI_API_KEY and MONGO_URI from your .env file into the environment.

4.2. Page and UI Configuration

st.set_page_config(...)
st.title("🤖 AI Customer Support Chatbot")
st.caption("Powered by Google's Gemini API & MongoDB")


st.set_page_config(): Sets the browser tab title, icon, and page layout.

st.title() and st.caption(): Display the main title and subtitle of the application.

4.3. Gemini API Configuration

SYSTEM_INSTRUCTION = """..."""
API_KEY = os.environ.get("GEMINI_API_KEY")
API_URL = f"..."


SYSTEM_INSTRUCTION: This multi-line string is a crucial prompt that defines the chatbot's persona, rules, and boundaries. It tells the Gemini model how to behave.

API Key Handling: The code first tries to get the GEMINI_API_KEY from Streamlit's secrets (for deployment) and falls back to environment variables (for local development). The app stops if the key is not found.

API_URL: The full URL endpoint for making requests to the Gemini model.

4.4. MongoDB Configuration

@st.cache_resource
def init_connection():
    # ...
    client = MongoClient(mongo_uri, tlsCAFile=certifi.where(), ...)
    return client

client = init_connection()


The @st.cache_resource decorator is very important. It tells Streamlit to run this function only once to establish the database connection and then reuse the same connection for all subsequent user sessions, which is highly efficient.

The function retrieves the MONGO_URI and connects to the database.

tlsCAFile=certifi.where() is the key fix for SSL handshake errors that often occur during deployment.

4.5. Database Helper Functions

The script includes several small functions to interact with the database:

get_db(): Returns the specific database instance (chatbot_db).

get_collection(): Returns the collection where logs are stored (chat_logs).

log_to_mongodb(): Inserts a new document containing the user's prompt, the bot's response, and a timestamp into the collection.

4.6. Chat History Management

if "messages" not in st.session_state:
    st.session_state.messages = [...]


st.session_state is a special Streamlit feature that acts like a memory for the application.

This code initializes a list called messages in the session state the very first time a user opens the app. This list stores the entire conversation history and persists between reruns.

4.7. Core Logic and User Input

This is the main interactive part of the app.

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input Handling ---
if prompt := st.chat_input("..."):
    # ...
    st.rerun()


Display Loop: The script first iterates through all messages currently stored in st.session_state.messages and displays them on the screen. This ensures the full conversation is always visible.

Input Handling: st.chat_input() creates the text input box at the bottom. When a user types a message and hits Enter:

The user's prompt is added to the st.session_state.messages list.

The get_gemini_response() function is called, sending the entire chat history to the API.

A "Thinking..." spinner is shown while waiting.

The AI's response is received and also added to the st.session_state.messages list.

The interaction is logged to MongoDB.

st.rerun() is called. This forces the entire script to run again from the top, which causes the "Display Loop" to redraw the screen with the new messages.

5. How to Customize

Change the Bot's Personality: The easiest way to customize the chatbot is by modifying the SYSTEM_INSTRUCTION string. You can change its name, its rules, and the context it's aware of.

Change the Database/Collection Name: You can easily change the names used in the get_db() and get_collection() functions if you prefer to use different ones.
