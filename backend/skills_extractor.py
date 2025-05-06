import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

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

# Predefined skill dictionaries (extend as needed)
programming_skills = ["Python", "Java", "C++", "JavaScript", "React", "Angular", "SQL", "NoSQL", "C#", "PHP", "Ruby", "Kotlin", "Swift"]
technical_skills = ["Cloud Computing", "AWS", "Azure", "GCP", "DevOps", "Networking", "Cybersecurity", "Data Analysis", "Machine Learning", "AI", "Docker", "Kubernetes", "Linux", "Windows Server"]
soft_skills = ["Communication", "Teamwork", "Problem-solving", "Leadership", "Time Management", "Adaptability", "Interpersonal Skills", "Critical Thinking", "Negotiation", "Conflict Resolution"]
management_skills = ["Project Management", "Team Leadership", "Strategic Planning", "Budgeting", "Delegation", "Performance Management", "Change Management", "Risk Management", "Decision Making"]

# def filter_keywords(text):
#     """
#     Filters out stop words, buzzwords, numbers, and irrelevant terms
#     from the given text, keeping only ATS-friendly keywords.
#     """
#     if not text:
#         return []

#     # 1. Tokenize the text
#     word_tokens = word_tokenize(text)

#     # 2. Remove stop words, punctuation, and convert to lowercase
#     filtered_words = [
#         word.lower() for word in word_tokens
#         if word.isalnum() and word.lower() not in stop_words
#     ]

#     # 3. Remove buzzwords and numbers
#     filtered_words = [
#         word for word in filtered_words
#         if word not in buzzwords and not word.isdigit()
#     ]
#     return filtered_words

def preprocess_text(text):
    """
    Preprocesses the input text by:
    - Converting to lowercase
    - Removing non-alphanumeric characters
    - Tokenizing the text
    - Removing stop words
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", '', text)
    tokens = word_tokenize(text)
    #stop_words = set(stopwords.words('english'))
    stop_words = set(stopWords)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    # 2. Remove stop words, punctuation, and convert to lowercase
    # filtered_tokens = [
    #     word.lower() for word in tokens
    #     if word.isalnum() and word.lower() not in stop_words
    # ]
    
     # 3. Remove buzzwords and numbers
    filtered_tokens = [
        word for word in filtered_tokens
        if word not in buzzwords and not word.isdigit()
    ]
    return filtered_tokens

def extract_skills(text):
    """
    Extracts and categorizes skills from the given text.
    """
    extracted_skills = {
        "programming_skills": [],
        "technical_skills": [],
        "soft_skills": [],
        "management_skills": [],
        "job_oriented_skills": [],  # To be populated later
    }
    if not text:
        return extracted_skills

    filtered_text = preprocess_text(text)

    # 1. Dictionary Matching
    for word in filtered_text:
        if word in programming_skills:
            extracted_skills["programming_skills"].append(word)
        elif word in technical_skills:
            extracted_skills["technical_skills"].append(word)
        elif word in soft_skills:
            extracted_skills["soft_skills"].append(word)
        elif word in management_skills:
            extracted_skills["management_skills"].append(word)

    # 2. Job-Oriented Skills (Extract directly from the text)
    #    This is a simplified example.  You might need more sophisticated NLP.
    for word in filtered_text:
        if word not in programming_skills + technical_skills + soft_skills + management_skills:
            extracted_skills["job_oriented_skills"].append(word)
    return extracted_skills

# import re
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# import logging

# # Configure logging
# logging.basicConfig(level=logging.ERROR,  # Change to DEBUG for more detailed logging
#                     format='%(asctime)s - %(levelname)s - %(message)s')

# try:
#     nltk.download('punkt')
#     nltk.download('stopwords')
# except Exception as e:
#     logging.error(f"Error during NLTK download: {e}")
#     #  Handle the error appropriately, e.g., exit or use a simplified approach

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
#     'a plus', 'etc', 'and more', 'etc.', 'and much more',
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
#     if not isinstance(text, str):
#         logging.error(f"Input text is not a string: {text}")
#         return ""
#     try:
#         text = text.lower()
#         text = re.sub(r"[^a-zA-Z0-9\s]", '', text)
#         tokens = word_tokenize(text)
#         filtered_tokens = [word for word in tokens if word not in stopWords]
#         filtered_tokens = [word for word in filtered_tokens if word not in buzzwords and not word.isdigit()]
#         return filtered_tokens
#     except Exception as e:
#         logging.error(f"Error in preprocess_text: {e}")
#         return ""



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
#     if not isinstance(text, str):
#         logging.error(f"Input text is not a string: {text}")
#         return extracted_skills

#     filtered_text = preprocess_text(text)

#     # 1. Dictionary Matching
#     for word in filtered_text:
#         try:
#             if word in programming_skills:
#                 extracted_skills["programming_skills"].append(word)
#             elif word in technical_skills:
#                 extracted_skills["technical_skills"].append(word)
#             elif word in soft_skills:
#                 extracted_skills["soft_skills"].append(word)
#             elif word in management_skills:
#                 extracted_skills["management_skills"].append(word)
#         except KeyError as e:
#             logging.error(f"KeyError in extract_skills: {e}, word: {word}")

#     # 2. Job-Oriented Skills (Extract directly from the text)
#     #   This is a simplified example.  You might need more sophisticated NLP.
#     for word in filtered_text:
#         if word not in programming_skills + technical_skills + soft_skills + management_skills:
#             extracted_skills["job_oriented_skills"].append(word)
#     return extracted_skills