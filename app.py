from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from resume_analyzer import analyze_resume

app = Flask(__name__)


# -------------------------
# HOME ROUTE
# -------------------------
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        # Get file + JD
        file = request.files.get('resume')
        job_description = request.form.get('job_description', '')

        resume_text = ""

        # -------------------------
        # EXTRACT TEXT FROM PDF
        # -------------------------
        if file:
            try:
                reader = PdfReader(file)

                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text + " "

            except Exception as e:
                return f"Error reading PDF: {str(e)}"

        # -------------------------
        # SAFETY CHECK
        # -------------------------
        if not resume_text.strip():
            return "Error: Resume text could not be extracted."

        if not job_description.strip():
            return "Error: Please enter a job description."

        # -------------------------
        # ANALYZE RESUME
        # -------------------------
        analysis = analyze_resume(resume_text, job_description)

        return render_template('index.html', analysis=analysis)

    return render_template('index.html')


# -------------------------
# RUN APP
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)