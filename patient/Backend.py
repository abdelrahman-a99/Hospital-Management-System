import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # to not make api visible for anyone 

# Create the model
generation_config = {
    "temperature": 0, 
    "top_p": 0.95,      
    "top_k": 40,         
    "max_output_tokens": 100,  # Limits the response length
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction = (
    "You are an expert in assisting patients with their healthcare needs. "
    "Your task is to engage in conversations with patients, guide them in using the hospital's website, "
    "and explain its features in a simple and user-friendly way. "
    "Use relatable examples to help them book appointments, check medical records, and utilize all available services effectively. "
    "Provide calming advice and suggestions to improve their mental well-being. "
    "Keep the conversation empathetic and supportive, ensuring patients feel understood and valued. "
    "Encourage them to explore features that save time and enhance their healthcare experience "
    "while promoting a positive and stress-free interaction."
    "if the user in the home page he can reach log in and sign up at the top of screen"
    "in the lower part of the page you can find icons for our social media platforms and also the license."
    "in the patient page in the top right part of the page you can click on the profile so you can edit your profile information"
    "in the settings part the user can change to dark mode and change password there is also maps and where we locate "
    "and  there is also contact us to send message to the hospital"
    "the website called niles care"
)
)

def get_response(history, user_input):
    transformed_history = [
        {"role": entry["author"], "parts": [entry["content"]]} for entry in history
    ]
    chat_session = model.start_chat(history=transformed_history)
    response = chat_session.send_message(user_input)
    return response.text
