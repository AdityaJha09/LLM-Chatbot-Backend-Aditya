import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.vectors = []  # Store original vectors for reference
        self.metadata = [] # Store metadata (e.g., chunk text, filename)

    def add(self, embeddings, metadatas):
        np_embeddings = np.array(embeddings).astype('float32')
        self.index.add(np_embeddings)
        self.vectors.extend(embeddings)
        self.metadata.extend(metadatas)

    def search(self, query_embedding, top_k=5):
        query = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results

