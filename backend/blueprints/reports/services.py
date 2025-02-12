import os
import openai

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY is missing! Set it in the environment.")

# ✅ Correct way to create an OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

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
            model="ft:gpt-3.5-turbo-0125:shai::AzddwFtj",  # Replace with your fine-tuned model ID
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





