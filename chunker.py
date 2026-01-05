import re

def chunk_markdown(text, max_chars=800, overlap=100):
    # Remove the document title (first H1)
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        text = "\n".join(lines[1:]).strip()

    sections = re.split(r'\n##\s+', text)
    chunks = []

    for section in sections:
        if not section.strip():
            continue

        header, *body = section.split('\n', 1)
        body_text = body[0] if body else ""

        combined = (header + "\n" + body_text).strip()

        # Skip empty or header-only chunks
        if len(combined.split()) < 10:
            continue

        if len(combined) <= max_chars:
            chunks.append((header.strip(), combined))
        else:
            start = 0
            while start < len(combined):
                end = start + max_chars
                chunk = combined[start:end]
                chunks.append((header.strip(), chunk))
                start = end - overlap

    return chunks
