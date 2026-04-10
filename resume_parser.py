import PyPDF2
import spacy
import re

# Load NLP model
nlp = spacy.load("en_core_web_sm")


# -------------------------
# Extract Text
# -------------------------
def extract_text(file):

    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


# -------------------------
# Skills Database
# -------------------------
# AUTO-LOADED SKILLS (from dataset)
skills_db = []

try:
    with open("learned_skills.txt", "r") as f:
        skills_db = [line.strip() for line in f.readlines()]
except:
    skills_db = ["python","sql","machine learning","data analysis"]


# -------------------------
# Extract Skills
# -------------------------
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in skills_db:
        if skill.lower() in text:
            found_skills.append(skill.lower())

    return list(set(found_skills))


# -------------------------
# Extract Name
# -------------------------
def extract_name(text):

    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Name not clearly detected"


# -------------------------
# Extract Contact
# -------------------------
def extract_contact(text):

    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    phone = re.findall(r"\+?\d[\d\s\-]{8,}\d", text)

    email_val = email[0] if email else ""
    phone_val = phone[0] if phone else ""

    return f"{email_val} | {phone_val}"


# -------------------------
# Detect Title
# -------------------------
def detect_title(text):

    titles = [

    "data scientist","data analyst","machine learning engineer",

    "full stack developer","software engineer",
    "backend developer","frontend developer",

    "cloud engineer","cloud developer","aws engineer",

    "cybersecurity analyst","security engineer","ethical hacker",

    "devops engineer"
    ]

    text = text.lower()

    for title in titles:
        if title in text:
            return title.title()

    return "Software Professional"


# -------------------------
# Extract Education
# -------------------------
def extract_education(text):

    education_keywords = [
        "b.tech","bachelor","m.tech","mba",
        "b.sc","bca","mca","b.e"
    ]

    education = []
    lines = text.split("\n")

    for line in lines:
        for word in education_keywords:
            if word in line.lower():
                education.append(line.strip())

    return education


# -------------------------
# Extract Projects (FIXED)
# -------------------------
def extract_projects(text):

    lines = text.split("\n")

    projects = []
    capture = False

    for line in lines:

        l = line.lower().strip()

        if "project" in l:
            capture = True
            continue

        if capture:

            # stop when new section starts
            if any(x in l for x in [
                "education",
                "certification",
                "skills",
                "experience",
                "summary"
            ]):
                break

            if len(line.strip()) > 5:
                projects.append(line.strip())

    return projects


# -------------------------
# Extract Certifications (FIXED)
# -------------------------
def extract_certifications(text):

    lines = text.split("\n")

    certs = []
    capture = False

    for line in lines:

        l = line.lower().strip()

        if "certification" in l:
            capture = True
            continue

        if capture:

            if any(x in l for x in [
                "project",
                "education",
                "skills",
                "experience"
            ]):
                break

            if len(line.strip()) > 5:
                certs.append(line.strip())

    return certs


# -------------------------
# Extract Summary
# -------------------------
def extract_summary(text):

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if len(lines) >= 3:
        return lines[:3]

    return lines


# -------------------------
# MAIN PARSER
# -------------------------
def parse_resume(file):

    text = extract_text(file)

    word_count = len(text.split())

    data = {

        "name": extract_name(text),

        "title": detect_title(text),

        "contact": extract_contact(text),

        "summary": extract_summary(text),

        "skills": extract_skills(text),

        "education": extract_education(text),

        "projects": extract_projects(text),

        "certifications": extract_certifications(text),

        "word_count": word_count,

        "raw_text": text

    }

    return data