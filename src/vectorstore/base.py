"""Vector-store abstractions and common filtering utilities."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievedDoc:
    doc_id: str
    text: str
    score: float
    metadata: dict[str, Any]


class BaseVectorStore(ABC):
    @abstractmethod
    def upsert(self, items: list[dict[str, Any]]) -> None:
        """Insert/update vectorized documents."""

    @abstractmethod
    def query(
        self,
        vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievedDoc]:
        """Search nearest neighbors with optional metadata filtering."""


def metadata_matches(metadata: dict[str, Any], filters: dict[str, Any] | None) -> bool:
    """Apply exact-match and `in` style filter constraints.

    Supported filter format:
    - {"region": "US-SOUTH"}
    - {"region": {"in": ["US-SOUTH", "US-WEST"]}}
    """
    if not filters:
        return True

    for key, expected in filters.items():
        actual = metadata.get(key)
        if isinstance(expected, dict) and "in" in expected:
            if actual not in set(expected["in"]):
                return False
        elif actual != expected:
            return False
    return True
