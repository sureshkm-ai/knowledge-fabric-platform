"""FastAPI application for enterprise multi-source analytics assistant."""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.knowledge.chunking import chunk_markdown_docs
from src.langgraph_app.runner import ask_question
from src.observability.logger import ObservabilityLogger
from src.observability.reports import read_trace, summarize_trace
from src.security.policies import AccessContext

app = FastAPI(title="Enterprise Multi-Source RAG Analytics Assistant", version="2.0.0")
logger = ObservabilityLogger()


class AskRequest(BaseModel):
    question: str
    user_id: str = "demo.user"
    role: str = "analyst"
    allowed_regions: list[str] = Field(default_factory=lambda: ["US-SOUTH"])
    business_units: list[str] = Field(default_factory=lambda: ["snacks"])
    include_evidence: bool = True


class AskResponse(BaseModel):
    trace_id: str
    route: str
    answer: str
    validation_notes: list[str]
    structured_evidence: list[dict] = Field(default_factory=list)
    document_evidence: list[dict] = Field(default_factory=list)
    diagnostics: dict = Field(default_factory=dict)


@app.get("/health")
def health():
    return {"status": "ok", "service": app.title, "version": app.version}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    trace_id = logger.new_trace_id()
    logger.log(trace_id, "question_received", {"question": req.question, "role": req.role, "regions": req.allowed_regions})

    ctx = AccessContext(
        user_id=req.user_id,
        role=req.role,
        allowed_regions=req.allowed_regions,
        business_units=req.business_units,
    )
    docs = chunk_markdown_docs()
    result = ask_question(req.question, ctx, docs)

    logger.log(
        trace_id,
        "answer_generated",
        {
            "route": result.get("route"),
            "validation": result.get("validation_notes", []),
            "diagnostics": result.get("diagnostics", {}),
        },
    )
    return AskResponse(
        trace_id=trace_id,
        route=result.get("route", "mixed"),
        answer=result.get("answer") or "",
        validation_notes=result.get("validation_notes", []),
        structured_evidence=result.get("sql_result", []) if req.include_evidence else [],
        document_evidence=result.get("docs", []) if req.include_evidence else [],
        diagnostics=result.get("diagnostics", {}),
    )


@app.post("/ask/v2", response_model=AskResponse)
def ask_v2(req: AskRequest):
    return ask(req)


@app.get("/trace/{trace_id}")
def trace(trace_id: str):
    return {"events": read_trace(trace_id), "summary": summarize_trace(trace_id).model_dump()}
