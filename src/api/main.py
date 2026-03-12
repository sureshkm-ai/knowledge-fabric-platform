from fastapi import FastAPI
from pydantic import BaseModel

from src.knowledge.chunking import chunk_markdown_docs
from src.langgraph_app.runner import ask_question
from src.observability.logger import ObservabilityLogger
from src.observability.reports import read_trace
from src.security.policies import AccessContext

app = FastAPI(title="Enterprise Multi-Source RAG Analytics Assistant")
logger = ObservabilityLogger()


class AskRequest(BaseModel):
    question: str
    user_id: str = "demo.user"
    role: str = "analyst"
    allowed_regions: list[str] = ["US-SOUTH"]
    business_units: list[str] = ["snacks"]
    include_evidence: bool = True


class AskResponse(BaseModel):
    trace_id: str
    route: str
    answer: str
    validation_notes: list[str]
    structured_evidence: list[dict] = []
    document_evidence: list[dict] = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    trace_id = logger.new_trace_id()
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
    )


@app.post("/ask/v2", response_model=AskResponse)
def ask_v2(req: AskRequest):
    return ask(req)


@app.get("/trace/{trace_id}")
def trace(trace_id: str):
    return {"events": read_trace(trace_id)}
