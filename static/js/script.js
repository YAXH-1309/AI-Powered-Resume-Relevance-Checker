document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analysis-form');
    const fileInput = document.getElementById('resume');
    const filePlaceholder = document.querySelector('.file-placeholder');
    const analyzeBtn = document.getElementById('analyze-btn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    const resultsSection = document.getElementById('results-section');
    const errorMessage = document.getElementById('error-message');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');

    // File input handling
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const fileName = this.files[0].name;
            filePlaceholder.textContent = fileName;
            filePlaceholder.style.color = '#333';
        } else {
            filePlaceholder.textContent = 'Choose a file (PDF, DOCX, or TXT)';
            filePlaceholder.style.color = '#666';
        }
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Hide any previous results or errors
        hideResults();
        hideError();
        
        // Show loading state
        showLoading();
        
        try {
            const formData = new FormData(form);
            
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayResults(data);
            } else {
                showError(data.error || 'An error occurred during analysis');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            hideLoading();
        }
    });

    // New analysis button
    newAnalysisBtn.addEventListener('click', function() {
        hideResults();
        hideError();
        form.reset();
        filePlaceholder.textContent = 'Choose a file (PDF, DOCX, or TXT)';
        filePlaceholder.style.color = '#666';
        document.querySelector('.upload-section').scrollIntoView({ behavior: 'smooth' });
    });

    function showLoading() {
        analyzeBtn.disabled = true;
        btnText.style.display = 'none';
        loader.style.display = 'inline-block';
    }

    function hideLoading() {
        analyzeBtn.disabled = false;
        btnText.style.display = 'inline';
        loader.style.display = 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth' });
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }

    function hideResults() {
        resultsSection.style.display = 'none';
    }

    function displayResults(data) {
        // Update score with animation
        const scoreValue = document.getElementById('score-value');
        animateScore(scoreValue, data.relevance_score || 0);
        
        // Update score circle color based on score
        const scoreCircle = document.querySelector('.score-circle');
        updateScoreColor(scoreCircle, data.relevance_score || 0);
        
        // Update summary
        document.getElementById('summary').textContent = data.summary || 'Analysis completed';
        
        // Update strengths
        updateList('strengths-list', data.strengths || []);
        
        // Update gaps
        updateList('gaps-list', data.gaps || []);
        
        // Update recommendations
        updateList('recommendations-list', data.recommendations || []);
        
        // Update matched skills
        updateSkills('matched-skills', data.key_skills_matched || []);
        
        // Update missing skills
        updateSkills('missing-skills', data.missing_skills || []);
        
        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function animateScore(element, targetScore) {
        let currentScore = 0;
        const increment = targetScore / 50; // Animation duration control
        
        const timer = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(timer);
            }
            element.textContent = Math.round(currentScore);
        }, 20);
    }

    function updateScoreColor(element, score) {
        // Remove existing color classes
        element.classList.remove('score-low', 'score-medium', 'score-high');
        
        // Add appropriate color class based on score
        if (score < 50) {
            element.style.background = 'linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%)';
        } else if (score < 75) {
            element.style.background = 'linear-gradient(135deg, #feca57 0%, #ff9ff3 100%)';
        } else {
            element.style.background = 'linear-gradient(135deg, #48dbfb 0%, #0abde3 100%)';
        }
    }

    function updateList(elementId, items) {
        const list = document.getElementById(elementId);
        list.innerHTML = '';
        
        if (items.length === 0) {
            const li = document.createElement('li');
            li.textContent = 'No specific items identified';
            li.style.fontStyle = 'italic';
            li.style.color = '#888';
            list.appendChild(li);
            return;
        }
        
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            list.appendChild(li);
        });
    }

    function updateSkills(elementId, skills) {
        const container = document.getElementById(elementId);
        container.innerHTML = '';
        
        if (skills.length === 0) {
            const span = document.createElement('span');
            span.textContent = 'None identified';
            span.style.fontStyle = 'italic';
            span.style.color = '#888';
            container.appendChild(span);
            return;
        }
        
        skills.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'skill-tag';
            span.textContent = skill;
            container.appendChild(span);
        });
    }

    // File drag and drop functionality
    const fileInputWrapper = document.querySelector('.file-input-display');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileInputWrapper.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        fileInputWrapper.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        fileInputWrapper.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight(e) {
        fileInputWrapper.style.borderColor = '#667eea';
        fileInputWrapper.style.background = '#f0f4ff';
    }
    
    function unhighlight(e) {
        fileInputWrapper.style.borderColor = '#ddd';
        fileInputWrapper.style.background = '#fafafa';
    }
    
    fileInputWrapper.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            fileInput.files = files;
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }
});