from pathlib import Path

from embeddings.format import clean_json
from embeddings.loader import load_pairs, to_documents
from embeddings.embedder import load_embedder
from embeddings.index import build_faiss, save_index

# ─── Configs ──────────────────────────────────────────────────────────────
RAW_JSON = Path("data/raw.json") # path to your raw data
CLEANED_JSON = Path("data/cleaned.json") # path where you want to save your cleaned data
INDEX_DIR = Path("data/index") # path where you want to store your indexed knowledge base

CHUNK_SIZE = 25_000
CHUNK_OVERLAP = 500

# or whatever huggingface embedding model you want to use
EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B" 


# Adjust batch sizes for your GPU/CPU
DEVICE = "cuda"
BATCH = 4
EMBED_BATCH = 256
# ────────────────────────────────────────────────────────────────────────────────

def main():
    clean_json(RAW_JSON, CLEANED_JSON)
    pairs = load_pairs(CLEANED_JSON)
    docs = to_documents(pairs, CHUNK_SIZE, CHUNK_OVERLAP)
    embedder = load_embedder(EMBED_MODEL, DEVICE, BATCH)
    faiss = build_faiss(docs, embedder, EMBED_BATCH)
    save_index(faiss, INDEX_DIR)

if __name__ == "__main__":
    main()
