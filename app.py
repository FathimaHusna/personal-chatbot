import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import OpenAI
import os

# Load environment variables from .env file
load_dotenv()
# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to extract text from PDF
def load_resume(resume_path):
    text = ""
    with open(resume_path, "rb") as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()+ "\n"
    return text


# Load resume data
resume_text = load_resume("resume.pdf")

# Streamlit UI
st.set_page_config(page_title="AI Resume Chatbot")
st.title("🤖 AI Resume Chatbot")
st.markdown("Ask anything about my professional profile.")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask a question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    prompt = f"""
You are a professional resume assistant.

Rules:
- Answer ONLY from the resume
- Be clear and professional
- If not found, say "Not available in the resume"

Resume:
{resume_text}

Question:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)