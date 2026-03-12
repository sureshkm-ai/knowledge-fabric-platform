from src.langgraph_app import nodes


def run_graph(state: dict, sql_runner, access_ctx, retriever, llm, filters: dict) -> dict:
    state = nodes.plan(state)
    state = nodes.extract_entities(state)
    state = nodes.prepare_sql(state)
    state = nodes.run_sql(state, sql_runner, access_ctx)
    state = nodes.retrieve_docs(state, retriever, filters)
    state = nodes.validate_evidence(state)
    state = nodes.synthesize_answer(state, llm)
    return state
