from fastapi import FastAPI, Request
from pydantic import BaseModel
from school_agent.agent import execute_query

app = FastAPI()

# Structure of the request body
class Question(BaseModel):
    query: str

# Endpoint to handle user queries
@app.post("/ask")
async def ask(question: Question):
    try:
        result = execute_query(question.query)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}