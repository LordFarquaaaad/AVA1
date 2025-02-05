from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import json

from app.models import Course, Assignment, db

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.student-submissions.me.readonly'
]

CREDENTIALS_PATH = "config/credentials.json"
TOKEN_PATH = "config/token.json"

def get_google_credentials():
    """Load or refresh Google Classroom API credentials"""
    credentials = None

    # Load existing token if available
    if os.path.exists(TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # Refresh token if expired
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    # If no valid credentials, start the OAuth flow
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        credentials = flow.run_local_server(port=0)

        # Save the credentials for next time
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(credentials.to_json())

    return credentials


def fetch_classroom_data():
    """Fetch courses and assignments from Google Classroom"""
    credentials = get_google_credentials()
    service = build("classroom", "v1", credentials=credentials)

    # Fetch courses
    courses = service.courses().list().execute().get("courses", [])
    
    for course in courses:
        db_course = Course(id=course["id"], name=course["name"])
        db.session.merge(db_course)

        # Fetch assignments for each course
        coursework = service.courses().courseWork().list(courseId=course["id"]).execute().get("courseWork", [])
        for work in coursework:
            db_assignment = Assignment(
                id=work["id"],
                course_id=course["id"],
                title=work["title"],
                max_points=work.get("maxPoints", 100),  # Default to 100 if missing
                due_date=work.get("dueDate")
            )
            db.session.merge(db_assignment)

    db.session.commit()
    return {"message": "Classroom data synced successfully!"}




