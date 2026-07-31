from __future__ import annotations
import streamlit as st
from src.auth import register_user, authenticate_user


def render_auth_page() -> None:
    st.session_state.setdefault("auth_mode", "login")
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("username",  "")
    st.session_state.setdefault("full_name", "")

    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        # Hero
        st.markdown("""
        <div style="text-align:center;padding:36px 0 8px;">
            <div style="font-size:3.2rem;margin-bottom:6px;">🤖</div>
            <h1 style="font-size:1.9rem;font-weight:800;color:#f1f5f9;margin:0;
                       letter-spacing:-0.5px;">AI Resume Matcher</h1>
            <p style="color:#64748b;font-size:0.92rem;margin:8px 0 0 0;">
                Resume Screening &amp; Candidate Matching System
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            _render_login_form()
        else:
            _render_register_form()


def _render_login_form() -> None:
    # Card title — complete self-contained HTML
    st.markdown("""
    <div style="background:#1e293b;border:1px solid #334155;border-radius:16px;
                padding:22px 26px 6px;box-shadow:0 8px 32px rgba(0,0,0,0.45);">
        <h3 style="color:#f1f5f9;font-size:1.1rem;font-weight:700;margin:0 0 4px 0;
                   padding-bottom:12px;border-bottom:1px solid #334155;">
            🔐 Login to your Account
        </h3>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username",  placeholder="Enter your username...", key="login_user")
        password = st.text_input("Password",  type="password", placeholder="••••••••",  key="login_pass")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀  Login", use_container_width=True)

    if submitted:
        if not username.strip() or not password.strip():
            st.error("⚠️ Please enter both username and password.")
        elif authenticate_user(username.strip(), password):
            display = _display_name(username.strip())
            st.session_state.logged_in = True
            st.session_state.username  = username.strip()
            st.session_state.full_name = display
            st.session_state.pop("auth_mode", None)
            st.success(f"Welcome back, {display}! 👋")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(
            "<p style='color:#64748b;font-size:0.87rem;margin:8px 0 0 0;'>"
            "Don't have an account?</p>",
            unsafe_allow_html=True,
        )
    with c2:
        if st.button("Register here →", use_container_width=True, key="go_register"):
            st.session_state.auth_mode = "register"
            st.rerun()


def _render_register_form() -> None:
    st.markdown("""
    <div style="background:#1e293b;border:1px solid #334155;border-radius:16px;
                padding:22px 26px 6px;box-shadow:0 8px 32px rgba(0,0,0,0.45);">
        <h3 style="color:#f1f5f9;font-size:1.1rem;font-weight:700;margin:0 0 4px 0;
                   padding-bottom:12px;border-bottom:1px solid #334155;">
            📝 Create an Account
        </h3>
    </div>
    """, unsafe_allow_html=True)

    with st.form("register_form", clear_on_submit=False):
        full_name = st.text_input("Full Name",       placeholder="Jane Smith",         key="reg_name")
        username  = st.text_input("Username",         placeholder="Enter your username...", key="reg_user")
        password  = st.text_input("Password",         type="password",
                                  placeholder="Min. 6 characters",                    key="reg_pass")
        confirm   = st.text_input("Confirm Password", type="password",
                                  placeholder="Repeat password",                       key="reg_confirm")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("✅  Register", use_container_width=True)

    if submitted:
        err = _validate_register(full_name, username, password, confirm)
        if err:
            st.error(err)
        elif register_user(username.strip(), password):
            st.success(f"🎉 Account created for **{full_name.strip()}**! You can now log in.")
            st.session_state.auth_mode = "login"
            st.rerun()
        else:
            st.error("❌ Registration failed — that username may already be taken.")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    if st.button("← Back to Login", use_container_width=True, key="go_login"):
        st.session_state.auth_mode = "login"
        st.rerun()


def _validate_register(name: str, username: str, pw: str, confirm: str) -> str:
    if not name.strip():     return "Full name is required."
    if not username.strip(): return "Username is required."
    if len(pw) < 6:          return "Password must be at least 6 characters."
    if pw != confirm:        return "Passwords do not match."
    return ""


def _display_name(username: str) -> str:
    return username.replace(".", " ").replace("_", " ").title()
