<<<<<<< HEAD
"""FastAPI application for enterprise multi-source analytics assistant."""
from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field
=======
from fastapi import FastAPI
from pydantic import BaseModel
>>>>>>> main

from src.knowledge.chunking import chunk_markdown_docs
from src.langgraph_app.runner import ask_question
from src.observability.logger import ObservabilityLogger
<<<<<<< HEAD
from src.observability.reports import read_trace, summarize_trace
from src.security.policies import AccessContext

app = FastAPI(title="Enterprise Multi-Source RAG Analytics Assistant", version="2.0.0")
=======
from src.observability.reports import read_trace
from src.security.policies import AccessContext

app = FastAPI(title="Enterprise Multi-Source RAG Analytics Assistant")
>>>>>>> main
logger = ObservabilityLogger()


class AskRequest(BaseModel):
    question: str
    user_id: str = "demo.user"
    role: str = "analyst"
<<<<<<< HEAD
    allowed_regions: list[str] = Field(default_factory=lambda: ["US-SOUTH"])
    business_units: list[str] = Field(default_factory=lambda: ["snacks"])
=======
    allowed_regions: list[str] = ["US-SOUTH"]
    business_units: list[str] = ["snacks"]
>>>>>>> main
    include_evidence: bool = True


class AskResponse(BaseModel):
    trace_id: str
    route: str
    answer: str
    validation_notes: list[str]
<<<<<<< HEAD
    structured_evidence: list[dict] = Field(default_factory=list)
    document_evidence: list[dict] = Field(default_factory=list)
    diagnostics: dict = Field(default_factory=dict)
=======
    structured_evidence: list[dict] = []
    document_evidence: list[dict] = []
>>>>>>> main


@app.get("/health")
def health():
<<<<<<< HEAD
    return {"status": "ok", "service": app.title, "version": app.version}
=======
    return {"status": "ok"}
>>>>>>> main


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    trace_id = logger.new_trace_id()
<<<<<<< HEAD
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
=======
    logger.log(trace_id, "question_received", {"question": req.question})
    ctx = AccessContext(user_id=req.user_id, role=req.role, allowed_regions=req.allowed_regions, business_units=req.business_units)
    docs = chunk_markdown_docs()
    result = ask_question(req.question, ctx, docs)
    logger.log(trace_id, "answer_generated", {"route": result["route"], "validation": result["validation_notes"]})
    return AskResponse(
        trace_id=trace_id,
        route=result["route"],
        answer=result["answer"] or "",
        validation_notes=result["validation_notes"],
        structured_evidence=result.get("sql_result", []) if req.include_evidence else [],
        document_evidence=result.get("docs", []) if req.include_evidence else [],
>>>>>>> main
    )


@app.post("/ask/v2", response_model=AskResponse)
def ask_v2(req: AskRequest):
    return ask(req)


@app.get("/trace/{trace_id}")
def trace(trace_id: str):
<<<<<<< HEAD
    return {"events": read_trace(trace_id), "summary": summarize_trace(trace_id).model_dump()}
=======
    return {"events": read_trace(trace_id)}
>>>>>>> main
