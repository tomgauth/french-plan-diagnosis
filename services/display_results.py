# services/display_results.py
import matplotlib.pyplot as plt
import streamlit as st
from fpdf import FPDF
import io
from services.logic import calculate_learning_speed, calculate_time_to_goal
import numpy as np


def logistic_curve(x, L, k, x0):
    """
    Logistic function to simulate an S-curve progression.
    L: Maximum value (total phrases)
    k: Growth rate
    x0: Midpoint (the week where the learning rate starts to slow)
    """
    return L / (1 + np.exp(-k * (x - x0)))
    return L / (1 + np.exp(-k * (x - x0)))

def display_results_on_page(email, current_level, conversations, total_phrases, study_time, learning_method, taking_lessons):
    # Display basic info
    st.write(f"**Email:** {email}")
    st.write(f"**Current Level:** {current_level}")
    st.write(f"**Conversation Goals:** {', '.join(conversations)}")
    st.write(f"**Total Phrases to Learn:** {total_phrases}")

    # Calculate learning speed and time to goal
    learning_speed = calculate_learning_speed(learning_method, taking_lessons)
    days_to_goal, weeks_to_goal = calculate_time_to_goal(total_phrases, study_time, learning_speed)

    # Display learning time estimate
    st.write(f"**Study Time per Day:** {study_time} minutes")
    st.write(f"**Learning Method:** {learning_method}")
    st.write(f"**Are you taking conversation lessons?** {taking_lessons}")
    st.write(f"**Estimated Time to Reach Your Goal:** {days_to_goal:.1f} days (~{weeks_to_goal:.1f} weeks)")

    # Create a progress graph (showing the estimated phrases learned over time)
    st.write("### Progress Graph: Estimated Phrases Learned Over Time")

    # Generate the data for the graph using logistic S-curve
    weeks = np.linspace(1, weeks_to_goal, int(weeks_to_goal))  # Create a list of weeks
    phrases_learned = logistic_curve(weeks, total_phrases, 0.03, weeks_to_goal / 2)  # S-curve learning

    # Plot the graph using Matplotlib
    fig, ax = plt.subplots()
    ax.plot(weeks, phrases_learned, color="green", label="Phrases Learned")
    ax.set_title("Estimated Learning Progress (S-curve)")
    ax.set_xlabel("Weeks")
    ax.set_ylabel("Phrases Learned")
    
    # Add a buffer at the top
    ax.set_ylim(0, total_phrases * 1.1)  # 10% buffer at the top
    
    # Set limits for the X-axis (weeks)
    ax.set_xlim(0, weeks_to_goal)
    
    # Remove the box around the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Display the graph
    st.pyplot(fig)

def generate_progress_graph(score):
    # Assuming the score corresponds to a number of weeks
    # Let's assume 12 weeks as an example for the learning plan
    weeks = list(range(1, 13))
    progress = [week * (score / 12) for week in weeks]  # Progress increases each week

    # Create a graph using Matplotlib
    fig, ax = plt.subplots()
    ax.plot(weeks, progress, marker='o', linestyle='-', color='b')
    ax.set_title('Estimated Progress Over 12 Weeks')
    ax.set_xlabel('Week')
    ax.set_ylabel('Progress (%)')
    ax.set_ylim([0, 100])

    return fig

def generate_pdf_with_graph(email, learning_plan, score, filename="learning_plan_with_graph.pdf"):
    # Generate a PDF with the learning plan and graph
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
    fig = generate_progress_graph(score)
    fig.savefig(buf, format="PNG")
    buf.seek(0)
    
    # Add graph to PDF
    pdf.image(buf, x=10, y=80, w=190)  # Adjust dimensions as needed
    
    # Output the PDF
    pdf.output(filename)
    return filename
