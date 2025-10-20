🤖 AI Customer Support Chatbot

A modern, intelligent chatbot designed for customer support, powered by Google's Gemini API and built with Streamlit. This application logs conversations to a MongoDB database and is ready for deployment.

✨ Features

Intelligent & Contextual Responses: Leverages the power of Google's Gemini API for human-like and helpful answers.

Conversation Logging: All user interactions are automatically logged to a MongoDB database for review, analysis, and service improvement.

Easy-to-Use Interface: Built with Streamlit for a clean, simple, and intuitive user experience.

Customizable Persona: The chatbot's personality, rules, and knowledge base can be easily configured through a central system instruction prompt.

Deployment Ready: Comes with all necessary configurations for a seamless deployment on cloud platforms like Render.

🛠️ Tech Stack

Frontend: Streamlit

Backend: Python/Flask

AI Model: Google Gemini API

Database: MongoDB Atlas

Deployment: Render

🚀 Getting Started

To get a local copy up and running, please follow these simple steps.

Prerequisites

Python 3.8 or higher

A Google Gemini API Key

A MongoDB Atlas account and a connection string

Installation & Setup

Clone the Repository

git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name


Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate


Install Dependencies
Install all the required Python libraries using the requirements.txt file.

pip install -r requirements.txt


Set Up Environment Variables
The application requires API keys for both Gemini and MongoDB.

Create a new file in the root of your project named .env.

Replace the placeholder values with your actual credentials.

.env file:

# Your Google Gemini API Key
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

# Your MongoDB Atlas Connection String
MONGO_URI="YOUR_MONGODB_CONNECTION_STRING_HERE"


▶️ Running the Application

Once the setup is complete, you can start the Streamlit application with the following command:

streamlit run streamlit_app.py


The application will open in your default web browser at http://localhost:8501.

☁️ Deployment

This application is ready to be deployed on Render.

Push your project to a GitHub repository.

On the Render dashboard, create a new Web Service and connect it to your repository.

Use the following settings during configuration:

Environment: Python 3

Build Command: pip install -r requirements.txt

Start Command: streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0

In the Advanced > Environment Variables section, add your GEMINI_API_KEY and MONGO_URI as secrets.

Deploy the service.

Important: Remember to update your MongoDB Atlas Network Access list to allow connections from anywhere (0.0.0.0/0) for the deployed app to connect successfully.

📄 License

This project is distributed under the MIT License. See LICENSE for more information.
