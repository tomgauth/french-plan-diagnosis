import streamlit as st
import pandas as pd
from codaio import Coda, Document, Table, Cell
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Coda API key and document/table IDs
CODA_API_KEY = os.getenv("CODA_API_KEY")
DOC_ID = 'jPJTMi7bJR'
STUDENTS_TABLE_ID = 'grid-qqR8f6GhaA'  # Replace with the actual table ID for 'Students'
RESULTS_TABLE_ID = 'grid-eId76STakx'  # Replace with the actual table ID for 'Form Assessment Results'

# Initialize Coda client
coda = Coda(CODA_API_KEY)
doc = Document(DOC_ID, coda=coda)

# Get the students table
students_table = doc.get_table(STUDENTS_TABLE_ID)
results_table = doc.get_table(RESULTS_TABLE_ID)


# Function to check if a user exists in the 'Students' table by email
def check_user_in_coda(email):
    df = pd.DataFrame(students_table.to_dict())
    matching_row = df[df['student_email'] == email]
    return not matching_row.empty


# Function to add a user to the 'Students' table if they don't exist
def add_student(first_name, last_name, username, password, email, level):
    if not check_user_in_coda(email):
        cells = [
            Cell(column='first name', value_storage=first_name),
            Cell(column='last name', value_storage=last_name),
            Cell(column='Username', value_storage=username),
            Cell(column='password', value_storage=password),
            Cell(column='Email', value_storage=email),
            Cell(column='Date Joined', value_storage=pd.Timestamp.now().strftime('%Y-%m-%d')),
            Cell(column='Level', value_storage=level),
        ]
        students_table.upsert_row(cells)
        st.success(f"Student {first_name} {last_name} added to Coda.")
    else:
        st.warning(f"Student with email {email} already exists.")


# Helper function to add student if they don't exist and save their results
def add_student_if_needed_and_save_results(email, assessment_data):
    # Check if the user exists in the Students table
    user_exists = check_user_in_coda(email)
    
    # If the user doesn't exist, add them to the Students table
    if not user_exists:
        add_student(first_name="", last_name="", username="", password="", email=email, level=assessment_data["level"])
        st.success(f"New user with email {email} added to Coda.")

    # Save assessment results to the Form Assessment Results table, linked to the student
    save_results_to_coda(email, assessment_data)
    st.success(f"Assessment results saved for {email}.")


# Function to save form assessment results to the 'Form Assessment Results' table
def save_results_to_coda(email, assessment_data):
    # Find the student by email to link the result to the student
    df = pd.DataFrame(students_table.to_dict())
    matching_row = df[df['student_email'] == email]

    if not matching_row.empty:
        student_email = matching_row.iloc[0]['student_email']  # Get the student ID
        cells = [
            Cell(column='student_email', value_storage=student_email),
            Cell(column='assessment_date', value_storage=pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')),
            Cell(column='assessment_data', value_storage=str(assessment_data)),  # Store assessment data as JSON or string
        ]
        results_table.upsert_row(cells)
        st.success(f"Assessment results for {email} saved successfully.")
    else:
        st.error(f"No student found with email {email}.")


