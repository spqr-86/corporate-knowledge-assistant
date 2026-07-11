"""Shared test fixtures.

ANCHOR: conftest
Role: `fake_embedder` replaces the OpenAI embedding seam in
      tools/handbook_search.py with a deterministic bag-of-words hashing
      embedder, so retrieval tests run without OPENAI_API_KEY and without
      the on-disk index cache (which would leak real embeddings in).
"""

from __future__ import annotations

import hashlib
import re

import numpy as np
import pytest

import tools.handbook_search as hs

_FAKE_DIM = 1024

# drop function words so short queries aren't dominated by "how much in the…"
# and content words (country names, topic terms) drive the ranking — a crude
# stand-in for what a real semantic embedding gives for free
_STOPWORDS = frozenset(
    "a an and are at by does for how i in is it much my of on or the to what".split()
)


def fake_embed(texts: list[str]) -> np.ndarray:
    """Deterministic bag-of-words embedding: each token hashes to a signed
    bucket, so texts sharing literal words get higher cosine similarity —
    enough for the ranking assertions in test_handbook_search.py."""
    vecs = np.zeros((len(texts), _FAKE_DIM), dtype=np.float32)
    for i, text in enumerate(texts):
        tokens = set(re.findall(r"[a-z0-9]+", text.lower())) - _STOPWORDS
        for tok in tokens:
            digest = hashlib.md5(tok.encode()).digest()
            bucket = int.from_bytes(digest[:4], "little") % _FAKE_DIM
            sign = 1.0 if digest[4] % 2 else -1.0
            # token length as a crude IDF proxy: long tokens (country/entity
            # names) are more discriminative than short generic ones
            vecs[i, bucket] += sign * len(tok)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vecs / norms


@pytest.fixture
def fake_embedder(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    """Swap the embedder seam for the fake and isolate the index cache."""
    monkeypatch.setattr(hs, "_embed", fake_embed)
    # bypass the on-disk cache of real embeddings and any in-memory index
    monkeypatch.setattr(hs, "_INDEX_PATH", tmp_path / "fake_index.npz")
    monkeypatch.setattr(hs, "_INDEX", None)
