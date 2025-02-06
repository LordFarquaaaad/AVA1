from flask import Blueprint, request, jsonify
from app.blueprints.google_classroom.controllers import fetch_student_grades
from app.blueprints.reports.services import generate_student_report
from app.extensions import get_google_credentials  # Ensure this function is implemented
from app.blueprints.reports import reports_bp 

@reports_bp.route("/generate", methods=["POST"])
def generate_report():
    """Generate a report based on Google Classroom data."""
    
    # Assuming credentials are available (In production, store them securely)
    credentials = get_google_credentials()

    # Fetch student data
    student_data = fetch_student_grades(credentials)

    reports = {}

    for student_id, data in student_data.items():
        student_name = data["name"]
        courses = data["courses"]
        
        # You might need to extract year level separately based on Google Classroom data structure
        year_level = "Primary"  # Placeholder for now

        # Generate AI-generated report
        report = generate_student_report(student_name, year_level, courses)

        reports[student_name] = report

    return jsonify(reports)


