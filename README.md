<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Description Analyzer</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 960px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1a5296; /* Darker blue */
            text-align: center;
            border-bottom: 2px solid #b0c4de;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        h2 {
            color: #4169e1; /* Royal Blue */
            margin-top: 30px;
            margin-bottom: 10px;
            border-bottom: 1px solid #b0c4de;
            padding-bottom: 5px;
        }
        p {
            margin-bottom: 15px;
        }
        ul, ol {
            margin-bottom: 15px;
        }
        ul {
            list-style-type: disc;
            padding-left: 20px;
        }
        ol {
            list-style-type: decimal;
            padding-left: 20px;
        }

        /* Banner Image  */
        .banner {
            width: 100%;
            height: 200px; /* Adjust as needed */
            background-color: #b0c4de; /* Light Steel Blue, placeholder */
            <!-- border-radius: 8px; -->
            margin-bottom: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
            background-size: cover;  /* Ensure image covers the area */
            background-position: center; /* Center the image */
        }
        .banner img{
           max-width: 100%; /* Make sure image doesn't exceed container width */
           max-height: 100%;
           border-radius: 8px;
        }

        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4169e1;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 10px;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #1a5296;
        }

        .highlight {
            background-color: #f0e68c; /* Khaki */
            padding: 2px 5px;
            border-radius: 3px;
            font-weight: bold;
        }

         /* Code Blocks  */
        pre {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            margin-bottom: 15px;
            font-family: monospace;
            font-size: 14px;
            line-height: 1.4;
        }
        code {
            font-family: monospace;
            font-size: 14px;
        }

    </style>
</head>
<body>
    <div class="container">
        <div class="banner">
           <img src="placeholder_image.png" alt="App Screenshot Banner">
        </div>
        <h1>Job Description Analyzer</h1>
        <p>
            The Job Description Analyzer is a Python Flask application designed to analyze job descriptions and compare them against candidate resumes or CVs.
            It extracts skills, categorizes them, and calculates a match percentage, highlighting matched and missing keywords.
        </p>

        <h2>Features</h2>
        <ul>
            <li><strong>Skill Extraction:</strong> Extracts skills from job descriptions and resumes/CVs.</li>
            <li><strong>Skill Categorization:</strong> Categorizes extracted skills (e.g., programming, technical, soft, management).</li>
            <li><strong>Match Analysis:</strong> Calculates a match percentage.</li>
             <li><strong>Keyword Matching:</strong> Identifies matched and missing keywords.</li>
            <li><strong>Scoring and Match Level:</strong> Provides a match level (e.g., Poor, Fair, Good, Perfect).</li>
            <li><strong>Web API:</strong> Flask-based API.</li>
        </ul>

        <h2>Tech Stack</h2>
        <ul>
            <li><strong>Backend:</strong> Python</li>
            <li><strong>Framework:</strong> Flask</li>
            <li><strong>NLP:</strong> NLTK</li>
            <li><strong>Other:</strong> re, logging</li>
            <li><strong>Deployment:</strong> Render</li>
        </ul>

        <h2>Project Structure</h2>
         <p>
            The core application logic is within <code>app.py</code>. Key functions:
        </p>
        <ul>
            <li><code>preprocess_text(text)</code>: Cleans and tokenizes text.</li>
            <li><code>extract_skills(text)</code>: Extracts and categorizes skills.</li>
            <li><code>get_match_level(percentage)</code>: Assigns a match level.</li>
            <li><code>match_skills(job_skills, candidate_skills, weights)</code>: Calculates match scores.</li>
            <li><code>analyze_match(job_description, resume_text, cv_text, weights)</code>: Orchestrates analysis.</li>
            <li><code>analyze()</code>: Flask route for analysis requests.</li>
        </ul>

        <h2>Deployment</h2>
        <p>
            The application is deployed on Render.
        </p>
        <h3>Render Deployment Steps</h3>
        <ol>
            <li><strong>Prepare Your Flask App:</strong><br>
                Ensure your Flask code is in a Git repository.  Create <code>requirements.txt</code>:<br>
                <pre><code>pip freeze > requirements.txt</code></pre>
                 Create a <code>Procfile</code>:<br>
                <pre><code>web: gunicorn app:app</code></pre>
            </li>
            <li><strong>Create a Render account:</strong> Sign up at <a href="https://render.com/">render.com</a>.</li>
            <li><strong>Connect your Git repository:</strong> Connect your project's Git repository to Render.</li>
            <li><strong>Create a Web Service:</strong> On Render, create a new "Web Service" and select your repository.</li>
            <li><strong>Configure:</strong><br>
                Environment: Choose a Python version.<br>
                Build Command: <code>pip install -r requirements.txt</code><br>
                Start Command: <code>gunicorn app:app</code><br>
                Region: Select a region.
            </li>
            <li><strong>Deploy:</strong> Render will build and deploy your Flask application.</li>
        </ol>

        <h2>Improvements</h2>
        <ul>
            <li>Add a frontend.</li>
            <li>Fine-tune skill extraction with more sophisticated NLP.</li>
            <li>Enhance to support more file formats.</li>
        </ul>
    </div>
</body>
</html>
