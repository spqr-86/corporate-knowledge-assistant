"""MCP server wrapping handbook retrieval as a standard MCP tool.

ANCHOR: handbook_mcp_server
Role: exposes tools/handbook_search.search_handbook over the Model Context
      Protocol (stdio transport) — the course requires showing MCP as a
      protocol, not just an internal ADK FunctionTool. hr_domain_agent
      connects to this via ADK's MCPToolset (see agents/hr_domain_agent.py).
Input/Output: MCP tool call {query, top_k?} -> same dict shape as
      tools/handbook_search.search_handbook.
Run standalone: `python3 -m mcp_server.handbook_mcp_server` (stdio server).

`role` is intentionally NOT an exposed parameter — mock RBAC only means
anything if the caller (the LLM) can't just self-report a higher role. It's
hardcoded to "employee" here until there's a real auth layer to derive it
from.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from tools.handbook_search import search_handbook

mcp = FastMCP("corporate-knowledge-handbook")


@mcp.tool(name="search_handbook")
def _search_handbook(query: str, top_k: int = 3) -> dict:
    """Search the GitLab Handbook HR subset (total-rewards, hiring, people-policies)."""
    return search_handbook(query, top_k=top_k, role="employee")


if __name__ == "__main__":
    mcp.run(transport="stdio")
