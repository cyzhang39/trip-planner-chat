import torch
from langchain_huggingface import HuggingFaceEmbeddings

def load_embedder(model_name, device="cpu", batch=4):
    embedder = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
        encode_kwargs={
            "batch_size": batch,
            "normalize_embeddings": True
        },
    )

    # if device.startswith("cuda"):      
    #     embedder._client = embedder._client.half()
    
    return embedder
