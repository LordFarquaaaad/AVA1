import openai
import os


# Set your OpenAI API key (replace with your actual key)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_report_prompt(student_name, year_level, courses):
    """
    Generate a tailored prompt for the student report based on their year level and courses.
    """
    # Generate a subject list for the prompt
    subjects = "\n".join(
        [f"{course['name']}: {course['average_grade']}%" for course in courses]
    )

    # Tailored prompt for primary school
    if year_level <= 6:
        return (
            f"Generate a supportive progress report for {student_name}, a primary school student in Year {year_level}. "
            f"Summarize their performance in the following subjects:\n{subjects}. "
            "Focus on strengths, classroom engagement, and age-appropriate suggestions for improvement. "
            "Use simple and encouraging language suitable for young students."
        )
    
    # Tailored prompt for high school
    elif year_level <= 12:
        return (
            f"Write a detailed progress report for {student_name}, a high school student in Year {year_level}. "
            f"Include their performance in these subjects:\n{subjects}. "
            "Highlight key achievements, areas for academic improvement, and future goals. "
            "Provide actionable feedback to help them succeed."
        )
    
    # Default fallback for other cases
    else:
        return (
            f"Generate a custom progress report for {student_name}, a student in Year {year_level}. "
            f"Summarize their performance across these subjects:\n{subjects}. "
            "Focus on meaningful feedback and actionable suggestions for improvement."
        )

def generate_student_report(student_name, year_level, courses):
    # Extract and format the grades into text
    grades_text = []
    
    for course in courses:
        course_name = course["name"]
        for assignment in course["assignments"]:
            grades_text.append(
                f"{course_name} - {assignment['title']}: {assignment['score']} / {assignment['max_points']}"
            )

    # Convert grades list into a formatted string
    grades_summary = "\n".join(grades_text)

    # Create the prompt for OpenAI
    prompt = (
        f"Generate a professional progress report for {student_name}, a student in Year {year_level}.\n"
        f"Their performance in various subjects is as follows:\n{grades_summary}.\n"
        "Provide insights into their strengths, areas for improvement, and overall academic progress."
    )

    # ✅ Correct OpenAI API Call (Updated for openai>=1.0.0)
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that generates professional academic reports for students."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


