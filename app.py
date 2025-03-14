import streamlit as st
import re
import secrets
import string
from datetime import datetime, timedelta

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Blacklist Common Passwords
    common_passwords = ["password", "123456", "qwerty", "admin", "letmein"]
    if password.lower() in common_passwords:
        feedback.append("❌ This password is too common. Choose a stronger one.")
        score = 0  # Reset score if password is common

    # Strength Rating
    if score == 4:
        feedback.append("✅ Strong Password!")
    elif score == 3:
        feedback.append("⚠️ Moderate Password - Consider adding more security features.")
    else:
        feedback.append("❌ Weak Password - Improve it using the suggestions above.")

    return score, feedback

# Function to generate a strong password
def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(characters) for _ in range(12))
        score, _ = check_password_strength(password)
        if score == 4:
            return password

# Function to calculate password entropy
def calculate_entropy(password):
    import math
    charset_size = 0
    if re.search(r"[a-z]", password):
        charset_size += 26
    if re.search(r"[A-Z]", password):
        charset_size += 26
    if re.search(r"\d", password):
        charset_size += 10
    if re.search(r"[!@#$%^&*]", password):
        charset_size += 8
    entropy = len(password) * math.log2(charset_size) if charset_size else 0
    return entropy

# Streamlit App
st.title("Password Strength Meter 🔒")



# Input for password
password = st.text_input("Enter your password:", type="password")

# Password History
if "password_history" not in st.session_state:
    st.session_state.password_history = []
if password:
    st.session_state.password_history.append(password)
    if len(st.session_state.password_history) > 5:
        st.session_state.password_history.pop(0)
st.sidebar.subheader("Password History")
for pwd in st.session_state.password_history:
    st.sidebar.write(pwd)

# Check password strength
if password:
    score, feedback = check_password_strength(password)
    entropy = calculate_entropy(password)
    
    # Display progress bar
    st.progress(score / 4)
    
    # Display feedback
    st.subheader("Feedback:")
    for message in feedback:
        st.write(message)
    
    # Display entropy
    st.subheader("Password Entropy:")
    st.write(f"Entropy: {entropy:.2f} bits (Higher is better)")

    # Password Expiry Check
    expiry_date = datetime.now() - timedelta(days=90)
    st.subheader("Password Expiry Check:")
    st.write(f"Your password was last changed on: {expiry_date.strftime('%Y-%m-%d')}")
    if datetime.now() > expiry_date:
        st.warning("⚠️ Your password is too old. Consider changing it.")

# Password Generator
st.subheader("Need a strong password?")
if st.button("Generate Strong Password"):
    strong_password = generate_strong_password()
    st.success(f"Generated Password: `{strong_password}`")

# Footer
st.markdown("---")
st.markdown("© 2023 Password Strength Meter. All rights reserved.")