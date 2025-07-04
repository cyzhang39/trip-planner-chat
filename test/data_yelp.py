import json
from pathlib import Path
from tqdm import tqdm

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
import time

from faiss import IndexFlatL2
from langchain_community.vectorstores import FAISS

# Configuration
DATA_DIR = Path("data/yelp")
OUTPUT_DIR = Path("data/index")
MAX_CHARS = 1000
CHECKPOINT_INTERVAL = 100000  # docs per checkpoint save

def chunk_text(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split text into chunks of up to max_chars characters."""
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]

def load_documents() -> list[Document]:
    docs: list[Document] = []
    included_ids = set()
    # Load businesses
    for line in tqdm(open(DATA_DIR / "yelp_academic_dataset_business.json", encoding="utf-8"), desc="Businesses"):
        b = json.loads(line)
        if b.get("is_open") != 1 or b.get("state") != "CA":
            continue

        business_id = b.get("business_id")
        included_ids.add(business_id)

        name        = b.get("name", "")
        address     = b.get("address", "")
        city        = b.get("city", "")
        postal_code = b.get("postal_code", "")
        stars       = b.get("stars", 0)
        review_cnt  = b.get("review_count", 0)
        categories  = b.get("categories") or ""
        attributes  = b.get("attributes") or {}
        hours       = b.get("hours") or {}

        content = (
            f"Name: {name}\n"
            f"Address: {address}\n"
            f"City: {city}\n"
            f"Postal Code: {postal_code}\n"
            f"Stars: {stars} ({review_cnt} reviews)\n"
            f"Categories: {categories}\n"
            f"Attributes: {json.dumps(attributes)}\n"
            f"Hours: {json.dumps(hours)}"
        )
        metadata = {
            "business_id": business_id,
            "type": "business",
            "state": b.get("state")
        }
        docs.append(Document(page_content=content, metadata=metadata))

    # Load reviews
    for line in tqdm(open(DATA_DIR / "yelp_academic_dataset_review.json", encoding="utf-8"), desc="Reviews"):
        r = json.loads(line)
        business_id = r.get("business_id")
        if business_id not in included_ids:
            continue
        text = r.get("text", "").strip()
        for chunk in chunk_text(text):
            if not chunk:
                continue
            metadata = {"business_id": r.get("business_id"), "type": "review", "reactions_number": b.get("useful", 0) + b.get("funny", 0) + b.get("cools", 0)}
            docs.append(Document(page_content=chunk, metadata=metadata))

    # Load tips
    for line in tqdm(open(DATA_DIR / "yelp_academic_dataset_tip.json", encoding="utf-8"), desc="Tips"):
        t = json.loads(line)
        business_id = t.get("business_id")
        if business_id not in included_ids:
            continue
        text = t.get("text", "").strip()
        if not text:
            continue
        metadata = {"business_id": t.get("business_id"), "type": "tip", "compliment_count": t.get("compliment_count")}
        docs.append(Document(page_content=text, metadata=metadata))

    return docs

def main():
    docs = load_documents()
    OUTPUT_DIR.mkdir(exist_ok=True)

    vector_store = None
    batch = []
    count = 0
    embedder = HuggingFaceEmbeddings(
        model_name="Qwen/Qwen3-Embedding-0.6B",
        model_kwargs={"device": "cuda"}
    )

    for doc in docs:
        batch.append(doc)
        count += 1
        # print(count)
        # Checkpoint at intervals
        if count % CHECKPOINT_INTERVAL == 0:
            print(f"Indexing and checkpointing {count} documents...")
            if vector_store is None:
                vector_store = FAISS.from_documents(batch, embedder)
            else:
                vector_store.add_documents(batch)
            # Save checkpoint
            cp_dir = OUTPUT_DIR / f"checkpoint_{count}"
            cp_dir.mkdir(parents=True, exist_ok=True)
            vector_store.save_local(cp_dir)
            batch = []

    # Process remaining docs
    if batch:
        print(f"Indexing final {len(batch)} documents, total {count}...")
        if vector_store is None:
            vector_store = FAISS.from_documents(batch, embedder)
        else:
            vector_store.add_documents(batch)

    # Final save
    vector_store.save_local(OUTPUT_DIR)
    print(f"Indexing complete. Total documents: {count}. Index saved to {OUTPUT_DIR}")
    

if __name__ == "__main__":
    main()