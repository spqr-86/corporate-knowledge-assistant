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
