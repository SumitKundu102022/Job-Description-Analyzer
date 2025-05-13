# This is a Flask application that analyzes job descriptions and resumes/CVs to match skills.
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from analyzer import analyze_match
from skills_extractor import programming_skills, technical_skills, soft_skills, management_skills, alternative_technical_skills_groups, skill_aliases


# Configure logging
logging.basicConfig(level=logging.DEBUG,  # Set to DEBUG for detailed logging
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)


# Define skill category weights (can be adjusted)
SKILL_WEIGHTS = {
    "programming_skills": 0.3,
    "technical_skills": 0.3,
    "soft_skills": 0.2,
    "management_skills": 0.2,
}

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to analyze the job description, resume, and CV.
    Handles the POST request from the frontend.
    """
    try:
        data = request.get_json()
        if not data:
            logging.error("/analyze:  data is None or empty. Returning error")
            return jsonify({'error': 'Invalid request: Expected JSON data.'}), 400

        job_description = data.get('jobDescription', '')
        resume_text = data.get('resumeText', '')
        cv_text = data.get('cvText', '')



        if not job_description or not (resume_text or cv_text):
            return jsonify({'error': 'Both job description and either resume or CV are required.'}), 400

        analysis_result = analyze_match(job_description, resume_text, cv_text, SKILL_WEIGHTS)
        return jsonify(analysis_result), 200
    except Exception as e:
        error_message = f"Error in /analyze: {str(e)}"
        logging.exception(error_message)
        return jsonify({'error': error_message}), 500
    
@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request: Expected JSON data.'}), 400

        category = data.get('category')
        skill = data.get('skill', '').lower()

        if category == 'programming_skills':
            programming_skills.add(skill)
        elif category == 'technical_skills':
            technical_skills.add(skill)
        elif category == 'soft_skills':
            soft_skills.add(skill)
        elif category == 'management_skills':
            management_skills.add(skill)
        elif category == 'alternative_technical_skills_groups':
            found = False
            for group in alternative_technical_skills_groups:
                if skill in group:
                    found = True
                    break
            if not found:
                alternative_technical_skills_groups.append({skill})
        elif category == 'skill_aliases':
            original = data.get('original', '').lower()
            if original:
                skill_aliases[original] = skill
        else:
            return jsonify({'error': 'Invalid skill category.'}), 400

        return jsonify({'message': 'Feedback received and skills updated.'}), 200

    except Exception as e:
        logging.exception("Error in /feedback")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
    # Set debug=True for development; set to False in production
    # Use a production server like Gunicorn or uWSGI for deployment
    # set debug=False in production for security reasons
    