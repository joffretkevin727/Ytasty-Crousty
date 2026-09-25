from pydantic import BaseModel, Field, field_validator


class UsersRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role: str = Field(
        ...,
        pattern="^(admin|staff|direction)$"
    )
    restaurant_id: int | None = None

    @field_validator("username")
    def validate_username(cls, v):
        if not (8 <= len(v) <= 12):
            raise ValueError("Username must be between 8 and 12 characters")
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if not (12 <= len(v) <= 64):
            raise ValueError("Password must be between 12 and 64 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(not c.isalnum() for c in v):
            raise ValueError("Password must contain at least one special character")
        return v


class UsersResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    role: str
    restaurant_id: int | None
