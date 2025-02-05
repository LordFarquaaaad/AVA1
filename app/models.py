from app.extensions import db

class Course(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Assignment(db.Model):
    id = db.Column(db.String, primary_key=True)
    course_id = db.Column(db.String, db.ForeignKey("course.id"), nullable=False)
    title = db.Column(db.String, nullable=False)
    max_points = db.Column(db.Float)
    due_date = db.Column(db.DateTime)

class Grade(db.Model):
    id = db.Column(db.String, primary_key=True)
    assignment_id = db.Column(db.String, db.ForeignKey("assignment.id"), nullable=False)
    student_name = db.Column(db.String, nullable=False)
    student_email = db.Column(db.String, nullable=False)
    score = db.Column(db.Float)

