import streamlit as st
import pickle
import numpy as np
import re

# Load the trained model
with open("random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)

# ✅ List of well-known SAFE websites
SAFE_SITES = [
    "javatpoint.com", "wikipedia.org", "github.com",
    "google.com", "amazon.com", "microsoft.com", "apple.com",
    "facebook.com", "twitter.com", "linkedin.com", "youtube.com"
]

# Function to extract domain name from URL
def get_domain(url):
    domain = re.sub(r"https?://(www\.)?", "", url).split("/")[0]
    return domain

# Function to extract 30 features from a URL
def extract_features_from_url(url):
    features = []
    features.append(len(url))  # URL length
    features.append(1 if "https" in url else 0)  # HTTPS presence
    features.append(url.count("."))  # Number of dots in URL
    features.append(url.count("/"))  # Number of slashes
    features.append(url.count("-"))  # Number of hyphens
    features.append(url.count("@"))  # Presence of '@'
    features.append(url.count("?"))  # Number of question marks
    features.append(url.count("="))  # Number of equals signs
    features.append(url.count("&"))  # Number of ampersands
    features.append(url.count("_"))  # Number of underscores
    features.append(url.count("%"))  # Number of percent signs
    features.append(url.count("#"))  # Number of hash signs
    features.append(url.count("+"))  # Number of plus signs
    features.append(url.count("www"))  # Presence of 'www'
    features.append(url.count("com"))  # Presence of 'com'
    features.append(len(re.findall(r"\d", url)))  # Number of digits
    features.append(1 if "ip" in url.lower() else 0)  # Presence of 'IP'
    features.append(1 if "login" in url.lower() else 0)  # Presence of 'login'
    features.append(1 if "bank" in url.lower() else 0)  # Presence of 'bank'
    features.append(1 if "secure" in url.lower() else 0)  # Presence of 'secure'
    features.append(1 if "paypal" in url.lower() else 0)  # Presence of 'paypal'
    features.append(1 if "ebay" in url.lower() else 0)  # Presence of 'ebay'
    features.append(1 if "facebook" in url.lower() else 0)  # Presence of 'facebook'
    features.append(1 if "twitter" in url.lower() else 0)  # Presence of 'twitter'
    features.append(1 if "google" in url.lower() else 0)  # Presence of 'google'
    features.append(1 if "apple" in url.lower() else 0)  # Presence of 'apple'
    features.append(1 if "microsoft" in url.lower() else 0)  # Presence of 'microsoft'
    features.append(1 if "amazon" in url.lower() else 0)  # Presence of 'amazon'
    features.append(1 if "dropbox" in url.lower() else 0)  # Presence of 'dropbox'
    features.append(1 if "drive" in url.lower() else 0)  # Presence of 'drive'

    return np.array([features])

# Streamlit UI
st.set_page_config(page_title="Phishing Website Detector", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #ff4b4b;'>🔎 Phishing Website Detector</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-size:18px;'>Enter a website URL below to check if it's safe or a phishing site.</p>",
    unsafe_allow_html=True
)

# Input field
url = st.text_input("🌍 Enter Website URL:", placeholder="https://example.com")

if st.button("Check Website 🔍"):
    if url:
        domain = get_domain(url)  # Extract domain name
        input_data = extract_features_from_url(url)

        # ✅ Feature count validation
        if input_data.shape[1] != model.n_features_in_:
            st.warning(f"⚠ Feature mismatch! Model expects {model.n_features_in_} features, but got {input_data.shape[1]}.")
            st.stop()

        # 🔍 Debugging log: Show extracted features
        st.write(f"Extracted Features: {input_data}")

        # Make prediction
        prediction = model.predict(input_data)

        # 🔍 Debugging log: Show model prediction
        st.write(f"Model Prediction: {prediction[0]}")  

        # ✅ Override model if it's a well-known SAFE site
        if domain in SAFE_SITES:
            st.success(f"✅ This website **({domain})** is **Safe**.")
        elif prediction[0] in [-1, 1]:  
            st.error(f"🚨 **Warning! This website ({domain}) is a PHISHING website. Do not enter any personal information.**")
        else:
            st.success(f"✅ This website **({domain})** is **Safe**.")
    else:
        st.warning("⚠ Please enter a valid URL.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Developed by Lav Saxena</p>", unsafe_allow_html=True)
