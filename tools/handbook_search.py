"""Embedding-based semantic search over the local GitLab Handbook subset.

ANCHOR: handbook_search
Role: retrieval tool for the ADK agent — real RAG (chunk + embed + cosine)
      over data/handbook. Replaced the earlier keyword/BM25 MVP, which ranked
      generic index files above country/entity-specific ones and so broke the
      country-awareness flow (an "I'm in the Netherlands" question could not
      surface bv-benefits-netherlands.md).
Input: query (str), top_k (int), role (str) for mock RBAC gating.
Output: dict {status, results:[{relative_path, title, snippet, score}]} —
      SAME shape the MCP server (mcp_server/handbook_mcp_server.py) and the
      ADK agent already depend on. Do not change the shape without updating both.
Embeddings: OpenAI text-embedding-3-small, batched once and cached to
      data/.handbook_index.npz keyed by a signature over the source files
      (path+size+mtime); rebuilt only when the handbook changes.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "handbook"
_INDEX_PATH = Path(__file__).resolve().parent.parent / "data" / ".handbook_index.npz"

_EMBED_MODEL = "text-embedding-3-small"
_MAX_CHUNK_CHARS = 1500
_MIN_CHUNK_CHARS = 30
# cosine below this counts as "no relevant match" so a nonsense query returns []
_SCORE_THRESHOLD = 0.30

_ROLE_RANK = {"employee": 0, "manager": 1, "hr_admin": 2}
# mock RBAC: relative-path prefixes gated to a minimum role
_RESTRICTED_PREFIXES: dict[str, str] = {
    "total-rewards/compensation": "manager",
}


def _min_role_for(relative_path: str) -> str:
    for prefix, role in _RESTRICTED_PREFIXES.items():
        if relative_path.startswith(prefix):
            return role
    return "employee"


def _role_allows(role: str, relative_path: str) -> bool:
    return _ROLE_RANK.get(role, 0) >= _ROLE_RANK[_min_role_for(relative_path)]


@dataclass
class Chunk:
    relative_path: str
    title: str
    text: str


def _split_into_chunks(text: str, default_title: str) -> list[tuple[str, str]]:
    """Split markdown into (title, chunk_text) by heading, capping chunk size."""
    chunks: list[tuple[str, str]] = []
    current_title = default_title
    buf: list[str] = []

    def flush() -> None:
        body = "\n".join(buf).strip()
        if len(body) < _MIN_CHUNK_CHARS:
            return
        # cap oversized sections into character windows
        for start in range(0, len(body), _MAX_CHUNK_CHARS):
            piece = body[start : start + _MAX_CHUNK_CHARS].strip()
            if len(piece) >= _MIN_CHUNK_CHARS:
                chunks.append((current_title, piece))

    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            flush()
            buf = []
            current_title = line.strip("# ").strip() or current_title
        buf.append(line)
    flush()
    return chunks


def _load_chunks() -> list[Chunk]:
    chunks: list[Chunk] = []
    for md_path in sorted(DATA_DIR.rglob("*.md")):
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        rel = str(md_path.relative_to(DATA_DIR))
        default_title = md_path.stem.replace("-", " ").replace("_", " ")
        # entity/name tokens from the path give the embedding a strong,
        # section-independent signal about which country/entity this is, so a
        # country query aligns with its file even when the section body doesn't
        # repeat the country name
        path_hint = rel.replace("/", " ").replace("-", " ").replace(".md", "")
        for title, body in _split_into_chunks(text, default_title):
            chunks.append(
                Chunk(
                    relative_path=rel,
                    title=title,
                    text=f"[{path_hint}] {title}\n{body}",
                )
            )
    return chunks


def _signature() -> str:
    parts = []
    for md_path in sorted(DATA_DIR.rglob("*.md")):
        st = md_path.stat()
        parts.append(f"{md_path.relative_to(DATA_DIR)}:{st.st_size}:{int(st.st_mtime)}")
    parts.append(_EMBED_MODEL)
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()


def _embed(texts: list[str]) -> np.ndarray:
    from openai import OpenAI

    client = OpenAI()
    resp = client.embeddings.create(model=_EMBED_MODEL, input=texts)
    vecs = np.array([d.embedding for d in resp.data], dtype=np.float32)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vecs / norms


@dataclass
class _Index:
    signature: str
    chunks: list[Chunk]
    matrix: np.ndarray  # (N, D) L2-normalized


_INDEX: _Index | None = None


def _build_index() -> _Index:
    chunks = _load_chunks()
    matrix = _embed([c.text for c in chunks])
    return _Index(signature=_signature(), chunks=chunks, matrix=matrix)


def _save_index(index: _Index) -> None:
    meta = [
        {"relative_path": c.relative_path, "title": c.title, "text": c.text}
        for c in index.chunks
    ]
    np.savez_compressed(
        _INDEX_PATH,
        signature=index.signature,
        matrix=index.matrix,
        meta=json.dumps(meta),
    )


def _load_cached_index(signature: str) -> _Index | None:
    if not _INDEX_PATH.exists():
        return None
    try:
        data = np.load(_INDEX_PATH, allow_pickle=False)
        if str(data["signature"]) != signature:
            return None
        meta = json.loads(str(data["meta"]))
        chunks = [Chunk(**m) for m in meta]
        return _Index(signature=signature, chunks=chunks, matrix=data["matrix"])
    except (KeyError, ValueError, OSError):
        return None


def _get_index() -> _Index:
    global _INDEX
    sig = _signature()
    if _INDEX is not None and _INDEX.signature == sig:
        return _INDEX
    cached = _load_cached_index(sig)
    if cached is not None:
        _INDEX = cached
        return _INDEX
    _INDEX = _build_index()
    _save_index(_INDEX)
    return _INDEX


def _snippet(text: str, width: int = 300) -> str:
    # drop the synthetic "[path hint] title" prefix line for display
    body = text.split("\n", 1)[-1] if text.startswith("[") else text
    return body[:width].strip().replace("\n", " ")


def search_handbook(query: str, top_k: int = 3, role: str = "employee") -> dict:
    """Semantic search over the GitLab Handbook subset.

    Args:
        query: natural-language question or keywords to search for.
        top_k: number of top matching documents to return (default 3).
        role: requesting user's role (employee/manager/hr_admin) — gates
            access to restricted sub-sections (mock RBAC, see _RESTRICTED_PREFIXES).

    Returns:
        dict with 'status' ('success' or 'error') and 'results': a list of
        {relative_path, title, snippet, score} for the best-matching docs,
        deduplicated to one entry per source file (highest-scoring chunk).
    """
    if not query or not query.strip():
        return {"status": "error", "error_message": "Empty query."}

    # lazy import (mirrors _embed) — keeps module import free of openai
    from openai import OpenAIError

    try:
        index = _get_index()
    except (OpenAIError, ConnectionError, OSError) as exc:
        return {
            "status": "error",
            "error_message": f"Failed to build handbook index (embedding error): {exc}",
        }
    if not index.chunks:
        return {
            "status": "error",
            "error_message": f"No handbook documents found under {DATA_DIR}.",
        }

    allowed = [
        i for i, c in enumerate(index.chunks) if _role_allows(role, c.relative_path)
    ]
    if not allowed:
        return {"status": "success", "results": []}

    try:
        q = _embed([query])[0]
    except (OpenAIError, ConnectionError, OSError) as exc:
        return {
            "status": "error",
            "error_message": f"Failed to embed query (embedding error): {exc}",
        }
    sims = index.matrix[allowed] @ q  # cosine (both L2-normalized)

    order = np.argsort(sims)[::-1]
    best_per_file: dict[str, tuple[float, Chunk]] = {}
    for j in order:
        score = float(sims[j])
        if score < _SCORE_THRESHOLD:
            break
        chunk = index.chunks[allowed[j]]
        prev = best_per_file.get(chunk.relative_path)
        if prev is None or score > prev[0]:
            best_per_file[chunk.relative_path] = (score, chunk)

    ranked = sorted(best_per_file.values(), key=lambda p: p[0], reverse=True)
    results = [
        {
            "relative_path": chunk.relative_path,
            "title": chunk.title,
            "snippet": _snippet(chunk.text),
            "score": round(score, 4),
        }
        for score, chunk in ranked[:top_k]
    ]
    return {"status": "success", "results": results}
