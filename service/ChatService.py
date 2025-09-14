from request.ChatRequest import ChatRequest
from response.ChatResponse import ChatResponse
from client.OpenAIClient import OpenAIClient

class ChatService:
    """Service class for chatbot business logic."""
    def __init__(self):
        self.openai_client = OpenAIClient()

    def get_answer(self, request: ChatRequest) -> ChatResponse:
        # Use OpenAIClient to get the answer from OpenAI API
        openai_response = self.openai_client.chat(prompt=request.question)

        return ChatResponse(answer=openai_response.content.strip())
