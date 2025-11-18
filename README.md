📄 README.md — Eliza Support Bot (Gemini 2.5 Flash Integrated)
💬 Overview

Eliza is an AI-powered customer support chatbot built using Streamlit and Google Gemini 2.5 Flash.
This tool helps simulate real-time chat support with modern UI, dark mode, canned responses, and message history.

🚀 Features

✔ Google Gemini 2.5 Flash integration

✔ Live chat interface

✔ Dark/Light mode toggle

✔ Canned responses for quick replies

✔ Auto-clear message box after sending

✔ Retry logic for Gemini API errors

✔ Clean user + bot bubble UI

✔ Scrollable chat history

📦 Requirements
1. Install Python

Python version required: 3.9 – 3.12

Download: https://www.python.org/downloads/

📁 Project Structure
project-folder/
│
├── app.py
├── .env
├── requirements.txt
└── static/
      └── logo.png     (optional)

🛠 Install Dependencies

Make a virtual environment (optional but recommended):

python -m venv venv


Activate:

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate


Install all required libraries:

pip install -r requirements.txt

📌 requirements.txt should include:
streamlit
python-dotenv
google-genai

🔑 Setup Google Gemini API Key

Go to:
https://aistudio.google.com/app/apikey

Create a new API key

Create a .env file in the project root:

GOOGLE_API_KEY=YOUR_API_KEY_HERE

▶ How to Run the App

Run Streamlit:

streamlit run app.py


The app will open in your browser automatically:

http://localhost:8501

💡 How to Use the Support Bot
1️⃣ Set a system prompt

This tells Eliza how to respond (support tone, agent rules, etc.)

2️⃣ Toggle Dark Mode (optional)

Makes UI dark/light instantly.

3️⃣ Use canned responses

Sidebar me predefined quick replies milti hain.

4️⃣ Type your message in the message box

Press Send, bot will reply.

5️⃣ Message box auto-clears

Next message type karne ke liye input box empty rahega.

⚙️ Troubleshooting
❌ API Key Not Working

Check .env file spelling

Regenerate API key from Google AI Studio

Restart the Streamlit app

📬 Support / Contact

If you want help improving this chatbot or adding new features (voice input, multi-agent mode, database logging), feel free to reach out.
