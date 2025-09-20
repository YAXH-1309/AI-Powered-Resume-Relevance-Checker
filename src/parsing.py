import fitz  # PyMuPDF
import streamlit as st

@st.cache_data
def extract_text_from_pdf(file_path):
    """Extracts text from a given PDF file path."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

@st.cache_data
def read_text_file(file_path):
    """Reads text from a given text file path."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading text file: {e}")
        return None