import streamlit as st
import tempfile
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY not set in .env file.")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.0-flash") # or other supported model

def summarize_text(text):
    response = model.generate_content(f"Summarize the following text:\n\n{text}")
    return response.text.strip()

def summarize_combined_pdfs(pdfs_folder):
    combined_text = ""
    for pdf_file in pdfs_folder:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(pdf_file.read())

        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        combined_text += "\n".join([doc.page_content for doc in docs])
        os.remove(temp_path)

    # Generate summary with Gemini
    return summarize_text(combined_text)

# Streamlit UI
st.title("Combined PDF Summarizer (Gemini)")

pdf_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if pdf_files:
    if st.button("Generate Summary"):
        st.write("Combined summary:")
        combined_summary = summarize_combined_pdfs(pdf_files)
        st.write(combined_summary)