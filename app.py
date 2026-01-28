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

# =========================================================
# EMAIL LOGIC
# =========================================================
def send_otp(receiver_email):
    otp = str(random.randint(100000, 999999))
    
    # Update these with your Gmail App Password for actual sending
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
# HOME PAGE
# =========================================================
if st.session_state.page == "home":
    st.title("🔒 CipherSphere")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.text_input("Email", key="l_email")
        st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            st.session_state.page = "dashboard"
            st.rerun()

    with tab2:
        signup_email = st.text_input("Email", key="s_email")
        signup_pass = st.text_input("Password", type="password", key="s_pass")
        signup_confirm = st.text_input("Confirm Password", type="password", key="s_confirm")

        if st.button("Register"):
            if signup_email and signup_pass == signup_confirm:
                st.session_state.user_email = signup_email
                st.session_state.page = "master_password"
                st.rerun()
            else:
                st.error("Passwords do not match or fields are empty")

# =========================================================
# MASTER PASSWORD PAGE
# =========================================================
elif st.session_state.page == "master_password":
    st.title("Create Master Password 🔐")
    mp = st.text_input("Master Password", type="password")
    cp = st.text_input("Confirm Master Password", type="password")

    if st.button("Create"):
        if mp == cp and mp != "":
            st.session_state.page = "email_verification"
            st.rerun()
        else:
            st.error("Passwords do not match")

# =========================================================
# EMAIL VERIFICATION PAGE (MODIFIED TO ALWAYS PROCEED)
# =========================================================
elif st.session_state.page == "email_verification":
    st.title("Verify Your Email 📧")
    
    if not st.session_state.otp_sent:
        st.write(f"OTP will be sent to **{st.session_state.user_email}**")
        if st.button("Send OTP"):
            try:
                # Attempt to send
                st.session_state.otp = send_otp(st.session_state.user_email)
                st.success("OTP sent!")
            except Exception as e:
                # Even if it fails (Bad Credentials), we set a dummy OTP and move on
                st.error(f"Google Error: {e}")
                st.warning("Switching to verification page anyway. (Use '000000' to test)")
                st.session_state.otp = "000000" 
            
            # This line ensures the next screen opens regardless of success/fail
            st.session_state.otp_sent = True
            st.rerun()

    else:
        st.info(f"Enter the code sent to {st.session_state.user_email}")
        user_otp = st.text_input("Enter OTP", placeholder="123456")

        if st.button("Verify OTP"):
            if user_otp == st.session_state.otp:
                st.success("Email Verified!")
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid OTP")
        
        if st.button("Back to Home"):
            st.session_state.otp_sent = False
            st.session_state.page = "home"
            st.rerun()

# =========================================================
# DASHBOARD
# =========================================================
elif st.session_state.page == "dashboard":
    st.title("🔓 Vault Dashboard")
    st.success(f"Welcome, {st.session_state.user_email}")
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()