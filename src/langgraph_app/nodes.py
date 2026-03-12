from src.langgraph_app.tools import choose_route, draft_sql, evidence_validate, extract_entities_simple


def plan(state: dict) -> dict:
    state["route"] = choose_route(state["question"])
    return state


def extract_entities(state: dict) -> dict:
    state["entities"] = extract_entities_simple(state["question"])
    return state


def prepare_sql(state: dict) -> dict:
    if state["route"] in {"structured", "mixed"}:
        state["sql"] = draft_sql(state["entities"])
    return state


def run_sql(state: dict, sql_runner, access_ctx) -> dict:
    if state.get("sql"):
        state["sql_result"] = sql_runner.run(state["sql"], access_ctx).to_dict(orient="records")
    return state


def retrieve_docs(state: dict, retriever, filters: dict) -> dict:
    if state["route"] in {"doc", "mixed"}:
        state["docs"] = [d.__dict__ for d in retriever.retrieve(state["question"], top_k=5, filters=filters)]
    return state


def validate_evidence(state: dict) -> dict:
    state["validation_notes"] = evidence_validate(state)
    return state


def synthesize_answer(state: dict, llm) -> dict:
    prompt = f"Question: {state['question']}\nStructured: {state.get('sql_result')}\nDocs: {state.get('docs')}"
    state["answer"] = llm.invoke(prompt, system_prompt="Ground answers in evidence and cite caveats.")
    return state
