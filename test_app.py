#!/usr/bin/env python3
"""
Simple test script to verify the application functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_processor import FileProcessor
from resume_analyzer import ResumeAnalyzer

def test_file_processor():
    """Test file processing functionality"""
    print("Testing File Processor...")
    
    processor = FileProcessor()
    
    # Test with a simple text content
    test_file_path = '/tmp/test_resume.txt'
    test_content = """
    John Doe
    Software Engineer
    
    Skills: Python, JavaScript, React, SQL
    Experience: 5 years in web development
    Education: Computer Science degree
    """
    
    # Create test file
    with open(test_file_path, 'w') as f:
        f.write(test_content)
    
    try:
        extracted_text = processor.extract_text(test_file_path)
        print(f"✅ Text extraction successful: {len(extracted_text)} characters")
        return True
    except Exception as e:
        print(f"❌ Text extraction failed: {e}")
        return False
    finally:
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_resume_analyzer():
    """Test resume analysis functionality"""
    print("\nTesting Resume Analyzer...")
    
    analyzer = ResumeAnalyzer()
    
    test_resume = """
    John Doe
    Software Engineer
    
    Skills: Python, JavaScript, React, SQL, Git
    Experience: 5 years in web development and data analysis
    Education: Bachelor's in Computer Science
    """
    
    test_job_description = """
    We are looking for a Senior Software Engineer with experience in:
    - Python programming
    - Web development frameworks
    - Database management (SQL)
    - Version control (Git)
    - React.js for frontend development
    
    Requirements:
    - 3+ years of experience
    - Computer Science degree preferred
    """
    
    try:
        result = analyzer.analyze(test_resume, test_job_description)
        
        print(f"✅ Analysis completed successfully")
        print(f"   Relevance Score: {result.get('relevance_score', 'N/A')}%")
        print(f"   Strengths: {len(result.get('strengths', []))} items")
        print(f"   Recommendations: {len(result.get('recommendations', []))} items")
        print(f"   Analysis Type: {result.get('analysis_type', 'AI' if analyzer.use_ai else 'fallback')}")
        
        return True
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def test_app_imports():
    """Test that the main app can be imported"""
    print("\nTesting App Imports...")
    
    try:
        import app
        print("✅ Main app imports successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running AI-Powered Resume Relevance Checker Tests\n")
    
    tests = [
        test_file_processor,
        test_resume_analyzer,
        test_app_imports
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📊 Test Results:")
    print(f"   Passed: {sum(results)}/{len(results)}")
    print(f"   Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\n🎉 All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. (Optional) Set up .env file with OpenAI API key")
        print("   3. Run: python app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)