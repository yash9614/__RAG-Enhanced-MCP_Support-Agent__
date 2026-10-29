"""MCP tool for knowledge base search."""
from mcp.server.fastmcp import FastMCP

from rag.retriever import search_knowledge

# This will be imported / mounted into the main MCP server
# Example usage inside mcp_server/server.py:


def register_rag_tools(mcp: FastMCP):
    @mcp.tool()
    def search_course_knowledge(query: str, top_k: int = 4) -> list:
        """Search the course knowledge base (docs, FAQs, policies).

        Returns relevant chunks with source citations.
        Use this when the user asks about course content, policies, or how-to questions.
        """
        return search_knowledge(query, top_k=top_k)

    return mcp
