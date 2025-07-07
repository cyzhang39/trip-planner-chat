from pathlib import Path

from embeddings.format import clean_json
from embeddings.loader import load_pairs, to_documents
from embeddings.embedder import load_embedder
from embeddings.index import build_faiss, save_index

RAW_JSON = Path("data/raw.json")
CLEANED_JSON = Path("data/cleaned.json")
INDEX_DIR = Path("data/index")
CHUNK_SIZE = 25000
CHUNK_OVERLAP = 500
EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B" 
DEVICE = "cuda"
BATCH = 4
EMBED_BATCH = 256


clean_json(RAW_JSON, CLEANED_JSON)
pairs = load_pairs(CLEANED_JSON)
docs = to_documents(pairs, CHUNK_SIZE, CHUNK_OVERLAP)
embedder = load_embedder(EMBED_MODEL, DEVICE, BATCH)
faiss = build_faiss(docs, embedder, EMBED_BATCH)
save_index(faiss, INDEX_DIR)


