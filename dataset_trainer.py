import os
from docx import Document
import re

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.lower()


def build_skill_database(dataset_path):

    all_text = ""

    for file in os.listdir(dataset_path):

        if file.endswith(".docx"):
            path = os.path.join(dataset_path, file)
            text = extract_text_from_docx(path)
            all_text += text + " "

    # Extract possible skills (basic keyword extraction)
    words = re.findall(r'\b[a-zA-Z\+\#\.]{2,}\b', all_text)

    # Remove common words
    stopwords = ["the","and","for","with","this","that","from","are","you"]
    skills = [w for w in words if w not in stopwords]

    # Get most frequent words
    from collections import Counter
    common_skills = Counter(skills).most_common(100)

    return [skill for skill, _ in common_skills]


if __name__ == "__main__":
    dataset_path = "Dataset"
    skills = build_skill_database(dataset_path)

    print("\nLearned Skills:\n")
    print(skills)

with open("learned_skills.txt", "w") as f:
    for skill in skills:
        f.write(skill + "\n")