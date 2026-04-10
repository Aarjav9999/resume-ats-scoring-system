Resume ATS Scoring System

An AI-powered Resume ATS (Applicant Tracking System) Scoring System that analyzes resumes and evaluates their compatibility with job descriptions using Natural Language Processing (NLP) and Machine Learning techniques.

🚀 Overview

Recruiters use ATS systems to filter resumes before human review. This project simulates that process by:

Parsing resumes
Matching them against job descriptions
Assigning an ATS score
Providing improvement suggestions
🎯 Features
Resume parsing (PDF/DOCX)
Keyword extraction using NLP
Job description matching
ATS score calculation (%)
Skill gap analysis
Suggestions to improve resume ranking
🧠 Tech Stack
Python
Pandas
NumPy
Scikit-learn
NLTK / SpaCy
Matplotlib / Seaborn
Streamlit / Flask (optional UI)
⚙️ How It Works
Upload Resume
Enter Job Description
Text preprocessing (tokenization, stopword removal)
Feature extraction (TF-IDF / CountVectorizer)
Similarity calculation (Cosine Similarity)
Generate ATS Score & feedback
📊 Example Output
ATS Score: 78%
Matching Keywords: Python, Machine Learning, SQL
Missing Skills: Deep Learning, AWS
Suggestions: Add relevant projects and measurable achievements
