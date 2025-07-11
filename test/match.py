import os
from huggingface_hub import InferenceClient
from langchain.vectorstores import FAISS
from dotenv import load_dotenv


load_dotenv()
API_KEY=os.getenv("HF_KEY")


client = InferenceClient(
    provider="auto",
    api_key=API_KEY, 
)

class HFInferenceClientEmbeddings:
    def __init__(self, client: InferenceClient, model: str):
        self.client = client
        self.model = model

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self.client.feature_extraction(texts, model=self.model)

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def __call__(self, text: str) -> list[float]:
        # so FAISS.load_local & similarity_search can do `self.embedding_function(query)`
        return self.embed_query(text)

embedder = HFInferenceClientEmbeddings(
    client=client,
    model="Qwen/Qwen3-Embedding-8B",
)

CHECKPOINT_DIR = "data/index"
vector_store = FAISS.load_local(
    CHECKPOINT_DIR,
    embedder,
    allow_dangerous_deserialization=True,
)

results = vector_store.similarity_search("best beach bars in California", k=3)
for doc in results:
    print(doc.metadata, doc.page_content[:200])
