from openai import OpenAI

def summarize_email(email_text):
    """Use AI to summarize an email"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Summarize this email:"},
                  {"role": "user", "content": email_text}]
    )
    return response["choices"][0]["message"]["content"]
