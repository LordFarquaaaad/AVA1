from flask import request, jsonify
from app.blueprints.reports import reports_bp
from app.models import Course, Grade, Assignment
from .services import generate_student_report

@reports_bp.route("/generate", methods=["POST"])
def generate_report():
    data = request.json
    student_name = data.get("student_name")
    student_email = data.get("student_email")
    year_level = data.get("year_level")

    if not student_name or not student_email or not year_level:
        return jsonify({"error": "Student name, email, and year level are required"}), 400

    # Fetch courses and grades for the student
    courses = []
    for course in Course.query.all():
        assignments = Assignment.query.filter_by(course_id=course.id).all()
        course_data = {
            "name": course.name,
            "average_grade": 0,
            "assignments": []
        }
        total_score = 0
        total_points = 0

        for assignment in assignments:
            grade = Grade.query.filter_by(assignment_id=assignment.id, student_email=student_email).first()
            if grade:
                course_data["assignments"].append({
                    "title": assignment.title,
                    "score": grade.score,
                    "max_points": assignment.max_points
                })
                total_score += grade.score
                total_points += assignment.max_points

        if total_points > 0:
            course_data["average_grade"] = round((total_score / total_points) * 100, 2)
            courses.append(course_data)

    if not courses:
        return jsonify({"error": f"No data found for student {student_name}"}), 404

    # Generate the report
    report = generate_student_report(student_name, year_level, courses)
    return jsonify({"report": report})

