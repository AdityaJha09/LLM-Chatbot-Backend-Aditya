from client.OpenAIClient import OpenAIClient

openai_client = OpenAIClient()  # Initialize the OpenAI client

def get_embeddings(text_chunks, model="text-embedding-3-small"):
    """
    Generates embeddings for a list of text chunks using OpenAIClient.
    Args:
        text_chunks (List[str]): List of text chunks.
        model (str): OpenAI embedding model name.
    Returns:
        List[List[float]]: List of embedding vectors.
    """
    return openai_client.embedding(text_chunks, model=model)

