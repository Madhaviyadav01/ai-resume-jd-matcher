"""
Provides curated, context-aware course and certification recommendations 
based on candidate skill gaps.
"""
from __future__ import annotations

CURATED_COURSES = {
    "aws": {
        "title": "AWS Certified Solutions Architect – Associate",
        "url": "https://aws.amazon.com/certification/certified-solutions-architect-associate/",
        "platform": "Amazon Web Services"
    },
    "docker": {
        "title": "Docker Certified Associate (DCA)",
        "url": "https://www.docker.com/docker-certification/",
        "platform": "Docker"
    },
    "kubernetes": {
        "title": "Certified Kubernetes Administrator (CKA)",
        "url": "https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/",
        "platform": "Linux Foundation"
    },
    "python": {
        "title": "Certified Associate in Python Programming (PCAP)",
        "url": "https://pythoninstitute.org/pcap",
        "platform": "Python Institute"
    },
    "fastapi": {
        "title": "Building APIs with FastAPI",
        "url": "https://www.coursera.org/search?query=fastapi",
        "platform": "Coursera"
    },
    "react": {
        "title": "Meta Front-End Developer Professional Certificate (React)",
        "url": "https://www.coursera.org/professional-certificates/meta-front-end-developer",
        "platform": "Coursera / Meta"
    },
    "sql": {
        "title": "Learn SQL Basics for Data Science Specialization",
        "url": "https://www.coursera.org/specializations/learn-sql-basics-data-science",
        "platform": "Coursera / UC Davis"
    },
    "postgresql": {
        "title": "PostgreSQL for Everybody Specialization",
        "url": "https://www.coursera.org/specializations/postgresql-for-everybody",
        "platform": "Coursera / UMich"
    },
    "mongodb": {
        "title": "MongoDB Native Certification",
        "url": "https://learn.mongodb.com/pages/certification-program",
        "platform": "MongoDB University"
    },
    "git": {
        "title": "Version Control with Git",
        "url": "https://www.coursera.org/learn/version-control-with-git",
        "platform": "Coursera / Atlassian"
    },
    "azure": {
        "title": "Microsoft Certified: Azure Fundamentals (AZ-900)",
        "url": "https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/",
        "platform": "Microsoft"
    },
    "gcp": {
        "title": "Google Cloud Associate Cloud Engineer",
        "url": "https://cloud.google.com/learn/certification/cloud-engineer",
        "platform": "Google Cloud"
    },
    "agile": {
        "title": "Professional Scrum Master (PSM I)",
        "url": "https://www.scrum.org/assessments/professional-scrum-master-i-certification",
        "platform": "Scrum.org"
    },
    "machine learning": {
        "title": "DeepLearning.AI Machine Learning Specialization",
        "url": "https://www.coursera.org/specializations/machine-learning-introduction",
        "platform": "Coursera / DeepLearning.AI"
    }
}


def get_course_recommendations(missing_skills: set | list | None, target_role: str = "Developer", limit: int = 4) -> list[dict]:
    """
    Generate robust, context-aware course recommendations for missing skills.

    Args:
        missing_skills (set/list/None): Skills the candidate is missing.
        target_role (str): Contextual role for dynamic title injection.
        limit (int): Maximum number of courses to return.

    Returns:
        list[dict]: List of course objects formatted as {"title": str, "url": str, "platform": str}.
    """
    if not missing_skills:
        return []

    recommended = []
    
    # Iterate through unique missing skills, keeping order stable via list/sort
    for skill in sorted(list(missing_skills)):
        skill_lower = skill.lower()
        
        if skill_lower in CURATED_COURSES:
            # Found in curated Official list
            base_course = CURATED_COURSES[skill_lower]
            recommended.append({
                "title": f"{base_course['title']} (Recommended for {target_role}s)",
                "url": base_course["url"],
                "platform": base_course["platform"]
            })
        else:
            # Fallback logic: dynamic search URL
            encoded_skill = skill.replace(" ", "%20")
            recommended.append({
                "title": f"{skill.title()} Professional Certification Track",
                "url": f"https://www.coursera.org/search?query={encoded_skill}%20certification",
                "platform": "Coursera Search"
            })
            
        if len(recommended) >= limit:
            break
            
    return recommended
