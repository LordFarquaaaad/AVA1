from flask import Blueprint, request, jsonify, render_template
from backend.blueprints.google_classroom.controllers import sync_classroom_data
from backend.blueprints.reports.services import generate_report_from_user_input, generate_report_from_classroom_data
from backend.extensions import get_google_credentials  # Ensure this function is implemented
from backend.blueprints.reports import reports_bp  
from backend.models import StudentSubmission, Assignment, Course

@reports_bp.route("/")
def view_reports():
    """Render the reports page."""
    return render_template("reports.html")


@reports_bp.route("/generate", methods=["POST"])
def generate_report():
    """Generate a report based on Google Classroom data stored in the database."""
    try:
        print("🔍 Starting report generation...")

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

@reports_bp.route("/generate-from-input", methods=["POST"])
def generate_report_from_input():
    """
    Generate a report based on freeform user input (React).
    """
    try:
        data = request.get_json()
        if not data or "input" not in data:
            return jsonify({"error": "Invalid input. Please provide input data."}), 400

        user_input = data["input"]
        print(f"🔍 Received input: {user_input}")

        # Generate report from user input
        report = generate_report_from_user_input(user_input)

        return jsonify({"report": report}), 200

    except Exception as e:
        print(f"❌ Error generating report from input: {e}")
        return jsonify({"error": "Internal server error"}), 500

@reports_bp.route("/generate-from-classroom", methods=["POST"])
def generate_report_from_classroom():
    """
    Generate a report based on structured classroom data.
    """
    try:
        data = request.get_json()
        if not data or "student_name" not in data or "year_level" not in data or "courses" not in data:
            return jsonify({"error": "Invalid input. Please provide student_name, year_level, and courses."}), 400

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




