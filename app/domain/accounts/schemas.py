from uuid import UUID
from pydantic import EmailStr

from app.domain.base.schemas import BaseSchema


class UserSchema(BaseSchema):
    id: UUID
    email: EmailStr
    is_superuser: bool
    is_active: bool
    is_verified: bool
    roles: list[str]


class UserCreateSchema(BaseSchema):
    email: EmailStr
    password: str
    is_superuser: bool
    is_active: bool
    is_verified: bool


class AccountCredentialsSchema(BaseSchema):
    email: EmailStr
    password: str


class TokenData(BaseSchema):
    id: UUID
    email: EmailStr
