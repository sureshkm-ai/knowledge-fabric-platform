from pydantic import BaseModel


class AccessContext(BaseModel):
    user_id: str
    role: str
    allowed_regions: list[str]
    business_units: list[str]


ROLE_POLICIES = {
    "analyst": {"can_access_confidential": False},
    "manager": {"can_access_confidential": True},
    "admin": {"can_access_confidential": True},
}
