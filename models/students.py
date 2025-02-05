from extensions import db

class Student(db.Model):
    __tablename__ = "students"

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Student {self.full_name}>"
