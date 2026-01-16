import streamlit as st
from streamlit.runtime.scriptrunner import RerunException, RerunData

# ---------------------------
# 1. Page Configuration
# ---------------------------
st.set_page_config(page_title="CipherSphere", page_icon="🔒", layout="centered")

# ---------------------------
# 2. Session State for Navigation
# ---------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "new_user" not in st.session_state:
    st.session_state.new_user = False  # Flag for new signup

# ---------------------------
# 3. Custom CSS for styling
# ---------------------------
st.markdown("""
    <style>
    .main { background-color: white; color: #000; }
    .stTextInput>div>div>input { background-color: #f9f9f9; color: #000; }
    .css-1avcm0n .st-c8 { color: #007bff; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    [data-testid="stImage"] { display: flex; justify-content: center; }
    h1.ciphersphere { text-align: center; color: #007bff; font-size: 2.5em; font-weight: bold; }
    footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# 4. Master Password Pages
# ---------------------------

# If a new user just signed up → Create Master Password
if st.session_state.new_user:
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Create Your Master Password 🔒")
    
    master_pass = st.text_input("Master Password", type="password", key="new_master_pass")
    confirm_pass = st.text_input("Confirm Master Password", type="password", key="confirm_master_pass")
    
    if st.button("Set Master Password"):
        if master_pass and master_pass == confirm_pass:
            st.success("Master Password set successfully!")
            st.session_state.logged_in = True
            st.session_state.new_user = False  # Reset flag
            raise RerunException(RerunData())
        else:
            st.error("Passwords do not match or are empty.")

# If existing user logged in → Enter Master Password
elif st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Enter Your Master Password 🔒")
    master_pass = st.text_input("Master Password", type="password", key="master_pass_input")
    
    if st.button("Submit"):
        # Replace with actual master password validation
        if master_pass == "123456":  # Placeholder
            st.success(f"Access Granted! Welcome {st.session_state.user_email}")
        else:
            st.error("Incorrect Master Password")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        raise RerunException(RerunData())

# ---------------------------
# 5. Homepage with Login/Signup
# ---------------------------
else:
    # Logo Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=250)
        st.markdown("<h1 class='ciphersphere'>CipherSphere</h1>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Login/Signup Tabs
    tab1, tab2 = st.tabs(["Log In", "Sign Up"])

    # ----- Login Tab -----
    with tab1:
        st.subheader("Login to your account")
        email_log = st.text_input("Email", key="login_email", placeholder="example@mail.com")
        pass_log = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            if email_log and pass_log:
                st.session_state.logged_in = True
                st.session_state.user_email = email_log
                raise RerunException(RerunData())
            else:
                st.error("Please enter your credentials.")

    # ----- Sign Up Tab -----
    with tab2:
        st.subheader("Create a new account")
        new_user_email = st.text_input("Email", key="signup_email", placeholder="yourname@mail.com")
        new_pass = st.text_input("Password", type="password", key="signup_pass")
        confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        if st.button("Register"):
            if new_pass == confirm_pass and new_user_email:
                st.success("Account created successfully!")
                st.session_state.user_email = new_user_email
                st.session_state.new_user = True
                raise RerunException(RerunData())
            else:
                st.error("Passwords do not match or email is empty.")

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: grey;'>© 2026 CipherSphere</p>", unsafe_allow_html=True)
