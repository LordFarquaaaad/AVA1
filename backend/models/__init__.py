from backend.extensions import db  # Ensure the database instance is imported

# Import all models explicitly
from backend.models.course import Course
from backend.models.assignment import Assignment
from backend.models.grade import Grade
from backend.models.students import Student
from backend.models.studentsubmission import StudentSubmission
from backend.models.user import User

# Ensure all models are available when importing `backend.models`
__all__ = ["Course", "Assignment", "Grade", "Student", "StudentSubmission", "User"]


