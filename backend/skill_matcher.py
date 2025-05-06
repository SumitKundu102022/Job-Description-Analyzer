from skills_extractor import extract_skills

def get_match_level(percentage):
    """
    Assigns a match level based on the match percentage.
    """
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
        "job_oriented_skills": {"score": 0, "missing": []},
        "overall_score": 0,
    }
    total_weight = sum(weights.values())
    if total_weight == 0:
        return match_results

    for category in job_skills:
        job_skills_list = job_skills[category]
        candidate_skills_list = candidate_skills[category]
        if not job_skills_list:
            match_results[category]["score"] = 100
            match_results[category]["missing"] = []
        else:
            matched_count = len([skill for skill in job_skills_list if skill in candidate_skills_list])
            match_results[category]["score"] = (matched_count / len(job_skills_list)) * 100
            match_results[category]["missing"] = [skill for skill in job_skills_list if skill not in candidate_skills_list]

    overall_score = 0
    for category, result in match_results.items():
        if category != "overall_score":
            overall_score += result["score"] * weights.get(category, 0)
    match_results["overall_score"] = overall_score / total_weight if total_weight else 0
    match_level = get_match_level(match_results["overall_score"])
    match_results["match_level"] = match_level
    return match_results

def analyze_job_candidate_fit(job_description, resume_text, cv_text, weights):
    """
    Analyzes the match between a job description and candidate profile (resume/CV).

    Args:
        job_description (str): The job description text.
        resume_text (str): The resume text.
        cv_text (str): The CV text.
        weights (dict):  A dictionary of weights for each skill category.
            e.g., {"programming_skills": 0.3, "technical_skills": 0.3, ...}

    Returns:
        dict: The analysis results, including match scores and missing skills.
    """
    job_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)
    cv_skills = extract_skills(cv_text)

    # Combine resume and CV skills (prioritize resume)
    candidate_skills = {}
    for category in resume_skills:
        candidate_skills[category] = resume_skills[category] + [
            skill for skill in cv_skills[category] if skill not in resume_skills[category]
        ]

    return match_skills(job_skills, candidate_skills, weights)

# from skills_extractor import extract_skills
# import logging

# # Configure logging
# logging.basicConfig(level=logging.ERROR,  # Change to DEBUG for more detailed logging
#                     format='%(asctime)s - %(levelname)s - %(message)s')

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
#         logging.warning("Total weight is 0. Returning default match results.")
#         return match_results

#     for category in job_skills:
#         try:
#             job_skills_list = job_skills[category]
#             candidate_skills_list = candidate_skills.get(category, [])
#             if not isinstance(job_skills_list, list):
#                 logging.error(f"job_skills[{category}] is not a list: {job_skills_list}")
#                 job_skills_list = [] # Treat as empty to avoid errors

#             if not job_skills_list:
#                 match_results[category]["score"] = 100
#                 match_results[category]["missing"] = []
#             else:
#                 matched_count = len([skill for skill in job_skills_list if skill in candidate_skills_list])
#                 match_results[category]["score"] = (matched_count / len(job_skills_list)) * 100
#                 match_results[category]["missing"] = [skill for skill in job_skills_list if skill not in candidate_skills_list]
#         except KeyError as e:
#             logging.error(f"KeyError accessing job_skills or candidate_skills: {e}")
#             match_results[category]["score"] = 0
#             match_results[category]["missing"] = []

#     overall_score = 0
#     for category, result in match_results.items():
#         if category != "overall_score":
#             overall_score += result["score"] * weights.get(category, 0)
#     match_results["overall_score"] = overall_score / total_weight if total_weight else 0
#     match_results["matchLevel"] = get_match_level(match_results["overall_score"])
#     return match_results

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
#     try:
#         job_skills = extract_skills(job_description)
#         resume_skills = extract_skills(resume_text)
#         cv_skills = extract_skills(cv_text)

#         # Combine resume and CV skills (prioritize resume)
#         candidate_skills = {}
#         for category in resume_skills:
#             candidate_skills[category] = resume_skills[category] + [
#                 skill for skill in cv_skills.get(category, []) if skill not in resume_skills[category]
#             ]
#         return match_skills(job_skills, candidate_skills, weights)
#     except Exception as e:
#         logging.error(f"Exception in analyze_job_candidate_fit: {e}")
#         return {  # Return a default error structure
#             "matchedKeywords": [],
#             "matchPercentage": 0,
#             "matchLevel": "Error",
#             "missingKeywords": [],
#             "error": str(e)
#         }