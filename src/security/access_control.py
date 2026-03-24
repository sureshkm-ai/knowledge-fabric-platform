import re

from src.security.policies import AccessContext, ROLE_POLICIES


def filter_sql_by_scope(sql: str, ctx: AccessContext) -> str:
    region_clause = "','".join(ctx.allowed_regions)
    bu_clause = "','".join(ctx.business_units)
    sql = sql.rstrip(" ;")
    scope_conditions = f"region IN ('{region_clause}') AND business_unit IN ('{bu_clause}')"

    # Find the position of ORDER BY or LIMIT to insert scope before them
    tail_match = re.search(r"\s+(ORDER\s+BY|LIMIT)\s+", sql, re.IGNORECASE)
    if tail_match:
        insert_pos = tail_match.start()
        core = sql[:insert_pos]
        tail = sql[insert_pos:]
        if re.search(r"\bWHERE\b", core, re.IGNORECASE):
            return f"{core} AND {scope_conditions}{tail}"
        return f"{core} WHERE {scope_conditions}{tail}"

    if " where " in sql.lower():
        return f"{sql} AND {scope_conditions}"
    return f"{sql} WHERE {scope_conditions}"


def filter_docs_by_access(docs: list[dict], ctx: AccessContext) -> list[dict]:
    allowed_conf = ROLE_POLICIES.get(ctx.role, {}).get("can_access_confidential", False)
    out = []
    for doc in docs:
        meta = doc.get("metadata", {})
        if meta.get("region") and meta["region"] not in ctx.allowed_regions:
            continue
        if meta.get("business_unit") and meta["business_unit"] not in ctx.business_units:
            continue
        if meta.get("classification") == "confidential" and not allowed_conf:
            continue
        out.append(doc)
    return out
