from rag.embedding.embedding import get_embeddings
from rag.vector_store.vector_store import VectorStore

class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve_context(self, query, embedding_model="text-embedding-3-small", top_k=5):
        # Get embedding for the query
        query_embedding = get_embeddings([query], model=embedding_model)[0]
        # Search for relevant chunks
        results = self.vector_store.search(query_embedding, top_k=top_k)
        # Combine retrieved chunks as context
        context = "\n".join(results)
        return context

