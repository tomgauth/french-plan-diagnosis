# main.py
import streamlit as st
from services.logic import calculate_phrases_to_learn
from services.display_results import display_results_on_page

# Frontend inputs
st.title("French Learning Plan Generator")

email = st.text_input("What's your email address?")
current_level = st.selectbox("What is your current French level?", ["A0.1", "A1", "A2", "B1", "B2"])

# Conversation goals (multiple selection)
conversations = st.multiselect(
    "Which conversations do you want to focus on?",
    ["Introduce yourself and talk about your life", "Talk about your weekend", "Explain in detail your journey learning French", 
    "Make a presentation at work", "Small talk with in-laws", "Be ready as an expat for doctor, post office, school, everyday things", 
    "Order in cafes and restaurants", "Speak French most of the time at home with my partner"]
)

# Select learning time per day (in minutes)
study_time = st.selectbox(
    "How long are you able to study per day?",
    [5, 10, 15, 20, 30, 45, 60, 90, 120]  # Max 2 hours (120 minutes)
)

# Select learning method
learning_method = st.selectbox(
    "What is your current method of learning?",
    ["None", "Flashcards", "Self-study (books/videos)", "Conversation lessons", "Other"]
)

# Are they taking conversation lessons?
taking_lessons = st.radio("Are you already taking conversation lessons?", ["Yes", "No"])

# When the user submits the form
if st.button("Generate Learning Plan"):
    # Calculate total phrases to learn based on their current level and goals
    total_phrases = calculate_phrases_to_learn(current_level, conversations)

    # Display the results on the page (logic to be added)
    display_results_on_page(email, current_level, conversations, total_phrases, study_time, learning_method, taking_lessons)
