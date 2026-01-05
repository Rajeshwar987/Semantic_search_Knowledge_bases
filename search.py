import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================
# Relevance thresholds
# =========================
STRONG_MATCH = 0.78
WEAK_MATCH = 0.60

# =========================
# Paths
# =========================
INDEX_PATH = "vector_store/faiss.index"
META_PATH = "vector_store/metadata.pkl"

# =========================
# Load embedding model
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# Load FAISS index
# =========================
index = faiss.read_index(INDEX_PATH)

# =========================
# Load metadata
# =========================
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

# =========================
# Stopwords for explainability
# =========================
STOPWORDS = {
    "in", "on", "at", "the", "a", "an", "to", "of", "for",
    "and", "or", "is", "are", "was", "were", "with"
}

# =========================
# Explainability helper
# =========================
def build_reason(query: str, meta: dict) -> str:
    title = meta["title"]
    section = meta["section"].replace("##", "").strip()

    if "resolution" in section.lower():
        return f"Provides remediation guidance related to {title.lower()}"

    if "symptom" in section.lower():
        return f"Describes symptoms related to {title.lower()}"

    if "root cause" in section.lower():
        return f"Explains underlying causes related to {title.lower()}"

    return f"Semantically related to {title.lower()}"


# =========================
# Core semantic search
# =========================
def semantic_search(query: str, top_k: int = 3, domain: str | None = None):
    print("DEBUG: semantic_search() from NEW search.py is running")

    # -------------------------
    # Step 1: Vector search
    # -------------------------
    query_vector = model.encode([query])
    k = min(top_k * 4, index.ntotal)
    distances, indices = index.search(query_vector, k)

    candidates = []

    for dist, idx in zip(distances[0], indices[0]):
        idx = int(idx)
        if idx >= len(metadata):
            continue

        meta = metadata[idx]

        # Domain filter
        if domain and meta["source"] != domain:
            continue

        # Distance → similarity
        score = 1 / (1 + float(dist))

        # Section-aware boosting
        section_lower = meta["section"].lower()
        if "resolution" in section_lower:
            score += 0.05
        elif "root cause" in section_lower:
            score += 0.03

        candidates.append({
            "score": round(score, 3),
            "title": meta["title"],
            "section": meta["section"],
            "source": meta["source"],
            "path": meta["path"],
            "reason": build_reason(query, meta)
        })

    candidates.sort(key=lambda x: x["score"], reverse=True)

    # -------------------------
    # Step 2: Document-level dedup
    # -------------------------
    doc_map = {}

    for c in candidates:
        doc_key = c["path"]
        section_clean = c["section"].replace("##", "").strip()

        if doc_key not in doc_map:
            doc_map[doc_key] = {
                "score": c["score"],
                "title": c["title"],
                "source": c["source"],
                "path": c["path"],
                "primary_section": section_clean,
                "supporting_sections": [],
                "reason": c["reason"]
            }
        else:
            current_primary = doc_map[doc_key]["primary_section"].lower()
            incoming_section = section_clean.lower()
            score_diff = abs(c["score"] - doc_map[doc_key]["score"])

            # Resolution-first bias when scores are close
            if (
                "resolution" in incoming_section
                and "resolution" not in current_primary
                and score_diff <= 0.05
            ):
                doc_map[doc_key]["supporting_sections"].append(
                    doc_map[doc_key]["primary_section"]
                )
                doc_map[doc_key]["primary_section"] = section_clean
                doc_map[doc_key]["score"] = c["score"]

            elif c["score"] > doc_map[doc_key]["score"]:
                doc_map[doc_key]["supporting_sections"].append(
                    doc_map[doc_key]["primary_section"]
                )
                doc_map[doc_key]["primary_section"] = section_clean
                doc_map[doc_key]["score"] = c["score"]

            else:
                doc_map[doc_key]["supporting_sections"].append(section_clean)

    deduped_results = list(doc_map.values())
    deduped_results.sort(key=lambda x: x["score"], reverse=True)
    # Filter out very weak secondary results
    deduped_results = [
        r for r in deduped_results if r["score"] >= WEAK_MATCH
    ]


    # -------------------------
    # Step 3: Confidence + return
    # -------------------------
    # if not deduped_results or deduped_results[0]["score"] < WEAK_MATCH:
    #     return {
    #         "summary": "No relevant knowledge base information found.",
    #         "results": [],
    #         "confidence": "LOW"
    #     }

    results = deduped_results[:top_k]
    top_score = results[0]["score"]

    if top_score < STRONG_MATCH:
        summary = (
            "A partially relevant knowledge base article was found, "
            "but it may not fully address the query intent."
        )
        confidence = "MEDIUM"
    else:
        summary = "Relevant knowledge base guidance found."
        confidence = "HIGH"
    explanation = (
        "Results are ranked based on semantic similarity to the query, "
        "with preference given to actionable remediation sections when relevance is comparable. "
        "Documents below the relevance threshold are excluded to reduce noise."
    )

    return {
        "summary": summary,
        "results": results,
        "confidence": confidence,
        "explanation": explanation
    }

# =========================
# Local sanity tests
# =========================
if __name__ == "__main__":
    print(semantic_search("report not visible in insights tab", domain="pega"))
    print(semantic_search("malware detected on server", domain="public_it"))
    print(semantic_search("completely unrelated query"))
