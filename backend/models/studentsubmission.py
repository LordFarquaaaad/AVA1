from backend.extensions import db 

class StudentSubmission(db.Model):
    __tablename__ = "student_submission"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    score = db.Column(db.Float, nullable=True)

    # Relationships
    student = db.relationship("Student", back_populates="submissions")

    def __repr__(self):
        return f"<Submission {self.id} - Student {self.student_id} - Assignment {self.assignment_id}>"
