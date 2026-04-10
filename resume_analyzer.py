import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------------
# DOMAIN SKILLS (STRONG)
# -------------------------
DOMAIN_SKILLS = {
    "data_scientist": [
        "python","pandas","numpy","matplotlib","seaborn",
        "scikit-learn","sklearn","machine learning","deep learning",
        "nlp","tensorflow","keras","statistics","sql","eda"
    ],
    "data_analyst": [
        "sql","excel","power bi","tableau",
        "data analysis","dashboard","reporting","statistics"
    ],
    "ml_engineer": [
        "machine learning","tensorflow","keras","scikit-learn",
        "model deployment","flask","fastapi","api"
    ],
    "cloud_developer": [
        "aws","azure","gcp","ec2","s3","lambda",
        "docker","kubernetes","terraform","jenkins",
        "ci/cd","devops","linux","microservices"
    ],
    "devops_engineer": [
        "docker","kubernetes","jenkins","ci/cd",
        "terraform","ansible","linux","aws"
    ],
    "backend_developer": [
        "python","java","node","django","flask",
        "spring boot","rest api","sql","mongodb"
    ],
    "frontend_developer": [
        "html","css","javascript","react",
        "angular","vue","bootstrap"
    ],
    "fullstack_developer": [
        "html","css","javascript","react",
        "node","mongodb","sql","api"
    ],
    "software_engineer": [
        "java","python","c++","oop",
        "data structures","algorithms"
    ],
    "ai_engineer": [
        "deep learning","nlp","tensorflow",
        "pytorch","computer vision"
    ]
}

# -------------------------
# NORMALIZE
# -------------------------
def normalize(text):
    if not isinstance(text, str):
        return ""
    return text.lower()

# -------------------------
# SKILL MATCH (STRICT)
# -------------------------
def extract_skills(text, skills):
    found = set()
    for skill in skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)
    return found

# -------------------------
# DOMAIN DETECTION (STRICT)
# -------------------------
def detect_domain(text):
    text = normalize(text)
    scores = {}
    for domain, skills in DOMAIN_SKILLS.items():
        count = sum(1 for skill in skills if skill in text)
        scores[domain] = count
    best_domain = max(scores, key=scores.get)
    return best_domain, scores

# -------------------------
# FINAL ATS SCORE
# -------------------------
def analyze_resume(resume_text, jd_text):
    resume_text = normalize(resume_text)
    jd_text = normalize(jd_text)

    # Detect domains
    resume_domain, resume_scores = detect_domain(resume_text)
    jd_domain, jd_scores = detect_domain(jd_text)

    jd_skills = DOMAIN_SKILLS[jd_domain]
    resume_skills = extract_skills(resume_text, jd_skills)

    matched = len(resume_skills)
    total = len(jd_skills)
    skill_match_ratio = matched / total if total else 0

    # -------------------------
    # SEMANTIC SIMILARITY
    # -------------------------
    emb1 = model.encode([resume_text])
    emb2 = model.encode([jd_text])
    similarity = cosine_similarity(emb1, emb2)[0][0]

    # -------------------------
    # STRICT SCORING LOGIC
    # -------------------------
    if resume_domain != jd_domain:
        final_score = (skill_match_ratio * 40 + similarity * 20)
    else:
        final_score = (skill_match_ratio * 80 + similarity * 20)
    final_score = round(final_score, 2)

    # -------------------------
    # MISSING SKILLS
    # -------------------------
    missing_skills = list(set(jd_skills) - set(resume_skills))

    # -------------------------
    # WEAKNESSES
    # -------------------------
    weaknesses = []
    if len(missing_skills) == 0:
        weaknesses.append("Profile is well aligned with the job description")
    elif len(missing_skills) == 1:
        weaknesses.append(f"Minor gap: missing {missing_skills[0]}")
    elif len(missing_skills) <= 3:
        weaknesses.append(f"Some gaps detected: {', '.join(missing_skills)}")
    else:
        weaknesses.append("Significant skill gaps detected for this role")

    if len(resume_text.split()) < 100:
        weaknesses.append("Resume content could be improved")

    # -------------------------
    # STRENGTHS
    # -------------------------
    strengths = list(resume_skills)[:6]

    return {
        "ATS_score": final_score,
        "Resume_Role": resume_domain,
        "JD_Role": jd_domain,
        "Skill_Match_%": round(skill_match_ratio * 100, 2),
        "strengths": strengths,
        "missing_skills": missing_skills[:10],
        "weaknesses": weaknesses
    }