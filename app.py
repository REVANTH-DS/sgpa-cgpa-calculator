import streamlit as st
from fpdf import FPDF

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="CGPA & SGPA Calculator",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 CGPA & SGPA Calculator")

# -------------------- Grade Point Mapping --------------------
grade_point_map = {
    "O (10)": 10,
    "A+ (9)": 9,
    "A (8)": 8,
    "B+ (7)": 7,
    "B (6)": 6,
    "C (5)": 5,
    "F (0)": 0,
    "Ab (0)": 0
}

# -------------------- Defaults --------------------
sgpa = None
cgpa = None

# -------------------- Calculator Selection --------------------
st.sidebar.header("Choose Calculator")
calc_option = st.sidebar.radio("Select Calculator", ["SGPA Calculator", "CGPA Calculator"])

# -------------------- SGPA CALCULATOR --------------------
if calc_option == "SGPA Calculator":
    st.subheader("SGPA Calculator")

    num_subjects = st.number_input("Enter Number of Subjects", min_value=1, max_value=20, step=1)

    grades = []
    credits = []

    grade_options = list(grade_point_map.keys())

    for i in range(int(num_subjects)):
        col1, col2 = st.columns([2, 1])
        with col1:
            grade = st.selectbox(f"Grade for Subject {i+1}", grade_options, key=f"grade_{i}")
            grades.append(grade)
        with col2:
            credit = st.number_input(f"Credits for Subject {i+1}", min_value=1, max_value=10, step=1, key=f"credit_{i}")
            credits.append(credit)

    if st.button("🎯 Calculate SGPA"):
        total_credits = 0
        total_grade_points = 0

        for i in range(int(num_subjects)):
            grade = grades[i]
            credit = credits[i]
            grade_point = grade_point_map[grade]

            total_credits += credit
            total_grade_points += grade_point * credit

        if total_credits == 0:
            st.error("Total credits cannot be zero.")
        else:
            sgpa = total_grade_points / total_credits
            cgpa = sgpa  # For now, assume CGPA = SGPA

            percentage = (sgpa - 0.75) * 10 if sgpa > 0.75 else 0
            st.success(f"SGPA: {sgpa:.2f}")
            st.info(f"Assumed CGPA: {cgpa:.2f}")
            st.info(f"Percentage: {percentage:.2f}% | Grade: {grades[0]}")

# -------------------- CGPA CALCULATOR --------------------
elif calc_option == "CGPA Calculator":
    st.subheader("CGPA Calculator")

    num_sems = st.number_input("Enter Number of Semesters Completed", min_value=1, max_value=12, step=1)

    sem_sgpas = []
    sem_credits = []

    for i in range(int(num_sems)):
        col1, col2 = st.columns([2, 1])
        with col1:
            sgpa_sem = st.number_input(f"SGPA for Sem {i+1}", min_value=0.0, max_value=10.0, step=0.01, key=f"sgpa_{i}")
            sem_sgpas.append(sgpa_sem)
        with col2:
            credit_sem = st.number_input(f"Credits for Sem {i+1}", min_value=1, max_value=40, step=1, key=f"credit_sem_{i}")
            sem_credits.append(credit_sem)

    if st.button("📈 Calculate CGPA"):
        total_credits = sum(sem_credits)
        weighted_sgpas = sum([sem_sgpas[i] * sem_credits[i] for i in range(int(num_sems))])

        if total_credits == 0:
            st.error("Total credits cannot be zero.")
        else:
            cgpa = weighted_sgpas / total_credits
            percentage = (cgpa - 0.75) * 10 if cgpa > 0.75 else 0
            st.success(f"CGPA: {cgpa:.2f}")
            st.info(f"Percentage: {percentage:.2f}%")

# -------------------- PDF EXPORT --------------------
if sgpa is not None or cgpa is not None:
    student_name = st.text_input("Enter Student Name")

    if st.button("📄 Download Report as PDF"):
        def generate_pdf(student_name, sgpa, cgpa):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)

            pdf.cell(200, 10, txt="CGPA & SGPA Report", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Student Name: {student_name}", ln=True)
            if sgpa is not None:
                pdf.cell(200, 10, txt=f"SGPA: {sgpa:.2f}", ln=True)
            if cgpa is not None:
                pdf.cell(200, 10, txt=f"CGPA: {cgpa:.2f}", ln=True)

            return pdf.output(dest="S").encode("latin1")

        if student_name:
            pdf_bytes = generate_pdf(student_name, sgpa, cgpa)
            st.download_button(
                label="⬇️ Download Report",
                data=pdf_bytes,
                file_name="Report_Card.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Please enter your name before downloading the PDF.")
