from fastapi import FastAPI, Request
from pydantic import BaseModel
from school_agent.agent import ask_sql_agent

app = FastAPI()

class Question(BaseModel):
    query: str

@app.post("/ask")
async def ask(question: Question):
    try:
        result = ask_sql_agent(question.query)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}
