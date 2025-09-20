from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# Import our custom modules
from resume_analyzer import ResumeAnalyzer
from file_processor import FileProcessor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
resume_analyzer = ResumeAnalyzer()
file_processor = FileProcessor()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        # Check if file was uploaded
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file uploaded'}), 400
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '').strip()
        
        # Validate inputs
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT files only.'}), 400
        
        # Process the uploaded file
        filename = secure_filename(file.filename)
        
        # Create a temporary file to process
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{filename.rsplit('.', 1)[1].lower()}") as temp_file:
            file.save(temp_file.name)
            
            # Extract text from resume
            resume_text = file_processor.extract_text(temp_file.name)
            
            # Clean up temporary file
            os.unlink(temp_file.name)
        
        if not resume_text.strip():
            return jsonify({'error': 'Could not extract text from the resume. Please ensure the file is not corrupted.'}), 400
        
        # Analyze resume against job description
        analysis_result = resume_analyzer.analyze(resume_text, job_description)
        
        return jsonify(analysis_result)
        
    except Exception as e:
        app.logger.error(f"Error analyzing resume: {str(e)}")
        return jsonify({'error': 'An error occurred while analyzing the resume. Please try again.'}), 500

@app.errorhandler(413)
def file_too_large(error):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)