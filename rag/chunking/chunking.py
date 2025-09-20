def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into chunks of specified size with optional overlap.
    Args:
        text (str): The input text to split.
        chunk_size (int): Number of characters per chunk.
        overlap (int): Number of overlapping characters between chunks.
    Returns:
        List[str]: List of text chunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

