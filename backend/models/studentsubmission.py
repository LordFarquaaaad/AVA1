from backend.extensions import db 

class StudentSubmission(db.Model):
    __tablename__ = "student_submission"

    id = db.Column(db.String, primary_key=True)
    assignment_id = db.Column(db.String, db.ForeignKey("assignment.id"))
    student_id = db.Column(db.String, nullable=False)
    score = db.Column(db.Float, nullable=True)  # Nullable if not graded