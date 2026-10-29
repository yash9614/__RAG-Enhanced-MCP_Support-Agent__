"""MCP Server for RAG-Enhanced Support Agent.

Registers:
- Existing support tools (placeholder — copy from project_mcp)
- RAG knowledge search tool
"""
import os
from mcp.server.fastmcp import FastMCP

from mcp_server.tools.rag_tools import register_rag_tools

# ---------------------------------------------------------------------------
# Create MCP server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    name="telusko-support-mcp",
    instructions="Support desk tools + course knowledge search. Respect JWT scopes.",
)

# ---------------------------------------------------------------------------
# Register RAG tools
# ---------------------------------------------------------------------------
register_rag_tools(mcp)

# ---------------------------------------------------------------------------
# Placeholder: register your existing support tools here
# (copy from your project_mcp/mcp_server/server.py)
# ---------------------------------------------------------------------------
@mcp.tool()
def list_my_courses() -> dict:
    """Example support tool — replace with real ones from project_mcp."""
    return {"courses": ["Python Basics", "Agentic AI"]}


# ---------------------------------------------------------------------------
# Run server (stdio or SSE)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Default: stdio (good for Claude Desktop / local clients)
    # For SSE: mcp.run(transport="sse", port=8001)
    mcp.run()
