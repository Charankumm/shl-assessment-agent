from fastapi import APIRouter

from app.models import (
    ChatRequest,
    ChatResponse
)

from app.agent import SHLAgent

router = APIRouter()

agent = SHLAgent()


@router.get("/health")
def health():

    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    response = agent.chat(
        [m.dict() for m in request.messages]
    )

    return ChatResponse(**response)