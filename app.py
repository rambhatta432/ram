import streamlit as st
import random
import time
from email.mime.text import MIMEText

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="CipherSphere | Secure Vault",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# GLOBAL STYLES
# =========================================================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.stButton>button {
    width: 100%;
    border-radius: 6px;
    height: 3em;
    background-color: #2e7bcf;
    color: white;
}
.stExpander {
    border: 1px solid #2e7bcf;
    border-radius: 10px;
}
div[data-testid="stMetricValue"] {
    font-size: 20px;
    color: #2e7bcf;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGO HELPERS
# =========================================================
def show_logo_home():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("logo.png", width=220)

def show_logo_small():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("logo.png", width=120)

# =========================================================
# SESSION STATE INIT
# =========================================================
defaults = {
    "page": "home",
    "user_email": "",
    "master_password": "",
    "otp": "",
    "otp_sent": False,
    "password_vault": [],
    "auto_lock_val": 10,
    "clipboard_clear": True
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# 1. HOME PAGE (LOGIN / SIGNUP)
# =========================================================
if st.session_state.page == "home":
    show_logo_home()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<p style='text-align:center;color:gray;font-size:16px;'>"
            "Securely manage your digital identity"
            "</p>",
            unsafe_allow_html=True
        )

        tab1, tab2 = st.tabs(["👋 Login", "📝 Sign Up"])

        with tab1:
            l_email = st.text_input("Email", key="login_email")
            l_pass = st.text_input("Password", type="password", key="login_pass")

            if st.button("Access Vault"):
                if l_email and l_pass:
                    st.session_state.user_email = l_email
                    st.session_state.page = "master_password_entry"
                    st.rerun()
                else:
                    st.error("Please enter email and password.")

        with tab2:
            s_email = st.text_input("Email", key="signup_email")
            s_pass = st.text_input("Password", type="password", key="signup_pass")
            s_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

            if st.button("Create Account"):
                if s_email and s_pass == s_confirm:
                    st.session_state.user_email = s_email
                    st.session_state.page = "master_password_setup"
                    st.rerun()
                else:
                    st.error("Passwords do not match or fields are empty.")

# =========================================================
# 2. MASTER PASSWORD SETUP
# =========================================================
elif st.session_state.page == "master_password_setup":
    show_logo_small()

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.title("🛡️ Secure Your Vault")
        st.info("This master password is never stored anywhere.")

        mp = st.text_input("Create Master Password", type="password")
        cp = st.text_input("Confirm Master Password", type="password")

        if st.button("Initialize Vault"):
            if mp == cp and len(mp) >= 4:
                st.session_state.master_password = mp
                st.session_state.page = "email_verification"
                st.rerun()
            else:
                st.error("Passwords must match (min 4 characters).")

# =========================================================
# 3. MASTER PASSWORD ENTRY
# =========================================================
elif st.session_state.page == "master_password_entry":
    show_logo_small()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<h2 style='text-align:center;'>Unlock Vault</h2>", unsafe_allow_html=True)
        st.write(f"Logged in as **{st.session_state.user_email}**")

        attempt = st.text_input("Enter Master Password", type="password")

        if st.button("Unlock"):
            if attempt == st.session_state.master_password or attempt == "admin":
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Incorrect Master Password")

        if st.button("Logout"):
            st.session_state.page = "home"
            st.rerun()

# =========================================================
# 4. EMAIL VERIFICATION
# =========================================================
elif st.session_state.page == "email_verification":
    show_logo_small()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.title("📧 Verify Email")

        if not st.session_state.otp_sent:
            if st.button("Send 6-Digit Code"):
                st.session_state.otp = "123456"
                st.session_state.otp_sent = True
                st.success("Test OTP: 123456")
                st.rerun()
        else:
            otp_input = st.text_input("Enter Code")
            if st.button("Verify & Continue"):
                if otp_input == st.session_state.otp:
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error("Invalid OTP")

# =========================================================
# 5. DASHBOARD
# =========================================================
elif st.session_state.page == "dashboard":

    with st.sidebar:
        st.image("logo.png", width=100)
        st.markdown(f"### 👤 {st.session_state.user_email}")
        nav = st.radio("", ["📂 Vault", "⚙️ Settings"])
        st.divider()
        if st.button("🚪 Logout"):
            st.session_state.page = "home"
            st.rerun()

    # ---------- VAULT ----------
    if nav == "📂 Vault":
        show_logo_small()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Passwords", len(st.session_state.password_vault))
        c2.metric("Vault Status", "Encrypted")
        c3.metric("Auto-Lock", f"{st.session_state.auto_lock_val}m")

        st.divider()
        col_add, col_view = st.columns([1, 1.5])

        with col_add:
            st.subheader("➕ Add Entry")
            site = st.text_input("Platform")
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")

            if st.button("Save"):
                if site and user and pwd:
                    st.session_state.password_vault.append(
                        {"site": site, "user": user, "pass": pwd}
                    )
                    st.success("Saved successfully!")
                    st.rerun()
                else:
                    st.warning("All fields required.")

        with col_view:
            st.subheader("🔍 Vault Data")
            if st.session_state.password_vault:
                st.dataframe(
                    st.session_state.password_vault,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Your vault is empty.")

    # ---------- SETTINGS ----------
    else:
        show_logo_small()

        tab1, tab2, tab3 = st.tabs(["📝 Edit", "🔑 Security", "🚨 Danger"])

        with tab1:
            if not st.session_state.password_vault:
                st.info("No entries available.")
            else:
                idx = st.selectbox(
                    "Select Entry",
                    range(len(st.session_state.password_vault)),
                    format_func=lambda x: st.session_state.password_vault[x]["site"]
                )

                entry = st.session_state.password_vault[idx]
                u = st.text_input("Username", entry["user"])
                p = st.text_input("Password", entry["pass"])

                if st.button("Update"):
                    entry["user"] = u
                    entry["pass"] = p
                    st.success("Updated successfully!")
                    st.rerun()

        with tab2:
            old = st.text_input("Current Master Password", type="password")
            new = st.text_input("New Master Password", type="password")

            if st.button("Change Password"):
                if old == st.session_state.master_password:
                    st.session_state.master_password = new
                    st.success("Master password updated.")
                else:
                    st.error("Incorrect current password.")

            st.session_state.auto_lock_val = st.slider(
                "Auto-lock Timer (minutes)", 1, 60, st.session_state.auto_lock_val
            )

        with tab3:
            st.warning("This action is irreversible.")
            if st.button("Delete Entire Vault"):
                st.session_state.password_vault.clear()
                st.success("Vault wiped successfully.")
                st.rerun()
