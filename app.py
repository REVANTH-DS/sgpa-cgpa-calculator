import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="BTech SGPA & CGPA Calculator", layout="centered")

st.title("🎓 BTech SGPA & CGPA Calculator")

# --- SGPA Calculator ---
def calculate_sgpa(grades, credits):
    total_points = sum(g * c for g, c in zip(grades, credits))
    total_credits = sum(credits)
    if total_credits == 0:
        return 0
    return total_points / total_credits

# --- CGPA Calculator ---
def calculate_cgpa(sgpas, sem_credits):
    total_points = sum(s * c for s, c in zip(sgpas, sem_credits))
    total_credits = sum(sem_credits)
    if total_credits == 0:
        return 0
    return total_points / total_credits

# --- Streamlit Form Logic ---
st.sidebar.title("📘 Choose Calculator")
calc_type = st.sidebar.radio("Select Calculator", ["SGPA Calculator", "CGPA Calculator"])

sgpa = None
cgpa = None

if calc_type == "SGPA Calculator":
    st.header("📘 SGPA Calculator")

    num_subjects = st.number_input("Number of Subjects", min_value=1, max_value=20, step=1, value=5)
    grades = []
    credits = []

    for i in range(int(num_subjects)):
        col1, col2 = st.columns(2)
        with col1:
            grade = st.selectbox(f"Grade for Subject {i+1}", [10, 9, 8, 7, 6, 5, 4], key=f"grade_{i}")
        with col2:
            credit = st.number_input(f"Credits for Subject {i+1}", min_value=1, max_value=6, step=1, key=f"credit_{i}")
        grades.append(grade)
        credits.append(credit)

    if st.button("🎯 Calculate SGPA"):
        sgpa = calculate_sgpa(grades, credits)
        cgpa = sgpa  # assume same for display
        percentage = (sgpa - 0.75) * 10
        st.success(f"SGPA: {sgpa:.2f}")
        st.info(f"Assumed CGPA: {cgpa:.2f}")
        st.info(f"Percentage: {percentage:.2f}% | Grade: {sgpa:.0f} (based on 10)")

elif calc_type == "CGPA Calculator":
    st.header("📗 CGPA Calculator")
    num_sems = st.number_input("Number of Semesters", min_value=1, max_value=12, step=1, value=4)
    sgpas = []
    sem_credits = []

    for i in range(int(num_sems)):
        col1, col2 = st.columns(2)
        with col1:
            sgpa_val = st.number_input(f"SGPA of Sem {i+1}", min_value=0.0, max_value=10.0, step=0.1, key=f"sgpa_{i}")
        with col2:
            sem_credit = st.number_input(f"Credits of Sem {i+1}", min_value=1, max_value=40, step=1, key=f"sem_credit_{i}")
        sgpas.append(sgpa_val)
        sem_credits.append(sem_credit)

    if st.button("🎯 Calculate CGPA"):
        cgpa = calculate_cgpa(sgpas, sem_credits)
        percentage = (cgpa - 0.75) * 10
        st.success(f"CGPA: {cgpa:.2f}")
        st.info(f"Percentage: {percentage:.2f}%")

# --- PDF Download Section ---
if sgpa or cgpa:
    student_name = st.text_input("Enter Student Name")
    if student_name:
        if st.button("📄 Generate & Download PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="🎓 SGPA & CGPA Report", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Student Name: {student_name}", ln=True)
            if sgpa:
                pdf.cell(200, 10, txt=f"SGPA: {sgpa:.2f}", ln=True)
            if cgpa:
                pdf.cell(200, 10, txt=f"CGPA: {cgpa:.2f}", ln=True)

            pdf_buffer = io.BytesIO()
            pdf.output(pdf_buffer)
            pdf_bytes = pdf_buffer.getvalue()

            st.download_button(
                label="⬇️ Download Report as PDF",
                data=pdf_bytes,
                file_name="SGPA_CGPA_Report.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("Please enter your name to enable PDF download.")
