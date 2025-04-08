import streamlit as st
import pdfplumber
import re
from typing import Set
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# ---------- SIDEBAR: Skill Input ----------
st.sidebar.title("🔧 Skill Configuration")
cskills = st.sidebar.text_area("Enter required skills (comma-separated):")
rskills = set(skill.strip().lower() for skill in cskills.split(",") if skill.strip())
# ---------- FUNCTIONS ----------
def etfpdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def ctext(text: str) -> str:
    text = re.sub(r"[^a-zA-Z ]", " ", text)  # remove everything except letters and spaces
    return text.lower()

def mskills(resumetxt, reqskills):
    words = set(resumetxt.split())  # unique words from resume
    found = words & reqskills     # matched skills
    missing = reqskills - found   # not found in resume
    return found, missing

# ---------- UI ----------
# st.set_page_config(page_title="AI Resume Analyzer", layout="centered")
st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and see how well it matches the job requirements.")

upfile = st.file_uploader("Choose your resume (PDF only):", type="pdf")

if upfile:
    resume_text = etfpdf(upfile)
    text = ctext(resume_text)
    fskills, msskills = mskills(text, rskills)

    score = int(len(fskills) / len(rskills) * 100) if rskills else 0

    st.subheader("✅ Match Report")
    st.write(f"**Match Score:** {score}%")
    st.write(f"**Skills Found:** {', '.join(sorted(fskills)) if fskills else 'None'}")
    st.write(f"**Missing Skills:** {', '.join(sorted(msskills)) if msskills else 'None'}")

    if score < 70:
        st.info("💡 For Considering add more relevant skills to improve your resume.")
    else:
        st.success("🎉 Great! Your resume looks well-aligned.")

