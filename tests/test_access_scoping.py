from src.security.access_control import filter_docs_by_access
from src.security.policies import AccessContext


def test_doc_access_region_filter():
    docs = [{"metadata": {"region": "US-WEST"}}, {"metadata": {"region": "US-SOUTH"}}]
    ctx = AccessContext(user_id="u", role="analyst", allowed_regions=["US-SOUTH"], business_units=["snacks"])
    out = filter_docs_by_access(docs, ctx)
    assert len(out) == 1
