from __future__ import annotations


# ---------------------------------------------------------------------------
# 1. format_score_color()
# ---------------------------------------------------------------------------

def format_score_color(score: float) -> str:
    """
    Map a numeric match score to a Streamlit-friendly hex colour code.

    Thresholds:
        • >= 75 %  →  ``#22c55e``  (green  — strong match)
        • >= 50 %  →  ``#f59e0b``  (amber  — moderate match)
        •  < 50 %  →  ``#ef4444``  (red    — weak match)

    Args:
        score (float): Match score in the range 0–100.

    Returns:
        str: A CSS hex colour string (e.g. ``"#22c55e"``).

    Example:
        >>> color = format_score_color(82.5)
        >>> st.markdown(
        ...     f'<span style="color:{color};font-weight:700;">{82.5}%</span>',
        ...     unsafe_allow_html=True,
        ... )
    """
    if score >= 75:
        return "#22c55e"   # green
    if score >= 50:
        return "#f59e0b"   # amber
    return "#ef4444"       # red


def format_score_label(score: float) -> str:
    """
    Return a short textual status label for a match score.

    Args:
        score (float): Match score in the range 0–100.

    Returns:
        str: One of ``"Strong Match"``, ``"Moderate Match"``,
             or ``"Weak Match"``.
    """
    if score >= 75:
        return "Strong Match"
    if score >= 50:
        return "Moderate Match"
    return "Weak Match"


# ---------------------------------------------------------------------------
# 2. create_skill_chips_html()
# ---------------------------------------------------------------------------

def create_skill_chips_html(skills_set: set, bg_color: str = "#1e3a5f") -> str:
    """
    Generate inline HTML/CSS skill badge chips for rendering in Streamlit.

    Each skill is wrapped in a ``<span>`` with a rounded pill design.
    Pass the result to ``st.markdown(..., unsafe_allow_html=True)``.

    Args:
        skills_set (set): A set of skill name strings (e.g. from
                          ``extract_skills()``).  May be empty.
        bg_color   (str): CSS background colour for the chip
                          (default: ``"#1e3a5f"`` — dark blue).
                          The chip border is derived as a lighter shade of
                          the same colour automatically via a brightness
                          bump in the ``filter`` property.

    Returns:
        str: An HTML string containing all chips wrapped in a flex
             ``<div>``.  Returns an empty ``<span>`` with placeholder text
             if ``skills_set`` is empty.

    Example — green chips for matched skills::

        html = create_skill_chips_html(matched_skills, bg_color="#14532d")
        st.markdown(html, unsafe_allow_html=True)

    Example — red chips for missing skills::

        html = create_skill_chips_html(missing_skills, bg_color="#450a0a")
        st.markdown(html, unsafe_allow_html=True)
    """
    if not skills_set:
        return (
            "<span style='color:#64748b;font-size:0.85rem;font-style:italic;'>"
            "None</span>"
        )

    # Derive a border colour that is slightly lighter than the background.
    # We add a CSS filter on the chip container to avoid needing colour math.
    chip_style = (
        f"display:inline-block;"
        f"background:{bg_color};"
        f"color:#f1f5f9;"
        f"border:1px solid rgba(255,255,255,0.18);"
        f"border-radius:20px;"
        f"padding:3px 11px;"
        f"margin:3px 4px 3px 0;"
        f"font-size:0.78rem;"
        f"font-weight:500;"
        f"white-space:nowrap;"
    )

    chips = "".join(
        f'<span style="{chip_style}">{skill.title()}</span>'
        for skill in sorted(skills_set)
    )

    container_style = (
        "display:flex;"
        "flex-wrap:wrap;"
        "gap:2px;"
        "margin:6px 0;"
    )

    return f'<div style="{container_style}">{chips}</div>'
