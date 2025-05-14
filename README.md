<h1>Job Description Analyzer</h1>

<div class="banner">
    <img src="placeholder_image.png" alt="App Screenshot Banner">
</div>

<p>
    The Job Description Analyzer is a Python Flask application designed to analyze job descriptions and compare them against candidate resumes or CVs. It extracts skills, categorizes them, and calculates a match percentage, highlighting matched and missing keywords. The frontend is built with React, TypeScript, and Tailwind CSS for a modern, responsive user interface.
</p>

<h2>Features</h2>
<ul>
    <li><strong>Skill Extraction:</strong> Extracts skills from job descriptions and resumes/CVs.</li>
    <li><strong>Skill Categorization:</strong> Categorizes extracted skills (e.g., programming, technical, soft, management).</li>
    <li><strong>Match Analysis:</strong> Calculates a match percentage.</li>
    <li><strong>Keyword Matching:</strong> Identifies matched and missing keywords.</li>
    <li><strong>Scoring and Match Level:</strong> Provides a match level (e.g., Poor, Fair, Good, Perfect).</li>
    <li><strong>Web API:</strong> Flask-based API.</li>
    <li><strong>Frontend:</strong> React-TypeScript User interface for interacting with the analyzer.</li>
    <li><strong>Feedback-Based Accuracy:</strong> Accepts feedback to improve skill matching accuracy.</li>
</ul>

<h2>Tech Stack</h2>
<ul>
    <li><strong>Frontend:</strong> React
        <ol>
            <li><strong>UI Library/Framework:</strong> React Bootstrap, Tailwind CSS</li>
            <li><strong>State Management:</strong> Redux</li>
            <li><strong>Other:</strong> framer-motion, lucide-react, React Icons</li>
            <li><strong>Deployment:</strong> Vercel</li>
        </ol>
    </li>
    <li><strong>Backend:</strong> Python
        <ol>
            <li><strong>Framework:</strong> Flask</li>
            <li><strong>NLP:</strong> NLTK</li>
            <li><strong>Other:</strong> re, logging</li>
            <li><strong>Deployment:</strong> Render</li>
        </ol>
    </li>
</ul>

<h2>Project Structure</h2>
<p>The project has a combined frontend and backend structure.</p>

<h3>Backend Folder Overview</h3>
<pre>
backend/
├── app.py                # Main Flask app
├── skills_extractor.py   # Skill extraction logic
├── skill_matcher.py      # Matching and scoring
├── feedback_handler.py   # NEW: Handles user feedback
├── utils.py              # Shared utility functions
</pre>

<h3>Frontend Overview</h3>
<ul>
    <li>React components and related files.</li>
    <li>Uses React Bootstrap and Tailwind CSS for styling.</li>
    <li>Uses React Scripts and Vite.</li>
</ul>

<h3>Key Backend Functions:</h3>
<ul>
    <li><code>preprocess_text(text)</code>: Cleans and tokenizes text.</li>
    <li><code>extract_skills(text)</code>: Extracts and categorizes skills.</li>
    <li><code>get_match_level(percentage)</code>: Assigns a match level.</li>
    <li><code>match_skills(job_skills, candidate_skills, weights)</code>: Calculates match scores.</li>
    <li><code>analyze_match(job_description, resume_text, cv_text, weights)</code>: Orchestrates analysis.</li>
    <li><code>analyze()</code>: Flask route for analysis requests.</li>
    <li><code>feedback()</code>: NEW Flask route to record user feedback for improved accuracy.</li>
</ul>

<h2>🔁 Feedback-Based Accuracy Improvement</h2>
<p>
A feedback system has been added to improve skill matching accuracy. It allows users to submit feedback on missing or mismatched skills. This feedback is logged and can be used to refine matching logic.
</p>

<h3>How It Works:</h3>
<ul>
    <li>New API endpoint: <code>/feedback</code></li>
    <li>Accepts job/resume text + user corrections</li>
    <li>Backend logs and stores this data for future analysis</li>
</ul>

<h4>Example POST /feedback Payload:</h4>
<pre>
{
  "job_description": "...",
  "resume_text": "...",
  "cv_text": "...",
  "user_feedback": {
    "Programming": ["JavaScript", "TypeScript"],
    "Database": ["MongoDB"]
  }
}
</pre>

<h4>Response:</h4>
<pre>
{
  "status": "success",
  "message": "Feedback recorded."
}
</pre>

<h2>Deployment</h2>
<p>
    The application is designed to be deployed with the frontend and backend handled separately.
</p>
<ul>
    <li>Backend: Deploy the Flask application to Render.</li>
    <li>Frontend: Deploy the React application to Vercel.</li>
</ul>

<h3>Render Deployment Steps (Backend)</h3>
<ol>
    <li><strong>Prepare Your Flask App:</strong><br>
        Ensure your Flask code is in a Git repository. Create <code>requirements.txt</code>:<br>
        <code>pip freeze > requirements.txt</code><br>
        Create a <code>Procfile</code>:<br>
        <code>web: gunicorn app:app</code>
    </li>
    <li><strong>Create a Render account:</strong> Sign up at <a href="https://render.com/">render.com</a>.</li>
    <li><strong>Connect your Git repository:</strong> Connect your project to Render.</li>
    <li><strong>Create a Web Service:</strong> Select your repo and deploy.</li>
    <li><strong>Configure:</strong><br>
        Build Command: <code>pip install -r requirements.txt</code><br>
        Start Command: <code>gunicorn app:app</code>
    </li>
    <li><strong>Deploy:</strong> Render will build and deploy the app.</li>
</ol>

<h3>Vercel Deployment Steps (Frontend)</h3>
<ol>
    <li><strong>Prepare Your React App:</strong> Ensure your code is in a Git repo.</li>
    <li><strong>Create a Vercel account:</strong> <a href="https://vercel.com/">vercel.com</a></li>
    <li><strong>Connect your repository:</strong> Select it in the dashboard.</li>
    <li><strong>Configure:</strong><br>
        Add an env variable like <code>REACT_APP_BACKEND_URL</code> pointing to your Render backend URL.
    </li>
    <li><strong>Deploy:</strong> Vercel will handle everything automatically.</li>
</ol>

<h2>Planned Improvements</h2>
<ul>
    <li>Integrate feedback to adapt future skill matching more accurately.</li>
    <li>Enhance to support PDF, DOCX, and multi-language files.</li>
</ul>
