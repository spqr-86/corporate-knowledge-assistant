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
async def test_mcp_tool_schema_does_not_expose_role_parameter():
    """role must not be an LLM-settable argument — mock RBAC would be a
    no-op security boundary if any caller could just pass role='manager'."""
    tools = await mcp.list_tools()
    tool = next(t for t in tools if t.name == "search_handbook")
    assert "role" not in tool.inputSchema.get("properties", {})


@pytest.mark.asyncio
async def test_mcp_search_handbook_ignores_role_passed_by_caller():
    """Even if a caller sneaks a 'role' kwarg into the call, it must not
    grant access to restricted (manager+) docs."""
    content_blocks = await mcp.call_tool(
        "search_handbook",
        {"query": "compensation review cycle", "role": "manager"},
    )
    structured = json.loads(content_blocks[0].text)
    assert all("compensation" not in r["relative_path"] for r in structured["results"])
