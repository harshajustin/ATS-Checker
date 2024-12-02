from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

from gemini_response import get_gemini_response
from process_pdf import process_uploaded_pdf

# Load environment variables
load_dotenv()

# Configure generative AI
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Google API Key not found. Please set it in the .env file.")
genai.configure(api_key=API_KEY)

def create_streamlit_ui():
    """
    Creates the Streamlit interface for ATS Resume Expert.
    """
    st.set_page_config(page_title="ATS Resume Expert", layout="wide")
    st.title("📑 ATS Resume Expert")
    st.markdown(
        "Optimize your resume for Applicant Tracking Systems (ATS) and get professional feedback instantly."
    )

    # Inputs
    input_text = st.text_area(
        "Job Description:", 
        key="input", 
        help="Paste the job description here for evaluation.",
        height=150)
    uploaded_file = st.file_uploader(
        "Upload Your Resume (PDF format only):", 
        type=["pdf"]
    )

    # Success message if resume is uploaded
    if uploaded_file:
        st.success("Resume uploaded successfully!", icon="✅")

    # Prompts for AI evaluation
    prompts = {
        "Tell Me About the Resume": """
        Assume the role of a seasoned Technical Human Resource Manager with expertise in hiring for technical roles. 
        Carefully review the provided resume in the context of the job description. Identify and elaborate on:
        - The candidate's key strengths and qualifications relevant to the role.
        - Any gaps, weaknesses, or areas for improvement in meeting the job requirements.
        Provide a balanced and professional assessment to guide both candidate and hiring decisions.
        """,
        
        "How Can I Improve My Skills": """
        As a career coach specializing in professional development and upskilling, analyze the provided resume and job description. 
        Offer actionable suggestions to enhance the candidate's profile, including:
        - Skills to acquire or improve.
        - Relevant certifications or training programs to pursue.
        - Experiences or projects to undertake that align with industry expectations.
        Tailor your advice to help the candidate stand out in their target field.
        """,
        
        "Percentage Match": """
        Act as a highly accurate and analytical ATS (Applicant Tracking System) scanner. 
        Compare the resume against the job description and provide a detailed report, including:
        1. The percentage match between the resume and job requirements.
        2. A list of critical keywords or skills missing from the resume.
        3. Professional recommendations for optimizing the resume to improve alignment with the job description.
        Ensure your feedback is specific, actionable, and focused on maximizing the candidate's chances of selection.
        """,
        
        "Generate Cold Email": """
        Imagine you are a motivated and resourceful recent graduate eager to make a strong impression on potential employers. 
        Write a concise, professional, and persuasive cold email to the client regarding the specified job. 
        The email should:
        - Convey enthusiasm for the role and alignment with the company's goals.
        - Highlight relevant skills, academic background, and unique contributions.
        - Include personal details such as your full name, degree, and contact information.
        - Be structured, direct, and impactful, leaving a lasting positive impression.
        Tailor the tone to be both professional and approachable.
        """
        }

    # Buttons for user actions
    actions = list(prompts.keys())
    selected_action = st.radio("Choose an Action:", actions, horizontal=True)

    if st.button("Submit"):
        if uploaded_file:
            try:
                pdf_content = process_uploaded_pdf(uploaded_file)
                response = get_gemini_response(input_text, pdf_content, prompts[selected_action])
                display_response(f"{selected_action} Result:", response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload a resume to proceed.")

def display_response(title, response):
    """
    Displays the AI-generated response in the Streamlit app.
    """
    st.subheader(title)
    if response:
        if title == "Generate Cold Email Result:":
            st.code(response, language="text")
        else:
            st.write(response) 
    else:
        st.error("No response received from the AI model.")

if __name__ == "__main__":
    create_streamlit_ui()
