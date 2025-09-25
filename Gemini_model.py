from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

API_KEY = os.getenv('Gemini_API_KEY')


client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)