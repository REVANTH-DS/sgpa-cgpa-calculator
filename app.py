import streamlit as st
import pandas as pd
import altair as alt

# --- Page Config ---
st.set_page_config(page_title="BTech SGPA & CGPA Calculator", page_icon="🎓")
st.title("🎓 BTech SGPA & CGPA Calculator with Dashboard")

# --- Sidebar ---
st.sidebar.title("📘 Choose Calculator")
calc_type = st.sidebar.radio("Select Calculator", ["SGPA Calculator", "CGPA Calculator"])

# --- Grade Mapping ---
def get_grade_point(percentage):
    if percentage >= 90:
        return 10, "O"
    elif percentage >= 80:
        return 9, "A+"
    elif percentage >= 70:
        return 8, "A"
    elif percentage >= 60:
        return 7, "B+"
    elif percentage >= 50:
        return 6, "B"
    elif percentage >= 40:
        return 5, "C"
    else:
        return 0, "F"

def get_classification(cgpa):
    if cgpa >= 7.5:
        return "🎖️ Distinction"
    elif cgpa >= 6.0:
        return "✅ First Class"
    elif cgpa >= 5.0:
        return "⚠️ Second Class"
    else:
        return "❌ Fail / Not Eligible"

# --- SGPA Logic ---
def calculate_sgpa(subjects):
    total_weighted = 0
    total_credits = 0
    for sub in subjects:
        total_weighted += sub['grade_point'] * sub['credits']
        total_credits += sub['credits']
    return round(total_weighted / total_credits, 2) if total_credits != 0 else 0.0

# --- CGPA Logic ---
def calculate_cgpa(sgpa_list):
    return round(sum(sgpa_list) / len(sgpa_list), 2) if sgpa_list else 0.0

# ========================
# SGPA Calculator Section
# ========================
if calc_type == "SGPA Calculator":
    st.subheader("🧮 SGPA Calculator (Add subject marks + credits)")

    num_subjects = st.number_input("Enter number of subjects:", min_value=1, max_value=15, value=6, step=1)

    subjects = []
    data_for_chart = []

    for i in range(int(num_subjects)):
        st.markdown(f"### Subject {i+1}")
        marks = st.number_input(f"Marks Obtained", min_value=0.0, step=1.0, key=f"marks_{i}")
        max_marks = st.number_input(f"Maximum Marks", min_value=1.0, step=1.0, key=f"max_marks_{i}")
        credits = st.number_input(f"Credits", min_value=1, max_value=10, step=1, key=f"credits_{i}")

        if max_marks > 0:
            percentage = (marks / max_marks) * 100
            grade_point, grade_letter = get_grade_point(percentage)
            st.info(f"📊 Percentage: **{percentage:.2f}%** | Grade: **{grade_letter}** ({grade_point})")

            subjects.append({
                "credits": credits,
                "grade_point": grade_point,
                "percentage": percentage,
                "grade": grade_letter,
                "subject": f"Sub {i+1}"
            })

            data_for_chart.append({
                "Subject": f"Sub {i+1}",
                "Percentage": percentage,
                "Credits": credits,
                "Grade": grade_letter
            })

    if st.button("🎯 Calculate SGPA"):
        sgpa = calculate_sgpa(subjects)
        st.success(f"✅ Your SGPA is: **{sgpa}**")

        df_chart = pd.DataFrame(data_for_chart)

        st.subheader("📊 Subject Performance Dashboard")
        bar_chart = alt.Chart(df_chart).mark_bar().encode(
            x='Subject',
            y='Percentage',
            color='Grade',
            tooltip=['Subject', 'Percentage', 'Grade', 'Credits']
        ).properties(height=350)

        pie_chart = alt.Chart(df_chart).mark_arc().encode(
            theta=alt.Theta(field="Credits", type="quantitative"),
            color=alt.Color(field="Grade", type="nominal"),
            tooltip=['Subject', 'Credits', 'Grade']
        ).properties(height=350)

        st.altair_chart(bar_chart, use_container_width=True)
        st.altair_chart(pie_chart, use_container_width=True)

# ========================
# CGPA Calculator Section
# ========================
elif calc_type == "CGPA Calculator":
    st.subheader("📘 CGPA Calculator")

    num_semesters = st.number_input("Enter number of semesters", min_value=1, max_value=12, value=2, step=1)

    sgpas = []
    data = []

    for i in range(int(num_semesters)):
        sgpa = st.number_input(f"SGPA for Semester {i+1}", min_value=0.0, max_value=10.0, step=0.01, key=f"sgpa_{i}")
        sgpas.append(sgpa)
        data.append({"Semester": f"Sem {i+1}", "SGPA": sgpa})

    if st.button("🎯 Calculate CGPA"):
        cgpa = calculate_cgpa(sgpas)
        classification = get_classification(cgpa)

        st.success(f"✅ Your CGPA is: **{cgpa}**")
        st.info(f"📘 Classification: **{classification}**")

        df = pd.DataFrame(data)

        st.subheader("📈 CGPA Dashboard – Semester Trend")
        line_chart = alt.Chart(df).mark_line(point=True).encode(
            x='Semester',
            y='SGPA',
            tooltip=['Semester', 'SGPA']
        ).properties(height=350)

        st.altair_chart(line_chart, use_container_width=True)
        from fpdf import FPDF

def generate_pdf(student_name, sgpa, cgpa):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, txt="STX SGPA & CGPA Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Student Name: {student_name}", ln=True)
    pdf.cell(200, 10, txt=f"SGPA: {sgpa:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"CGPA: {cgpa:.2f}", ln=True)

    return pdf.output(dest="S").encode("latin1")

# Add download button
student_name = st.text_input("Enter Student Name")

if st.button("📄 Download Report as PDF"):
    if student_name and sgpa and cgpa:
        pdf_bytes = generate_pdf(student_name, sgpa, cgpa)
        st.download_button(label="Download Report",
                           data=pdf_bytes,
                           file_name="STX_Report_Card.pdf",
                           mime="application/pdf")
    else:
        st.warning("Please enter Student Name and ensure SGPA/CGPA are calculated.")


