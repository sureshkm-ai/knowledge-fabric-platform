import pandas as pd

from src.langgraph_app.graph import run_graph
from src.security.policies import AccessContext
from src.vectorstore.base import RetrievedDoc


class FakeRunner:
    def run(self, sql, ctx):
<<<<<<< HEAD
        return pd.DataFrame([{"date": "2024-01-01", "region": "US-SOUTH", "total_net_sales": 1.0}])
=======
        return pd.DataFrame([{"date": "2024-01-01", "total_net_sales": 1.0}])
>>>>>>> main


class FakeRetriever:
    def retrieve(self, q, top_k=5, filters=None):
<<<<<<< HEAD
        return [RetrievedDoc("d1", "policy note", 0.8, {"region": "US-SOUTH"})]


class FakeLLM:
    def invoke(self, prompt, system_prompt=None, temperature=0.1, max_tokens=600):
        return "grounded answer"


def test_graph_end_to_end_mixed():
    state = run_graph(
        {"question": "Why are Texas sales down?"},
        FakeRunner(),
        AccessContext(user_id="u", role="analyst", allowed_regions=["US-SOUTH"], business_units=["snacks"]),
        FakeRetriever(),
        FakeLLM(),
        {},
    )
    assert state["answer"] == "grounded answer"
    assert state["route"] == "mixed"
    assert "validation_notes" in state
    assert "diagnostics" in state
=======
        return [RetrievedDoc("d1", "policy note", 0.8, {})]


class FakeLLM:
    def invoke(self, prompt, system_prompt=None):
        return "grounded answer"


def test_graph_end_to_end():
    state = run_graph({"question": "Texas sales"}, FakeRunner(), AccessContext(user_id="u", role="analyst", allowed_regions=["US-SOUTH"], business_units=["snacks"]), FakeRetriever(), FakeLLM(), {})
    assert state["answer"] == "grounded answer"
    assert state["route"] in {"mixed", "structured", "doc"}
>>>>>>> main
