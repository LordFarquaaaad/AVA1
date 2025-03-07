# backend/models/template.py
from datetime import datetime
from backend.extensions import db  # Assume Flask-SQLAlchemy setup in database.py

class Template(db.Model):
    __tablename__ = "templates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    categories = db.Column(db.JSON, nullable=False)  # Use JSON for flexible category structure
    schoolLevel = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "categories": self.categories,
            "schoolLevel": self.schoolLevel,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()