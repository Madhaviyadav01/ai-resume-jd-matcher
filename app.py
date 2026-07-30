"""
app.py — AI Resume–JD Matcher | Main Entry Point
==================================================
Run:  streamlit run app.py

Author: AI Resume–JD Matcher (MCA Major Project)
"""

import streamlit as st
from src.database import init_db


# ── 1. Page config (must be first Streamlit call) ─────────────────────────
st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── 2. Global CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Background */
.stApp { background-color: #0f172a; color: #e2e8f0; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #1e293b;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important;
}

/* File uploader */
[data-testid="stFileUploadDropzone"] {
    background: #1e293b !important;
    border: 2px dashed #334155 !important;
    border-radius: 12px !important;
    color: #94a3b8 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 10px 24px;
    font-weight: 600;
    font-size: 0.93rem;
    transition: opacity 0.18s, transform 0.12s;
    width: 100%;
}
.stButton > button:hover  { opacity: 0.88; transform: translateY(-1px); }
.stButton > button:active { transform: translateY(0); }

/* Metrics */
[data-testid="stMetric"] {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 14px 18px;
}
[data-testid="stMetricValue"] { color: #38bdf8 !important; font-weight: 700; }
[data-testid="stMetricLabel"] { color: #64748b !important; font-size: 0.78rem; }

/* Progress bar */
.stProgress > div > div { background: linear-gradient(90deg,#2563eb,#7c3aed); border-radius:4px; }

/* Divider */
hr { border-color: #1e293b; margin: 12px 0; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #1e293b; border-radius: 10px; gap: 4px; }
.stTabs [data-baseweb="tab"]      { color: #94a3b8; border-radius: 8px; padding: 8px 16px; }
.stTabs [aria-selected="true"]    { background: #2563eb !important; color: #fff !important; }

/* Alerts */
.stSuccess { background: #14532d !important; color: #86efac !important; border-color: #16a34a !important; }
.stWarning { background: #422006 !important; color: #fcd34d !important; border-color: #d97706 !important; }
.stError   { background: #450a0a !important; color: #fca5a5 !important; border-color: #dc2626 !important; }
</style>
""", unsafe_allow_html=True)


# ── 3. Database init (once per process) ───────────────────────────────────
@st.cache_resource
def _init_database():
    init_db()
    return True

_init_database()


# ── 4. Session state defaults ─────────────────────────────────────────────
for _k, _v in {
    "logged_in"   : False,
    "username"    : "",
    "full_name"   : "",
    "current_page": "dashboard",
    "auth_mode"   : "login",
    "last_result" : None,
}.items():
    st.session_state.setdefault(_k, _v)


# ── 5. Router ─────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    from views.auth_view import render_auth_page
    render_auth_page()

else:
    username  = st.session_state.username
    full_name = st.session_state.full_name or username

    # ── Sidebar ───────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 12px;">
            <div style="font-size:2.2rem;">🤖</div>
            <div style="font-weight:800;font-size:1.1rem;color:#f1f5f9;
                        letter-spacing:-0.3px;margin-top:4px;">AI Resume Matcher</div>
            <div style="font-size:0.72rem;color:#475569;margin-top:2px;">Semantic Resume Matching System</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── Logged User card ──────────────────────────────────────────────
        st.markdown(
            f"<div style='background:#0f172a;border:1px solid #334155;"
            f"border-radius:10px;padding:10px 14px;margin-bottom:14px;'>"
            f"<div style='font-size:0.7rem;font-weight:700;color:#475569;"
            f"text-transform:uppercase;letter-spacing:0.07em;'>Logged User</div>"
            f"<div style='font-weight:700;color:#e2e8f0;font-size:0.96rem;"
            f"margin-top:4px;'>{username}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # ── Navigation ────────────────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.72rem;font-weight:700;color:#475569;"
            "text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;'>"
            "Navigation</p>",
            unsafe_allow_html=True,
        )
        page = st.radio(
            "nav",
            ["Dashboard", "History"],
            key="nav_radio",
            label_visibility="collapsed",
        )
        st.session_state.current_page = (
            "dashboard" if page == "Dashboard" else "history"
        )

        st.divider()

        # ── About ─────────────────────────────────────────────────────────
        st.markdown("### About")
        st.info(
            "**This tool helps you:**\n\n"
            "- Measures how your resume matches a job description\n"
            "- Identify important job keywords\n"
            "- Improve your resume based on missing terms"
        )

        # ── How It Works ──────────────────────────────────────────────────
        st.markdown("### How It Works")
        st.markdown(
            "1. Upload candidate resume(s)\n"
            "2. Paste the Job Description\n"
            "3. Click **Analyze Match**\n"
            "4. Review match score &amp; missing skills"
        )

        st.divider()

        # ── Logout ────────────────────────────────────────────────────────
        if st.button("Logout", key="logout_btn", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # ── Main content ──────────────────────────────────────────────────────
    if st.session_state.current_page == "dashboard":
        from views.matcher_view import render_matcher_page
        render_matcher_page(username, full_name)
    else:
        from views.history_view import render_history_page
        render_history_page(username)
