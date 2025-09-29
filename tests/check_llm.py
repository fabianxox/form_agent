import os
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Init client
client = Groq(api_key=GROQ_API_KEY)

def generate_questions(prompt: str) -> str:
    """Call LLM via Groq to generate questions."""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are friendly technical interviewer."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Groq API error:", e)
        return "Oops! Something went wrong generating questions."

# --- Quick test ---
if __name__ == "__main__":
    result = generate_questions("Generate 3 Python interview questions.")
    print("LLM response:\n", result)
