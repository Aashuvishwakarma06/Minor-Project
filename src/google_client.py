# google_client.py
from google import genai
import os

# Get your API key from environment variable or directly paste (not recommended for public)
API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

def chat_with_model(messages, model="gemini-1.5-flash"):
    """
    Replaces OpenAI chat completion with Google Gemini model
    """

    # Extract user + system messages
    conversation = []
    for m in messages:
        role = m.get("role")
        content = m.get("content")
        if role == "system":
            conversation.append(f"System: {content}")
        elif role == "user":
            conversation.append(f"User: {content}")
        elif role == "assistant":
            conversation.append(f"Assistant: {content}")

    # Join all previous messages
    prompt = "\n".join(conversation)

    # Generate response
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text.strip()
