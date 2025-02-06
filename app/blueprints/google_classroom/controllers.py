from googleapiclient.discovery import build
from app.extensions import get_google_credentials, db
from app.models import Course, Assignment, StudentSubmission

def fetch_classroom_data(credentials):
    """Fetch courses, coursework, and student submissions for teachers."""
    try:
        # Initialize Google Classroom API
        service = build("classroom", "v1", credentials=credentials)

        # ✅ Step 1: Fetch the teacher's courses
        courses = service.courses().list().execute().get("courses", [])
        print(f"✅ Found {len(courses)} courses.")

        for course in courses:
            print(f"📚 Syncing Course: {course['name']} (ID: {course['id']})")

            # Save course to the database
            db_course = Course(
                id=course["id"],
                name=course["name"]
            )
            db.session.merge(db_course)

            # ✅ Step 2: Fetch coursework (assignments, quizzes, materials)
            coursework = service.courses().courseWork().list(courseId=course["id"]).execute().get("courseWork", [])
            print(f"✏️ Found {len(coursework)} assignments in {course['name']}.")

            for work in coursework:
                db_assignment = Assignment(
                    id=work["id"],
                    course_id=course["id"],
                    title=work["title"],
                    max_points=work.get("maxPoints", 100),  # Default to 100 if missing
                    due_date=work.get("dueDate")
                )
                db.session.merge(db_assignment)

                # ✅ Step 3: Fetch student submissions for each assignment
                submissions = service.courses().courseWork().studentSubmissions().list(
                    courseId=course["id"], courseWorkId=work["id"]
                ).execute().get("studentSubmissions", [])

                for submission in submissions:
                    student_id = submission.get("userId")
                    assigned_grade = submission.get("assignedGrade", None)  # None if not graded

                    db_submission = StudentSubmission(
                        id=submission["id"],
                        assignment_id=work["id"],
                        student_id=student_id,
                        score=assigned_grade
                    )
                    db.session.merge(db_submission)

        # Commit changes to the database
        db.session.commit()
        print("✅ Classroom data synced successfully!")
        return {"message": "Classroom data synced successfully!"}

    except Exception as e:
        print(f"❌ Error fetching classroom data: {e}")
        return {"error": str(e)}

def fetch_student_grades(credentials):
    """Fetch student grades from Google Classroom."""
    try:
        service = build("classroom", "v1", credentials=credentials)

        # Fetch courses
        courses = service.courses().list().execute().get("courses", [])
        student_data = {}

        for course in courses:
            course_id = course["id"]
            course_name = course["name"]

            # Fetch coursework (assignments)
            coursework = service.courses().courseWork().list(courseId=course_id).execute().get("courseWork", [])
            
            for work in coursework:
                assignment_id = work["id"]
                assignment_title = work["title"]
                max_points = work.get("maxPoints", 100)

                # Fetch student submissions (grades)
                submissions = service.courses().courseWork().studentSubmissions().list(
                    courseId=course_id, courseWorkId=assignment_id
                ).execute().get("studentSubmissions", [])

                for submission in submissions:
                    student_id = submission.get("userId")
                    score = submission.get("assignedGrade", "Not Graded")

                    # Store data in a dictionary
                    if student_id not in student_data:
                        student_data[student_id] = {"name": f"Student-{student_id}", "courses": {}}

                    if course_name not in student_data[student_id]["courses"]:
                        student_data[student_id]["courses"][course_name] = []

                    student_data[student_id]["courses"][course_name].append({
                        "assignment": assignment_title,
                        "score": score,
                        "max_points": max_points
                    })

        return student_data

    except Exception as e:
        print(f"❌ Error fetching student grades: {e}")
        return {"error": str(e)}

def sync_classroom_data(credentials):
    """Fetch courses and assignments from Google Classroom and sync to DB."""
    try:
        service = build("classroom", "v1", credentials=credentials)
        
        # Fetch and sync courses
        courses = service.courses().list().execute().get("courses", [])
        if not courses:
            print("❌ No courses found!")
            return {"error": "No courses found"}

        print(f"✅ Found {len(courses)} courses.")
        for course in courses:
            print(f"📚 Syncing course: {course['name']} (ID: {course['id']})")
            db_course = Course(id=course["id"], name=course["name"])
            db.session.merge(db_course)

            # Fetch and sync assignments
            coursework = service.courses().courseWork().list(courseId=course["id"]).execute().get("courseWork", [])
            for work in coursework:
                db_assignment = Assignment(
                    id=work["id"],
                    course_id=course["id"],
                    title=work["title"],
                    max_points=work.get("maxPoints", 100),  # Default max points
                    due_date=work.get("dueDate")
                )
                db.session.merge(db_assignment)

        db.session.commit()
        return {"message": "Classroom data synced successfully!"}

    except Exception as e:
        print(f"❌ Error syncing data: {e}")
        db.session.rollback()  # Rollback in case of error
        return {"error": str(e)}



