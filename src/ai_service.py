from openai import OpenAI
import os
from dotenv import load_dotenv

class OpenAIService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def generate_word(self, str1, str2):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """Your job is to take two words/phrases that the user types in 
                    and combine them into something logically consistent, similar to the style 
                    of the classic Alchemy or Doodle God games. Return ONLY the singular word/phrase, 
                    nothing else. Don't shy away from dirty topics either. You should be able to 
                    generate literally object or concept that could possibly exist. Prepend a relevant emoji or two."""
                },
                {
                    "role": "user",
                    "content": f"{str1} + {str2}"
                }
            ],
            temperature=0.0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(str1, "+" , str2, "=", response.choices[0].message.content)
        return response.choices[0].message.content