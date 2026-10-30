import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from docx import Document


# Load environment variables
load_dotenv(Path.cwd() / ".env", override=True)

# Initialize Groq Client
Client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Define prompts
prompts = [
    {
        "role": "user",
        "content": "Hello! Tell me what you can do."
    }
]

# Send request
response = Client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=prompts
)

# Print response
print(response.choices[0].message.content)


# Read Word document
doc = Document("Menna_Farghaly_CV (2).docx")

# Extract text
text = ""

for paragraph in doc.paragraphs:
    text += paragraph.text + "\n"

# Print extracted text
print(text)
system_prompt = """
You are my personal CV assistant.

You have access to my CV, which contains my personal,
educational, professional, and technical information.

Your task is to answer any questions about me based ONLY
on the information provided in my CV.

Instructions:

1. Always use my CV as your primary source of information.

2. Answer questions accurately using the information
   available in my CV.

3. Never invent, assume, or hallucinate any information
   that is not mentioned in my CV.

4. If the answer is not available in my CV, clearly say:
   "This information is not mentioned in my CV."

5. You can answer questions about:
   - Education
   - Technical Skills
   - Programming Languages
   - Projects
   - Certifications
   - Training
   - Work Experience
   - Achievements
   - Contact Information

6. Answer in the same language used by the user.

7. Keep answers clear, professional, and concise.

8. If someone asks you to summarize my qualifications,
   provide a professional summary based on my CV.

Remember:
Your role is to represent my qualifications accurately.
Never create false information about me.
"""


# Read CV
doc = Document("Menna_Farghaly_CV (2).docx")

cv_text = "\n".join(
    paragraph.text for paragraph in doc.paragraphs
)

# Create prompts
prompts = [
    {
        "role": "system",
        "content": system_prompt
    },
    {
        "role": "user",
        "content": f"My CV content:\n\n{cv_text}"
    }
]

while True:

    question = input("Ask me anything about my CV: ")

    if question.lower() == "exit":
        break

    prompts.append({
        "role": "user",
        "content": question
    })

    response = Client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=prompts
    )

    answer = response.choices[0].message.content

    print("\nAssistant:", answer)

    prompts.append({
        "role": "assistant",
        "content": answer
    })