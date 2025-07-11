from collections import Counter
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedder = HuggingFaceEmbeddings(
        model_name="Qwen/Qwen3-Embedding-0.6B",
        model_kwargs={"device": device}
    )

    vector_store = FAISS.load_local(
        "data/index",
        embedder,
        allow_dangerous_deserialization=True
    )

    docs = list(vector_store.docstore._dict.values())

    lengths = []
    for doc in docs:
        tokens = embedder._client.tokenizer(
            doc.page_content,
            return_tensors="pt"
        )["input_ids"][0]
        lengths.append(len(tokens))

    buckets = Counter()
    for L in lengths:
        low = (L // 1000) * 1000
        high = low + 999
        buckets[f"{low}-{high}"] += 1

    print("Document length distribution (in tokens):")
    for bucket in sorted(buckets, key=lambda x: int(x.split("-")[0])):
        print(f"{bucket}: {buckets[bucket]} document(s)")

if __name__ == "__main__":
    main()
