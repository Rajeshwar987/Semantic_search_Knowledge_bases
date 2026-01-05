import os
from chunker import chunk_markdown

DOC_ROOT = "data/docs"

def load_markdown_files():
    documents = []

    for root, _, files in os.walk(DOC_ROOT):
        for file in files:
            if not file.endswith(".md"):
                continue

            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            source = "pega" if "pega" in root else "public_it"
            doc_id = file.replace(".md", "")

            documents.append({
                "doc_id": doc_id,
                "path": path,
                "source": source,
                "content": content
            })

    return documents


def ingest():
    all_chunks = []

    docs = load_markdown_files()

    for doc in docs:
        text = doc["content"]

        # Extract title (first line)
        title = text.split("\n")[0].replace("#", "").strip()

        chunks = chunk_markdown(text)

        for section, chunk_text in chunks:
            all_chunks.append({
                "text": chunk_text,
                "metadata": {
                    "doc_id": doc["doc_id"],
                    "title": title,
                    "section": section,
                    "source": doc["source"],
                    "path": doc["path"]
                }
            })

    return all_chunks


if __name__ == "__main__":
    chunks = ingest()
    print(f"Total chunks created: {len(chunks)}")
    print(chunks[0])