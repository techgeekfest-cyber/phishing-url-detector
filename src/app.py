import streamlit as st
import joblib
import pandas as pd
from urllib.parse import urlparse
import re

# Load trained model
model = joblib.load("phishing_model.pkl")

st.title("🔐 AI Phishing URL Detector")

st.write("Enter a website URL to check whether it is phishing or legitimate.")

# Feature extractor
def extract_basic_features(url):
    features = {}

    parsed = urlparse(url)
    domain = parsed.netloc

    features["UsingIP"] = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+", domain) else -1
    features["LongURL"] = 1 if len(url) > 75 else -1
    features["Symbol@"] = 1 if "@" in url else -1
    features["PrefixSuffix-"] = 1 if "-" in domain else -1
    features["HTTPS"] = 1 if parsed.scheme == "https" else -1

    return features


url = st.text_input("Enter URL here:")

if url:

    features = extract_basic_features(url)

    expected_features = [
        "UsingIP",
        "LongURL",
        "Symbol@",
        "PrefixSuffix-",
        "HTTPS"
    ]

    sample_df = pd.DataFrame(
        [[features[f] for f in expected_features]],
        columns=expected_features
    )

    prediction = model.predict(sample_df)[0]
    confidence = model.predict_proba(sample_df)[0].max()

    if prediction == -1:
        st.error("⚠️ Phishing Website Detected")
    else:
        st.success("✅ Legitimate Website")

    
    st.write(f"Confidence: {confidence:.2f}")