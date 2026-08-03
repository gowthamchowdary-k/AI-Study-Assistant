from google import genai
import numpy as np
from config import GEMINI_API_KEY

def embed_text(text: str) -> list[float]:
    """
    Generate embedding values for a single text string using Gemini API.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Check your environment variables.")
        
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return response.embeddings[0].values

def create_embeddings(chunks):
    """
    Creates embeddings for the text inside each chunk using the Gemini API.
    """
    if not chunks:
        raise ValueError("No text chunks found to embed.")

    texts = [
        chunk["text"].strip()
        for chunk in chunks
        if chunk.get("text", "").strip()
    ]

    if not texts:
        raise ValueError("All extracted chunks are empty.")

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Check your environment variables.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Batch embed texts using Gemini's API
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=texts
    )
    
    embeddings_list = [emb.values for emb in response.embeddings]
    
    embeddings = np.asarray(
        embeddings_list,
        dtype=np.float32
    )

    if embeddings.ndim != 2:
        raise ValueError(
            f"Expected a 2D embedding array, got shape {embeddings.shape}"
        )

    return embeddings