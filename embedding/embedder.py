import torch
from langchain_huggingface import HuggingFaceEmbeddings

def load_embedder(model_name: str, device: str = "cpu", batch: int = 4):
    """
    Load a huggingface embedder
    """
    embedder = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
        encode_kwargs={
            "batch_size": batch,
            "normalize_embeddings": True
        },
    )
    # use lower precision for less vram usage
    # if device.startswith("cuda"):      
    #     embedder._client = embedder._client.half()
    
    return embedder
