from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embedder = HuggingFaceEmbeddings(
    model_name="Qwen/Qwen3-Embedding-0.6B",
    model_kwargs={"device": "cuda"}      
)

CHECKPOINT_DIR = "data/index"

vector_store = FAISS.load_local(CHECKPOINT_DIR, embedder, allow_dangerous_deserialization=True)


docs = vector_store.similarity_search("best beach bars in California", k=5)
# for d in docs:
#     print(d.metadata, d.page_content[:200])