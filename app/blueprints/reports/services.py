import openai
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")  # Make sure to load this securely

def generate_student_report(student_name, year_level, courses):
    """Generate an AI-powered student progress report."""

    # Convert grades into a descriptive string
    grades_text = "\n".join([
        f"{assignment['assignment']}: {assignment['score']} / {assignment['max_points']} in {course}"
        for course, assignments in courses.items()
        for assignment in assignments
    ])

    # Construct the prompt dynamically based on student year level
    prompt = f"""
    You are an AI assistant tasked with writing student progress reports.

    Student Name: {student_name}
    Year Level: {year_level}
    
    Grades:
    {grades_text}

    Please generate a professional, well-written progress report summarizing the student's performance.
    Provide encouragement, highlight strengths, and suggest areas for improvement.
    """
    
    # Call OpenAI API using the updated method
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that generates student progress reports."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content



