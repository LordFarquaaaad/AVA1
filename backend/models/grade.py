from backend.extensions import db

class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.student_id"), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.id"), nullable=False)
    grade = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Grade {self.grade} for Student {self.student_id} on Assignment {self.assignment_id}>"

