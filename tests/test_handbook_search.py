from tools.handbook_search import search_handbook


def test_search_returns_relevant_result_for_known_topic():
    result = search_handbook("parental leave benefits")
    assert result["status"] == "success"
    assert len(result["results"]) > 0
    assert any(
        "parental" in r["title"].lower() or "parental" in r["snippet"].lower()
        for r in result["results"]
    )


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
