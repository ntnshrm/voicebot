from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

from services.openai_client import client

from services.conversation_store import (
    load_conversation,
    save_conversation
)

router = APIRouter()

EXTRACTED_DIR = "../data/extracted"
PROMPT_PATH = "../backend/prompts/doctor_prompt.txt"


class ChatRequest(BaseModel):
    report_id: str
    question: str


class ChatResponse(BaseModel):
    answer: str


def load_report_text(report_id: str) -> str:
    path = f"{EXTRACTED_DIR}/{report_id}.txt"
    if not os.path.exists(path):
        raise FileNotFoundError("Extracted report not found")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_system_prompt(report_text: str) -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        template = f.read()
    return template.replace("{REPORT_TEXT}", report_text)


@router.post("/chat", response_model=ChatResponse)
def chat_with_report(req: ChatRequest):
    try:
        report_text = load_report_text(req.report_id)
        system_prompt = load_system_prompt(report_text)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Report not found")

    history = load_conversation(req.report_id)

    messages = [
        {"role": "system", "content": system_prompt},
        *history,
        {"role": "user", "content": req.question}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        temperature=0.3
    )

    answer = response.choices[0].message.content.strip()

    # update conversation history
    history.extend([
        {"role": "user", "content": req.question},
        {"role": "assistant", "content": answer}
    ])
    save_conversation(req.report_id, history)

    return {"answer": answer}

