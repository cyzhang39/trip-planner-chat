import torch
from pathlib import Path
from typing import List
from custom_langchain.vectorstores import FAISS
from custom_langchain.docstore.document import Document

def build_faiss(docs: List[Document], embedder, embed_batch: int = 256):
    """
    Construct FAISS indexes from batched documents
    """
    vs = None
    for i in range(0, len(docs), embed_batch):
        batch = docs[i : i + embed_batch]
        if vs is None:
            vs = FAISS.from_documents(batch, embedder)
        else:
            vs.add_documents(batch)
        torch.cuda.empty_cache()
        # print(f"Embedded batch {i}")
    print(f"Completed FAISS indexing of {len(docs)} vectors")

    return vs

def save_index(store: FAISS, output_dir: Path):
    """
    Save index
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(output_dir))
    print(f"Index saved to {output_dir}")
