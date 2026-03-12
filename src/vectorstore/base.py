from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RetrievedDoc:
    doc_id: str
    text: str
    score: float
    metadata: dict


class BaseVectorStore(ABC):
    @abstractmethod
    def upsert(self, items: list[dict]) -> None:
        ...

    @abstractmethod
    def query(self, vector: list[float], top_k: int = 5, filters: dict | None = None) -> list[RetrievedDoc]:
        ...
