from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from chatbot import answer_question

app = FastAPI(title="AI Engineer Assessment")


class Question(BaseModel):
    question: str


class Answer(BaseModel):
    answer: str
    sources: list[str]


@app.post("/ask", response_model=Answer)
async def ask(request: Question):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    return await answer_question(question)