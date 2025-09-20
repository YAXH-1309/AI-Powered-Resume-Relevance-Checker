# AI-Powered Resume Relevance Checker 🚀

[](https://ai-powered-resume-relevance-checker-hxu7qsunemxa5ckaiak7sr.streamlit.app/)

This project is a submission for the **Code4Edtech Challenge by Innomatics Research Labs**. It's an AI-powered web application designed to automate the time-consuming process of resume screening, providing instant, actionable insights for both recruiters and students.

## Live Demo

You can access the live, deployed application here:
**[https://ai-powered-resume-relevance-checker-hxu7qsunemxa5ckaiak7sr.streamlit.app/](https://ai-powered-resume-relevance-checker-hxu7qsunemxa5ckaiak7sr.streamlit.app/)**

## 🎥 Presentation Video

https://youtu.be/aCuio5EWeZ0?si=O4P7o7x1q3B4eoCi

## ✨ Key Features

  * **Automated Scoring**: Generates a relevance score from 0-100 by semantically comparing a resume against a job description.
  * **Instant Verdict**: Provides a clear "High," "Medium," or "Low" fit verdict to help recruiters prioritize candidates.
  * **Gap Analysis**: Highlights crucial skills, technologies, or experiences mentioned in the job description that are missing from the resume.
  * **Personalized Feedback**: Offers constructive, AI-generated feedback to help students improve their resumes for future opportunities.
  * **Interactive UI**: A simple and intuitive web interface built with Streamlit.

## 🛠️ Tech Stack

  * **Language**: Python
  * **Web Framework**: Streamlit
  * **AI/LLM Orchestration**: LangChain (or Direct SDK)
  * **Core AI Model**: Google Gemini Pro
  * **File Parsing**: PyMuPDF

## 🚀 How to Run Locally

To set up and run this project on your own machine, follow these steps:

**1. Clone the Repository**

```bash
git clone https://github.com/your-username/AI-Powered-Resume-Relevance-Checker.git
cd AI-Powered-Resume-Relevance-Checker
```

**2. Create and Activate a Virtual Environment**

```bash
# Create the environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Set Up Environment Variables**

  * Create a file named `.env` in the root of the project folder.
  * Add your Google Gemini API key to this file:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

**5. Run the Streamlit App**

```bash
streamlit run app.py
```
