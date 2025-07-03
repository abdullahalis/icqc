from openai import OpenAI
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()
url = os.getenv("DATABASE_URL")
engine = create_engine(url)
conn = engine.connect()
print(conn.execute(text("SELECT 1")).fetchall())


# client = OpenAI(
#   api_key=os.getenv("OPEN_AI_API_KEY")
# )

# completion = client.chat.completions.create(
#   model="gpt-4o-mini",
#   store=True,
#   messages=[
#     {"role": "user", "content": "write a haiku about ai"}
#   ]
# )

# print(completion.choices[0].message);
