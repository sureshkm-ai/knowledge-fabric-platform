from src.security.policies import AccessContext, ROLE_POLICIES


def filter_sql_by_scope(sql: str, ctx: AccessContext) -> str:
    region_clause = "','".join(ctx.allowed_regions)
    bu_clause = "','".join(ctx.business_units)
    sql = sql.rstrip(" ;")
    if " where " in sql.lower():
        return f"{sql} AND region IN ('{region_clause}') AND business_unit IN ('{bu_clause}')"
    return f"{sql} WHERE region IN ('{region_clause}') AND business_unit IN ('{bu_clause}')"


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
