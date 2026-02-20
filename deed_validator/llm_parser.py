import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def parse_with_llm(raw_text:str)->dict:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found. Put it in .env file in project root.")
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are a data extraction assistant. Return ONLY vaild JSON."},
                {"role": "user","content": f"""Extract the following fields from the text and return JSON: county,date_signed,date_recorded,amount_numeric,amount_words Text:{raw_text}"""}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(content)