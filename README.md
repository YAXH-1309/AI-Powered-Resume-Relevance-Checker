# AI-Powered Resume Relevance Checker

An intelligent web application built for the Code4Edtech hackathon that analyzes resumes against job descriptions to generate relevance scores and provide actionable feedback.

## ✨ Features

- **Smart Resume Analysis**: Upload resumes in PDF, DOCX, or TXT format
- **AI-Powered Matching**: Uses OpenAI GPT for intelligent analysis (with fallback keyword matching)
- **Relevance Scoring**: Get a percentage score showing how well your resume matches the job
- **Detailed Feedback**: Receive specific strengths, gaps, and improvement recommendations
- **Skills Analysis**: See which skills match and which are missing
- **Modern Web Interface**: Clean, responsive design with drag-and-drop file upload
- **Real-time Processing**: Fast analysis with loading indicators and error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YAXH-1309/AI-Powered-Resume-Relevance-Checker.git
   cd AI-Powered-Resume-Relevance-Checker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key for enhanced AI analysis
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Key (optional - app works without it using fallback analysis)
OPENAI_API_KEY=your_openai_api_key_here

# Flask Configuration
SECRET_KEY=your_secret_key_for_production
FLASK_DEBUG=True
FLASK_ENV=development
```

**Note**: The application works perfectly without an OpenAI API key, using intelligent keyword-based analysis as a fallback.

## 💡 How It Works

1. **Upload Resume**: Drag and drop or browse to select your resume file
2. **Paste Job Description**: Copy the job posting into the text area
3. **AI Analysis**: The system analyzes the match using either AI or keyword matching
4. **Get Results**: Receive a detailed breakdown including:
   - Relevance percentage score
   - Key strengths identified
   - Areas for improvement
   - Specific recommendations
   - Skills matched vs missing

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **AI Integration**: OpenAI GPT API
- **File Processing**: PyPDF2, python-docx
- **Styling**: Custom CSS with modern design patterns

## 📁 Project Structure

```
AI-Powered-Resume-Relevance-Checker/
├── app.py                 # Main Flask application
├── resume_analyzer.py     # Core analysis logic
├── file_processor.py      # File handling and text extraction
├── requirements.txt       # Python dependencies
├── test_app.py           # Test suite
├── templates/            # HTML templates
│   ├── index.html        # Main page
│   ├── 404.html          # Error page
│   └── 500.html          # Server error page
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Stylesheets
│   └── js/
│       └── script.js     # JavaScript functionality
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🧪 Testing

Run the test suite to verify functionality:

```bash
python test_app.py
```

The tests verify:
- File processing for different formats
- Resume analysis functionality
- Application imports and basic functionality

## 🎯 API Endpoints

- `GET /` - Main application page
- `POST /analyze` - Submit resume and job description for analysis
- Returns JSON with analysis results including score, feedback, and recommendations

## 📱 Browser Support

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## 🚀 Deployment

For production deployment:

1. Set `FLASK_ENV=production` in your environment
2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```
3. Configure reverse proxy (nginx/Apache)
4. Set up SSL certificate

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Hackathon Project

Built for the Code4Edtech hackathon to help job seekers optimize their resumes using AI technology.

## 🔗 Links

- [GitHub Repository](https://github.com/YAXH-1309/AI-Powered-Resume-Relevance-Checker)
- [Demo](http://localhost:5000) (when running locally)

## 📞 Support

For questions or issues, please open an issue on GitHub or contact the maintainer.
