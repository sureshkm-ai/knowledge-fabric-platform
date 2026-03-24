from src.vectorstore.base import metadata_matches


def test_metadata_exact_match():
    assert metadata_matches({"region": "US-SOUTH"}, {"region": "US-SOUTH"})
    assert not metadata_matches({"region": "US-WEST"}, {"region": "US-SOUTH"})


def test_metadata_in_match():
    assert metadata_matches({"region": "US-SOUTH"}, {"region": {"in": ["US-SOUTH", "US-WEST"]}})
    assert not metadata_matches({"region": "EU"}, {"region": {"in": ["US-SOUTH", "US-WEST"]}})
