import openai
import pytest

import tools.handbook_search as hs
from tools.handbook_search import search_handbook

# all tests run against the deterministic fake embedder (tests/conftest.py) —
# no OPENAI_API_KEY needed
pytestmark = pytest.mark.usefixtures("fake_embedder")


def test_search_returns_error_dict_when_embedding_fails(monkeypatch):
    """OpenAI/network failures must honor the documented contract
    ({status: error, ...}) instead of raising out of search_handbook."""

    def _boom(texts):
        raise openai.OpenAIError("no api key / network down")

    monkeypatch.setattr(hs, "_embed", _boom)
    monkeypatch.setattr(hs, "_INDEX", None)
    result = search_handbook("parental leave benefits")
    assert result["status"] == "error"
    assert result["error_message"]


def test_search_returns_relevant_result_for_known_topic():
    result = search_handbook("parental leave benefits")
    assert result["status"] == "success"
    assert len(result["results"]) > 0
    assert any(
        "parental" in r["title"].lower() or "parental" in r["snippet"].lower()
        for r in result["results"]
    )


def test_search_ranks_country_specific_file_top():
    # RAG must surface the entity-specific handbook file, not a generic index,
    # when the query names a country — this is what the country-awareness demo
    # depends on (keyword BM25 ranked generic _index.md above the country file).
    result = search_handbook("how much parental leave in the Netherlands")
    assert result["status"] == "success"
    assert result["results"], "expected at least one result"
    assert "netherlands" in result["results"][0]["relative_path"].lower()


def test_search_empty_query_errors():
    result = search_handbook("")
    assert result["status"] == "error"


def test_search_no_match_returns_empty_results():
    result = search_handbook("zqxvwplk zzyyxxwwqq")
    assert result["status"] == "success"
    assert result["results"] == []


def test_search_excludes_compensation_docs_for_employee_role():
    result = search_handbook("compensation review cycle", role="employee")
    assert result["status"] == "success"
    assert all("compensation" not in r["relative_path"] for r in result["results"])


def test_search_includes_compensation_docs_for_manager_role():
    result = search_handbook("compensation review cycle", role="manager")
    assert result["status"] == "success"
    assert any("compensation" in r["relative_path"] for r in result["results"])
