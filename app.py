import os
import streamlit as st
from dotenv import load_dotenv
from src.parsing import extract_text_from_pdf, read_text_file
from src.analysis import run_analysis
from src.ui_components import display_analysis_results

# --- Page Configuration ---
st.set_page_config(
    page_title="Innomatics Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# --- Load Environment Variables ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Google API Key not found. Please set it in your .env file.")
    st.stop()

# --- Constants ---
JD_FOLDER = "data/jds"
RESUME_FOLDER = "data/resumes"

# --- Helper Functions ---
def get_file_list(folder_path):
    try:
        return [f for f in os.listdir(folder_path)]
    except FileNotFoundError:
        st.error(f"Folder not found: {folder_path}")
        return []

# --- Main Application ---
st.title("AI-Powered Resume Relevance Checker 🚀")
st.markdown("Select a Job Description and a Resume to see the magic happen!")

# --- UI Selectors ---
jd_files = get_file_list(JD_FOLDER)
resume_files = get_file_list(RESUME_FOLDER)

if not jd_files or not resume_files:
    st.stop()

col1, col2 = st.columns(2)
with col1:
    selected_jd = st.selectbox("Step 1: Select Job Description", jd_files)
with col2:
    selected_resume = st.selectbox("Step 2: Select Resume", resume_files)

# --- Analysis Trigger ---
if st.button("Analyze Now", type="primary", use_container_width=True):
    if selected_jd and selected_resume:
        with st.spinner("Our AI is analyzing the documents... Please wait."):
            # Construct full file paths
            jd_path = os.path.join(JD_FOLDER, selected_jd)
            resume_path = os.path.join(RESUME_FOLDER, selected_resume)

            # Extract text content
            if jd_path.endswith('.pdf'):
                jd_text = extract_text_from_pdf(jd_path)
            else:
                jd_text = read_text_file(jd_path)
            
            resume_text = extract_text_from_pdf(resume_path)

            if jd_text and resume_text:
                # Run the core analysis
                analysis_results = run_analysis(resume_text, jd_text)
                
                if analysis_results:
                    # Display results using our component
                    display_analysis_results(analysis_results)
                else:
                    st.error("Analysis failed. Please check the logs or file contents.")
            else:
                st.error("Could not read text from one or both files.")