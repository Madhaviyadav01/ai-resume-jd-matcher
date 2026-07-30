"""
src/skill_extractor.py — Technical Skill Extraction & Gap Analysis
===================================================================
Provides:
    extract_skills(text)              -> set[str]
    get_missing_skills(resume, jd)    -> tuple[set[str], set[str]]

Skills are matched case-insensitively using whole-word regex so short tokens
like "r", "c", or "go" are not spuriously matched inside longer words.

Author: AI Resume–JD Matcher (MCA Major Project)
"""

from __future__ import annotations

import re
from typing import Set, Tuple

from src.preprocess import clean_text


# ---------------------------------------------------------------------------
# Comprehensive ~100-skill vocabulary
# ---------------------------------------------------------------------------

TECH_SKILLS: list[str] = [
    # ── Programming Languages ──────────────────────────────────────────────
    "python", "java", "javascript", "typescript", "c", "c++", "c#",
    "go", "rust", "ruby", "kotlin", "swift", "scala", "r", "matlab",
    "perl", "php", "bash", "shell", "dart", "elixir", "haskell",

    # ── Data Science & ML (concepts) ──────────────────────────────────────
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "reinforcement learning", "data science",
    "feature engineering", "model deployment", "mlops", "data analysis",
    "statistical modeling", "time series", "a/b testing",

    # ── ML / DL Frameworks ────────────────────────────────────────────────
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
    "lightgbm", "catboost", "hugging face", "transformers",
    "sentence transformers", "spacy", "nltk", "opencv",

    # ── Data Manipulation ─────────────────────────────────────────────────
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
    "tableau", "power bi",

    # ── Databases ─────────────────────────────────────────────────────────
    "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis",
    "cassandra", "elasticsearch", "oracle", "dynamodb", "bigquery",
    "neo4j", "firebase",

    # ── Cloud & Infrastructure ────────────────────────────────────────────
    "aws", "azure", "gcp", "google cloud", "lambda", "ec2", "s3",
    "cloud run", "kubernetes", "docker", "terraform", "ansible",
    "cloudformation", "helm", "serverless",

    # ── Web / API ─────────────────────────────────────────────────────────
    "fastapi", "flask", "django", "rest api", "graphql", "react",
    "angular", "vue", "node.js", "express", "html", "css",
    "next.js", "spring boot", "asp.net",

    # ── DevOps & Version Control ──────────────────────────────────────────
    "git", "github", "gitlab", "bitbucket", "ci/cd", "jenkins",
    "github actions", "circleci", "travis ci", "argocd",

    # ── Data Engineering ──────────────────────────────────────────────────
    "airflow", "spark", "hadoop", "kafka", "dbt", "etl",
    "data pipeline", "data warehouse", "snowflake", "databricks",
    "flink", "beam",

    # ── General Engineering ───────────────────────────────────────────────
    "agile", "scrum", "jira", "linux", "unix", "microservices",
    "system design", "object oriented", "functional programming",
    "design patterns", "tdd", "bdd", "api development",
]

# Pre-compile a regex pattern per skill for O(n_skills) whole-word lookup.
# Skills with spaces use substring matching; single tokens use \\b boundaries.
_SKILL_PATTERNS: dict[str, re.Pattern] = {}
for _skill in TECH_SKILLS:
    if " " in _skill:
        _SKILL_PATTERNS[_skill] = re.compile(re.escape(_skill), re.IGNORECASE)
    else:
        _SKILL_PATTERNS[_skill] = re.compile(
            r"\b" + re.escape(_skill) + r"\b", re.IGNORECASE
        )


# ---------------------------------------------------------------------------
# 1. extract_skills()
# ---------------------------------------------------------------------------

def extract_skills(text: str) -> Set[str]:
    """
    Extract recognised technical skills from raw or pre-cleaned text.

    The function first cleans the text, then checks each skill in
    ``TECH_SKILLS`` using whole-word / phrase regex matching to avoid
    false positives (e.g. "r" matching inside "react").

    Args:
        text (str): Raw or pre-cleaned text (resume or job description).

    Returns:
        set[str]: Lower-case skill strings found in the text.
    """
    cleaned = clean_text(text)
    found: Set[str] = set()

    for skill, pattern in _SKILL_PATTERNS.items():
        if pattern.search(cleaned):
            found.add(skill)

    return found


# ---------------------------------------------------------------------------
# 2. get_missing_skills()
# ---------------------------------------------------------------------------

def get_missing_skills(
    resume_text: str,
    jd_text: str,
) -> Tuple[Set[str], Set[str]]:
    """
    Compare skills in a resume against those required by a job description.

    Args:
        resume_text (str): Raw text of the candidate's resume.
        jd_text     (str): Raw text of the job description.

    Returns:
        tuple[set[str], set[str]]: A two-element tuple:
            - ``matched_skills`` — skills present in **both** the resume and JD
              (``jd_skills & resume_skills``).
            - ``missing_skills`` — skills in the JD but **absent** from the
              resume (``jd_skills - resume_skills``).

    Example:
        >>> matched, missing = get_missing_skills(resume_txt, jd_txt)
        >>> print("Matched:", matched)
        >>> print("Missing:", missing)
    """
    resume_skills: Set[str] = extract_skills(resume_text)
    jd_skills:     Set[str] = extract_skills(jd_text)

    matched_skills: Set[str] = jd_skills & resume_skills
    missing_skills: Set[str] = jd_skills - resume_skills

    return matched_skills, missing_skills


def get_skill_gaps(resume_text: str, jd_text: str) -> tuple[Set[str], Set[str], Set[str]]:
    """
    Compute comprehensive skill gaps between a resume and job description.

    Args:
        resume_text (str): The candidate's resume text.
        jd_text (str): The raw job description text.

    Returns:
        tuple containing:
            - matched_skills (set): Intersection (skills in both).
            - missing_skills (set): Present in JD, missing in resume.
            - extra_skills (set): Present in resume, not requested in JD.
    """
    resume_skills: Set[str] = extract_skills(resume_text)
    jd_skills:     Set[str] = extract_skills(jd_text)

    matched_skills = resume_skills & jd_skills
    missing_skills = jd_skills - resume_skills
    extra_skills   = resume_skills - jd_skills

    return matched_skills, missing_skills, extra_skills
