from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# 1) Re‐instantiate your embedder exactly as before
embedder = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen3-Embedding-0.6B",
    model_kwargs={"device": "cuda"}       # or cpu, whatever you used
)

# 2) Point to the folder for your last checkpoint
CHECKPOINT_DIR = "./../data/index"

# 3) Load the FAISS index from disk
vector_store = FAISS.load_local(CHECKPOINT_DIR, embedder, allow_dangerous_deserialization=True)

# Now `vector_store` contains exactly the ~4M docs you had embedded so far.
# You can immediately do:
docs = vector_store.similarity_search("best beach bars in California", k=5)
for d in docs:
    print(d.metadata, d.page_content[:200])