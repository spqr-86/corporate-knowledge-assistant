"""Keyword search over the local GitLab Handbook markdown subset.

ANCHOR: handbook_search
Role: retrieval tool for the ADK agent — simple keyword/BM25-style search
      over ~/projects/ai/corporate-knowledge-assistant/data/handbook.
Input: query (str), top_k (int)
Output: list of {path, title, snippet, score} dicts
No embeddings/vector DB yet — MVP for the ADK loop; swap for real
retrieval (chunking + embeddings) once the agent loop works end to end.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "handbook"

_WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z\-']+")


@dataclass
class Document:
    path: Path
    title: str
    text: str
    tokens: list[str]


def _tokenize(text: str) -> list[str]:
    return [w.lower() for w in _WORD_RE.findall(text)]


def _load_documents() -> list[Document]:
    docs: list[Document] = []
    for md_path in sorted(DATA_DIR.rglob("*.md")):
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        title = md_path.stem.replace("-", " ").replace("_", " ")
        for line in text.splitlines():
            if line.strip().startswith("# "):
                title = line.strip("# ").strip()
                break
        docs.append(
            Document(path=md_path, title=title, text=text, tokens=_tokenize(text))
        )
    return docs


_DOCS_CACHE: list[Document] | None = None


def _get_docs() -> list[Document]:
    global _DOCS_CACHE
    if _DOCS_CACHE is None:
        _DOCS_CACHE = _load_documents()
    return _DOCS_CACHE


def _score(query_tokens: list[str], doc: Document) -> float:
    if not doc.tokens:
        return 0.0
    doc_len = len(doc.tokens)
    score = 0.0
    for qt in query_tokens:
        count = doc.tokens.count(qt)
        if count:
            score += count / doc_len * 1000
    return score


def _snippet(doc: Document, query_tokens: list[str], width: int = 300) -> str:
    lower = doc.text.lower()
    for qt in query_tokens:
        idx = lower.find(qt)
        if idx != -1:
            start = max(0, idx - width // 2)
            end = min(len(doc.text), idx + width // 2)
            return doc.text[start:end].strip().replace("\n", " ")
    return doc.text[:width].strip().replace("\n", " ")


def search_handbook(query: str, top_k: int = 3) -> dict:
    """Search the GitLab Handbook subset (total-rewards, hiring, people-policies).

    Args:
        query: natural-language question or keywords to search for.
        top_k: number of top matching documents to return (default 3).

    Returns:
        dict with 'status' ('success' or 'error') and 'results': a list of
        {relative_path, title, snippet, score} for the best-matching docs.
    """
    query_tokens = _tokenize(query)
    if not query_tokens:
        return {"status": "error", "error_message": "Empty query."}

    docs = _get_docs()
    if not docs:
        return {
            "status": "error",
            "error_message": f"No handbook documents found under {DATA_DIR}.",
        }

    scored = [(d, _score(query_tokens, d)) for d in docs]
    scored = [pair for pair in scored if pair[1] > 0]
    scored.sort(key=lambda pair: pair[1], reverse=True)

    if not scored:
        return {"status": "success", "results": []}

    results = []
    for doc, score in scored[:top_k]:
        results.append(
            {
                "relative_path": str(doc.path.relative_to(DATA_DIR)),
                "title": doc.title,
                "snippet": _snippet(doc, query_tokens),
                "score": round(score, 2),
            }
        )
    return {"status": "success", "results": results}
