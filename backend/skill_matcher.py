from skills_extractor import extract_skills
import logging


def resolve_alternative_groups(job_skills_set, resume_skills_set, alternative_groups):
    matched_keywords = set()
    skipped_keywords = set()

    for group in alternative_groups:
        group_in_jd = group & job_skills_set
        if not group_in_jd:
            continue  # this group isn't in the JD, skip it

        if group & resume_skills_set:
            # At least one match, pick one to show as matched
            matched_keywords.add(next(iter(group & resume_skills_set)))
        else:
            # No matches, pick one from JD group to show as missing
            skipped_keywords.add(next(iter(group_in_jd)))

        # Exclude entire group from regular matching
        job_skills_set -= group_in_jd

    return matched_keywords, skipped_keywords



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

