from request.ChatRequest import ChatRequest
from response.ChatResponse import ChatResponse
from client.OpenAIClient import OpenAIClient
from rag.retrieval.retrieval import Retriever
from rag.vector_store.vector_store import VectorStore
from rag.pdf_ingestion.pdf_ingestion import ingest_pdfs
from rag.chunking.chunking import chunk_text
from rag.embedding.embedding import get_embeddings

class ChatService:
    """Service class for chatbot business logic."""
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.vector_store = VectorStore(dim=1536)
        self.retriever = Retriever(self.vector_store)
        # Populate vector store with embeddings and metadata at startup
        pdf_texts = ingest_pdfs()
        all_chunks = []
        all_metadatas = []
        for fname, text in pdf_texts.items():
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            all_metadatas.extend([f"{fname}: {chunk}" for chunk in chunks])
        embeddings = get_embeddings(all_chunks)
        self.vector_store.add(embeddings, all_metadatas)

    def get_answer(self, request: ChatRequest) -> ChatResponse:
        # Retrieve RAG context for the user's question
        context = self.retriever.retrieve_context(request.question)
        # Combine context and question for the prompt
        prompt = f"Context:\n{context}\n\nQuestion: {request.question}"
        # Use OpenAIClient to get the answer from OpenAI API
        openai_response = self.openai_client.chat(prompt=prompt)

        return ChatResponse(answer=openai_response.content.strip())
