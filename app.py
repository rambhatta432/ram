import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(page_title="CipherSphere", page_icon="🔒", layout="centered")

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "otp" not in st.session_state:
    st.session_state.otp = ""
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "password_vault" not in st.session_state:
    st.session_state.password_vault = []  # List of dicts to store credentials

# =========================================================
# EMAIL LOGIC
# =========================================================
def send_otp(receiver_email):
    otp = str(random.randint(100000, 999999))
    SENDER_EMAIL = "yourgmail@gmail.com"
    SENDER_PASSWORD = "your_gmail_app_password" 

    msg = MIMEText(f"Your CipherSphere OTP is: {otp}")
    msg["Subject"] = "CipherSphere Email Verification"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    return otp

# =========================================================
# NAVIGATION LOGIC
# =========================================================

# --- 1. HOME PAGE ---
if st.session_state.page == "home":
    st.title("🔒 CipherSphere")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.text_input("Email", key="l_email")
        st.text_input("Password", type="password", key="l_pass")
        if st.button("Login", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    with tab2:
        signup_email = st.text_input("Email", key="s_email")
        signup_pass = st.text_input("Password", type="password", key="s_pass")
        signup_confirm = st.text_input("Confirm Password", type="password", key="s_confirm")
        if st.button("Register", use_container_width=True):
            if signup_email and signup_pass == signup_confirm:
                st.session_state.user_email = signup_email
                st.session_state.page = "master_password"
                st.rerun()
            else:
                st.error("Invalid input or passwords do not match")

# --- 2. MASTER PASSWORD PAGE ---
elif st.session_state.page == "master_password":
    st.title("Create Master Password 🔐")
    mp = st.text_input("Master Password", type="password")
    cp = st.text_input("Confirm Master Password", type="password")
    if st.button("Continue"):
        if mp == cp and mp != "":
            st.session_state.page = "email_verification"
            st.rerun()
        else:
            st.error("Passwords must match")

# --- 3. EMAIL VERIFICATION PAGE ---
elif st.session_state.page == "email_verification":
    st.title("Verify Your Email 📧")
    if not st.session_state.otp_sent:
        if st.button("Send OTP"):
            try:
                st.session_state.otp = send_otp(st.session_state.user_email)
                st.success("OTP sent!")
            except Exception as e:
                st.error(f"Gmail Error: {e}")
                st.warning("Proceeding with test code: 000000")
                st.session_state.otp = "000000" 
            st.session_state.otp_sent = True
            st.rerun()
    else:
        user_otp = st.text_input("Enter 6-digit Code")
        if st.button("Verify & Enter Vault"):
            if user_otp == st.session_state.otp:
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid OTP")

# --- 4. DASHBOARD (SEARCH & ADD PASSWORDS) ---
elif st.session_state.page == "dashboard":
    st.title("🔓 Your Secure Vault")
    st.write(f"Logged in as: **{st.session_state.user_email}**")
    
    # Sidebar for Navigation/Logout
    with st.sidebar:
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    # Layout for Search and Add
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("➕ Add New Credential")
        new_site = st.text_input("Website/App Name")
        new_user = st.text_input("Username/Email")
        new_pass = st.text_input("Password", type="password")
        
        if st.button("Save to Vault"):
            if new_site and new_user and new_pass:
                st.session_state.password_vault.append({
                    "site": new_site,
                    "user": new_user,
                    "pass": new_pass
                })
                st.success(f"Saved credentials for {new_site}!")
            else:
                st.warning("Please fill all fields")

    with col2:
        st.subheader("🔍 Search Vault")
        search_query = st.text_input("Search by Website Name")
        
        if search_query:
            results = [item for item in st.session_state.password_vault if search_query.lower() in item['site'].lower()]
            if results:
                for res in results:
                    with st.expander(f"📍 {res['site']}"):
                        st.write(f"**Username:** {res['user']}")
                        st.write(f"**Password:** `{res['pass']}`")
            else:
                st.info("No matching credentials found.")
        else:
            st.info("Enter a website name to search.")

    st.divider()
    st.subheader("📋 All Credentials")
    if not st.session_state.password_vault:
        st.write("Your vault is empty.")
    else:
        # Display as a table for clarity
        st.table(st.session_state.password_vault)
