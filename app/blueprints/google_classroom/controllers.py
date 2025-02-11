from googleapiclient.discovery import build
from app.extensions import get_google_credentials, db
from app.models import Course, Assignment, StudentSubmission
from datetime import date


def sync_classroom_data(credentials):
    """
    Fetch and sync courses, coursework, and student submissions from Google Classroom.
    """
    try:
        print("🔍 Checking stored credentials for /sync...")
        service = build("classroom", "v1", credentials=credentials)

        print("📡 Sending request: Fetching courses...")
        courses = fetch_all_courses(service)
        if not courses:
            print("❌ No courses found!")
            return {"error": "No courses found"}

        print(f"✅ Found {len(courses)} courses.")
        for course in courses:
            print(f"\n📚 Syncing Course: {course['name']} (ID: {course['id']})")
            db_course = Course(id=course["id"], name=course["name"])
            db.session.merge(db_course)

            # Fetch coursework (assignments, quizzes)
            print(f"📡 Fetching coursework for {course['name']}...")
            coursework = fetch_all_coursework(service, course["id"])
            if not coursework:
                print(f"⚠️ No coursework found for course: {course['name']}")
                continue

            print(f"✏️ Found {len(coursework)} assignments in {course['name']}.")
            for work in coursework:
                print(f"📖 Assignment: {work['title']} (ID: {work['id']})")

                # ✅ Convert dueDate from dict → string (YYYY-MM-DD)
                due_date_data = work.get("dueDate")  # Example: {"year": 2025, "month": 2, "day": 5}
                if due_date_data:
                    due_date = f"{due_date_data['year']}-{due_date_data['month']:02d}-{due_date_data['day']:02d}"
                else:
                    due_date = None  # Handle missing dates properly

                # ✅ Ensure maxPoints is set
                max_points = work.get("maxPoints", 100)  # Default to 100 if missing

                db_assignment = Assignment(
                    id=work["id"],
                    course_id=course["id"],
                    title=work["title"],
                    max_points=max_points,
                    due_date=due_date,  # Now stored as a string
                )
                db.session.merge(db_assignment)

                # Fetch student submissions
                print(f"📡 Fetching student submissions for {work['title']}...")
                submissions = fetch_all_submissions(service, course["id"], work["id"])
                if not submissions:
                    print(f"⚠️ No submissions found for {work['title']}.")
                    continue

                print(f"📄 Found {len(submissions)} submissions for {work['title']}.")
                for submission in submissions:
                    student_id = submission.get("userId")
                    assigned_grade = submission.get("assignedGrade", None)  # May be missing

                    print(f"📝 Submission: Student {student_id} | Score: {assigned_grade}")

                    db_submission = StudentSubmission(
                        id=submission["id"],
                        assignment_id=work["id"],
                        student_id=student_id,
                        score=assigned_grade,
                    )
                    db.session.merge(db_submission)

        db.session.commit()
        print("✅ Classroom data synced successfully!")
        return {"message": "Classroom data synced successfully!"}

    except Exception as e:
        print(f"❌ Error syncing data: {e}")
        db.session.rollback()
        return {"error": str(e)}


# ---------------- FETCH HELPERS ---------------- #

def fetch_all_courses(service):
    """ Fetch all courses with pagination. """
    courses = []
    next_page_token = None

    while True:
        try:
            response = service.courses().list(pageToken=next_page_token).execute()
            fetched_courses = response.get("courses", [])
            courses.extend(fetched_courses)
            next_page_token = response.get("nextPageToken")

            # Debugging Output
            print(f"📚 API Response: {len(fetched_courses)} new courses fetched.")
            for course in fetched_courses:
                print(f"    ✅ {course['name']} (ID: {course['id']})")

            if not next_page_token:
                break
        except Exception as e:
            print(f"❌ Error fetching courses: {e}")
            break

    return courses


def fetch_all_coursework(service, course_id):
    """ Fetch all coursework for a given course with pagination. """
    coursework = []
    next_page_token = None

    while True:
        try:
            response = service.courses().courseWork().list(courseId=course_id, pageToken=next_page_token).execute()
            fetched_coursework = response.get("courseWork", [])
            coursework.extend(fetched_coursework)
            next_page_token = response.get("nextPageToken")

            # Debugging Output
            print(f"✏️ API Response: {len(fetched_coursework)} new assignments fetched.")
            for work in fetched_coursework:
                print(f"    ✅ {work['title']} (ID: {work['id']})")

            if not next_page_token:
                break
        except Exception as e:
            print(f"❌ Error fetching coursework for Course {course_id}: {e}")
            break

    return coursework


def fetch_all_submissions(service, course_id, coursework_id):
    """ Fetch all student submissions for a given coursework with pagination. """
    submissions = []
    next_page_token = None

    while True:
        try:
            response = service.courses().courseWork().studentSubmissions().list(
                courseId=course_id, courseWorkId=coursework_id, pageToken=next_page_token
            ).execute()
            fetched_submissions = response.get("studentSubmissions", [])
            submissions.extend(fetched_submissions)
            next_page_token = response.get("nextPageToken")

            # Debugging Output
            print(f"📄 API Response: {len(fetched_submissions)} new submissions fetched.")
            for submission in fetched_submissions:
                student_id = submission.get("userId")
                assigned_grade = submission.get("assignedGrade", "Not Graded")
                print(f"    ✅ Submission: Student {student_id} | Score: {assigned_grade}")

            if not next_page_token:
                break
        except Exception as e:
            print(f"❌ Error fetching submissions for coursework {coursework_id}: {e}")
            break

    return submissions






