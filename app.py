import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="CipherSphere",
    page_icon="🚀",
    layout="centered"
)

# 2. Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }

    h1, h2, h3, h4, h5, h6, label, p {
        color: #222222;
    }

    .stButton > button {
        width: 100%;
        height: 3em;
        background-color: #007BFF;
        color: white;
        border-radius: 6px;
        border: none;
        font-size: 16px;
    }

    .stTextInput input {
        border-radius: 6px;
    }

    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Logo + Welcome Section
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("https://via.placeholder.com/140", width=140)
    st.markdown(
        "<h1 style='text-align:center; color:#007BFF;'>CipherSphere</h1>"
        "<p style='text-align:center; color: #555;'>Please login or create an account</p>",
        unsafe_allow_html=True
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# 4. Login & Signup BELOW
tab1, tab2 = st.tabs(["🔐 Log In", "📝 Sign Up"])

# -------- LOGIN TAB --------
with tab1:
    st.markdown("### Login to your account")
    email_log = st.text_input("Email Address", placeholder="example@mail.com", key="login_email_tab1")
    pass_log = st.text_input("Password", type="password", key="login_pass_tab1")

    if st.button("Login", key="login_button_tab1"):
        if email_log and pass_log:
            st.success(f"Welcome back, {email_log}!")
        else:
            st.error("Please enter both email and password.")

# -------- SIGNUP TAB --------
with tab2:
    st.markdown("### Create a new account")
    new_user = st.text_input("Email Address", placeholder="yourname@mail.com", key="signup_email_tab2")
    new_pass = st.text_input("Password", type="password", key="signup_pass_tab2")
    confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm_tab2")

    if st.button("Register", key="signup_button_tab2"):
        if not new_user or not new_pass:
            st.error("All fields are required.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        else:
            st.success("Account created successfully!")

# 5. Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color: #777;'>© 2026 CipherSphere</p>",
    unsafe_allow_html=True
)
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="CipherSphere",
    page_icon="🚀",
    layout="wide"
)

# 2. Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }

    h1 {
        color: #007BFF;
        text-align: center;
        margin-bottom: 10px;
    }

    .stButton>button {
        width: 100%;
        height: 2.5em;
        background-color: #007BFF;
        color: white;
        border-radius: 6px;
        border: none;
        font-size: 14px;
    }

    .stTextInput>div>div>input {
        border-radius: 6px;
        height: 2em;
    }

    .box {
        border: 1px solid #ddd;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
    }

    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }

    .footer {
        text-align: center;
        color: #777;
        margin-top: 30px;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header with Logo
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div class="center">
    <img src="logo.jpg" width="100"><br>
    <h1>CipherSphere</h1>
</div>
""", unsafe_allow_html=True)

# 4. Layout: Login and Signup side by side
col1, col2, col3 = st.columns([1, 2, 1])  # center layout

with col2:
    # Container for both boxes
    st.markdown('<div class="center">', unsafe_allow_html=True)

    # -------- LOGIN BOX --------
    st.markdown('<div class="box" style="width: 280px; margin-right: 20px;">', unsafe_allow_html=True)
    st.markdown("### Log In", unsafe_allow_html=True)
    email_log = st.text_input("Email Address", placeholder="example@mail.com", key="login_email")
    pass_log = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login", key="login_button"):
        if email_log and pass_log:
            st.success(f"Welcome back, {email_log}!")
        else:
            st.error("Please enter both email and password.")
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- SIGNUP BOX --------
    st.markdown('<div class="box" style="width: 280px; margin-left: 20px;">', unsafe_allow_html=True)
    st.markdown("### Sign Up", unsafe_allow_html=True)
    new_user = st.text_input("Email Address", placeholder="yourname@mail.com", key="signup_email")
    new_pass = st.text_input("Password", type="password", key="signup_pass")
    confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm")
    if st.button("Register", key="signup_button"):
        if not new_user or not new_pass:
            st.error("All fields are required.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match.")
        else:
            st.success("Account created successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # end container

# 5. Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="footer">© 2026 CipherSphere</div>', unsafe_allow_html=True)
