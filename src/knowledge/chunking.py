from pathlib import Path


def chunk_markdown_docs(source_dir: str = "data/knowledge") -> list[dict]:
    docs = []
    for path in Path(source_dir).glob("*.md"):
        text = path.read_text()
        chunks = [text[i:i+350] for i in range(0, len(text), 350)]
        for idx, chunk in enumerate(chunks):
            docs.append({
                "doc_id": f"{path.stem}::{idx}",
                "text": chunk,
                "metadata": {
                    "owner": "analytics_coe",
                    "effective_date": "2024-01-01",
                    "domain": "retail_ops",
                },
            })
    return docs
