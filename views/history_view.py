"""
views/history_view.py  —  Analysis History Screen
==================================================
Displays previous resume analyses for the logged-in user.

Features:
    • Summary table (Resume, JD, Score, Date, Status)
    • Per-row "View Details" expander
    • Per-row "Delete" button
    • Empty-state message when no records exist

DESIGN RULE:
    Every st.markdown(unsafe_allow_html=True) call contains COMPLETE,
    self-contained HTML. Tags are NEVER split across calls.

Backend calls:
    src.database.get_user_history(username)        -> list[dict]
    src.database.delete_history(record_id, username) -> dict
    src.utils.format_score_color(score)            -> str
    src.utils.format_score_label(score)            -> str
    src.utils.create_skill_chips_html(skills, bg)  -> str
"""
from __future__ import annotations
import streamlit as st
from src.database import get_user_history, delete_history
from src.utils    import format_score_color, format_score_label, create_skill_chips_html


# ── Public entry point ──────────────────────────────────────────────────────

def render_history_page(username: str) -> None:
    """Render the full history view."""

    # Page heading (complete HTML)
    st.markdown(
        "<h2 style='color:#f1f5f9;font-size:1.7rem;font-weight:800;"
        "margin:0 0 4px 0;'>📋 Analysis History</h2>"
        "<p style='color:#64748b;font-size:0.86rem;margin:0 0 20px 0;'>"
        "All previous resume analyses for your account.</p>",
        unsafe_allow_html=True,
    )

    records = get_user_history(username)

    if not records:
        _render_empty_state()
        return

    # Summary stats
    scores = [r["match_score"] for r in records]
    c1, c2, c3 = st.columns(3)
    c1.metric("📊 Total Analyses",   len(records))
    c2.metric("📈 Avg Match Score",  f"{round(sum(scores)/len(scores), 1)}%")
    c3.metric("🏆 Best Match Score", f"{round(max(scores), 1)}%")

    st.divider()

    # Column headers (complete HTML)
    st.markdown("""
    <div style="display:grid;grid-template-columns:2fr 2fr 1fr 1.4fr 1fr 1fr 1fr;
                gap:8px;padding:8px 14px;background:#0f172a;
                border-radius:8px;margin-bottom:6px;">
        <span style="font-size:0.71rem;font-weight:700;color:#475569;
                     text-transform:uppercase;letter-spacing:0.07em;">Resume</span>
        <span style="font-size:0.71rem;font-weight:700;color:#475569;
                     text-transform:uppercase;letter-spacing:0.07em;">Job Description</span>
        <span style="font-size:0.71rem;font-weight:700;color:#475569;
                     text-transform:uppercase;letter-spacing:0.07em;">Score</span>
        <span style="font-size:0.71rem;font-weight:700;color:#475569;
                     text-transform:uppercase;letter-spacing:0.07em;">Date</span>
        <span style="font-size:0.71rem;font-weight:700;color:#475569;
                     text-transform:uppercase;letter-spacing:0.07em;">Status</span>
        <span style="font-size:0.71rem;font-weight:700;color:#475569;
                     text-transform:uppercase;letter-spacing:0.07em;">Details</span>
        <span style="font-size:0.71rem;font-weight:700;color:#475569;
                     text-transform:uppercase;letter-spacing:0.07em;">Delete</span>
    </div>
    """, unsafe_allow_html=True)

    # Rows
    for rec in records:
        _render_row(rec, username)


# ── Empty state ─────────────────────────────────────────────────────────────

def _render_empty_state() -> None:
    st.markdown("""
    <div style="background:#1e293b;border:1px dashed #334155;border-radius:16px;
                padding:48px 24px;text-align:center;margin-top:20px;">
        <div style="font-size:2.8rem;margin-bottom:12px;">📄</div>
        <h3 style="color:#f1f5f9;font-size:1rem;font-weight:700;margin:0 0 8px 0;">
            No analyses yet
        </h3>
        <p style="color:#64748b;font-size:0.85rem;margin:0;">
            Upload a resume and a job description on the Dashboard to run your first analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ── Single history row ───────────────────────────────────────────────────────

def _render_row(rec: dict, username: str) -> None:
    rid   = rec["id"]
    score = rec["match_score"]
    color = format_score_color(score)
    label = format_score_label(score)
    date  = rec["timestamp"][:10] if rec["timestamp"] else "—"

    # Status badge colours
    badge_bg  = {"Strong Match": "#14532d", "Moderate Match": "#422006", "Weak Match": "#450a0a"}
    badge_txt = {"Strong Match": "#86efac", "Moderate Match": "#fcd34d", "Weak Match": "#fca5a5"}

    resume_short = rec["resume_name"][:22] + "…" if len(rec["resume_name"]) > 24 else rec["resume_name"]
    jd_short     = rec["jd_name"][:22]    + "…" if len(rec["jd_name"])     > 24 else rec["jd_name"]

    # Row card (complete self-contained HTML)
    st.markdown(f"""
    <div style="background:#1e293b;border:1px solid #334155;border-radius:10px;
                padding:10px 14px;margin-bottom:4px;
                display:grid;grid-template-columns:2fr 2fr 1fr 1.4fr 1fr 1fr 1fr;
                gap:8px;align-items:center;">
        <span style="color:#e2e8f0;font-size:0.82rem;font-weight:500;
                     overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
              title="{rec['resume_name']}">📄 {resume_short}</span>
        <span style="color:#94a3b8;font-size:0.82rem;
                     overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
              title="{rec['jd_name']}">📋 {jd_short}</span>
        <span style="color:{color};font-weight:700;font-size:0.9rem;">{score:.1f}%</span>
        <span style="color:#64748b;font-size:0.78rem;">📅 {date}</span>
        <span style="background:{badge_bg.get(label,'#1e293b')};color:{badge_txt.get(label,'#e2e8f0')};
                     border-radius:20px;padding:2px 10px;font-size:0.71rem;font-weight:600;
                     white-space:nowrap;">{label}</span>
    </div>
    """, unsafe_allow_html=True)

    # Detail + delete columns (Streamlit widgets)
    _, dc, _, dl_col = st.columns([3.2, 1.3, 0.2, 1])

    with dc:
        with st.expander("View Details", expanded=False):
            _render_detail(rec)

    with dl_col:
        # Guard: only show delete once per record
        confirm_key = f"del_confirm_{rid}"
        btn_key     = f"del_btn_{rid}"

        if st.session_state.get(confirm_key):
            ok = st.button("✅ Confirm", key=f"del_ok_{rid}", use_container_width=True)
            if ok:
                result = delete_history(rid, username)
                if result["success"]:
                    st.success("Deleted.")
                else:
                    st.error(result["message"])
                st.session_state.pop(confirm_key, None)
                st.rerun()
        else:
            if st.button("🗑️ Delete", key=btn_key, use_container_width=True):
                st.session_state[confirm_key] = True
                st.rerun()

    st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)


# ── Detail panel ─────────────────────────────────────────────────────────────

def _render_detail(rec: dict) -> None:
    score = rec["match_score"]
    color = format_score_color(score)
    label = format_score_label(score)

    # Score line (complete HTML)
    st.markdown(
        f"<p style='font-size:0.8rem;color:#64748b;margin:0 0 12px 0;'>"
        f"<strong style='color:#e2e8f0;'>Match Score:</strong> "
        f"<span style='color:{color};font-weight:700;'>{score:.1f}% — {label}</span></p>",
        unsafe_allow_html=True,
    )

    # Parse comma-separated skill strings
    def _parse(s: str) -> set:
        return {x.strip() for x in s.split(",") if x.strip()} if s else set()

    matched = _parse(rec.get("matched_skills", ""))
    missing = _parse(rec.get("missing_skills", ""))
    extra   = _parse(rec.get("extra_skills",   ""))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<p style='color:#22c55e;font-weight:600;font-size:0.79rem;"
            "margin-bottom:4px;'>✅ Matched</p>",
            unsafe_allow_html=True,
        )
        st.markdown(create_skill_chips_html(matched, "#14532d"), unsafe_allow_html=True)
    with c2:
        st.markdown(
            "<p style='color:#ef4444;font-weight:600;font-size:0.79rem;"
            "margin-bottom:4px;'>❌ Missing</p>",
            unsafe_allow_html=True,
        )
        st.markdown(create_skill_chips_html(missing, "#450a0a"), unsafe_allow_html=True)
    with c3:
        st.markdown(
            "<p style='color:#f59e0b;font-weight:600;font-size:0.79rem;"
            "margin-bottom:4px;'>➕ Extra</p>",
            unsafe_allow_html=True,
        )
        st.markdown(create_skill_chips_html(extra, "#422006"), unsafe_allow_html=True)
