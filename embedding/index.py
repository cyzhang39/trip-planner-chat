import torch
from pathlib import Path
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document

def build_faiss(docs, embedder, embed_batch):
    vs = None
    for i in range(0, len(docs), embed_batch):
        batch = docs[i : i + embed_batch]
        if vs is None:
            vs = FAISS.from_documents(batch, embedder)
        else:
            vs.add_documents(batch)
        # torch.cuda.empty_cache()
        # print(f"Embedded batch {i}")
    print(f"Completed FAISS indexing of {len(docs)} vectors")

    return vs

def save_index(store, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(output_dir))
    print(f"Index saved to {output_dir}")
