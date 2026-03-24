<<<<<<< HEAD
"""pgvector integration for enterprise deployments."""
from __future__ import annotations

import json

=======
import json
>>>>>>> main
import psycopg

from src.vectorstore.base import BaseVectorStore, RetrievedDoc


class PgVectorStore(BaseVectorStore):
    def __init__(self, dsn: str, table: str = "doc_vectors"):
        self.dsn = dsn
        self.table = table

    def upsert(self, items: list[dict]) -> None:
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                for item in items:
                    cur.execute(
<<<<<<< HEAD
                        f"INSERT INTO {self.table}(doc_id, text, embedding, metadata) VALUES (%s, %s, %s::vector, %s::jsonb) "
=======
                        f"INSERT INTO {self.table}(doc_id,text,embedding,metadata) VALUES (%s,%s,%s::vector,%s::jsonb) "
>>>>>>> main
                        f"ON CONFLICT(doc_id) DO UPDATE SET text=EXCLUDED.text, embedding=EXCLUDED.embedding, metadata=EXCLUDED.metadata",
                        (item["doc_id"], item["text"], item["vector"], json.dumps(item.get("metadata", {}))),
                    )
            conn.commit()

    def query(self, vector: list[float], top_k: int = 5, filters: dict | None = None) -> list[RetrievedDoc]:
<<<<<<< HEAD
        filter_sql = ""
        params: list = [vector, vector]
        if filters:
            clauses = []
            for key, value in filters.items():
                if isinstance(value, dict) and "in" in value:
                    clauses.append(f"metadata->>'{key}' = ANY(%s)")
                    params.append(value["in"])
                else:
                    clauses.append(f"metadata->>'{key}' = %s")
                    params.append(str(value))
            filter_sql = " WHERE " + " AND ".join(clauses)

        params.append(top_k)
        sql = (
            f"SELECT doc_id, text, metadata, 1 - (embedding <=> %s::vector) AS score "
            f"FROM {self.table}"
            f"{filter_sql} "
            "ORDER BY embedding <=> %s::vector LIMIT %s"
        )

        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, tuple(params))
=======
        with psycopg.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT doc_id, text, metadata, 1-(embedding <=> %s::vector) AS score FROM {self.table} ORDER BY embedding <=> %s::vector LIMIT %s",
                    (vector, vector, top_k),
                )
>>>>>>> main
                return [RetrievedDoc(r[0], r[1], float(r[3]), r[2]) for r in cur.fetchall()]
