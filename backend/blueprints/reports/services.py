import os
import openai

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is missing! Set it in the environment.")

# ✅ Correct way to create an OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_student_report(student):
    """Generates a detailed AI report for a given student."""
    if not isinstance(student, dict):  # Ensure student is a dictionary
        return "⚠️ Invalid student data format."

    # Extract data from the student object with fallback values
    name = student.get("name", {}).get("value", "The student")
    achievement = student.get("academicPerformance", {}).get("value", "Meets Expectations")
    behavior = student.get("behaviorAttitude", {}).get("value", "Generally Well-Behaved")
    participation = student.get("participationEngagement", {}).get("value", "Participates Regularly")
    work_habits = student.get("effortWorkEthic", {}).get("value", "Usually Meets Deadlines")
    social_skills = student.get("socialEmotionalDevelopment", {}).get("value", "Works Well with Others")
    communication = student.get("communication", {}).get("value", "Communicates Effectively")
    personal_development = student.get("personalDevelopment", {}).get("value", "Demonstrates Steady Progress")
    attendance = student.get("attendancePunctuality", {}).get("value", "Rarely Absent")
    comments = student.get("comments", {}).get("value", "").strip()

    # Construct the prompt
    prompt = f"""
Generate a professional school report for the student based on the following attributes:
- **Student Name**: {name}
- **Academic Achievement**: {achievement}
- **Behavior and Conduct**: {behavior}
- **Participation and Engagement**: {participation}
- **Work Habits and Time Management**: {work_habits}
- **Social Skills and Collaboration**: {social_skills}
- **Communication Skills**: {communication}
- **Personal Development**: {personal_development}
- **Attendance**: {attendance}

{f'Additional Comments: {comments}' if comments else ''}

**Instructions for AI:**
1. Write in a professional, supportive, and constructive tone.
2. Avoid generic statements, and include additional comments to personalize the report—make it specific to the selected performance attributes.
3. Provide balanced feedback: highlight strengths and offer guidance on improvement areas.
4. Ensure the report flows naturally and doesn't sound AI-generated.
6. Vary sentence structure and avoid repetitive phrasing.
7. Ensure grammar, punctuation, and spelling are correct.

Example Structure:
- Opening Sentence: Introduce the student and summarize their overall performance.
- Detailed Performance Breakdown: Discuss each category concisely.
- Conclusion: End with a positive note, encouragement, or suggested improvement.

Now, write a well-structured, professional report.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350  # Ensuring each report is detailed but not exceeding limits
        )
        report = response.choices[0].message.content.strip()

        return report  # Return the report as-is (UTF-8 encoded)
    except Exception as e:
        print(f"❌ AI Generation Error: {e}")
        return "⚠️ Error generating AI-enhanced report."



def generate_bulk_reports(students):
    """Reuses generate_student_report() to generate reports for multiple students."""
    return [{"name": student.get("name", "Unnamed"), "report": generate_student_report(student)} for student in students]

def generate_report_from_user_input(user_input):
    """
    Generate a report based on freeform teacher input.
    """
    try:
        # Construct the prompt for user input
        prompt = f"Teacher's comments: {user_input}\n"
        prompt += "Write a detailed and actionable report based on these comments."

        # ✅ Correct OpenAI API call (NEW SDK SYNTAX)
        response = client.chat.completions.create(  # FIXED
            model="gpt-4-turbo",  # Replace with your fine-tuned model ID
            messages=[
                {"role": "system", "content": "You are an expert report generator for student performance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        # ✅ Extract and return the generated report
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error generating report from user input: {e}")
        raise


def generate_report_from_classroom_data(student_name, year_level, courses):
    """
    Generate a report based on structured classroom data.
    """
    try:
        # Construct the prompt for classroom data
        prompt = f"Student: {student_name}, Year: {year_level}\n"
        prompt += "Grades:\n"
        for course, assignments in courses.items():
            prompt += f"{course}: "
            prompt += ", ".join([f"{a['assignment']} ({a['score']} / {a['max_points']})" for a in assignments])
            prompt += "\n"
        prompt += "\nWrite a detailed academic performance report with constructive feedback and improvement suggestions."

        # ✅ Correct OpenAI API call (NEW SDK SYNTAX)
        response = client.chat.completions.create(  # FIXED
            model="ft:gpt-3.5-turbo-0125:shai::Az138VuK",  # Replace with your fine-tuned model ID
            messages=[
                {"role": "system", "content": "You are an expert academic performance report generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # ✅ Extract and return the generated report
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error generating report from classroom data: {e}")
        raise

def suggest_ai_comments(student_name, subject):
    """
    Generate AI-based suggestions for student comments.
    """
    prompt = f"Provide a short constructive comment for {student_name} in {subject}, focusing on strengths and areas to improve."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5 turbo",
            messages=[{"role": "system", "content": "You are an AI assistant for teachers."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating comments: {str(e)}"


