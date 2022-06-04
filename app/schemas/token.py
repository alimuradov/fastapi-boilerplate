from typing import Optional, List

from pydantic import BaseModel, UUID4


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    id: UUID4
    role: str = None


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []