import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from ingest import ingest

VECTOR_DIR = "vector_store"
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
META_PATH = os.path.join(VECTOR_DIR, "metadata.pkl")

def build_index():
    os.makedirs(VECTOR_DIR, exist_ok=True)

    chunks = ingest()
    texts = [c["text"] for c in chunks]
    metadata = [
        {
            **c["metadata"],
            "text": c["text"]   # 👈 keep chunk text internally
        }
        for c in chunks
    ]  


    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"Indexed {len(texts)} chunks")
    print(f"Vector dimension: {dim}")

if __name__ == "__main__":
    build_index()
