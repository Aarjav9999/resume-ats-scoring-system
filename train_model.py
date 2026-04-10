import os
from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

dataset_path = "Dataset"

texts = []
labels = []

# Assign labels based on folder or keyword (simple approach)
def detect_role(text):
    text = text.lower()

    if "data scientist" in text:
        return "Data Scientist"
    elif "data analyst" in text:
        return "Data Analyst"
    elif "machine learning" in text:
        return "ML Engineer"
    elif "developer" in text:
        return "Software Developer"
    else:
        return "Software Engineer"

for file in os.listdir(dataset_path):

    if file.endswith(".docx"):
        doc = Document(os.path.join(dataset_path, file))
        text = "\n".join([p.text for p in doc.paragraphs])

        role = detect_role(text)

        texts.append(text[:1000])   # limit size
        labels.append(role)

# Convert to embeddings
X = model.encode(texts)

# Train ML model
clf = RandomForestClassifier()
clf.fit(X, labels)

# Save model
joblib.dump(clf, "ml_role_model.pkl")

print("✅ Model trained and saved!")