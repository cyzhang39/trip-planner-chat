from pathlib import Path
import json
from typing import List, Tuple
from langchain_community.docstore.document import Document
from langchain_community.text_splitter import RecursiveCharacterTextSplitter

def load_pairs(cleaned_json):
    pairs = []
    with cleaned_json.open("r") as f:
        for l in f:
            obj = json.loads(l)
            pairs.append((obj["title"], obj["text"]))
    return pairs

def to_documents(pairs, size, overlap):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " ", "", "!", "?"],
    )
    docs = []
    for title, text in pairs:
        for chunk in splitter.split_text(text):
            docs.append(Document(page_content=chunk, metadata={"title": title}))
    print(f"Convereted {len(docs)} chunks from {len(pairs)} documents")
    
    return docs
