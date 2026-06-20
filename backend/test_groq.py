import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": "You return only one emoji. No words."
        },
        {
            "role": "user",
            "content": "Choose one emoji for the emotion: happy"
        }
    ],
    temperature=0.7,
    max_tokens=5
)

print(response.choices[0].message.content)