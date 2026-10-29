"""Example: how to call the RAG tool from the backend (or any MCP client)."""
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call_search_knowledge(query: str, top_k: int = 4):
    """Minimal example of calling the RAG MCP tool."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "search_course_knowledge",
                arguments={"query": query, "top_k": top_k},
            )
            return result


# Usage in chat loop (pseudo):
# results = await call_search_knowledge(user_question)
# then inject results into the LLM prompt
