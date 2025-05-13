import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import logging

# Download required NLTK data (run this once)
try:
    # nltk.download('punkt_tab')
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
programming_skills = {skill.lower() for skill in [ "Python","Java", "C++", "JavaScript", "React", "Angular", "SQL", "NoSQL", "C#", "PHP", "Ruby", "Kotlin", "Swift","Go", "Rust", "Dart", "Perl", "Shell Scripting"]}
technical_skills = {skill.lower() for skill in [ "Object Oriented Programming","object-oriented programming","oop", "oops","Cloud Computing", "AWS", "Azure", "GCP", "DevOps", "Networking", "Cybersecurity", "Data Analysis", "Machine Learning", "AI", "Docker", "Kubernetes", "Linux", "Windows Server","Data Science", "Big Data", "Blockchain", "Virtualization", "CI/CD", "Agile", "Scrum", "ITIL", "SEO", "HTML", "CSS","typescript","json","xml","yaml","git","github","bootstrap","tailwind","material-ui","flask","django","fastapi","spring","hibernate","angularjs","vuejs","nodejs","expressjs","mongodb","postgresql","mysql","Postman","Redis","RabbitMQ","Kafka","TensorFlow","PyTorch","scikit-learn","Pandas","NumPy","Matplotlib","Seaborn","OpenCV","PowerShell", "Bash"]}
soft_skills = {skill.lower() for skill in ["Communication", "Teamwork", "Problem-solving", "Leadership", "Time Management", "Adaptability", "Interpersonal Skills", "Critical Thinking", "Negotiation", "Conflict Resolution"]}
management_skills = {skill.lower() for skill in ["Project Management", "Team Leadership", "Strategic Planning", "Budgeting", "Delegation", "Performance Management", "Change Management", "Risk Management", "Decision Making"]}


# Alternative technical skills groups
alternative_technical_skills_groups = [ 
    {s.lower() for s in group}
    for group in [
        {"MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQL Server"},
        {"HTML", "XML", "XHTML"},
        {"CSS", "SCSS", "SASS"},
        {"JavaScript", "TypeScript"},
        {"React", "Angular", "Vue", "Svelte"},
        {"Node.js", "Express.js", "Django", "Flask", "Spring Boot"},
        {"C", "C++"},
        {"Java", "Kotlin", "Scala"},
        {"Python", "Ruby", "Perl"},
        {"Git", "Bitbucket", "GitLab"},
        {"AWS", "Azure", "Google Cloud Platform"},
        {"Docker", "Podman"},
        {"Kubernetes", "OpenShift", "Docker Swarm"},
        {"Jenkins", "GitHub Actions", "CircleCI", "Travis CI"},
        {"Linux", "Unix"},
        {"Figma", "Adobe XD", "Sketch"},
        {"SQL", "NoSQL"},
        {"REST API", "GraphQL"},
        {"TensorFlow", "PyTorch", "Scikit-learn"},
        {"Spring", "Hibernate"}
    ]
]

# Skill normalization mapping
skill_aliases = {
    "html5": "html",
    "css3": "css",
    "js": "javascript",
    "nodejs": "node.js",
    "expressjs": "express.js",
    "object-oriented programming": "object oriented programming",
    "oops": "object-oriented programming",
    "oop": "object oriented programming",
    # "oop": "oops",
    # "object oriented programming": "object-oriented programming",
    "ability to work in a team": "teamwork"
    # Add more as needed
}




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
        
        # Join tokens into phrases for aliasing
        joined_text = " ".join(tokens)
        for phrase, alias in skill_aliases.items():
            if phrase in joined_text:
                tokens.append(alias)
        
        # Then clean as before
        tokens = [skill_aliases.get(tok, tok) for tok in tokens]
        filtered_tokens = [word for word in tokens if word not in stopWords and word not in buzzwords and not word.isdigit() and word not in string.punctuation]
        # # Normalize skills using skill_aliases
        # normalized_tokens = []
        # for word in filtered_tokens:
        #     normalized = skill_aliases.get(word, word)  # replace if alias exists
        #     if normalized not in stopWords and normalized not in buzzwords and not normalized.isdigit():
        #         normalized_tokens.append(normalized)
        
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
    text_tokens_set = set(filtered_text)  # for exact match
    joined_text = " ".join(filtered_text)
    logging.debug(f"extract_skills: text_tokens_set----------------------------------------------------------------------------->: {text_tokens_set}")
    logging.debug(f"extract_skills: joined_text: {joined_text}")

    #filtered_text_set = set(filtered_text)  # Create a set for faster lookup
   

    for category, skills in [
        ("programming_skills", programming_skills),
        ("technical_skills", technical_skills),
        ("soft_skills", soft_skills),
        ("management_skills", management_skills),
    ]:  
        extracted = []
        for skill in skills:
            if skill in text_tokens_set:
                extracted.append(skill)
            elif " " in skill and skill in joined_text:  # handle multi-word skills like 'machine learning'
                extracted.append(skill)
        # extracted = [skill for skill in skills if skill in joined_text]
        #extracted = [skill for skill in skills if any(skill == token for token in filtered_text)]
        extracted_skills[category] = extracted
        logging.debug(f"extract_skills----********------: {category}: {extracted}")

    return extracted_skills


