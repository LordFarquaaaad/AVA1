from backend.extensions import db

class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)  # Reference student_id
    grade = db.Column(db.Float, nullable=False)
