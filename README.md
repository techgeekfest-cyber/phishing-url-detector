# Phishing URL Detector (AI + Cybersecurity Project)

This project detects whether a URL is phishing or legitimate using a Machine Learning model trained on security-related website features.

It combines Artificial Intelligence and Cybersecurity concepts to classify suspicious URLs based on structural indicators.

---

## Features

- Logistic Regression phishing detection model
- ~93% classification accuracy
- Command-line URL prediction support
- Feature importance analysis
- Saved trained model using joblib
- Real-time URL structure inspection

---

## Dataset

The dataset contains 11,000+ URLs with 30 phishing indicators such as:

- HTTPS usage
- URL length
- presence of @ symbol
- prefix-suffix in domain
- IP address usage
- traffic indicators
- domain age signals

---

## Project Structure
phishing-url-detector/
│
├── dataset/
│ └── phishing.csv
│
├── src/
│ └── detector.py
│
├── phishing_model.pkl
├── requirements.txt
├── README.md
└── venv/

## Installation

Clone the repository:


git clone <your-repository-link>

# Install dependencies:


pip install -r requirements.txt

# Run the detector:

python3 src/detector.py https://example.com

## Example Output

Checking URL: https://example.com

Legitimate website


---

## Model Details

Algorithm used:

- Logistic Regression

Accuracy achieved:

- ~93%

---

## Future Improvements

- Add more phishing feature extraction rules
- Build web interface version
- Deploy as browser extension
- Integrate real-time threat intelligence APIs

---

## Author

Built as part of a self-driven AI + Cybersecurity learning project.