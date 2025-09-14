from fastapi import APIRouter
from request.ChatRequest import ChatRequest
from response.ChatResponse import ChatResponse
from service.ChatService import ChatService

chatrouter = APIRouter()
chat_service = ChatService()

@chatrouter.post("/chat", response_model=ChatResponse,tags=["Chat"])
def chat(request: ChatRequest):
    return chat_service.get_answer(request)
