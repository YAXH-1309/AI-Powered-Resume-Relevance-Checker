import re
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

@st.cache_data
def get_llm_response(resume_text, jd_text):
    """Uses an LLM to perform semantic analysis of the resume against the JD."""
    
    prompt = PromptTemplate(
        input_variables=["jd", "resume"],
        template="""
        You are an expert AI hiring assistant for a top tech company. Your task is to evaluate a candidate's resume against a job description with extreme accuracy.
        
        Analyze the provided JOB DESCRIPTION and RESUME TEXT, and generate a structured JSON-like response with the following keys:
        - "relevance_score": An integer score from 0 to 100.
        - "fit_verdict": A single-word verdict: "High", "Medium", or "Low".
        - "missing_elements": A Python list of strings detailing the top 3-5 crucial skills or experiences from the JD that are missing in the resume.
        - "feedback": A concise, encouraging paragraph for the student, suggesting specific improvements.
        - "summary": A one-sentence summary of the candidate's suitability.

        JOB DESCRIPTION:
        ---
        {jd}
        ---

        RESUME TEXT:
        ---
        {resume}
        ---

        Provide ONLY the structured JSON-like text as your response. Do not include any other explanatory text.
        Example Response Format:
        {{
            "relevance_score": 85,
            "fit_verdict": "High",
            "missing_elements": ["Experience with cloud cost optimization", "Terraform certification"],
            "feedback": "Your project experience with AWS is strong. To better align with this role, consider gaining hands-on experience with Terraform and exploring cloud cost management techniques.",
            "summary": "A strong candidate with relevant cloud experience, lacking specific DevOps tooling mentioned in the job description."
        }}
        """
    )

    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
        chain = prompt | llm | StrOutputParser()
        response_text = chain.invoke({"jd": jd_text, "resume": resume_text})
        return response_text
    except Exception as e:
        st.error(f"An error occurred with the AI model: {e}")
        return None

def parse_llm_response(response_text):
    """Parses the structured text response from the LLM into a dictionary."""
    try:
        # Use regex to find all key-value pairs, handling lists and nested quotes
        score = int(re.search(r'"relevance_score":\s*(\d+)', response_text).group(1))
        verdict = re.search(r'"fit_verdict":\s*"([^"]+)"', response_text).group(1)
        missing = eval(re.search(r'"missing_elements":\s*(\[.*?\])', response_text, re.DOTALL).group(1))
        feedback = re.search(r'"feedback":\s*"([^"]+)"', response_text).group(1)
        summary = re.search(r'"summary":\s*"([^"]+)"', response_text).group(1)

        return {
            "relevance_score": score,
            "fit_verdict": verdict,
            "missing_elements": missing,
            "feedback": feedback,
            "summary": summary
        }
    except Exception as e:
        st.warning("Could not fully parse the AI response. Displaying raw text.")
        return {"raw": response_text}

def run_analysis(resume_text, jd_text):
    """Orchestrates the full analysis process."""
    if not resume_text or not jd_text:
        return None
    
    llm_response_text = get_llm_response(resume_text, jd_text)
    
    if llm_response_text:
        parsed_results = parse_llm_response(llm_response_text)
        # You can add a 'hard_match' score here and weigh it if you want.
        # For an MVP, the LLM's score is powerful enough.
        return parsed_results
    return None