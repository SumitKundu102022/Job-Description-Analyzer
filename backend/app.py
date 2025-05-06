import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,  # Set to DEBUG for detailed logging
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)

# Download required NLTK data (run this once)
try:
    # nltk.download('punkt')
    # nltk.download('stopwords')
    pass
except Exception as e:
    logging.error(f"Error downloading NLTK data: {e}")
    # Handle the error appropriately, e.g., return an error to the client or exit

# Define stop words and buzzwords (extend as needed)
stopWords = set(stopwords.words('english'))
buzzwords = {
    'synergy', 'paradigm', 'innovative', 'world-class', 'cutting-edge',
    'best-of-breed', 'mission-critical', 'value-added', 'proactive',
    'dynamic', 'team-player', 'go-getter', 'solution-oriented',
    'results-driven', 'fast-paced', 'high-performing', 'strategic',
    'excellent communication skills', 'strong work ethic', 'detail-oriented',
    'self-motivated', 'highly motivated', 'ability to work independently',
    'proven track record', 'extensive experience', 'knowledge of', 'familiarity with',
    'background in', 'expertise in', 'skilled in', 'proficient in',
    'a plus', 'etc', 'and more', 'etc.', 'and much more',
    'responsibilities included', 'role and responsibilities', 'key responsibilities'
}
buzzwords = set(buzzwords)  # Convert buzzwords to set for efficiency

# Predefined skill dictionaries (extend as needed)
programming_skills = {skill.lower() for skill in [ "Python", "Java", "C++", "JavaScript", "React", "Angular", "SQL", "NoSQL", "C#", "PHP", "Ruby", "Kotlin", "Swift","Go", "Rust", "Dart", "Perl", "Shell Scripting"]}
technical_skills = {skill.lower() for skill in [ "Cloud Computing", "AWS", "Azure", "GCP", "DevOps", "Networking", "Cybersecurity", "Data Analysis", "Machine Learning", "AI", "Docker", "Kubernetes", "Linux", "Windows Server","Data Science", "Big Data", "Blockchain", "Virtualization", "CI/CD", "Agile", "Scrum", "ITIL", "SEO", "HTML", "CSS","typescript","json","xml","yaml","html5","css3","bootstrap","tailwind","material-ui","flask","django","fastapi","spring","hibernate","angularjs","vuejs","nodejs","expressjs","mongodb","postgresql","mysql","Postman","Redis","RabbitMQ","Kafka","TensorFlow","PyTorch","scikit-learn","Pandas","NumPy","Matplotlib","Seaborn","OpenCV"]}
soft_skills = {skill.lower() for skill in ["Communication", "Teamwork", "Problem-solving", "Leadership", "Time Management", "Adaptability", "Interpersonal Skills", "Critical Thinking", "Negotiation", "Conflict Resolution"]}
management_skills = {skill.lower() for skill in ["Project Management", "Team Leadership", "Strategic Planning", "Budgeting", "Delegation", "Performance Management", "Change Management", "Risk Management", "Decision Making"]}


def preprocess_text(text):
    """
    Preprocesses the input text.

    Args:
        text (str): The text to preprocess.

    Returns:
        list: A list of preprocessed tokens.
    """
    if not isinstance(text, str):
        logging.error(f"preprocess_text: Input is not a string. Returning empty list. Input: {text}")
        return []
    try:
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\+\s]", '', text)  # Keep '+' for C++
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in stopWords and word not in buzzwords and not word.isdigit() and word not in string.punctuation]
        logging.debug(f"preprocess_text: filtered_tokens: {filtered_tokens}")
        return filtered_tokens
    except Exception as e:
        logging.error(f"Error in preprocess_text: {e}")
        return []  # Return empty list in case of error



def extract_skills(text):
    """
    Extracts and categorizes skills from the given text.

    Args:
        text (str): The text to extract skills from.

    Returns:
        dict: A dictionary of extracted skills, categorized.
    """
    extracted_skills = {
        "programming_skills": [],
        "technical_skills": [],
        "soft_skills": [],
        "management_skills": [],
    }
    if not isinstance(text, str):
        logging.error(f"extract_skills: Input is not a string. Returning default skills. Input: {text}")
        return extracted_skills

    filtered_text = preprocess_text(text)
    joined_text = " ".join(filtered_text)
    logging.debug(f"extract_skills: joined_text: {joined_text}")

    #filtered_text_set = set(filtered_text)  # Create a set for faster lookup
    # logging.debug(f"extract_skills: filtered_text_set: {filtered_text_set}")

    for category, skills in [
        ("programming_skills", programming_skills),
        ("technical_skills", technical_skills),
        ("soft_skills", soft_skills),
        ("management_skills", management_skills),
    ]:
        extracted = [skill for skill in skills if skill in joined_text]
        extracted_skills[category] = extracted
        logging.debug(f"extract_skills: {category}: {extracted}")

    return extracted_skills



def get_match_level(percentage):
    """
    Assigns a match level based on the match percentage.

    Args:
      percentage (float): The match percentage.

    Returns:
      str: The match level.
    """
    if not isinstance(percentage, (int, float)):
        logging.warning(f"get_match_level: Input percentage is not a number. Returning 'Poor'. Input: {percentage}")
        return 'Poor'
    if percentage >= 90:
        return 'Perfect'
    elif percentage >= 70:
        return 'Good'
    elif percentage >= 50:
        return 'Fair'
    else:
        return 'Poor'



def match_skills(job_skills, candidate_skills, weights):
    """
    Calculates match scores for each skill category and an overall score.

    Args:
        job_skills (dict):  Categorized skills from the job description.
        candidate_skills (dict): Categorized skills from the candidate profile.
        weights (dict): Weights for each skill category.

    Returns:
        dict:  Match results, including scores and missing skills.
    """
    match_results = {
        "programming_skills": {"score": 0, "missing": []},
        "technical_skills": {"score": 0, "missing": []},
        "soft_skills": {"score": 0, "missing": []},
        "management_skills": {"score": 0, "missing": []},
        "overall_score": 0,
    }
    total_weight = sum(weights.values())
    if total_weight == 0:
        logging.warning("match_skills: Total weight is 0. Returning default results.")
        return match_results

    for category in job_skills:
        try:
            job_skills_list = job_skills[category]
            candidate_skills_list = candidate_skills.get(category, [])  # Use .get()
            if not isinstance(job_skills_list, list):
                logging.error(f"match_skills: job_skills[{category}] is not a list.  Skipping category. value: {job_skills_list}")
                continue  # Skip to the next category
            if not job_skills_list:
                match_results[category]["score"] = 100
                match_results[category]["missing"] = []
            else:
                matched_count = len([skill for skill in job_skills_list if skill in candidate_skills_list])
                match_results[category]["score"] = (matched_count / len(job_skills_list)) * 100
                match_results[category]["missing"] = [skill for skill in job_skills_list if skill not in candidate_skills_list]
        except KeyError as e:
            logging.error(f"KeyError in match_skills: {e}, category: {category}")
            match_results[category]["score"] = 0
            match_results[category]["missing"] = []

    overall_score = 0
    for category, result in match_results.items():
        if category != "overall_score":
            overall_score += result["score"] * weights.get(category, 0)
    match_results["overall_score"] = overall_score / total_weight if total_weight else 0
    match_results["matchLevel"] = get_match_level(match_results["overall_score"])
    return match_results



def analyze_job_candidate_fit(job_description, resume_text, cv_text, weights):
    """
    Analyzes the match between a job description and candidate profile (resume/CV).

    Args:
        job_description (str): The job description text.
        resume_text (str): The resume text.
        cv_text (str): The CV text.
        weights (dict):  A dictionary of weights for each skill category.

    Returns:
        dict: The analysis results, including match scores and missing skills.
    """
    try:
        job_skills = extract_skills(job_description)
        resume_skills = extract_skills(resume_text)
        cv_skills = extract_skills(cv_text)
        # Combine resume and CV skills
        candidate_skills = {}
        for category in resume_skills:
            candidate_skills[category] = resume_skills[category] + [skill for skill in cv_skills.get(category, []) if skill not in resume_skills[category]]

        return match_skills(job_skills, candidate_skills, weights)
    except Exception as e:
        error_message = f"Error in analyze_job_candidate_fit: {str(e)}"
        logging.exception(error_message)
        return {
            "matchedKeywords": [],
            "matchPercentage": 0,
            "matchLevel": "Error",
            "missingKeywords": [],
            "error": error_message
        }



def analyze_match(job_description, resume_text, cv_text, weights):
    """
    Analyzes the match between the job description and the resume/CV.

    Args:
        job_description (str): The job description text.
        resume_text (str): The resume text.
        cv_text (str): The CV text.
        weights (dict):  A dictionary of weights for each skill category.

    Returns:
        dict: A dictionary containing the analysis results, including matched keywords,
              match percentage, match level, and missing keywords.
    """
    try:
        job_skills = extract_skills(job_description)
        resume_skills = extract_skills(resume_text)
        cv_skills = extract_skills(cv_text)
        # Combine resume and CV skills
        candidate_skills = {}
        for category in resume_skills:
            candidate_skills[category] = resume_skills[category] + [skill for skill in cv_skills.get(category, []) if skill not in resume_skills[category]]

        match_result = match_skills(job_skills, candidate_skills, weights)

        # Extract relevant information from match_result
        matched_keywords = set()
        missing_keywords = set()
        total_job_skills = 0
        total_matched_skills = 0

        logging.debug(f"analyze_match: job_skills: {job_skills}")
        logging.debug(f"analyze_match: candidate_skills: {candidate_skills}")

        for category, result in match_result.items():
            if category != "overall_score" and category != "matchLevel":
                job_skills_in_category = set(job_skills.get(category, []))
                candidate_skills_in_category = set(candidate_skills.get(category, []))

                matched_keywords.update(job_skills_in_category.intersection(candidate_skills_in_category))
                missing_keywords.update(job_skills_in_category - candidate_skills_in_category)

                total_job_skills += len(job_skills_in_category)
                total_matched_skills += len(job_skills_in_category.intersection(candidate_skills_in_category))

        match_percentage = (total_matched_skills / total_job_skills) * 100 if total_job_skills else 0
        match_level = get_match_level(match_percentage)

        return {
            "matchedKeywords": list(matched_keywords),
            "matchPercentage": round(match_percentage),
            "matchLevel": match_level,
            "missingKeywords": list(missing_keywords),
        }
    except Exception as e:
        error_message = f"Error in analyze_match: {str(e)}"
        logging.exception(error_message)
        return {
            "matchedKeywords": [],
            "matchPercentage": 0,
            "matchLevel": "Error",
            "missingKeywords": [],
            "error": error_message
        }


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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


#Main Flask application for analyzing job descriptions and resumes/CVs
# import re
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# app = Flask(__name__)
# CORS(app)  # Enable CORS for cross-origin requests (allow React frontend to communicate)

# # Download required NLTK data (run this once)
# nltk.download('punkt')
# nltk.download('stopwords')

# # Define stop words and buzzwords (extend as needed)
# stopWords = set(stopwords.words('english'))
# buzzwords = {
#     'synergy', 'paradigm', 'innovative', 'world-class', 'cutting-edge',
#     'best-of-breed', 'mission-critical', 'value-added', 'proactive',
#     'dynamic', 'team-player', 'go-getter', 'solution-oriented',
#     'results-driven', 'fast-paced', 'high-performing', 'strategic',
#     'excellent communication skills', 'strong work ethic', 'detail-oriented',
#     'self-motivated', 'highly motivated', 'ability to work independently',
#     'proven track record', 'extensive experience', 'knowledge of', 'familiarity with',
#     'background in', 'expertise in', 'skilled in', 'proficient in',
#     'a plus', 'etc', 'and more', 'etc.', 'and much more','eg', 'for example',
#     'for instance', 'such as', 'including', 'like', 'in addition to','eg.'
#     'responsibilities included', 'role and responsibilities', 'key responsibilities'
# }

# # Predefined skill dictionaries (extend as needed)
# programming_skills = ["Python", "Java", "C++", "JavaScript", "React", "Angular", "SQL", "NoSQL", "C#", "PHP", "Ruby", "Kotlin", "Swift"]
# technical_skills = ["Cloud Computing", "AWS", "Azure", "GCP", "DevOps", "Networking", "Cybersecurity", "Data Analysis", "Machine Learning", "AI", "Docker", "Kubernetes", "Linux", "Windows Server"]
# soft_skills = ["Communication", "Teamwork", "Problem-solving", "Leadership", "Time Management", "Adaptability", "Interpersonal Skills", "Critical Thinking", "Negotiation", "Conflict Resolution"]
# management_skills = ["Project Management", "Team Leadership", "Strategic Planning", "Budgeting", "Delegation", "Performance Management", "Change Management", "Risk Management", "Decision Making"]



# def preprocess_text(text):
#     """
#     Preprocesses the input text by:
#     - Converting to lowercase
#     - Removing non-alphanumeric characters
#     - Tokenizing the text
#     - Removing stop words
#     """
#     text = text.lower()
#     text = re.sub(r"[^a-zA-Z0-9\+\s]", '', text) # Keep '+' for C++
#     tokens = word_tokenize(text)
#     stop_words = set(stopWords)
#     filtered_tokens = [word for word in tokens if word not in stop_words and word not in buzzwords and not word.isdigit()]
#     return filtered_tokens

# def extract_skills(text):
#     """
#     Extracts and categorizes skills from the given text.
#     """
#     extracted_skills = {
#         "programming_skills": [],
#         "technical_skills": [],
#         "soft_skills": [],
#         "management_skills": [],
#         "job_oriented_skills": [],  # To be populated later
#     }
#     if not text:
#         return extracted_skills

#     filtered_text = preprocess_text(text)
#     filtered_text_set = set(filtered_text) # Create a set for faster lookup
    
#     # Use filtered_text_set for faster lookup
#     for word in filtered_text_set:
#         if word in programming_skills:
#             extracted_skills["programming_skills"].append(word)
#         elif word in technical_skills:
#             extracted_skills["technical_skills"].append(word)
#         elif word in soft_skills:
#             extracted_skills["soft_skills"].append(word)
#         elif word in management_skills:
#             extracted_skills["management_skills"].append(word)

#     # 2. Job-Oriented Skills (Extract directly from the text)
#     #    This is a simplified example.  You might need more sophisticated NLP.
#     for word in filtered_text_set:
#         if word not in programming_skills + technical_skills + soft_skills + management_skills:
#             extracted_skills["job_oriented_skills"].append(word)
#     return extracted_skills

# def get_match_level(percentage):
#     """
#     Assigns a match level based on the match percentage.
#     """
#     if percentage >= 90:
#         return 'Perfect'
#     elif percentage >= 70:
#         return 'Good'
#     elif percentage >= 50:
#         return 'Fair'
#     else:
#         return 'Poor'
    
# def match_skills(job_skills, candidate_skills, weights):
#     """
#     Calculates match scores for each skill category and an overall score.

#     Args:
#         job_skills (dict):  Categorized skills from the job description.
#         candidate_skills (dict): Categorized skills from the candidate profile.
#         weights (dict): Weights for each skill category.

#     Returns:
#         dict:  Match results, including scores and missing skills.
#     """
#     match_results = {
#         "programming_skills": {"score": 0, "missing": []},
#         "technical_skills": {"score": 0, "missing": []},
#         "soft_skills": {"score": 0, "missing": []},
#         "management_skills": {"score": 0, "missing": []},
#         "job_oriented_skills": {"score": 0, "missing": []},
#         "overall_score": 0,
#     }
#     total_weight = sum(weights.values())
#     if total_weight == 0:
#         return match_results

#     for category in job_skills:
#         job_skills_list = job_skills[category]
#         candidate_skills_list = candidate_skills.get(category, [])  # Use .get()
#         if not job_skills_list:
#             match_results[category]["score"] = 100
#             match_results[category]["missing"] = []
#         else:
#             matched_count = len([skill for skill in job_skills_list if skill in candidate_skills_list])
#             match_results[category]["score"] = (matched_count / len(job_skills_list)) * 100
#             match_results[category]["missing"] = [skill for skill in job_skills_list if skill not in candidate_skills_list]

#     overall_score = 0
#     for category, result in match_results.items():
#         if category != "overall_score":
#             overall_score += result["score"] * weights.get(category, 0)
#     match_results["overall_score"] = overall_score / total_weight if total_weight else 0
#     match_results["matchLevel"] = get_match_level(match_results["overall_score"])
#     return match_results

# def analyze_match(job_description, resume_text, cv_text, weights):
#     """
#     Analyzes the match between the job description and the resume/CV.

#     Args:
#         job_description (str): The job description text.
#         resume_text (str): The resume text.
#         cv_text (str): The CV text.
#         weights (dict):  A dictionary of weights for each skill category.

#     Returns:
#         dict: A dictionary containing the analysis results, including matched keywords,
#               match percentage, match level, and missing keywords.
#     """
#     job_skills = extract_skills(job_description)
#     resume_skills = extract_skills(resume_text)
#     cv_skills = extract_skills(cv_text)
#     # Combine resume and CV skills
#     candidate_skills = {}
#     for category in resume_skills:
#         candidate_skills[category] = resume_skills[category] + [skill for skill in cv_skills.get(category, []) if skill not in resume_skills[category]]

#     match_result = match_skills(job_skills, candidate_skills, weights)

#     # Extract relevant information from match_result
#     matched_keywords = set()
#     missing_keywords = set()
#     total_job_skills = 0
#     total_matched_skills = 0
#     for category, result in match_result.items():
#         if category != "overall_score" and category != "matchLevel":  # avoid processing overall score
#             job_skills_in_category = job_skills[category]
#             missing_skills_in_category = result["missing"]
#             matched_skills_in_category = [skill for skill in job_skills_in_category if skill not in missing_skills_in_category]

#             matched_keywords.update(matched_skills_in_category)
#             missing_keywords.update(missing_skills_in_category)
#             total_job_skills += len(job_skills_in_category)
#             total_matched_skills += len(matched_skills_in_category)

#     match_percentage = (total_matched_skills / total_job_skills) * 100 if total_job_skills else 0
#     match_level = get_match_level(match_percentage)
#     return {
#         "matchedKeywords": list(matched_keywords),
#         "matchPercentage": round(match_percentage),
#         "matchLevel": match_level,
#         "missingKeywords": list(missing_keywords),
#     }


# # Define skill category weights (can be adjusted)
# SKILL_WEIGHTS = {
#     "programming_skills": 0.3,
#     "technical_skills": 0.3,
#     "soft_skills": 0.2,
#     "management_skills": 0.2,
#     "job_oriented_skills": 0.2,  # Give some weight, even if extracted from job description
# }


# @app.route('/analyze', methods=['POST'])
# def analyze():
#     """
#     Endpoint to analyze the job description, resume, and CV.
#     Handles the POST request from the frontend.
#     """
#     try:
#         data = request.get_json()
#         job_description = data['jobDescription']
#         resume_text = data['resumeText']
#         cv_text = data['cvText']

#         if not job_description or not (resume_text or cv_text):
#             return jsonify({'error': 'Both job description and either resume or CV are required.'}), 400

#         analysis_result = analyze_match(job_description, resume_text, cv_text,SKILL_WEIGHTS)
#         return jsonify(analysis_result), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



# if __name__ == '__main__':
#     app.run(debug=True, port=5001)  # Run the app on port 5001 (or any port you prefer)
    
    
#----------------------------------------------------------------------------------------------------------------------------------------    
    
# def analyze_job_candidate_fit(job_description, resume_text, cv_text, weights):
#     """
#     Analyzes the match between a job description and candidate profile (resume/CV).

#     Args:
#         job_description (str): The job description text.
#         resume_text (str): The resume text.
#         cv_text (str): The CV text.
#         weights (dict):  A dictionary of weights for each skill category.
#             e.g., {"programming_skills": 0.3, "technical_skills": 0.3, ...}

#     Returns:
#         dict: The analysis results, including match scores and missing skills.
#     """
#     job_skills = extract_skills(job_description)
#     resume_skills = extract_skills(resume_text)
#     cv_skills = extract_skills(cv_text)

#     # Combine resume and CV skills (prioritize resume)
#     candidate_skills = {}
#     for category in resume_skills:
#         candidate_skills[category] = resume_skills[category] + [
#             skill for skill in cv_skills[category] if skill not in resume_skills[category]
#         ]

#     return match_skills(job_skills, candidate_skills, weights)
# #1------------------------------------------------------------------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>

#2------------------------------------------------------------------------------------------------------------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from skill_matcher import analyze_job_candidate_fit

# app = Flask(__name__)
# CORS(app)

# # Define skill category weights (can be adjusted)
# SKILL_WEIGHTS = {
#     "programming_skills": 0.3,
#     "technical_skills": 0.3,
#     "soft_skills": 0.2,
#     "management_skills": 0.2,
#     "job_oriented_skills": 0.2,  # Give some weight, even if extracted from job description
# }

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     try:
#         data = request.get_json()
#         print("-----------------")
#         print("BACKEND: Received data from frontend:")
#         print(json.dumps(data, indent=2))
#         print("-----------------")
#         job_description = data['jobDescription']
#         resume_text = data['resumeText']
#         cv_text = data['cvText']

#         if not job_description or not (resume_text or cv_text):
#             return jsonify({'error': 'Both job description and either resume or CV are required.'}), 400

#         analysis_result = analyze_job_candidate_fit(job_description, resume_text, cv_text, SKILL_WEIGHTS)
#         print("-----------------")
#         print("BACKEND: Analysis result from skill_matcher:")
#         print(json.dumps(analysis_result, indent=2))  # Use json.dumps for pretty printing
#         print("-----------------")
#         return jsonify(analysis_result), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

#3------------------------------------------------------------------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from skill_matcher import analyze_job_candidate_fit
# import logging
# import json  # Import the json module

# # Configure logging
# logging.basicConfig(level=logging.DEBUG,  # Set to DEBUG for maximum information
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# app = Flask(__name__)
# CORS(app)

# # Define skill category weights (can be adjusted)
# SKILL_WEIGHTS = {
#     "programming_skills": 0.3,
#     "technical_skills": 0.3,
#     "soft_skills": 0.2,
#     "management_skills": 0.2,
#     "job_oriented_skills": 0.2,
# }

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     """
#     Endpoint to analyze the job description, resume, and CV.
#     Handles the POST request from the frontend.
#     """
#     try:
#         logging.info("Received request to /analyze")
#         data = request.get_json()
#         logging.debug(f"Request data: {json.dumps(data, indent=2)}")  # Log the data

#         # Check if data is None or not a dictionary
#         if data is None or not isinstance(data, dict):
#             error_message = "Invalid request: Expected JSON data."
#             logging.error(error_message)
#             return jsonify({'error': error_message}), 400

#         job_description = data.get('jobDescription', '')  # Use .get() with defaults
#         resume_text = data.get('resumeText', '')
#         cv_text = data.get('cvText', '')

#         # Log the extracted values
#         logging.debug(f"job_description: {job_description}")
#         logging.debug(f"resume_text: {resume_text}")
#         logging.debug(f"cv_text: {cv_text}")

#         if not job_description or not (resume_text or cv_text):
#             error_message = 'Both job description and either resume or CV are required.'
#             logging.error(error_message)
#             return jsonify({'error': error_message}), 400

#         try:
#             analysis_result = analyze_job_candidate_fit(job_description, resume_text, cv_text, SKILL_WEIGHTS)
#             logging.debug(f"Analysis result: {json.dumps(analysis_result, indent=2)}")  # Log result
#             return jsonify(analysis_result), 200
#         except Exception as e:
#             error_message = f"Error during analysis: {str(e)}"
#             logging.exception(error_message)  # Log the full traceback
#             return jsonify({'error': error_message}), 500

#     except Exception as e:
#         error_message = f"Exception in /analyze: {str(e)}"
#         logging.exception(error_message)  # Log the full traceback
#         return jsonify({'error': error_message}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)
