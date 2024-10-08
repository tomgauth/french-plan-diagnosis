# services/display_results.py
import matplotlib.pyplot as plt
import streamlit as st
import io
from fpdf import FPDF

def generate_progress_graph_with_teacher(score, lessons_per_week, hours_per_week):
    weeks = list(range(1, 13))
    
    # Progress with teacher (faster learning rate)
    progress_with_teacher = [week * (score / 12) + lessons_per_week for week in weeks]

    # Progress without teacher (slower learning rate)
    progress_without_teacher = [week * (score / 24) for week in weeks]

    fig, ax = plt.subplots()
    ax.plot(weeks, progress_with_teacher, marker='o', linestyle='-', color='green', label="With Teacher")
    ax.plot(weeks, progress_without_teacher, marker='o', linestyle='--', color='red', label="Without Teacher")
    ax.set_title('Estimated Progress Over 12 Weeks')
    ax.set_xlabel('Week')
    ax.set_ylabel('Progress (in % of target words)')
    ax.legend()

    return fig

def display_results_on_page(email, current_level, target_level, score, learning_plan, lessons_per_week, hours_per_week):
    st.write(f"**Email:** {email}")
    st.write(f"**Current Level:** {current_level}")
    st.write(f"**Target Level:** {target_level}")
    st.write(f"**Total Score:** {score}")
    st.write(f"**Generated Learning Plan:** {learning_plan}")
    
    # Show progress graph
    st.write("### Estimated Progress Over Time")
    fig = generate_progress_graph_with_teacher(score, lessons_per_week, hours_per_week)
    st.pyplot(fig)

def generate_pdf_with_graph(email, learning_plan, score, lessons_per_week, hours_per_week, filename="learning_plan_with_graph.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # Add title and email
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Personalized Learning Plan", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.multi_cell(0, 10, f"Learning Plan:\n{learning_plan}")
    
    # Save progress graph to a buffer
    buf = io.BytesIO()
    fig = generate_progress_graph_with_teacher(score, lessons_per_week, hours_per_week)
    fig.savefig(buf, format="PNG")
    buf.seek(0)
    
    # Add graph to PDF
    pdf.image(buf, x=10, y=80, w=190)  # Adjust dimensions as needed
    
    pdf.output(filename)
    return filename