from skills_extractor import extract_skills,alternative_technical_skills_groups
from skill_matcher import match_skills, get_match_level, resolve_alternative_groups
import logging


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
        logging.debug(f"analyze_match: job_skills---------------------------------------------------->>>>>>>>>>>>>>>>>>>>>: {job_skills}")
        resume_skills = extract_skills(resume_text)
        logging.debug(f"analyze_match: resume_skills------------------------------------------------->>>>>>>>>>>>>>>>>>>>>: {resume_skills}")
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
        
        # Flattened sets for alt-group matching
        job_flat = set(skill.lower() for cat in job_skills.values() for skill in cat)
        resume_flat = set(skill.lower() for cat in candidate_skills.values() for skill in cat)
        
        matched_from_alternatives, missing_from_alternatives = resolve_alternative_groups(
            job_flat, resume_flat, alternative_technical_skills_groups
        )
        
        
        # Update matched and missing keywords with alternative group results
        matched_keywords.update(matched_from_alternatives)
        missing_keywords.update(missing_from_alternatives)
        
        # Now remove all group members from regular missing
        for group in alternative_technical_skills_groups:
            if matched_from_alternatives & group:
                missing_keywords -= group
        
        # Calculate match percentage
        match_percentage = (total_matched_skills / total_job_skills) * 100 if total_job_skills else 0
        match_level = get_match_level(match_percentage)

        return {
            "matchedKeywords": sorted(list(matched_keywords)),
            "matchPercentage": round(match_percentage),
            "matchLevel": match_level,
            "missingKeywords": sorted(list(missing_keywords)),
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
