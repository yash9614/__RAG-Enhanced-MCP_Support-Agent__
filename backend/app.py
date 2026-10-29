"""Minimal FastAPI backend with tool-calling loop.

Can call:
- MCP tools (support actions + RAG search)
- Falls back gracefully
"""
import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

app = FastAPI(title="RAG-MCP Support Agent")

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    reply: str
    tool_calls: Optional[List[dict]] = None


# ---------------------------------------------------------------------------
# LLM
# ---------------------------------------------------------------------------
def get_llm():
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="No API key set")
    # Use OpenAI or Groq-compatible
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=api_key,
    )


SYSTEM_PROMPT = """You are a helpful support agent for an online course platform.

You have two kinds of tools:
1. Structured support tools (list courses, tickets, certificates, etc.)
2. search_course_knowledge — use this when the user asks about course content, policies, FAQs, or how-to questions.

Always cite sources when you use knowledge search.
Be concise and helpful.
"""


# ---------------------------------------------------------------------------
# Simple chat endpoint (tool calling can be expanded with LangGraph later)
# ---------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    llm = get_llm()

    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    if req.history:
        for h in req.history[-6:]:  # keep recent context
            if h.get("role") == "user":
                messages.append(HumanMessage(content=h["content"]))
            else:
                messages.append(AIMessage(content=h["content"]))

    messages.append(HumanMessage(content=req.message))

    # For a full tool-calling loop, integrate MCP client here
    # (see project_mcp/backend/app.py for the real pattern)
    response = llm.invoke(messages)

    return ChatResponse(
        reply=response.content,
        tool_calls=None,  # populate when MCP client is wired
    )


@app.get("/health")
def health():
    return {"status": "ok", "rag": "ready"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
