import openai
import os
import re
import json
from typing import Dict, List

class ResumeAnalyzer:
    """Analyzes resumes against job descriptions using AI."""
    
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.environ.get('OPENAI_API_KEY')
        if api_key:
            openai.api_key = api_key
            self.use_ai = True
        else:
            self.use_ai = False
            print("Warning: OpenAI API key not found. Using fallback analysis.")
    
    def analyze(self, resume_text: str, job_description: str) -> Dict:
        """Analyze resume against job description and return results."""
        
        if self.use_ai:
            return self._ai_analysis(resume_text, job_description)
        else:
            return self._fallback_analysis(resume_text, job_description)
    
    def _ai_analysis(self, resume_text: str, job_description: str) -> Dict:
        """Use OpenAI API for intelligent analysis."""
        try:
            prompt = f"""
            Analyze the following resume against the job description and provide a detailed assessment.
            
            JOB DESCRIPTION:
            {job_description}
            
            RESUME:
            {resume_text}
            
            Please provide your analysis in the following JSON format:
            {{
                "relevance_score": <score_out_of_100>,
                "summary": "<brief_summary_of_match>",
                "strengths": ["<strength1>", "<strength2>", "<strength3>"],
                "gaps": ["<gap1>", "<gap2>", "<gap3>"],
                "recommendations": ["<recommendation1>", "<recommendation2>", "<recommendation3>"],
                "key_skills_matched": ["<skill1>", "<skill2>", "<skill3>"],
                "missing_skills": ["<skill1>", "<skill2>", "<skill3>"]
            }}
            
            Focus on:
            1. Technical skills alignment
            2. Experience relevance
            3. Education requirements
            4. Soft skills match
            5. Overall fit
            
            Provide specific, actionable feedback.
            """
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert HR consultant and resume analyzer. Provide detailed, constructive feedback on resume-job fit."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            # Parse the AI response
            ai_response = response.choices[0].message.content.strip()
            
            # Extract JSON from the response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                
                # Validate and set defaults
                result.setdefault('relevance_score', 50)
                result.setdefault('summary', 'Analysis completed')
                result.setdefault('strengths', [])
                result.setdefault('gaps', [])
                result.setdefault('recommendations', [])
                result.setdefault('key_skills_matched', [])
                result.setdefault('missing_skills', [])
                
                return result
            else:
                # If JSON parsing fails, create a structured response from the text
                return self._parse_ai_text_response(ai_response)
                
        except Exception as e:
            print(f"AI analysis failed: {str(e)}")
            return self._fallback_analysis(resume_text, job_description)
    
    def _parse_ai_text_response(self, ai_response: str) -> Dict:
        """Parse AI response when JSON format fails."""
        # Simple parsing logic for when JSON format isn't followed
        score_match = re.search(r'(\d+)/100|(\d+)%|score.*?(\d+)', ai_response, re.IGNORECASE)
        score = 50  # default
        if score_match:
            for group in score_match.groups():
                if group:
                    score = min(100, max(0, int(group)))
                    break
        
        return {
            'relevance_score': score,
            'summary': 'AI analysis completed - see detailed feedback below',
            'strengths': ['Analysis completed using AI'],
            'gaps': ['Please check detailed feedback'],
            'recommendations': ['Review the full analysis for specific recommendations'],
            'key_skills_matched': [],
            'missing_skills': [],
            'full_ai_response': ai_response
        }
    
    def _fallback_analysis(self, resume_text: str, job_description: str) -> Dict:
        """Provide basic analysis when AI is not available."""
        
        # Simple keyword-based analysis
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()
        
        # Extract common technical skills and keywords
        tech_skills = [
            'python', 'javascript', 'java', 'react', 'angular', 'vue', 'node.js',
            'sql', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'docker',
            'kubernetes', 'git', 'html', 'css', 'machine learning', 'ai',
            'data science', 'analytics', 'project management', 'agile', 'scrum'
        ]
        
        # Find matching skills
        matching_skills = []
        missing_skills = []
        
        for skill in tech_skills:
            if skill in job_lower:
                if skill in resume_lower:
                    matching_skills.append(skill.title())
                else:
                    missing_skills.append(skill.title())
        
        # Calculate basic relevance score
        if len(matching_skills) + len(missing_skills) > 0:
            relevance_score = int((len(matching_skills) / (len(matching_skills) + len(missing_skills))) * 100)
        else:
            relevance_score = 60  # Default when no specific skills are detected
        
        # Adjust score based on text similarity
        common_words = set(resume_lower.split()) & set(job_lower.split())
        if len(common_words) > 10:
            relevance_score = min(100, relevance_score + 10)
        
        return {
            'relevance_score': relevance_score,
            'summary': f'Basic analysis shows {relevance_score}% relevance based on keyword matching',
            'strengths': matching_skills[:3] if matching_skills else ['Profile submitted for analysis'],
            'gaps': missing_skills[:3] if missing_skills else ['Consider adding more relevant keywords'],
            'recommendations': [
                'Add more specific technical skills mentioned in the job description',
                'Include quantifiable achievements and results',
                'Tailor your resume to match the job requirements more closely'
            ],
            'key_skills_matched': matching_skills,
            'missing_skills': missing_skills,
            'analysis_type': 'fallback'
        }