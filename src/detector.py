import pandas as pd

# Load dataset
data = pd.read_csv("data/phishing.csv")

# Separate features and labels
X = data.drop("class", axis=1)
y = data["class"]

# Show dataset info
print("Feature matrix shape:", X.shape)
print("Label vector shape:", y.shape)

# Show class distribution
print("\nClass distribution:")
print(y.value_counts())

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

import os
import joblib

if os.path.exists("phishing_model.pkl"):
    model = joblib.load("phishing_model.pkl")
    print("Loaded saved model!")
else:
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    joblib.dump(model, "phishing_model.pkl")
    print("Model trained and saved!")



# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt

# ROC Curve
y_prob = model.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test, y_prob, pos_label=1)
auc_score = roc_auc_score(y_test, y_prob)

plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")
plt.plot([0,1], [0,1], linestyle="--")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.savefig("roc_curve.png")
plt.close()

print("ROC curve saved as roc_curve.png")
print("\nModel Accuracy:", accuracy)

from sklearn.ensemble import RandomForestClassifier

# Train Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Predict with Random Forest
rf_pred = rf_model.predict(X_test)

# Evaluate Random Forest
rf_accuracy = accuracy_score(y_test, rf_pred)

print("\nRandom Forest Accuracy:", rf_accuracy)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Legitimate", "Phishing"],
            yticklabels=["Legitimate", "Phishing"])

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.savefig("confusion_matrix.png")
plt.close()

print("Confusion matrix saved as confusion_matrix.png")

import pandas as pd

# Show feature importance
feature_importance = pd.Series(model.coef_[0], index=X.columns)
feature_importance = feature_importance.sort_values(ascending=False)

print("\nTop 10 phishing indicators:\n")
print(feature_importance.head(10))

import sys
from urllib.parse import urlparse
import re


def extract_basic_features(url):
    from urllib.parse import urlparse
    import re

    features = {}

    parsed = urlparse(url)
    domain = parsed.netloc

    # Using IP address instead of domain
    features["UsingIP"] = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+", domain) else -1

    # Long URL detection
    features["LongURL"] = 1 if len(url) > 75 else -1

    # Presence of @ symbol
    features["Symbol@"] = 1 if "@" in url else -1

    # Dash in domain
    features["PrefixSuffix-"] = 1 if "-" in domain else -1

    # HTTPS usage
    features["HTTPS"] = 1 if parsed.scheme == "https" else -1

    # Suspicious keywords
    suspicious_keywords = ["login", "secure", "account", "verify", "update"]
    features["RequestURL"] = 1 if any(word in url.lower() for word in suspicious_keywords) else -1

    # URL shorteners
    shorteners = ["bit.ly", "tinyurl.com", "goo.gl"]
    features["ShortURL"] = 1 if any(service in url.lower() for service in shorteners) else -1

    return features
# Command-line URL prediction (prototype)
if len(sys.argv) > 1:
    print("\nChecking URL:", sys.argv[1])

    url = sys.argv[1]

features = extract_basic_features(url)

sample_df = pd.DataFrame([features])

# Fill missing columns with default value (-1)
for col in X.columns:
    if col not in sample_df:
        sample_df[col] = -1

sample_df = sample_df[X.columns]

prediction = model.predict(sample_df)

if prediction[0] == -1:
    print("⚠️ Phishing website detected")
else:
    print("✅ Legitimate website")