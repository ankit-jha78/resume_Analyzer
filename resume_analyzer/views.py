from django.shortcuts import render
import pdfplumber  # PyMuPDF

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def extract_text_from_pdf(file):
    """Extract all text from uploaded PDF file"""
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # check if not None
                text += page_text + "\n"
    return text.strip()

def ask_gemini(prompt):
    """Send prompt to Gemini and return response"""
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

def simple_upload(request):
    response = None
    resume_text = ""
    job_description = ""

    if request.method == "POST":
        job_description = request.POST.get("job_description", "")
        resume_file = request.FILES.get("resume")
        action = request.POST.get("action")
        custom_question = request.POST.get("custom_question", "")

        # Extract resume text if file uploaded
        if resume_file:
            resume_text = extract_text_from_pdf(resume_file)

        # Handle actions
        if action == "resume_info" and resume_text:
            prompt = f"Read this resume:\n{resume_text}\n\nTell me what this resume is about in simple language."
            response = ask_gemini(prompt)

        elif action == "improve_skills" and resume_text and job_description:
            prompt = f"Based on the job description below, suggest how this person can improve their skills.\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
            response = ask_gemini(prompt)

        elif action == "missing_keywords" and resume_text and job_description:
            prompt = f"Compare the resume and job description. List keywords missing from the resume that are important in the job description.\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
            response = ask_gemini(prompt)

        elif action == "percentage_match" and resume_text and job_description:
            prompt = f"Rate how well this resume matches the job description on a scale of 1 to 100 and explain the reason.\n\nJob Description:\n{job_description}\n\nResume:\n{resume_text}"
            response = ask_gemini(prompt)

        elif action == "generate_questions" and resume_text:
            prompt = f"""
            You are an AI assistant that generates interview questions based on resume content.
            Resume: {resume_text}
            Task: Generate 15 relevant interview questions (mix of technical and behavioral).
            """
            response = ask_gemini(prompt)

        elif action == "custom_question_submit" and resume_text and custom_question:
            prompt = f"This is the resume:\n{resume_text}\n\nAnswer this question:\n{custom_question}"
            response = ask_gemini(prompt)

        else:
            response = "⚠️ Please upload a resume and provide job description if required."

    return render(request, "website/index.html", {"response": response})
