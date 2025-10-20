
import os
import requests
import streamlit as st
from pymongo import MongoClient, DESCENDING
from pymongo.server_api import ServerApi
from datetime import datetime
from dotenv import load_dotenv
import certifi  # Import the certifi library

# Load environment variables from .env file at the very beginning
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Customer Support Chatbot",
    page_icon="🤖",
    layout="centered",
)

# --- UI Setup ---
st.title("🤖 AI Customer Support Chatbot")
st.caption("Powered by Google's Gemini API & MongoDB")

# --- Gemini API Configuration ---
# System instruction to guide the chatbot's behavior
SYSTEM_INSTRUCTION = """
You are 'SupportBot', a friendly and professional AI customer support assistant.
Your primary goal is to provide clear, accurate, and helpful information to users.

**Instructions:**
- Always start with a warm and friendly greeting.
- Use formatting like bullet points (*) or bold text (**) to make your answers easy to read.
- If a user's question is vague, ask clarifying questions to better understand their needs before providing an answer.
- If you do not know the answer to a question, politely and honestly say "I'm sorry, I don't have the information on that. Please contact our human support team at support@example.com for more detailed assistance."
- Maintain a positive, patient, and professional tone throughout the conversation.
- Conclude your responses by asking if there is anything else you can help with.

**Boundaries:**
- Strictly avoid engaging in off-topic conversations, expressing personal opinions, or generating any unsafe or inappropriate content.
- Do not provide financial, legal, or medical advice under any circumstances.

**Context:**
- For your reference, the current date is Monday, October 20, 2025.
- You are assisting users primarily based in India.
"""

# Fetch Gemini API key from Streamlit secrets or environment variables
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("Gemini API key is not set. Please create a .env file or set Streamlit secrets.")
    st.stop()
    
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={API_KEY}"

# --- MongoDB Configuration ---
@st.cache_resource
def init_connection():
    """Initializes a connection to MongoDB."""
    mongo_uri = ""
    try:
        # First, try to get the URI from Streamlit's secrets
        mongo_uri = st.secrets["MONGO_URI"]
    except (KeyError, FileNotFoundError):
        # If not found, fall back to the environment variable from the .env file
        mongo_uri = os.environ.get("MONGO_URI")

    if not mongo_uri:
        st.warning("MONGO_URI not found. Chat logs will not be saved.")
        return None
        
    try:
        # Use certifi to provide the necessary SSL certificates for deployment
        client = MongoClient(mongo_uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {e}")
        return None

client = init_connection()

# --- Functions for DB Operations ---
def get_db():
    """Returns the database instance from the client."""
    if client:
        return client.chatbot_db # Database name is 'chatbot_db'
    return None

def get_collection(db):
    """Returns the chat_logs collection from the database."""
    if db is not None:
        return db.chat_logs # Collection name is 'chat_logs'
    return None

def log_to_mongodb(user_prompt, bot_response):
    """Logs a user-bot interaction to the MongoDB collection."""
    db = get_db()
    collection = get_collection(db)
    if collection is not None:
        try:
            collection.insert_one({
                "user_prompt": user_prompt,
                "bot_response": bot_response,
                "timestamp": datetime.utcnow()
            })
        except Exception as e:
            # Silently fail for the user, but log for the developer
            print(f"Could not log message to MongoDB: {e}")

def fetch_chat_logs():
    """Fetches the most recent chat logs from MongoDB."""
    db = get_db()
    collection = get_collection(db)
    if collection is not None:
        # Fetch the last 25 logs, sorted by most recent
        logs = collection.find().sort("timestamp", DESCENDING).limit(25)
        return list(logs)
    return []


# --- Chat History Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# --- Core Chat Logic ---
def get_gemini_response(user_prompt, chat_history):
    """
    Sends the user prompt and chat history to the Gemini API and gets a response.
    """
    # Format the conversation history for the API
    contents = []
    for message in chat_history:
        role = "user" if message["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": message["content"]}]})
    
    # Add the current user prompt
    contents.append({"role": "user", "parts": [{"text": user_prompt}]})

    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "generationConfig": { "temperature": 0.7, "topP": 0.9, "topK": 40, "maxOutputTokens": 2048 }
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            error_message = result.get('promptFeedback', {}).get('blockReason', 'Unknown reason')
            return f"I'm sorry, I couldn't generate a response. Reason: {error_message}"
            
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Error: {e}")
        return "Failed to communicate with the AI service. Please try again later."
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return "An internal server error occurred."

# --- Display Chat History ---
# This is the single source of truth for displaying messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- User Input Handling ---
if prompt := st.chat_input("What can I help you with?"):
    # 1. Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Get bot response
    # We display a spinner while waiting for the response
    with st.spinner("Thinking..."):
        response = get_gemini_response(prompt, st.session_state.messages)
        
        # 3. Add bot response to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

        # 4. Log the complete interaction to MongoDB
        log_to_mongodb(prompt, response)
    
    # 5. Rerun the script to display the new messages
    st.rerun()

