from app.models import db, Course, Assignment, Grade
from app import create_app

# Create the Flask app and app context
app = create_app()
app.app_context().push()

# Seed data function
def seed_data():
    print("Seeding the database with test data...")

    # Clear existing data
    Grade.query.delete()
    Assignment.query.delete()
    Course.query.delete()

    # Add test courses
    course1 = Course(id="course1", name="Mathematics")
    course2 = Course(id="course2", name="English")
    db.session.add_all([course1, course2])

    # Add test assignments
    assignment1 = Assignment(id="assign1", course_id="course1", title="Addition Test", max_points=100)
    assignment2 = Assignment(id="assign2", course_id="course2", title="Reading Comprehension", max_points=100)
    db.session.add_all([assignment1, assignment2])

    # Add test grades for a student
    grade1 = Grade(id="grade1", assignment_id="assign1", student_name="Alice Johnson", student_email="alice.johnson@example.com", score=85)
    grade2 = Grade(id="grade2", assignment_id="assign2", student_name="Alice Johnson", student_email="alice.johnson@example.com", score=90)
    db.session.add_all([grade1, grade2])

    # Commit the changes
    db.session.commit()
    print("Test data seeded successfully!")

# Run the seeding function
if __name__ == "__main__":
    seed_data()
