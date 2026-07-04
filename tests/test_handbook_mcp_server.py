import json

import pytest

from mcp_server.handbook_mcp_server import mcp


@pytest.mark.asyncio
async def test_mcp_server_exposes_search_handbook_tool():
    tools = await mcp.list_tools()
    names = {t.name for t in tools}
    assert "search_handbook" in names


@pytest.mark.asyncio
async def test_mcp_search_handbook_returns_results_for_known_topic():
    content_blocks = await mcp.call_tool(
        "search_handbook", {"query": "parental leave benefits"}
    )
    structured = json.loads(content_blocks[0].text)
    assert structured["status"] == "success"
    assert len(structured["results"]) > 0


@pytest.mark.asyncio
async def test_mcp_search_handbook_defaults_to_employee_role():
    """role defaults to employee when the caller doesn't specify one — the
    MCP layer trusts its caller's role argument (see docstring); the actual
    LLM-exploit defense lives one layer up in
    guardrails/role_binding.py's before_tool_callback, which always
    overwrites this arg from session state before it ever reaches here."""
    content_blocks = await mcp.call_tool(
        "search_handbook", {"query": "compensation review cycle"}
    )
    structured = json.loads(content_blocks[0].text)
    assert all("compensation" not in r["relative_path"] for r in structured["results"])


@pytest.mark.asyncio
async def test_mcp_search_handbook_respects_explicit_role_argument():
    """A trusted caller (the role_binding callback) can legitimately grant
    manager-level access by passing role='manager' — this layer's job is
    just to honor whatever role it's given, not to authenticate it."""
    content_blocks = await mcp.call_tool(
        "search_handbook",
        {"query": "compensation review cycle", "role": "manager"},
    )
    structured = json.loads(content_blocks[0].text)
    assert any("compensation" in r["relative_path"] for r in structured["results"])
