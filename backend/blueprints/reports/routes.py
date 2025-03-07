from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from backend.blueprints.google_classroom.controllers import sync_classroom_data
from backend.blueprints.reports.services import generate_report_from_user_input, generate_report_from_classroom_data, suggest_ai_comments, generate_bulk_reports, generate_student_report
from backend.extensions import get_google_credentials
from backend.models import StudentSubmission, Assignment, Course, Template
from datetime import datetime
from backend.blueprints.reports import reports_bp

# Report Generation Endpoints

@reports_bp.route("/reports/generate", methods=["POST"])
@jwt_required()
def generate_report():
    """
    Generate reports for students using AI, optionally using custom templates.
    Request Body: {students: [{name, schoolLevel, categories, templateId}]}
    """
    try:
        data = request.get_json()
        print(f"📥 Received Data: {data}")  # Log incoming request

        if not data or "students" not in data:
            return jsonify({"error": "Invalid request, 'students' key missing"}), 400

        # Get user ID from JWT
        user_id = get_jwt_identity()
        jwt_data = get_jwt()
        username = jwt_data.get("username")  # Assuming username is in additional claims

        reports = []
        for student in data["students"]:
            name = student.get("name", "Unnamed Student")
            schoolLevel = student.get("schoolLevel", "Primary School")
            categories = student.get("categories", {})

            # Optionally load and apply a template (e.g., based on templateId in studentsData)
            template_id = student.get("templateId")  # Add this to studentsData if using a template
            if template_id:
                template = Template.query.get(template_id)
                if template and template.teacher_id == int(user_id):  # Use user_id from JWT
                    categories = {**categories, **template.categories}  # Merge template categories

            # Validate categories data
            if not isinstance(categories, dict):
                return jsonify({"error": f"Invalid 'categories' format for {name}"}), 400

            # Generate AI-enhanced report using generate_student_report
            student_report = generate_student_report({
                "name": {"value": name},
                "academicPerformance": {"value": categories.get("academicPerformance", {}).get("value", "Meets Expectations")},
                "behaviorAttitude": {"value": categories.get("behaviorAttitude", {}).get("value", "Generally Well-Behaved")},
                "participationEngagement": {"value": categories.get("participationEngagement", {}).get("value", "Participates Regularly")},
                "effortWorkEthic": {"value": categories.get("effortWorkEthic", {}).get("value", "Usually Meets Deadlines")},
                "socialEmotionalDevelopment": {"value": categories.get("socialEmotionalDevelopment", {}).get("value", "Works Well with Others")},
                "attendancePunctuality": {"value": categories.get("attendancePunctuality", {}).get("value", "Rarely Absent")},
                "comments": {"value": categories.get("comments", {}).get("comments", "").strip() or ""}
            })

            reports.append({"name": name, "report": student_report})

        return jsonify({"reports": reports})
    except Exception as e:
        print(f"❌ Error generating reports: {e}")
        return jsonify({"error": "Failed to generate reports"}), 500

@reports_bp.route("/reports/generate-bulk", methods=["POST"])
@jwt_required()
def generate_bulk():
    """API route to generate multiple student reports in bulk using the same function."""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided in the request."}), 400

        students = data.get("students", [])
        if not students:
            return jsonify({"error": "No students provided."}), 400

        # Get user ID from JWT (not used directly here but included for consistency)
        user_id = get_jwt_identity()

        reports = generate_bulk_reports(students)
        return jsonify({"reports": reports})

    except Exception as e:
        print(f"Error in bulk report generation: {e}")
        return jsonify({"error": f"An error occurred while generating reports: {str(e)}"}), 500

@reports_bp.route("/")
@jwt_required()
def view_reports():
    """Render the reports page."""
    # Since this is a GET route rendering a template, we might not need JWT for rendering
    # but we'll keep it for authentication. Adjust frontend to handle token if needed.
    jwt_data = get_jwt()
    username = jwt_data.get("username")  # Assuming username is in additional claims
    return render_template("reports.html", username=username)

@reports_bp.route("/reports/generate/google/classroom", methods=["POST"])
@jwt_required()
def generate_report_classroom_1():
    """Generate a report based on Google Classroom data stored in the database."""
    try:
        print("🔍 Starting report generation...")

        # Get user ID from JWT
        user_id = get_jwt_identity()

        # Step 1: Retrieve credentials
        credentials = get_google_credentials()
        if not credentials:
            print("❌ Failed to load credentials!")
            return jsonify({"error": "Failed to load credentials"}), 401

        print("✅ Credentials loaded successfully.")

        # Step 2: Sync the latest Google Classroom data before generating reports
        print("🔄 Syncing Google Classroom data...")
        sync_result = sync_classroom_data(credentials)
        if "error" in sync_result:
            print(f"❌ Sync failed: {sync_result['error']}")
            return jsonify(sync_result), 500  # Return error if sync fails

        print("✅ Sync completed successfully.")

        # Step 3: Fetch student data from the database
        print("📡 Fetching student grades from the database...")
        student_data = {}

        submissions = StudentSubmission.query.all()
        for submission in submissions:
            student_id = submission.student_id
            assignment = Assignment.query.get(submission.assignment_id)
            course = Course.query.get(assignment.course_id) if assignment else None

            if student_id not in student_data:
                student_data[student_id] = {"name": f"Student-{student_id}", "courses": {}}

            if course and course.name not in student_data[student_id]["courses"]:
                student_data[student_id]["courses"][course.name] = []

            student_data[student_id]["courses"][course.name].append({
                "assignment": assignment.title if assignment else "Unknown Assignment",
                "score": submission.score if submission.score is not None else "Not Graded",
                "max_points": assignment.max_points if assignment else 100
            })

        if not student_data:
            print("❌ No student data found in the database!")
            return jsonify({"error": "No student data found"}), 400

        print(f"✅ Retrieved data for {len(student_data)} students.")

        # Step 4: Generate reports
        reports = {}

        for student_id, data in student_data.items():
            student_name = data["name"]
            courses = data["courses"]

            # Extract year level (placeholder for now)
            year_level = "Primary"

            print(f"📝 Generating report for {student_name}...")

            try:
                report = generate_student_report(student_name, year_level, courses)
                reports[student_name] = report
                print(f"✅ Report generated for {student_name}.")
            except Exception as e:
                print(f"❌ Error generating report for {student_name}: {e}")
                reports[student_name] = {"error": "Failed to generate report"}

        print("📄 All reports generated successfully!")
        return jsonify(reports)

    except Exception as e:
        print(f"❌ Unexpected error in generate_report: {e}")
        return jsonify({"error": "Internal server error"}), 500

@reports_bp.route("/reports/generate-from-input", methods=["POST"])
@jwt_required()
def generate_report_from_input():
    """
    Generate a report based on freeform user input (React).
    """
    try:
        data = request.get_json()
        if not data or "input" not in data:
            return jsonify({"error": "Invalid input. Please provide input data."}), 400

        user_id = get_jwt_identity()  # Not used directly but included for consistency
        user_input = data["input"]
        print(f"🔍 Received input: {user_input}")

        # Generate report from user input
        report = generate_report_from_user_input(user_input)

        return jsonify({"report": report}), 200

    except Exception as e:
        print(f"❌ Error generating report from input: {e}")
        return jsonify({"error": "Internal server error"}), 500

@reports_bp.route("/reports/generate-from-classroom", methods=["POST"])
@jwt_required()
def generate_report_from_classroom():
    """
    Generate a report based on structured classroom data.
    """
    try:
        data = request.get_json()
        if not data or "student_name" not in data or "year_level" not in data or "courses" not in data:
            return jsonify({"error": "Invalid input. Please provide student_name, year_level, and courses."}), 400

        user_id = get_jwt_identity()  # Not used directly but included for consistency
        student_name = data["student_name"]
        year_level = data["year_level"]
        courses = data["courses"]
        print(f"🔍 Received classroom data for: {student_name}")

        # Generate report from classroom data
        report = generate_report_from_classroom_data(student_name, year_level, courses)

        return jsonify({"report": report}), 200

    except Exception as e:
        print(f"❌ Error generating report from classroom data: {e}")
        return jsonify({"error": "Internal server error"}), 500

@reports_bp.route("/reports/suggest-comments", methods=["POST"])
@jwt_required()
def suggest_comments():
    """
    Suggest AI-generated comments for a student and subject.
    Request Body: {studentName, subject}
    """
    data = request.json
    user_id = get_jwt_identity()  # Not used directly but included for consistency
    student_name = data.get("studentName", "The student")
    subject = data.get("subject", "the subject")

    ai_comment = suggest_ai_comments(student_name, subject)
    return jsonify({"suggestedComments": ai_comment})

# Template Management Endpoints
@reports_bp.route("/templates", methods=["POST"])
@jwt_required()
def create_template():
    """
    Create a new custom report template for the authenticated teacher.
    Request Body: {name, categories, schoolLevel}
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        name = data.get("name")
        categories = data.get("categories", [])
        schoolLevel = data.get("schoolLevel", "Primary School")

        if not name or not categories:
            return jsonify({"error": "Template name and categories are required"}), 400

        template = Template(
            name=name,
            categories=categories,
            schoolLevel=schoolLevel,
            teacher_id=int(user_id),  # Use user_id from JWT
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        template.save()

        return jsonify(template.to_json()), 201
    except Exception as e:
        print(f"❌ Error creating template: {e}")
        return jsonify({"error": "Failed to create template"}), 500

@reports_bp.route("/templates", methods=["GET"])
@jwt_required()
def get_templates():
    """
    Retrieve all templates for the authenticated teacher, filtered by schoolLevel.
    Query Param: schoolLevel (optional, defaults to "Primary School")
    """
    try:
        user_id = get_jwt_identity()
        schoolLevel = request.args.get("schoolLevel", "Primary School")
        templates = Template.query.filter_by(teacher_id=int(user_id), schoolLevel=schoolLevel).all()
        return jsonify([t.to_json() for t in templates]), 200
    except Exception as e:
        print(f"❌ Error fetching templates: {e}")
        return jsonify({"error": "Failed to fetch templates"}), 500

@reports_bp.route("/templates/<int:template_id>", methods=["PUT"])
@jwt_required()
def update_template(template_id):
    """
    Update an existing template for the authenticated teacher.
    Request Body: {name, categories, schoolLevel}
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        template = Template.query.get_or_404(template_id)
        if template.teacher_id != int(user_id):  # Use user_id from JWT
            return jsonify({"error": "Unauthorized"}), 403

        template.name = data.get("name", template.name)
        template.categories = data.get("categories", template.categories)
        template.schoolLevel = data.get("schoolLevel", template.schoolLevel)
        template.updated_at = datetime.utcnow()
        template.save()

        return jsonify(template.to_json()), 200
    except Exception as e:
        print(f"❌ Error updating template: {e}")
        return jsonify({"error": "Failed to update template"}), 500

@reports_bp.route("/templates/<int:template_id>", methods=["DELETE"])
@jwt_required()
def delete_template(template_id):
    """
    Delete a template for the authenticated teacher.
    """
    try:
        user_id = get_jwt_identity()
        template = Template.query.get_or_404(template_id)
        if template.teacher_id != int(user_id):  # Use user_id from JWT
            return jsonify({"error": "Unauthorized"}), 403

        template.delete()
        return "", 204
    except Exception as e:
        print(f"❌ Error deleting template: {e}")
        return jsonify({"error": "Failed to delete template"}), 500

