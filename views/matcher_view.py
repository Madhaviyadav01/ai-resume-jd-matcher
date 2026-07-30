"""
views/matcher_view.py  —  Main Recruitment Dashboard
======================================================
Layout (as specified):

LEFT SIDEBAR (appended to existing app.py sidebar):
    ## About
    Info box: what the tool does
    ## How It Works
    Numbered steps

MAIN CANVAS (vertical stack):
    Description text
    File uploader  (PDF resume)
    Text area      (Paste JD)
    Analyze Match button
    → Results section (shown after analysis)

DESIGN RULE:
    Every st.markdown(unsafe_allow_html=True) call contains COMPLETE,
    self-contained HTML. Tags are NEVER split across calls.

Backend pipeline (never modified here):
    src.parser            extract_text(file)
    src.preprocess        clean_text(text)
    src.skill_extractor   extract_skills(text), get_missing_skills(r, jd)
    src.matcher           get_match_score(r, jd)
    src.database          save_history(...), get_user_history(username)
    src.utils             format_score_color, format_score_label,
                          create_skill_chips_html
"""
from __future__ import annotations
import streamlit as st

from src.parser          import extract_text
from src.preprocess      import clean_text
from src.skill_extractor import extract_skills, get_skill_gaps
from src.matcher         import get_match_score, generate_recommendations
from src.database        import save_history, get_user_history
from src.utils           import (format_score_color, format_score_label,
                                 create_skill_chips_html)


# ── SBERT warm-up (cached per process) ─────────────────────────────────────

@st.cache_resource(show_spinner="⚙️ Loading AI model …")
def _load_model():
    from src.matcher import _get_model
    return _get_model()


# ── Public entry point ──────────────────────────────────────────────────────

def render_matcher_page(username: str, full_name: str) -> None:
    _load_model()

    # ── Main canvas ────────────────────────────────────────────────────────
    if st.session_state.get("last_result"):
        _render_results(username)
    else:
        _render_input_form(username)


# ===========================================================================
# INPUT FORM  (vertical stack)
# ===========================================================================

def _render_input_form(username: str) -> None:

    # Description text
    st.write(
        "Upload your resume (PDF) and paste a job description to see how well they match!"
    )
    st.caption(
        "This tool uses Sentence-BERT + Cosine Similarity to analyze your resume "
        "against job requirements."
    )

    st.markdown("---")

    # ── Resume upload ────────────────────────────────────────────────────────
    st.markdown("#### Upload your resume (PDF)")
    resume_file = st.file_uploader(
        "Resume",
        type=["pdf", "docx"],
        key="resume_upload",
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Job description (tabbed) ─────────────────────────────────────────────
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #94A3B8 !important;
        border: none !important;
        padding: 8px 16px;
        border-radius: 6px 6px 0 0;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #F8FAFC !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
    .stTabs [aria-selected="true"] {
        color: #818CF8 !important;
        background-color: rgba(99, 102, 241, 0.1) !important;
        border-bottom: 2px solid #818CF8 !important;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("#### Job Description")

    paste_tab, upload_tab = st.tabs(["📝 Paste Text", "📁 Upload File"])

    jd_raw_text = ""
    jd_name     = "Pasted JD"

    with paste_tab:
        jd_raw_text = st.text_area(
            "Job Description",
            height=200,
            placeholder="Paste the full job description here …",
            key="jd_text",
            label_visibility="collapsed",
        )

    with upload_tab:
        jd_file = st.file_uploader(
            "📁 Drag & Drop Job Description (PDF, DOCX, TXT) or click to browse files",
            type=["pdf", "docx", "txt"],
            key="jd_file",
        )
        if jd_file is not None:
            # Cache extracted text to avoid re-reading BytesIO on rerun
            if st.session_state.get("_jd_cache_name") != jd_file.name:
                if jd_file.name.lower().endswith(".txt"):
                    text = jd_file.read().decode("utf-8", errors="ignore")
                else:
                    text = extract_text(jd_file)
                st.session_state["_jd_cache_name"] = jd_file.name
                st.session_state["_jd_cache_text"] = text
            jd_raw_text = st.session_state.get("_jd_cache_text", "")
            jd_name     = jd_file.name
            st.success(f"✅ Loaded: **{jd_file.name}**")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Analyze button ───────────────────────────────────────────────────────
    if st.button("Analyze Match", key="analyze_btn"):
        _run_analysis(username, resume_file, jd_raw_text, jd_name)


# ===========================================================================
# ANALYSIS PIPELINE
# ===========================================================================

def _run_analysis(username, resume_file, jd_raw_text: str, jd_name: str = "Pasted JD") -> None:
    if resume_file is None:
        st.warning("⚠️ Please upload a resume (PDF or DOCX) before analyzing.")
        return
    if not jd_raw_text.strip():
        st.warning("⚠️ Please provide a job description (paste text or upload a file).")
        return

    try:
        with st.status("🤖 Running AI Analysis …", expanded=True) as status:
            st.write("📄 Extracting resume text …")
            resume_raw = extract_text(resume_file)
            if not resume_raw.strip():
                status.update(label="❌ Extraction failed", state="error")
                st.error("Could not extract text from the resume. Make sure it is not a scanned image.")
                return

            st.write("📋 Processing job description …")
            clean_r  = clean_text(resume_raw)
            clean_jd = clean_text(jd_raw_text)

            st.write("🧠 Computing SBERT embeddings …")
            score = get_match_score(clean_r, clean_jd)

            st.write("🔍 Analysing skill gap …")
            matched, missing, extra_skills = get_skill_gaps(resume_raw, jd_raw_text)
            jd_skills_count = len(matched) + len(missing)

            st.write("💡 Building recommendations …")
            analysis_data = generate_recommendations(resume_raw, jd_raw_text, missing, score)

            save_history(
                username       = username,
                resume_name    = resume_file.name,
                match_score    = score,
                missing_skills = list(missing),
                jd_name        = "Pasted JD",
                matched_skills = list(matched),
                extra_skills   = list(extra_skills),
            )

            st.session_state["last_result"] = {
                "resume_name"    : resume_file.name,
                "jd_name"        : jd_name,
                "score"          : score,
                "matched"        : matched,
                "missing"        : missing,
                "extra"          : extra_skills,
                "insights"       : analysis_data["insights"],
                "recommendations": analysis_data["recommendations"],
                "jd_skills_count": jd_skills_count,
            }

            status.update(label="✅ Analysis complete!", state="complete", expanded=False)

        st.rerun()

    except Exception as exc:
        st.error(f"❌ Analysis failed — {exc}")


# ===========================================================================
# RESULTS VIEW
# ===========================================================================

def _render_results(username: str) -> None:
    res   = st.session_state["last_result"]
    score = res["score"]
    color = format_score_color(score)
    label = format_score_label(score)

    # Heading
    st.markdown(
        f"<h2 style='color:#f1f5f9;font-size:1.6rem;font-weight:800;margin:0;'>"
        f"📊 Analysis Results</h2>"
        f"<p style='color:#64748b;font-size:0.85rem;margin:4px 0 16px;'>"
        f"📄 {res['resume_name']}</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Score row
    sc, mc = st.columns([1, 2.5], gap="large")
    with sc:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e293b,#0f172a);
                    border:2px solid {color};border-radius:18px;
                    padding:28px 16px;text-align:center;">
            <div style="font-size:3.2rem;font-weight:800;color:{color};
                        line-height:1;letter-spacing:-2px;">{score:.1f}%</div>
            <div style="font-size:0.8rem;font-weight:700;color:{color};
                        margin-top:8px;text-transform:uppercase;">{label}</div>
            <div style="font-size:0.7rem;color:#475569;margin-top:4px;">Overall Match</div>
        </div>
        """, unsafe_allow_html=True)

    with mc:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("✅ Matched",  len(res["matched"]))
        m2.metric("❌ Missing",  len(res["missing"]))
        m3.metric("➕ Extra",    len(res["extra"]))
        m4.metric("📋 JD Total", res["jd_skills_count"])
        # Dynamic progress bar color based on score
        _bar_color = "#F59E0B" if score < 50 else ("#3B82F6" if score < 75 else "#10B981")
        st.markdown(f"""
        <div style="margin-top:10px;">
            <div style="display:flex;justify-content:space-between;
                        align-items:center;margin-bottom:5px;">
                <span style="font-size:0.78rem;color:#94A3B8;font-weight:500;">
                    Overall Match Progress
                </span>
                <span style="font-size:0.85rem;font-weight:700;color:{_bar_color};">
                    {score:.1f}%
                </span>
            </div>
            <div style="background:#1E293B;border-radius:99px;height:10px;
                        overflow:hidden;">
                <div style="width:{score:.1f}%;background:{_bar_color};
                            height:100%;border-radius:99px;
                            transition:width 0.6s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Skills breakdown
    st.markdown("##### 🔍 Skills Breakdown")
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("**✅ Matched Skills**")
        st.markdown(_skill_badges(res["matched"], "#14532d", "#bbf7d0", "No matched skills"), unsafe_allow_html=True)
    with s2:
        st.markdown("**❌ Missing Skills**")
        st.markdown(_skill_badges(res["missing"], "#450a0a", "#fecaca", "No missing skills"), unsafe_allow_html=True)
    with s3:
        st.markdown("**➕ Extra Skills**")
        st.markdown(_skill_badges(res["extra"],   "#1e293b", "#94a3b8", "No extra skills"),   unsafe_allow_html=True)

    st.divider()

    # ── Dynamic Insights (Full Width) ────────────────────────────────────────
    is_strong = score >= 50 and len(res["matched"]) > 0
    
    if is_strong:
        st.markdown("##### 💪 Strength Summary")
        accent_color = "#10b981" # Emerald for strength
    else:
        st.markdown("##### ⚠️ Gap Analysis")
        accent_color = "#f59e0b" # Amber for gap/warning
        
    for s in res["insights"]:
        st.markdown(
            f"<div style='background:#1e293b;border-left:3px solid {accent_color};"
            f"border-radius:6px;padding:10px 14px;margin-bottom:8px;"
            f"font-size:0.85rem;color:#f8fafc;line-height:1.4;'>{s}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Text Recommendations (Full Width) ────────────────────────────────────
    st.markdown("##### 💡 Actionable Insights")
    for r in res["recommendations"]:
        st.markdown(
            f"<div style='background:#1e293b;border-left:3px solid #3b82f6;"
            f"border-radius:6px;padding:10px 14px;margin-bottom:8px;"
            f"font-size:0.85rem;color:#e0e7ff;line-height:1.5;'>{r}</div>",
            unsafe_allow_html=True,
        )
        
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Skill Recommendations (Pill Badges) ──────────────────────────────────
    st.markdown("##### 🎯 Recommended Skills to Acquire")
    st.markdown(
        _skill_badges(res["missing"], bg="#1e1b4b", text_color="#c7d2fe", empty_msg="No major skill gaps detected"), 
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── Courses & Certificates Recommendations ───────────────────────────────
    st.markdown("##### 🎓 Courses & Certificates Recommendations")
    st.caption("Adding these skills to your resume will boost 🚀 your chances of getting shortlisted!")

    if not res["missing"]:
        st.success("🎉 Great job! Your resume already covers all key skills for this role.")
    else:
        from src.courses_manager import get_course_recommendations
        limit = st.slider(
            "Choose Number of Course Recommendations:", 
            min_value=1, max_value=5, value=3, 
            key="course_limit_slider"
        )
        courses = get_course_recommendations(res["missing"], limit=limit)
        for i, course in enumerate(courses, 1):
            # Use raw HTML for target="_blank" safety, though markdown links technically open in new tab automatically in Streamlit, 
            # this is bulletproof for strict user requirements.
            c_html = (
                f"<div style='margin-bottom:8px;font-size:0.9rem;'>"
                f"<span style='font-weight:700;color:#94a3b8;'>({i})</span> "
                f"<a href='{course['url']}' target='_blank' style='color:#3b82f6;text-decoration:none;font-weight:600;'>{course['title']}</a> "
                f"<span style='color:#64748b;font-size:0.8rem;'> — {course['platform']}</span>"
                f"</div>"
            )
            st.markdown(c_html, unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 Analyze Another Resume", key="reset_btn"):
        st.session_state.pop("last_result", None)
        for k in ["resume_upload", "jd_text", "_jd_cache_name", "_jd_cache_text"]:
            st.session_state.pop(k, None)
        st.rerun()


# ===========================================================================
# SKILL BADGE HELPER
# ===========================================================================

def _skill_badges(skills: set, bg: str, text_color: str, empty_msg: str) -> str:
    """
    Return a self-contained HTML block: a scrollable flexbox container
    of pill badges — one per skill. Shows a muted empty-state badge if
    the skill set is empty.
    """
    if not skills:
        return (
            f"<div style='color:#475569;font-size:0.78rem;"
            f"font-style:italic;margin-top:4px;padding:4px 0;'>"
            f"— {empty_msg}"
            f"</div>"
        )

    badges = "".join(
        f"<span style='"
        f"display:inline-block;"
        f"background:{bg};"
        f"color:{text_color};"
        f"border-radius:20px;"
        f"padding:3px 10px;"
        f"margin:3px 4px 3px 0;"
        f"font-size:0.73rem;"
        f"font-weight:600;"
        f"white-space:nowrap;"
        f"'>{s.title()}</span>"
        for s in sorted(skills)
    )

    return (
        f"<div style='"
        f"display:flex;"
        f"flex-wrap:wrap;"
        f"gap:0;"
        f"max-height:180px;"
        f"overflow-y:auto;"
        f"padding:4px 0 6px;"
        f"scrollbar-width:thin;"
        f"scrollbar-color:#334155 transparent;"
        f"'>{badges}</div>"
    )
