from __future__ import annotations

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Lazy-load cache
# ---------------------------------------------------------------------------

_MODEL_NAME: str = "all-MiniLM-L6-v2"
_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    """
    Return the cached SentenceTransformer model, loading it on first call.

    Thread safety: Streamlit runs each user session in its own thread.
    The module-level cache is per-process, so in a multi-user deployment
    the model is shared across sessions (read-only after loading — safe).
    """
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


# ---------------------------------------------------------------------------
# get_match_score()
# ---------------------------------------------------------------------------

def get_match_score(resume_text: str, jd_text: str) -> float:
    """
    Compute the semantic similarity between a resume and a job description.

    Steps:
        1. Lazy-load the SBERT ``all-MiniLM-L6-v2`` model (cached after
           first call — no reload overhead on subsequent invocations).
        2. Encode ``resume_text`` and ``jd_text`` into 384-dim embeddings.
        3. Compute cosine similarity between the two embedding vectors.
        4. Clamp the raw similarity to ``[0, 1]`` to guard against
           floating-point edge cases, then scale to a percentage.

    Args:
        resume_text (str): Pre-cleaned resume text
                           (use ``src.preprocess.clean_text`` beforehand).
        jd_text     (str): Pre-cleaned job description text.

    Returns:
        float: Match score in the range ``[0.00, 100.00]``, rounded to
               2 decimal places.  Returns ``0.0`` if either input is empty.

    Example:
        >>> from src.preprocess import clean_text
        >>> from src.matcher import get_match_score
        >>> score = get_match_score(clean_text(resume), clean_text(jd))
        >>> print(f"{score}%")
        74.31%
    """
    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    model = _get_model()

    # Encode — shape: (1, embedding_dim)
    resume_embedding = model.encode([resume_text])
    jd_embedding     = model.encode([jd_text])

    # cosine_similarity returns a 2-D array; extract the scalar
    raw: float = float(cosine_similarity(resume_embedding, jd_embedding)[0][0])

    # Clamp to [0, 1] and convert to percentage
    score = max(0.0, min(1.0, raw)) * 100
    return round(score, 2)


def generate_recommendations(resume_text: str, jd_text: str, missing_skills: set, match_score: float) -> dict[str, list[str]]:
    """
    Generate dynamic recommendations based on the match score and missing skills.
    
    Returns:
        dict: containing:
            - 'insights': List of strength or gap insight strings.
            - 'recommendations': List of actionable steps including skill acquisition.
    """
    insights = []
    recs = []
    
    if match_score >= 70:
        insights.append("🎯 Resume is strongly aligned with the job requirements")
        insights.append("📌 Good foundation — targeted additions will strengthen this")
        recs.append("✨ Personalise your cover letter to highlight overlapping skills")
        recs.append("🔍 Review bullet points to ensure key achievements are quantified")
    elif match_score >= 50:
        insights.append("📌 Good foundation — targeted additions will strengthen this")
        recs.append("🔍 Add a dedicated Skills section listing all JD-relevant technologies")
        recs.append("📄 Tailor resume keywords to mirror the job description language")
    else:
        insights.append("⚠️ Resume needs significant alignment to this role")
        insights.append("⚠️ Highlight core competencies required by the JD")
        recs.append("📄 Complete rewrite of summary and skills sections recommended")
        recs.append("📈 Quantify achievements with numbers, percentages, and impact metrics")
        
    TIPS = {
        "docker": "🐳 Containerise a personal project with Docker",
        "kubernetes": "☸️ Study Kubernetes and explore the CKA certification path",
        "aws": "☁️ Start with the AWS Cloud Practitioner certification",
        "tensorflow": "⚡ Build a TensorFlow project — image classifier or NLP model",
        "pytorch": "🔥 Practice PyTorch through fast.ai or official tutorials",
        "mlops": "⚙️ Explore MLflow, DVC, or Kubeflow for MLOps",
        "sql": "🗄️ Strengthen SQL with CTEs, window functions, complex joins",
        "fastapi": "⚡ Build and deploy a REST API with FastAPI",
        "nlp": "📝 Complete the Hugging Face NLP course",
        "machine learning": "🤖 Complete Andrew Ng ML course or a Kaggle challenge",
        "ci/cd": "🔁 Set up a CI/CD pipeline with GitHub Actions",
    }
    
    for s in list(missing_skills)[:5]:
        if s in TIPS:
            recs.append(TIPS[s])
        else:
            recs.append(f"📚 Build hands-on experience with **{s.title()}**")
            
    return {
        "insights": insights[:5],
        "recommendations": recs[:5]
    }
