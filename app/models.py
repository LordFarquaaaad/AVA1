from app.extensions import db

class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Assignment(db.Model):
    __tablename__ = "assignment"

    id = db.Column(db.String, primary_key=True)
    course_id = db.Column(db.String, db.ForeignKey("course.id"))
    title = db.Column(db.String, nullable=False)
    max_points = db.Column(db.Integer)
    due_date = db.Column(db.String, nullable=True)  # Optional

class StudentSubmission(db.Model):
    __tablename__ = "student_submission"

    id = db.Column(db.String, primary_key=True)
    assignment_id = db.Column(db.String, db.ForeignKey("assignment.id"))
    student_id = db.Column(db.String, nullable=False)
    score = db.Column(db.Float, nullable=True)  # Nullable if not graded


