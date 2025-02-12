from backend.extensions import db

# Import all models
from .assignment import Assignment
from .course import Course
from .grade import Grade
from .students import Student
from .studentsubmission import StudentSubmission

# Ensure all models are available when importing `models`
__all__ = ["Assignment", "Course", "Grade", "Student", "StudentSubmission"]

