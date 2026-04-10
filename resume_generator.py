import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_resume(data):

    os.makedirs("generated_resumes", exist_ok=True)
    file_path = "generated_resumes/improved_resume.pdf"

    c = canvas.Canvas(file_path, pagesize=letter)

    # Page width
    width, height = letter

    # ===== HEADER =====
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height-60, data["name"])

    c.setFont("Helvetica", 12)
    c.drawString(50, height-80, data["title"])

    c.setFont("Helvetica", 10)
    c.drawString(50, height-100, data["contact"])

    # ===== LEFT COLUMN =====
    y = height-150

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "SUMMARY")

    y -= 20
    c.setFont("Helvetica", 10)
    for line in data["summary"]:
        c.drawString(50, y, line)
        y -= 15

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "EDUCATION")

    y -= 20
    c.setFont("Helvetica", 10)
    for edu in data["education"]:
        c.drawString(50, y, edu)
        y -= 15

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "CERTIFICATIONS")

    y -= 20
    for cert in data["certifications"]:
        c.drawString(50, y, cert)
        y -= 15

    # ===== RIGHT COLUMN =====
    y = height-150

    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y, "SKILLS")

    y -= 20
    c.setFont("Helvetica", 10)

    for skill in data["skills"]:
        c.drawString(350, y, skill)
        y -= 15

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y, "PROJECTS")

    y -= 20
    for project in data["projects"]:
        c.drawString(350, y, project)
        y -= 15

    c.save()

    return file_path