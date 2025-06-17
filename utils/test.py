from data import load_documents, MAX_CHARS
from langchain.embeddings import HuggingFaceEmbeddings
import time

docs = load_documents()[:100]
embedder = HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-0.6B")
t0 = time.time()
_ = [embedder.embed_query(d.page_content) for d in docs]
t1 = time.time()

rate = len(docs) / (t1 - t0)   # docs per second
print(f"≈{rate:.1f} docs/sec")
